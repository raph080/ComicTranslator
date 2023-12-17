# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'paintwidget.ui'
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
from PySide6.QtWidgets import (QApplication, QGroupBox, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QSlider, QSpacerItem,
    QSpinBox, QVBoxLayout, QWidget)
from resources import resources_rc

class Ui_paintWidget(object):
    def setupUi(self, paintWidget):
        if not paintWidget.objectName():
            paintWidget.setObjectName(u"paintWidget")
        paintWidget.resize(308, 507)
        self.verticalLayout = QVBoxLayout(paintWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox = QGroupBox(paintWidget)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.verticalLayout_2.addWidget(self.label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.sizeSlider = QSlider(self.groupBox)
        self.sizeSlider.setObjectName(u"sizeSlider")
        self.sizeSlider.setMinimum(1)
        self.sizeSlider.setMaximum(50)
        self.sizeSlider.setValue(10)
        self.sizeSlider.setOrientation(Qt.Horizontal)

        self.horizontalLayout.addWidget(self.sizeSlider)

        self.sizeSpinBox = QSpinBox(self.groupBox)
        self.sizeSpinBox.setObjectName(u"sizeSpinBox")
        self.sizeSpinBox.setMinimum(1)
        self.sizeSpinBox.setMaximum(50)
        self.sizeSpinBox.setValue(10)

        self.horizontalLayout.addWidget(self.sizeSpinBox)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_2.addWidget(self.label_2)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.hardnessSlider = QSlider(self.groupBox)
        self.hardnessSlider.setObjectName(u"hardnessSlider")
        self.hardnessSlider.setMaximum(50)
        self.hardnessSlider.setValue(1)
        self.hardnessSlider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_2.addWidget(self.hardnessSlider)

        self.hardnessSpinBox = QSpinBox(self.groupBox)
        self.hardnessSpinBox.setObjectName(u"hardnessSpinBox")
        self.hardnessSpinBox.setMinimum(0)
        self.hardnessSpinBox.setMaximum(50)

        self.horizontalLayout_2.addWidget(self.hardnessSpinBox)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout_2.addWidget(self.label_4)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.previewLabel = QLabel(self.groupBox)
        self.previewLabel.setObjectName(u"previewLabel")
        self.previewLabel.setMinimumSize(QSize(80, 80))
        self.previewLabel.setMaximumSize(QSize(80, 80))
        self.previewLabel.setStyleSheet(u"background-color: white")

        self.horizontalLayout_3.addWidget(self.previewLabel)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)


        self.verticalLayout.addWidget(self.groupBox)

        self.letterDetectionGroup = QGroupBox(paintWidget)
        self.letterDetectionGroup.setObjectName(u"letterDetectionGroup")
        self.verticalLayout_3 = QVBoxLayout(self.letterDetectionGroup)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_3 = QLabel(self.letterDetectionGroup)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_3.addWidget(self.label_3)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.borderSlider = QSlider(self.letterDetectionGroup)
        self.borderSlider.setObjectName(u"borderSlider")
        self.borderSlider.setMaximum(20)
        self.borderSlider.setValue(10)
        self.borderSlider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_5.addWidget(self.borderSlider)

        self.borderSpinBox = QSpinBox(self.letterDetectionGroup)
        self.borderSpinBox.setObjectName(u"borderSpinBox")
        self.borderSpinBox.setMaximum(20)
        self.borderSpinBox.setValue(10)

        self.horizontalLayout_5.addWidget(self.borderSpinBox)


        self.verticalLayout_3.addLayout(self.horizontalLayout_5)

        self.label_5 = QLabel(self.letterDetectionGroup)
        self.label_5.setObjectName(u"label_5")

        self.verticalLayout_3.addWidget(self.label_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.blurSlider = QSlider(self.letterDetectionGroup)
        self.blurSlider.setObjectName(u"blurSlider")
        self.blurSlider.setMaximum(20)
        self.blurSlider.setValue(5)
        self.blurSlider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_6.addWidget(self.blurSlider)

        self.blurSpinBox = QSpinBox(self.letterDetectionGroup)
        self.blurSpinBox.setObjectName(u"blurSpinBox")
        self.blurSpinBox.setMaximum(20)
        self.blurSpinBox.setValue(5)

        self.horizontalLayout_6.addWidget(self.blurSpinBox)


        self.verticalLayout_3.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)

        self.letterRemovalButton = QPushButton(self.letterDetectionGroup)
        self.letterRemovalButton.setObjectName(u"letterRemovalButton")
        icon = QIcon()
        icon.addFile(u":/text-slash.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.letterRemovalButton.setIcon(icon)

        self.horizontalLayout_4.addWidget(self.letterRemovalButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)


        self.verticalLayout.addWidget(self.letterDetectionGroup)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(paintWidget)

        QMetaObject.connectSlotsByName(paintWidget)
    # setupUi

    def retranslateUi(self, paintWidget):
        paintWidget.setWindowTitle(QCoreApplication.translate("paintWidget", u"Form", None))
        self.groupBox.setTitle(QCoreApplication.translate("paintWidget", u"Pencil", None))
        self.label.setText(QCoreApplication.translate("paintWidget", u"Size", None))
        self.label_2.setText(QCoreApplication.translate("paintWidget", u"Hardness", None))
        self.hardnessSpinBox.setSuffix(QCoreApplication.translate("paintWidget", u" %", None))
        self.label_4.setText(QCoreApplication.translate("paintWidget", u"Preview", None))
        self.previewLabel.setText("")
        self.letterDetectionGroup.setTitle(QCoreApplication.translate("paintWidget", u"Letter Detection", None))
        self.label_3.setText(QCoreApplication.translate("paintWidget", u"Border", None))
        self.label_5.setText(QCoreApplication.translate("paintWidget", u"Blur", None))
        self.letterRemovalButton.setText(QCoreApplication.translate("paintWidget", u"letter removal", None))
    # retranslateUi

