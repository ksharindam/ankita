# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ankita.ui'
#
# Created: Mon Jan  2 02:33:12 2017
#      by: PyQt4 UI code generator 4.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(596, 500)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.frameShape = QtGui.QFrame(self.centralwidget)
        self.frameShape.setFrameShape(QtGui.QFrame.Box)
        self.frameShape.setFrameShadow(QtGui.QFrame.Raised)
        self.frameShape.setObjectName(_fromUtf8("frameShape"))
        self.gridLayout_2 = QtGui.QGridLayout(self.frameShape)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.lineBtn = QtGui.QPushButton(self.frameShape)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/line.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.lineBtn.setIcon(icon)
        self.lineBtn.setIconSize(QtCore.QSize(32, 32))
        self.lineBtn.setCheckable(True)
        self.lineBtn.setObjectName(_fromUtf8("lineBtn"))
        self.gridLayout_2.addWidget(self.lineBtn, 2, 0, 1, 1)
        self.pencilBtn = QtGui.QPushButton(self.frameShape)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/pencil.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pencilBtn.setIcon(icon1)
        self.pencilBtn.setIconSize(QtCore.QSize(32, 32))
        self.pencilBtn.setCheckable(True)
        self.pencilBtn.setObjectName(_fromUtf8("pencilBtn"))
        self.gridLayout_2.addWidget(self.pencilBtn, 1, 0, 1, 1)
        self.rectBtn = QtGui.QPushButton(self.frameShape)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/rectangle.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.rectBtn.setIcon(icon2)
        self.rectBtn.setIconSize(QtCore.QSize(32, 32))
        self.rectBtn.setCheckable(True)
        self.rectBtn.setObjectName(_fromUtf8("rectBtn"))
        self.gridLayout_2.addWidget(self.rectBtn, 3, 0, 1, 1)
        self.polygonBtn = QtGui.QPushButton(self.frameShape)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/polygon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.polygonBtn.setIcon(icon3)
        self.polygonBtn.setIconSize(QtCore.QSize(32, 32))
        self.polygonBtn.setCheckable(True)
        self.polygonBtn.setObjectName(_fromUtf8("polygonBtn"))
        self.gridLayout_2.addWidget(self.polygonBtn, 3, 1, 1, 1)
        self.polylineBtn = QtGui.QPushButton(self.frameShape)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/polyline.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.polylineBtn.setIcon(icon4)
        self.polylineBtn.setIconSize(QtCore.QSize(32, 32))
        self.polylineBtn.setCheckable(True)
        self.polylineBtn.setObjectName(_fromUtf8("polylineBtn"))
        self.gridLayout_2.addWidget(self.polylineBtn, 2, 1, 1, 1)
        self.brushBtn = QtGui.QPushButton(self.frameShape)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(_fromUtf8(":/brush.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.brushBtn.setIcon(icon5)
        self.brushBtn.setIconSize(QtCore.QSize(32, 32))
        self.brushBtn.setCheckable(True)
        self.brushBtn.setObjectName(_fromUtf8("brushBtn"))
        self.gridLayout_2.addWidget(self.brushBtn, 1, 1, 1, 1)
        self.ovalBtn = QtGui.QPushButton(self.frameShape)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(_fromUtf8(":/oval.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ovalBtn.setIcon(icon6)
        self.ovalBtn.setIconSize(QtCore.QSize(32, 32))
        self.ovalBtn.setCheckable(True)
        self.ovalBtn.setObjectName(_fromUtf8("ovalBtn"))
        self.gridLayout_2.addWidget(self.ovalBtn, 4, 0, 1, 1)
        self.label = QtGui.QLabel(self.frameShape)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 3)
        self.floodfillBtn = QtGui.QPushButton(self.frameShape)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(_fromUtf8(":/floodfill.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.floodfillBtn.setIcon(icon7)
        self.floodfillBtn.setIconSize(QtCore.QSize(32, 32))
        self.floodfillBtn.setCheckable(True)
        self.floodfillBtn.setObjectName(_fromUtf8("floodfillBtn"))
        self.gridLayout_2.addWidget(self.floodfillBtn, 5, 0, 1, 1)
        self.eraserBtn = QtGui.QPushButton(self.frameShape)
        self.eraserBtn.setText(_fromUtf8(""))
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(_fromUtf8(":/eraser.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.eraserBtn.setIcon(icon8)
        self.eraserBtn.setIconSize(QtCore.QSize(32, 32))
        self.eraserBtn.setCheckable(True)
        self.eraserBtn.setObjectName(_fromUtf8("eraserBtn"))
        self.gridLayout_2.addWidget(self.eraserBtn, 1, 2, 1, 1)
        self.roundedrectBtn = QtGui.QPushButton(self.frameShape)
        self.roundedrectBtn.setText(_fromUtf8(""))
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(_fromUtf8(":/roundedrect.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.roundedrectBtn.setIcon(icon9)
        self.roundedrectBtn.setIconSize(QtCore.QSize(32, 32))
        self.roundedrectBtn.setCheckable(True)
        self.roundedrectBtn.setObjectName(_fromUtf8("roundedrectBtn"))
        self.gridLayout_2.addWidget(self.roundedrectBtn, 3, 2, 1, 1)
        self.splineBtn = QtGui.QPushButton(self.frameShape)
        self.splineBtn.setText(_fromUtf8(""))
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(_fromUtf8(":/curve.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.splineBtn.setIcon(icon10)
        self.splineBtn.setIconSize(QtCore.QSize(32, 32))
        self.splineBtn.setCheckable(True)
        self.splineBtn.setObjectName(_fromUtf8("splineBtn"))
        self.gridLayout_2.addWidget(self.splineBtn, 2, 2, 1, 1)
        self.sprayBtn = QtGui.QPushButton(self.frameShape)
        self.sprayBtn.setText(_fromUtf8(""))
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(_fromUtf8(":/spray.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.sprayBtn.setIcon(icon11)
        self.sprayBtn.setIconSize(QtCore.QSize(32, 32))
        self.sprayBtn.setCheckable(True)
        self.sprayBtn.setObjectName(_fromUtf8("sprayBtn"))
        self.gridLayout_2.addWidget(self.sprayBtn, 5, 1, 1, 1)
        self.textBtn = QtGui.QPushButton(self.frameShape)
        self.textBtn.setText(_fromUtf8(""))
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(_fromUtf8(":/text.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.textBtn.setIcon(icon12)
        self.textBtn.setIconSize(QtCore.QSize(32, 32))
        self.textBtn.setCheckable(True)
        self.textBtn.setObjectName(_fromUtf8("textBtn"))
        self.gridLayout_2.addWidget(self.textBtn, 5, 2, 1, 1)
        self.arcBtn = QtGui.QPushButton(self.frameShape)
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap(_fromUtf8(":/arc.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.arcBtn.setIcon(icon13)
        self.arcBtn.setIconSize(QtCore.QSize(32, 32))
        self.arcBtn.setCheckable(True)
        self.arcBtn.setObjectName(_fromUtf8("arcBtn"))
        self.gridLayout_2.addWidget(self.arcBtn, 4, 2, 1, 1)
        self.circleBtn = QtGui.QPushButton(self.frameShape)
        self.circleBtn.setText(_fromUtf8(""))
        icon14 = QtGui.QIcon()
        icon14.addPixmap(QtGui.QPixmap(_fromUtf8(":/circle.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.circleBtn.setIcon(icon14)
        self.circleBtn.setIconSize(QtCore.QSize(32, 32))
        self.circleBtn.setCheckable(True)
        self.circleBtn.setObjectName(_fromUtf8("circleBtn"))
        self.gridLayout_2.addWidget(self.circleBtn, 4, 1, 1, 1)
        self.verticalLayout.addWidget(self.frameShape)
        self.frameColor = QtGui.QFrame(self.centralwidget)
        self.frameColor.setFrameShape(QtGui.QFrame.Box)
        self.frameColor.setFrameShadow(QtGui.QFrame.Raised)
        self.frameColor.setObjectName(_fromUtf8("frameColor"))
        self.gridLayout = QtGui.QGridLayout(self.frameColor)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_2 = QtGui.QLabel(self.frameColor)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.linecolorBtn = QtGui.QRadioButton(self.frameColor)
        self.linecolorBtn.setChecked(True)
        self.linecolorBtn.setObjectName(_fromUtf8("linecolorBtn"))
        self.gridLayout.addWidget(self.linecolorBtn, 1, 0, 1, 1)
        self.fillcolorBtn = QtGui.QRadioButton(self.frameColor)
        self.fillcolorBtn.setObjectName(_fromUtf8("fillcolorBtn"))
        self.gridLayout.addWidget(self.fillcolorBtn, 2, 0, 1, 1)
        self.checkEditColors = QtGui.QCheckBox(self.frameColor)
        self.checkEditColors.setObjectName(_fromUtf8("checkEditColors"))
        self.gridLayout.addWidget(self.checkEditColors, 3, 0, 1, 1)
        self.btnLineColor = QtGui.QPushButton(self.frameColor)
        self.btnLineColor.setMaximumSize(QtCore.QSize(46, 27))
        self.btnLineColor.setText(_fromUtf8(""))
        self.btnLineColor.setObjectName(_fromUtf8("btnLineColor"))
        self.gridLayout.addWidget(self.btnLineColor, 1, 1, 1, 1)
        self.btnFillColor = QtGui.QPushButton(self.frameColor)
        self.btnFillColor.setMaximumSize(QtCore.QSize(46, 27))
        self.btnFillColor.setObjectName(_fromUtf8("btnFillColor"))
        self.gridLayout.addWidget(self.btnFillColor, 2, 1, 1, 1)
        self.verticalLayout.addWidget(self.frameColor)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.scrollArea = QtGui.QScrollArea(self.centralwidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setAlignment(QtCore.Qt.AlignCenter)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollWidget = QtGui.QWidget()
        self.scrollWidget.setGeometry(QtCore.QRect(0, 0, 255, 454))
        self.scrollWidget.setObjectName(_fromUtf8("scrollWidget"))
        self.scrollArea.setWidget(self.scrollWidget)
        self.horizontalLayout.addWidget(self.scrollArea)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(0, -1, -1, 8)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.frameActions = QtGui.QFrame(self.centralwidget)
        self.frameActions.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frameActions.setFrameShadow(QtGui.QFrame.Raised)
        self.frameActions.setObjectName(_fromUtf8("frameActions"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.frameActions)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.undoBtn = QtGui.QPushButton(self.frameActions)
        self.undoBtn.setText(_fromUtf8(""))
        icon15 = QtGui.QIcon()
        icon15.addPixmap(QtGui.QPixmap(_fromUtf8(":/undo.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.undoBtn.setIcon(icon15)
        self.undoBtn.setObjectName(_fromUtf8("undoBtn"))
        self.horizontalLayout_3.addWidget(self.undoBtn)
        self.redoBtn = QtGui.QPushButton(self.frameActions)
        self.redoBtn.setText(_fromUtf8(""))
        icon16 = QtGui.QIcon()
        icon16.addPixmap(QtGui.QPixmap(_fromUtf8(":/redo.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.redoBtn.setIcon(icon16)
        self.redoBtn.setObjectName(_fromUtf8("redoBtn"))
        self.horizontalLayout_3.addWidget(self.redoBtn)
        self.verticalLayout_2.addWidget(self.frameActions)
        self.frameAdjust = QtGui.QFrame(self.centralwidget)
        self.frameAdjust.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frameAdjust.setFrameShadow(QtGui.QFrame.Raised)
        self.frameAdjust.setObjectName(_fromUtf8("frameAdjust"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.frameAdjust)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.labelBrush = QtGui.QLabel(self.frameAdjust)
        self.labelBrush.setObjectName(_fromUtf8("labelBrush"))
        self.verticalLayout_3.addWidget(self.labelBrush)
        self.brushSlider = QtGui.QSlider(self.frameAdjust)
        self.brushSlider.setMinimum(2)
        self.brushSlider.setMaximum(32)
        self.brushSlider.setPageStep(1)
        self.brushSlider.setProperty("value", 8)
        self.brushSlider.setOrientation(QtCore.Qt.Horizontal)
        self.brushSlider.setObjectName(_fromUtf8("brushSlider"))
        self.verticalLayout_3.addWidget(self.brushSlider)
        self.labelOpacity = QtGui.QLabel(self.frameAdjust)
        self.labelOpacity.setObjectName(_fromUtf8("labelOpacity"))
        self.verticalLayout_3.addWidget(self.labelOpacity)
        self.opacitySlider = QtGui.QSlider(self.frameAdjust)
        self.opacitySlider.setMaximum(255)
        self.opacitySlider.setPageStep(1)
        self.opacitySlider.setProperty("value", 255)
        self.opacitySlider.setOrientation(QtCore.Qt.Horizontal)
        self.opacitySlider.setObjectName(_fromUtf8("opacitySlider"))
        self.verticalLayout_3.addWidget(self.opacitySlider)
        self.labelLineWidth = QtGui.QLabel(self.frameAdjust)
        self.labelLineWidth.setObjectName(_fromUtf8("labelLineWidth"))
        self.verticalLayout_3.addWidget(self.labelLineWidth)
        self.lineSlider = QtGui.QSlider(self.frameAdjust)
        self.lineSlider.setMinimum(1)
        self.lineSlider.setMaximum(32)
        self.lineSlider.setPageStep(1)
        self.lineSlider.setOrientation(QtCore.Qt.Horizontal)
        self.lineSlider.setObjectName(_fromUtf8("lineSlider"))
        self.verticalLayout_3.addWidget(self.lineSlider)
        self.verticalLayout_2.addWidget(self.frameAdjust)
        self.frameOptions = QtGui.QFrame(self.centralwidget)
        self.frameOptions.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frameOptions.setFrameShadow(QtGui.QFrame.Raised)
        self.frameOptions.setObjectName(_fromUtf8("frameOptions"))
        self.gridLayout_4 = QtGui.QGridLayout(self.frameOptions)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.label_3 = QtGui.QLabel(self.frameOptions)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_4.addWidget(self.label_3, 1, 0, 1, 1)
        self.labelPattern = QtGui.QLabel(self.frameOptions)
        self.labelPattern.setText(_fromUtf8(""))
        self.labelPattern.setAlignment(QtCore.Qt.AlignCenter)
        self.labelPattern.setObjectName(_fromUtf8("labelPattern"))
        self.gridLayout_4.addWidget(self.labelPattern, 1, 1, 1, 1)
        self.checkPattern = QtGui.QCheckBox(self.frameOptions)
        self.checkPattern.setObjectName(_fromUtf8("checkPattern"))
        self.gridLayout_4.addWidget(self.checkPattern, 0, 0, 1, 2)
        self.verticalLayout_2.addWidget(self.frameOptions)
        self.frame = QtGui.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.gridLayout_3 = QtGui.QGridLayout(self.frame)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.verticalLayout_2.addWidget(self.frame)
        self.labelZoom = QtGui.QLabel(self.centralwidget)
        self.labelZoom.setObjectName(_fromUtf8("labelZoom"))
        self.verticalLayout_2.addWidget(self.labelZoom)
        self.zoomSlider = QtGui.QSlider(self.centralwidget)
        self.zoomSlider.setMinimum(1)
        self.zoomSlider.setMaximum(8)
        self.zoomSlider.setPageStep(1)
        self.zoomSlider.setOrientation(QtCore.Qt.Horizontal)
        self.zoomSlider.setObjectName(_fromUtf8("zoomSlider"))
        self.verticalLayout_2.addWidget(self.zoomSlider)
        self.verticalLayout_2.setStretch(3, 1)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.horizontalLayout.setStretch(1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 596, 24))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuEdit = QtGui.QMenu(self.menubar)
        self.menuEdit.setObjectName(_fromUtf8("menuEdit"))
        self.menuTransform = QtGui.QMenu(self.menubar)
        self.menuTransform.setObjectName(_fromUtf8("menuTransform"))
        MainWindow.setMenuBar(self.menubar)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuTransform.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Ankita", None))
        self.lineBtn.setToolTip(_translate("MainWindow", "Straight Line", None))
        self.pencilBtn.setToolTip(_translate("MainWindow", "Pencil", None))
        self.rectBtn.setToolTip(_translate("MainWindow", "Rectangle", None))
        self.polygonBtn.setToolTip(_translate("MainWindow", "Polygon", None))
        self.polylineBtn.setToolTip(_translate("MainWindow", "Polyline", None))
        self.brushBtn.setToolTip(_translate("MainWindow", "Brush", None))
        self.ovalBtn.setToolTip(_translate("MainWindow", "Oval", None))
        self.label.setText(_translate("MainWindow", "<b>Drawing Tools<b>", None))
        self.floodfillBtn.setToolTip(_translate("MainWindow", "Floodfill", None))
        self.eraserBtn.setToolTip(_translate("MainWindow", "Eraser", None))
        self.roundedrectBtn.setToolTip(_translate("MainWindow", "Rounded Rect", None))
        self.splineBtn.setToolTip(_translate("MainWindow", "Curved Line", None))
        self.sprayBtn.setToolTip(_translate("MainWindow", "Color Spray", None))
        self.arcBtn.setToolTip(_translate("MainWindow", "Arc", None))
        self.circleBtn.setToolTip(_translate("MainWindow", "Centered Circle", None))
        self.label_2.setText(_translate("MainWindow", "<b>Color Tools<b>", None))
        self.linecolorBtn.setText(_translate("MainWindow", "Set Line :", None))
        self.fillcolorBtn.setText(_translate("MainWindow", "Set Fill :", None))
        self.checkEditColors.setToolTip(_translate("MainWindow", "Click on palette \n"
"to change colors", None))
        self.checkEditColors.setText(_translate("MainWindow", "Edit Colors", None))
        self.btnFillColor.setText(_translate("MainWindow", "x", None))
        self.undoBtn.setToolTip(_translate("MainWindow", "Undo", None))
        self.redoBtn.setToolTip(_translate("MainWindow", "Redo", None))
        self.labelBrush.setText(_translate("MainWindow", "Brush Size : 8", None))
        self.labelOpacity.setText(_translate("MainWindow", "Fill Opacity : 255", None))
        self.labelLineWidth.setText(_translate("MainWindow", "Line Width : 1", None))
        self.label_3.setText(_translate("MainWindow", "Pattern :", None))
        self.checkPattern.setText(_translate("MainWindow", "Use Pattern \n"
" in Brush", None))
        self.labelZoom.setText(_translate("MainWindow", "  Zoom :   1x", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit", None))
        self.menuTransform.setTitle(_translate("MainWindow", "Transform", None))

import ankita_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

