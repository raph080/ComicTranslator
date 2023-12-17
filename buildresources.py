import tempfile
import subprocess
import os

"""
name : compileResources
description : compite the resource file using maya binary files
"""


def compileResources():
    rsc_filename = 'resources/resources.qrc'
    command = [
        "pyside6-rcc", rsc_filename, "-o",
        rsc_filename.replace(".qrc", "_rc.py")
    ]

    process = subprocess.Popen(command,
                               stdout=subprocess.PIPE,
                               stdin=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    process.communicate()


"""
name : compileUis
description : compile all the ui files from smartshelf/ui to py files
"""


def compileUis():

    ui_path = 'ui'
    for path, _, files in os.walk(ui_path):

        for file in files:
            if not file.endswith(".ui"):
                continue

            ui_file = os.path.join(path, file)
            py_file = ui_file.replace(".ui", ".py")

            # check if python file already exists
            if os.path.isfile(py_file):
                ui_time = os.path.getmtime(ui_file)
                py_time = os.path.getmtime(py_file)
                # if python file created after ui file, skip
                if (py_time >= ui_time):
                    continue

            print("compile : " + ui_file)
            tmp_file_path = os.path.join(ui_path, 'tmp.py')

            os.system("pyside6-uic " + ui_file + " -o " + tmp_file_path)

            fin = open(tmp_file_path, "rt")
            fout = open(py_file, "wt")

            for line in fin:
                fout.write(
                    line.replace('import resources_rc',
                                 'from resources import resources_rc'))

            fin.close()
            fout.close()
            os.remove(tmp_file_path)
