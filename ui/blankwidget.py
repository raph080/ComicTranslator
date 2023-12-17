# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'blankwidget.ui'
##
## Created by: Qt User Interface Compiler version 6.6.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDoubleSpinBox, QGridLayout, QHBoxLayout,
    QLabel, QPushButton, QSizePolicy, QSlider,
    QSpacerItem, QVBoxLayout, QWidget)
from resources import resources_rc

class Ui_blankWidget(object):
    def setupUi(self, blankWidget):
        if not blankWidget.objectName():
            blankWidget.setObjectName(u"blankWidget")
        blankWidget.resize(293, 526)
        self.verticalLayout = QVBoxLayout(blankWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(blankWidget)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.contrastSlider = QSlider(blankWidget)
        self.contrastSlider.setObjectName(u"contrastSlider")
        self.contrastSlider.setMaximum(100)
        self.contrastSlider.setValue(100)
        self.contrastSlider.setOrientation(Qt.Horizontal)

        self.horizontalLayout.addWidget(self.contrastSlider)

        self.contrastSpinBox = QDoubleSpinBox(blankWidget)
        self.contrastSpinBox.setObjectName(u"contrastSpinBox")
        self.contrastSpinBox.setMaximum(1.000000000000000)
        self.contrastSpinBox.setSingleStep(0.010000000000000)
        self.contrastSpinBox.setValue(1.000000000000000)

        self.horizontalLayout.addWidget(self.contrastSpinBox)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.label_2 = QLabel(blankWidget)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout.addWidget(self.label_2)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.brightnessSlider = QSlider(blankWidget)
        self.brightnessSlider.setObjectName(u"brightnessSlider")
        self.brightnessSlider.setMaximum(100)
        self.brightnessSlider.setValue(100)
        self.brightnessSlider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_2.addWidget(self.brightnessSlider)

        self.brightnessSpinBox = QDoubleSpinBox(blankWidget)
        self.brightnessSpinBox.setObjectName(u"brightnessSpinBox")
        self.brightnessSpinBox.setMaximum(1.000000000000000)
        self.brightnessSpinBox.setSingleStep(0.010000000000000)
        self.brightnessSpinBox.setValue(1.000000000000000)

        self.horizontalLayout_2.addWidget(self.brightnessSpinBox)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.label_3 = QLabel(blankWidget)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout.addWidget(self.label_3)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.sharpnessSlider = QSlider(blankWidget)
        self.sharpnessSlider.setObjectName(u"sharpnessSlider")
        self.sharpnessSlider.setMaximum(100)
        self.sharpnessSlider.setValue(50)
        self.sharpnessSlider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_3.addWidget(self.sharpnessSlider)

        self.sharpnessSpinBox = QDoubleSpinBox(blankWidget)
        self.sharpnessSpinBox.setObjectName(u"sharpnessSpinBox")
        self.sharpnessSpinBox.setMaximum(2.000000000000000)
        self.sharpnessSpinBox.setSingleStep(0.010000000000000)
        self.sharpnessSpinBox.setValue(1.000000000000000)

        self.horizontalLayout_3.addWidget(self.sharpnessSpinBox)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.label_4 = QLabel(blankWidget)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout.addWidget(self.label_4)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.temperatureSlider = QSlider(blankWidget)
        self.temperatureSlider.setObjectName(u"temperatureSlider")
        self.temperatureSlider.setMaximum(100)
        self.temperatureSlider.setValue(50)
        self.temperatureSlider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_4.addWidget(self.temperatureSlider)

        self.temperatureSpinBox = QDoubleSpinBox(blankWidget)
        self.temperatureSpinBox.setObjectName(u"temperatureSpinBox")
        self.temperatureSpinBox.setMaximum(1.000000000000000)
        self.temperatureSpinBox.setSingleStep(0.010000000000000)
        self.temperatureSpinBox.setValue(0.500000000000000)

        self.horizontalLayout_4.addWidget(self.temperatureSpinBox)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.label_5 = QLabel(blankWidget)
        self.label_5.setObjectName(u"label_5")

        self.verticalLayout.addWidget(self.label_5)

        self.widget = QWidget(blankWidget)
        self.widget.setObjectName(u"widget")
        self.widget.setFocusPolicy(Qt.ClickFocus)
        self.horizontalLayout_6 = QHBoxLayout(self.widget)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.blankDownButton = QPushButton(self.widget)
        self.blankDownButton.setObjectName(u"blankDownButton")
        icon = QIcon()
        icon.addFile(u":/down.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.blankDownButton.setIcon(icon)
        self.blankDownButton.setIconSize(QSize(32, 32))
        self.blankDownButton.setFlat(True)

        self.gridLayout_2.addWidget(self.blankDownButton, 2, 1, 1, 1)

        self.blankRightButton = QPushButton(self.widget)
        self.blankRightButton.setObjectName(u"blankRightButton")
        icon1 = QIcon()
        icon1.addFile(u":/right.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.blankRightButton.setIcon(icon1)
        self.blankRightButton.setIconSize(QSize(32, 32))
        self.blankRightButton.setFlat(True)

        self.gridLayout_2.addWidget(self.blankRightButton, 1, 2, 1, 1)

        self.blankTopButton = QPushButton(self.widget)
        self.blankTopButton.setObjectName(u"blankTopButton")
        icon2 = QIcon()
        icon2.addFile(u":/up.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.blankTopButton.setIcon(icon2)
        self.blankTopButton.setIconSize(QSize(32, 32))
        self.blankTopButton.setFlat(True)

        self.gridLayout_2.addWidget(self.blankTopButton, 0, 1, 1, 1)

        self.blankLeftButton = QPushButton(self.widget)
        self.blankLeftButton.setObjectName(u"blankLeftButton")
        icon3 = QIcon()
        icon3.addFile(u":/left.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.blankLeftButton.setIcon(icon3)
        self.blankLeftButton.setIconSize(QSize(32, 32))
        self.blankLeftButton.setFlat(True)

        self.gridLayout_2.addWidget(self.blankLeftButton, 1, 0, 1, 1)


        self.horizontalLayout_6.addLayout(self.gridLayout_2)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addWidget(self.widget)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_4)

        self.autoGridAlignmentButton = QPushButton(blankWidget)
        self.autoGridAlignmentButton.setObjectName(u"autoGridAlignmentButton")

        self.horizontalLayout_5.addWidget(self.autoGridAlignmentButton)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_3)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(blankWidget)

        QMetaObject.connectSlotsByName(blankWidget)
    # setupUi

    def retranslateUi(self, blankWidget):
        blankWidget.setWindowTitle(QCoreApplication.translate("blankWidget", u"Form", None))
        self.label.setText(QCoreApplication.translate("blankWidget", u"Contrast", None))
        self.label_2.setText(QCoreApplication.translate("blankWidget", u"Brightness", None))
        self.label_3.setText(QCoreApplication.translate("blankWidget", u"Sharpness", None))
        self.label_4.setText(QCoreApplication.translate("blankWidget", u"Hue", None))
        self.label_5.setText(QCoreApplication.translate("blankWidget", u"Offset", None))
        self.blankDownButton.setText("")
#if QT_CONFIG(shortcut)
        self.blankDownButton.setShortcut(QCoreApplication.translate("blankWidget", u"Down", None))
#endif // QT_CONFIG(shortcut)
        self.blankRightButton.setText("")
#if QT_CONFIG(shortcut)
        self.blankRightButton.setShortcut(QCoreApplication.translate("blankWidget", u"Right", None))
#endif // QT_CONFIG(shortcut)
        self.blankTopButton.setText("")
#if QT_CONFIG(shortcut)
        self.blankTopButton.setShortcut(QCoreApplication.translate("blankWidget", u"Up", None))
#endif // QT_CONFIG(shortcut)
        self.blankLeftButton.setText("")
#if QT_CONFIG(shortcut)
        self.blankLeftButton.setShortcut(QCoreApplication.translate("blankWidget", u"Left", None))
#endif // QT_CONFIG(shortcut)
        self.autoGridAlignmentButton.setText(QCoreApplication.translate("blankWidget", u"Automatic grid alignment", None))
    # retranslateUi

