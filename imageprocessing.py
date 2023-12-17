from sklearn.cluster import KMeans
import numpy as np
import cv2
import math
import pytesseract
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageEnhance, ImageOps
from PySide6 import QtCore, QtGui
import io
from PIL import Image, ImageQt


def np_image_to_pil_image(np_image):
    return Image.fromarray(np_image.astype(np.uint8))


def pil_image_to_np_image(image: Image) -> np.array:
    return np.array(image)


def pil_image_to_qpixmap(img):
    qim = ImageQt.ImageQt(img)
    return QtGui.QPixmap.fromImage(qim)


def qpixmap_to_pil_image(pixmap):
    buffer = QtCore.QBuffer()
    buffer.open(QtCore.QBuffer.ReadWrite)
    pixmap.save(buffer, "PNG")
    return Image.open(io.BytesIO(buffer.data()))


def pil_mask_to_pixmap(mask: Image, color: tuple) -> QtGui.QPixmap:
    image = Image.new(mode="RGBA", size=mask.size, color=color)
    channels = mask.split()
    image.putalpha(channels[0])
    return pil_image_to_qpixmap(image)


def crop_image(image: Image, size: tuple, offset: tuple = (0, 0)) -> Image:
    image = ImageChops.offset(image, int(offset[0]), int(offset[1]))
    image = image.crop((0, 0, size[0], size[1]))
    return image


def apply_mask_to_image(image: Image, mask: Image) -> None:
    channels = mask.split()
    image.putalpha(channels[0])


def to_black_and_white(image: Image, threshold: int = 180) -> Image:
    def fn(x): return 255 if x > threshold else 0
    return image.convert('L').point(fn, mode='1')


def to_black_and_white2(image, threshold=180):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)[1]


def get_intersections(lines):
    def line_intersection(line1, line2):
        xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
        ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

        def det(a, b):
            return a[0] * b[1] - a[1] * b[0]

        div = det(xdiff, ydiff)
        if div == 0:
            return None

        d = (det(*line1), det(*line2))
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div
        return x, y

    inters = []

    for i in range(len(lines)):
        for j in range(len(lines)):
            if i != j:
                inter = line_intersection(lines[i], lines[j])
                if inter:
                    inters.append(inter)
    return inters


def get_all_corners(image: Image) -> list[tuple]:
    np_image = pil_image_to_np_image(image)
    gray = cv2.cvtColor(np_image, cv2.COLOR_BGR2GRAY)

    width = np_image.shape[1]
    height = np_image.shape[0]

    blur = cv2.medianBlur(gray, 5)
    sharpen_kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    sharpen = cv2.filter2D(blur, -1, sharpen_kernel)

    # Threshold and morph close
    thresh = cv2.threshold(sharpen, 160, 255, cv2.THRESH_BINARY_INV)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

    # Find contours and filter using threshold area
    cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    min_area = int(width/6*width/6)
    max_area = int(width/5*width/5)

    lines = []
    for c in cnts:
        area = cv2.contourArea(c)
        if area > min_area and area < max_area:
            x, y, w, h = cv2.boundingRect(c)
            lines2 = []
            lines2.append([(0, y), (width, y)])  # first horiz
            lines2.append([(0, y+h), (width, y+h)])
            lines2.append([(x, 0), (x, height)])
            lines2.append([(x+w, 0), (x+w, height)])

            # for line in lines2:
            #     cv2.line(image, line[0], line[1], (0, 0, 255), 3)

            lines.extend(lines2)

    inters = get_intersections(lines)

    kmeans = KMeans(n_clusters=5*7*4, n_init='auto')
    kmeans.fit(inters)

    centroids = []

    for c in kmeans.cluster_centers_:
        centroids.append((int(c[0]), int(c[1])))
        # cv2.circle(image, centroids[-1],
        #            radius=0, color=(0, 255, 0), thickness=50)

    return centroids


def get_4_external_corners(centroids):
    br = max(centroids)
    tl = min(centroids)
    tr = max(centroids, key=lambda c: c[0] + br[1] - c[1])
    bl = max(centroids, key=lambda c: tl[0] - c[0] + c[1])

    return tl, tr, bl, br


def get_cell_rectangle(centroids, cell_index):
    tlc, trc, blc, brc = get_4_external_corners(centroids)

    # for c in [tlc, trc, blc, brc]:
    #     cv2.circle(image, c,
    #                radius=0, color=(0, 255, 0), thickness=50)

    x = cell_index % 5
    y = math.floor(cell_index / 5)

    center = [
        tlc[0] + (trc[0] - tlc[0]) / 5 * (x + 0.5),
        tlc[1] + (blc[1] - tlc[1]) / 7 * (y + 0.5)]

    tl = filter(lambda c: c[1] < center[1], centroids)
    tl = filter(lambda c: c[0] < center[0], tl)
    tl = max(tl)

    tr = filter(lambda c: c[1] < center[1], centroids)
    tr = filter(lambda c: c[0] > center[0], tr)
    tr = max(tr, key=lambda c: tlc[0] - c[0] + c[1])

    bl = filter(lambda c: c[1] > center[1], centroids)
    bl = filter(lambda c: c[0] < center[0], bl)
    bl = max(bl, key=lambda c: c[0] + trc[1] - c[1])

    br = filter(lambda c: c[1] > center[1], centroids)
    br = filter(lambda c: c[0] > center[0], br)
    br = min(br)

    tl = (max(tl[0], bl[0]), max(tl[1], tr[1]))
    br = (min(tr[0], br[0]), min(bl[1], br[1]))

    # x, y, w, h
    return [tl[0], tl[1], br[0] - tl[0], br[1] - tl[1]]


def get_cell_rectangles(image: Image) -> list[tuple[float, float, float, float]]:
    centroids = get_all_corners(image)

    rects = []
    for i in range(5*7):
        rect = get_cell_rectangle(centroids, i)
        rects.append(rect)
    return rects

# cv2.imshow('image', image)
# cv2.waitKey()


def get_text_boxes(image: Image) -> list:
    image_bw = to_black_and_white(image)
    tmp_str = pytesseract.image_to_boxes(image_bw, lang='fra')
    boxes = []
    for line in tmp_str.splitlines():
        data = line.split(" ")
        data = [data[0]] + list(map(int, data[1:]))
        boxes.append(data)
    return boxes


def closest_points(points):
    from itertools import combinations

    def distance(p1, p2):
        d1 = p2[0] - p1[0]
        d2 = p2[1] - p1[1]
        return math.sqrt(d1**2 + d2**2)

    closest_points = None
    min_dist = float('inf')

    for p1, p2 in combinations(points, 2):
        dist = distance(p1, p2)

        if dist < min_dist:
            closest_points = (p1, p2)
            min_dist = dist

    return closest_points


def get_text_mask(image: Image, blur: int = 5, radius: int = 10) -> Image:
    boxes = get_text_boxes(image)

    mask = create_mask(image.size)

    draw = ImageDraw.Draw(mask)
    # Draw a regular rectangle
    # Draw a rounded rectangle
    # draw.rounded_rectangle((50, 50, 150, 150), fill="blue", outline="yellow",
    #                        width=3, radius=7)

    border_width = 8
    for data in boxes:
        if data[0] != '~':
            # print(data)
            x = data[1] - border_width
            y = image.height - data[2] + border_width
            w = data[3] + border_width * 2
            h = data[4] - data[2] + border_width * 2
            draw.rounded_rectangle(
                (x, y-h, w, y), fill="white", radius=radius)

    return mask.filter(ImageFilter.GaussianBlur(radius=blur))


def find_pattern(image: Image, pattern: Image) -> tuple:
    np_image = pil_image_to_np_image(image)
    np_pattern = pil_image_to_np_image(pattern)

    def to_black_and_white(image, threshold=180):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)[1]

    # remove the black lines from pencil
    bw = to_black_and_white(np_image)
    white = np.zeros(np_image.shape, dtype=np.uint8)
    white.fill(255)
    image_no_pencil = cv2.bitwise_and(np_image, white, white, mask=bw)

    # Converting them to grayscale
    img_gray = cv2.cvtColor(image_no_pencil,
                            cv2.COLOR_BGR2GRAY)
    temp_gray = cv2.cvtColor(np_pattern,
                             cv2.COLOR_BGR2GRAY)

    # Passing the image to matchTemplate method
    match = None
    try:
        match = cv2.matchTemplate(
            image=img_gray, templ=temp_gray,
            method=cv2.TM_CCOEFF_NORMED)
    except:
        return (0, 0)

    _, _, _, max_loc = cv2.minMaxLoc(match)

    return (max_loc[0] + temp_gray.shape[1] / 2, max_loc[1] + temp_gray.shape[0] / 2)


def add_images(images):
    result = images[0].copy()
    for image in images[1:]:
        result = ImageChops.add(result, image)
    return result


def sub_images(images):
    result = images[0].copy()
    for image in images[1:]:
        result = ImageChops.subtract(result, image)
    return result


def compose(*layers):
    result = layers[0].copy()
    for layer in layers[1:]:
        result = ImageChops.add(result, layer)
        # result.paste(layer, (0, 0), layer)
    return result


def invert(image: Image) -> Image:
    return ImageOps.invert(image)


def draw_line(image: Image, width: int, color, *points) -> None:
    draw = ImageDraw.Draw(image)
    draw.line(points, fill=color, width=width)

    for p in points:
        draw_disc(image, p, color=color, radius=width/2)


def draw_disc(image: Image, pos: tuple, color, radius: int = 5) -> None:
    draw = ImageDraw.Draw(image)
    draw.ellipse((pos[0]-radius, pos[1]-radius, pos[0] +
                 radius, pos[1]+radius), fill=color)


def blur(image: Image, radius: int = 5) -> Image:
    return image.filter(ImageFilter.GaussianBlur(radius=radius))


def copy(image: Image) -> Image:
    return image.copy()


def setTemperature(image: Image, value: float) -> Image:
    kelvin_table = {
        1000: (255, 56, 0),
        1100: (255, 71, 0),
        1200: (255, 83, 0),
        1300: (255, 93, 0),
        1400: (255, 101, 0),
        1500: (255, 109, 0),
        1600: (255, 115, 0),
        1700: (255, 121, 0),
        1800: (255, 126, 0),
        1900: (255, 131, 0),
        2000: (255, 138, 18),
        2100: (255, 142, 33),
        2200: (255, 147, 44),
        2300: (255, 152, 54),
        2400: (255, 157, 63),
        2500: (255, 161, 72),
        2600: (255, 165, 79),
        2700: (255, 169, 87),
        2800: (255, 173, 94),
        2900: (255, 177, 101),
        3000: (255, 180, 107),
        3100: (255, 184, 114),
        3200: (255, 187, 120),
        3300: (255, 190, 126),
        3400: (255, 193, 132),
        3500: (255, 196, 137),
        3600: (255, 199, 143),
        3700: (255, 201, 148),
        3800: (255, 204, 153),
        3900: (255, 206, 159),
        4000: (255, 209, 163),
        4100: (255, 211, 168),
        4200: (255, 213, 173),
        4300: (255, 215, 177),
        4400: (255, 217, 182),
        4500: (255, 219, 186),
        4600: (255, 221, 190),
        4700: (255, 223, 194),
        4800: (255, 225, 198),
        4900: (255, 227, 202),
        5000: (255, 228, 206),
        5100: (255, 230, 210),
        5200: (255, 232, 213),
        5300: (255, 233, 217),
        5400: (255, 235, 220),
        5500: (255, 236, 224),
        5600: (255, 238, 227),
        5700: (255, 239, 230),
        5800: (255, 240, 233),
        5900: (255, 242, 236),
        6000: (255, 243, 239),
        6100: (255, 244, 242),
        6200: (255, 245, 245),
        6300: (255, 246, 247),
        6400: (255, 248, 251),
        6500: (255, 249, 253),
        6600: (254, 249, 255),
        6700: (252, 247, 255),
        6800: (249, 246, 255),
        6900: (247, 245, 255),
        7000: (245, 243, 255),
        7100: (243, 242, 255),
        7200: (240, 241, 255),
        7300: (239, 240, 255),
        7400: (237, 239, 255),
        7500: (235, 238, 255),
        7600: (233, 237, 255),
        7700: (231, 236, 255),
        7800: (230, 235, 255),
        7900: (228, 234, 255),
        8000: (227, 233, 255),
        8100: (225, 232, 255),
        8200: (224, 231, 255),
        8300: (222, 230, 255),
        8400: (221, 230, 255),
        8500: (220, 229, 255),
        8600: (218, 229, 255),
        8700: (217, 227, 255),
        8800: (216, 227, 255),
        8900: (215, 226, 255),
        9000: (214, 225, 255),
        9100: (212, 225, 255),
        9200: (211, 224, 255),
        9300: (210, 223, 255),
        9400: (209, 223, 255),
        9500: (208, 222, 255),
        9600: (207, 221, 255),
        9700: (207, 221, 255),
        9800: (206, 220, 255),
        9900: (205, 220, 255),
        10000: (207, 218, 255),
        10100: (207, 218, 255),
        10200: (206, 217, 255),
        10300: (205, 217, 255),
        10400: (204, 216, 255),
        10500: (204, 216, 255),
        10600: (203, 215, 255),
        10700: (202, 215, 255),
        10800: (202, 214, 255),
        10900: (201, 214, 255),
        11000: (200, 213, 255),
        11100: (200, 213, 255),
        11200: (199, 212, 255),
        11300: (198, 212, 255),
        11400: (198, 212, 255),
        11500: (197, 211, 255),
        11600: (197, 211, 255),
        11700: (197, 210, 255),
        11800: (196, 210, 255),
        11900: (195, 210, 255),
        12000: (195, 209, 255)
    }
    keys = list(kelvin_table.keys())
    temperatureId = 4  # (keys[-1] - keys[0]) * value + keys[0]
    temperature = keys[int(temperatureId / 200 * (len(keys) - 1))]

    r, g, b = kelvin_table[temperature]
    matrix = (r / 255.0, 0.0, 0.0, 0.0, 0.0, g / 255.0, 0.0, 0.0, 0.0, 0.0,
              b / 255.0, 0.0)
    return image.convert('RGB', matrix)


def set_contrast(image: Image, value: float) -> Image:
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(value)


def set_brightness(image: Image, value: float) -> Image:
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(value)


def set_sharpness(image: Image, value: float) -> Image:
    enhancer = ImageEnhance.Sharpness(image)
    return enhancer.enhance(value)


def rgb_to_hsv(rgb):
    # Translated from source of colorsys.rgb_to_hsv
    # r,g,b should be a numpy arrays with values between 0 and 255
    # rgb_to_hsv returns an array of floats between 0.0 and 1.0.
    rgb = rgb.astype('float')
    hsv = np.zeros_like(rgb)
    # in case an RGBA array was passed, just copy the A channel
    hsv[..., 3:] = rgb[..., 3:]
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    maxc = np.max(rgb[..., :3], axis=-1)
    minc = np.min(rgb[..., :3], axis=-1)
    hsv[..., 2] = maxc
    mask = maxc != minc
    hsv[mask, 1] = (maxc - minc)[mask] / maxc[mask]
    rc = np.zeros_like(r)
    gc = np.zeros_like(g)
    bc = np.zeros_like(b)
    rc[mask] = (maxc - r)[mask] / (maxc - minc)[mask]
    gc[mask] = (maxc - g)[mask] / (maxc - minc)[mask]
    bc[mask] = (maxc - b)[mask] / (maxc - minc)[mask]
    hsv[..., 0] = np.select(
        [r == maxc, g == maxc], [bc - gc, 2.0 + rc - bc], default=4.0 + gc - rc)
    hsv[..., 0] = (hsv[..., 0] / 6.0) % 1.0
    return hsv


def hsv_to_rgb(hsv):
    # Translated from source of colorsys.hsv_to_rgb
    # h,s should be a numpy arrays with values between 0.0 and 1.0
    # v should be a numpy array with values between 0.0 and 255.0
    # hsv_to_rgb returns an array of uints between 0 and 255.
    rgb = np.empty_like(hsv)
    rgb[..., 3:] = hsv[..., 3:]
    h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    i = (h * 6.0).astype('uint8')
    f = (h * 6.0) - i
    p = v * (1.0 - s)
    q = v * (1.0 - s * f)
    t = v * (1.0 - s * (1.0 - f))
    i = i % 6
    conditions = [s == 0.0, i == 1, i == 2, i == 3, i == 4, i == 5]
    rgb[..., 0] = np.select(conditions, [v, q, p, p, t, v], default=v)
    rgb[..., 1] = np.select(conditions, [v, v, v, q, p, p], default=t)
    rgb[..., 2] = np.select(conditions, [v, p, t, v, v, q], default=p)
    return rgb.astype('uint8')


def set_hue(image, hue):
    np_image = pil_image_to_np_image(image)
    hsv = rgb_to_hsv(np_image)
    hsv[..., 0] = hue
    rgb = hsv_to_rgb(hsv)
    return Image.fromarray(rgb, 'RGBA')


def create_mask(size):
    return Image.new(mode="L", size=size, color="black")
