#!/usr/bin/env python
__version__ = '3.2'

import sys, os
import ui_ankita
from PIL import Image, ImageDraw, ImageQt
from random import randint

from PyQt4.QtCore import pyqtSignal, QPoint, Qt, QSettings
from PyQt4.QtGui import QApplication, QMainWindow, QLabel, QHBoxLayout, QGridLayout, QPixmap
from PyQt4.QtGui import QPainter, QPainterPath, QPen, QBrush, qRgb, QColor, QCursor, QFont, QFontMetrics
from PyQt4.QtGui import QFontComboBox, QSlider, QLineEdit, QTransform
from PyQt4.QtGui import QDialog, QDialogButtonBox, QFileDialog, QColorDialog, QButtonGroup

default_clr_array = [
"#ffffff", "#ffffff", "#cccccc", "#999999", "#666666", "#000000",
"#e066ff", "#d15fee", "#9b30ff", "#912cee", "#7d26cd", "#551a8b",
"#4169e1", "#3a5fcd", "#0000ff", "#0000ee", "#0000cd", "#00008b",
"#c0ffc0", "#80ff80", "#00ff00", "#00ee00", "#00cd00", "#008b00",
"#ff6a6a", "#ff3030", "#ff0000", "#ee0000", "#cd0000", "#8b0000",
"#ffff00", "#ffa500", "#00ffff", "#008b8b", "#ff00ff", "#8b008b",
"#ffffff", "#ffffff", "#ffffff", "#ffffff", "#ffffff", "#ffffff", 
"#ffffff", "#ffffff", "#ffffff", "#ffffff", "#ffffff", "#ffffff"
]

pattern_array = [
":/densedots.png", ":/dots.png", ":/zigzag.png", ":/brick.png", ":/hlines.png"
]

def brush_cursor(thickness):
    pm = QPixmap(thickness, thickness)
    pm.fill(QColor(0,0,0,0))
    painter = QPainter(pm)
    painter.drawEllipse(0,0, thickness-1, thickness-1)
    painter.setPen(Qt.white)
    painter.drawEllipse(1,1, thickness-3, thickness-3)
    painter.end()
    return QCursor(pm)

class Label(QLabel):
    """ It is the Canvas on which drawing is done """
    mouseClicked = pyqtSignal(QPoint, bool)
    mouseReleased = pyqtSignal(QPoint)
    mouseMoved = pyqtSignal(QPoint)
    def __init__(self, width, height, parent):
        super(Label, self).__init__(parent)
        self.setSizePolicy(0, 0) #QSizePolicy.Fixed
        self.pixmap = QPixmap(width,height)
        self.pixmap.fill()
        self.setMouseTracking(True)
        self.mouse_pressed = False
        self.history = []
        self.current_index = -1
        self.scale = 1
        self.setCursor(QCursor(QPixmap(":/cursor_pencil.png")))
        #self.setCursor(brush_cursor(8))
        self.update()
        self.updateHistory()
    def mousePressEvent(self, ev):
        self.mouse_pressed = True
        self.mouseClicked.emit(QPoint(ev.x()/self.scale, ev.y()/self.scale), True)
        #print "%ix%i"%(ev.x(),ev.y())
    def mouseMoveEvent(self, ev):
        self.mouseMoved.emit(QPoint(ev.x()/self.scale, ev.y()/self.scale))
    def mouseReleaseEvent(self, ev):
        self.mouseReleased.emit(QPoint(ev.x()/self.scale, ev.y()/self.scale))
        self.mouse_pressed = False

    def setPixmap(self, pixmap):
        if self.scale != 1:
            pixmap = pixmap.scaledToWidth(self.pixmap.width()*self.scale)
        super(Label, self).setPixmap(pixmap)
    def update(self):
        self.setPixmap(self.pixmap)

    def updateHistory(self):
        """ Appends copy of current pixmap to undo list """
        pixmap = self.pixmap.copy()
        if len(self.history) > self.current_index+1:
            del self.history[self.current_index+1:]
        self.history.append(pixmap)
        self.current_index += 1
        if self.current_index == 21: # Max Undo = 20
            self.history.pop(0)
            self.current_index -= 1
    def undo(self):
        if self.current_index==0:
            return
        self.pixmap = self.history[self.current_index-1].copy()
        self.update()
        self.current_index -= 1
        self.text_input = False
    def redo(self):
        if self.current_index==len(self.history)-1:
            return
        self.pixmap = self.history[self.current_index+1].copy()
        self.update()
        self.current_index += 1
        self.text_input = False


class ColorGrid(QLabel):
    """ Color Palette that holds many colors. Emit signal with QColor when a color is clicked"""
    colorSelected = pyqtSignal(QColor)
    def __init__(self, parent):
        super(ColorGrid, self).__init__(parent)
        self.setSizePolicy(0, 0) #QSizePolicy.Fixed
        self.column = 6
        self.row = 8
        self.box_size = 24
        self.pixmap = QPixmap(self.column*self.box_size+1,self.row*self.box_size+1)
        self.pixmap.fill()
        self.drawPalette()
        self.edit_colors = False
    def drawPalette(self):
        painter = QPainter()
        painter.begin(self.pixmap)
        for index,color in enumerate(clr_array):
            painter.setBrush(QBrush(QColor(color)))
            painter.drawRect((index%self.column)*self.box_size,
                            (index//self.column)*self.box_size, self.box_size,self.box_size)
        painter.drawLine(0,0,self.box_size,self.box_size)
        painter.drawLine(0,self.box_size,self.box_size,0)
        painter.end()
        self.setPixmap(self.pixmap)

    def mousePressEvent(self, ev):
        x, y = ev.x(), ev.y()
        if x == 0 or y == 0: return
        index = ((y-1)//self.box_size) * self.column + (x-1)//self.box_size
        if index >= len(clr_array): return
        color = QColor(clr_array[index])
        if self.edit_colors:
            if index == 0: return
            color = QColorDialog.getColor(color, self)
            if color.isValid():
                clr_array[index] = color
                self.drawPalette()
            return
        if index == 0:
            color.setAlpha(0)
        self.colorSelected.emit(color)
    def resetPalette(self):
        global clr_array
        clr_array = default_clr_array[:]
        self.drawPalette()

class PatternGrid(QLabel):
    """ Pattern Grid that holds many patterns. Emit signal with QPixmap when clicked"""
    patternSelected = pyqtSignal(QPixmap)
    def __init__(self, parent):
        super(PatternGrid, self).__init__(parent)
        self.setSizePolicy(0, 0) #QSizePolicy.Fixed
        self.column = 5
        self.row = 1
        self.box_size = 24
        self.pixmap = QPixmap(self.column*self.box_size+1,self.row*self.box_size+1)
        self.pixmap.fill()
        self.drawPalette()
    def drawPalette(self):
        painter = QPainter()
        painter.begin(self.pixmap)
        for index,pattern in enumerate(pattern_array):
            painter.drawPixmap((index%self.column)*self.box_size,
                            (index//self.column)*self.box_size, QPixmap(pattern))
            painter.drawRect((index%self.column)*self.box_size,
                            (index//self.column)*self.box_size, self.box_size,self.box_size)
        painter.end()
        self.setPixmap(self.pixmap)

    def mousePressEvent(self, ev):
        x, y = ev.x(), ev.y()
        if x == 0 or y == 0: return
        index = ((y-1)//self.box_size) * self.column + (x-1)//self.box_size
        if index >= len(pattern_array): return
        pattern = QPixmap(pattern_array[index])
        self.patternSelected.emit(pattern)

class Window(QMainWindow, ui_ankita.Ui_MainWindow):
    """ This class creates main window and all child widgets """
    def __init__(self):
        QMainWindow.__init__(self)
        self.filename = ""
        self.points = []
        self.btnMode = "pencil"
        self.corner_roundness = 20
        self.line_width = 0
        self.brush_size = 8
        self.eraser_size = 32
        self.spray_size = 24
        self.spray_density = 3
        self.brush_color = QColor(0,0,0,0)
        self.brush_pattern = QPixmap(":/dots.png")
        self.painter = QPainter()
        self.pen = QPen()
        self.pen.setCapStyle(Qt.RoundCap)
        self.brush = QBrush(self.brush_color)
        self.settings = QSettings()
        global clr_array
        clr_array = list(self.settings.value("ColorPalette", default_clr_array[:]).toStringList())
        self.setupUi(self)
    def setupUi(self, win):
        super(Window, self).setupUi(win)
        # Change some widget property
        self.btnLineColor.setStyleSheet("QPushButton{background-color: #000000;}")
        self.gridLayout.setRowStretch(5,1)
        self.gridLayout_3.setRowStretch(6, True)
        # Add additional widgets
        self.gridLayout.removeWidget(self.checkEditColors)
        self.status = QLabel("Pointer : 0, 0", win)
        self.status.setFixedSize(140, 16)
        self.menubar.setCornerWidget(self.status)
        canvaswidth = int(self.settings.value("CanvasWidth", 800).toString())
        canvasheight = int(self.settings.value("CanvasHeight", 600).toString())
        self.canvas = Label(canvaswidth, canvasheight, win)
        self.canvas.setStyleSheet("QLabel{background-color: #cccccc;}")
        #self.canvas.setStyleSheet("QLabel{background-image:url(:/pencil.png);}")
        hLayout = QHBoxLayout(self.scrollWidget)
        hLayout.addWidget(self.canvas)
        self.color_picker = ColorPicker(win)
        self.gridLayout.addWidget(self.color_picker,0,1,1,1)
        self.palette = ColorGrid(win)
        self.gridLayout.addWidget(self.palette,3,0,1,2)
        self.gridLayout.addWidget(self.checkEditColors,4,0,1,2)
        self.labelPattern.setPixmap(self.brush_pattern)
        self.labelPattern.setFrameShape(0x0002)
        self.labelPattern.setSizePolicy(0, 0) #QSizePolicy.Fixed
        self.pattern_grid = PatternGrid(win)
        self.gridLayout_4.addWidget(self.pattern_grid, 2,0,1,2)
        # Create Menu Actions
        self.menuFile.addAction("New", self.newImage, "Ctrl+N")
        self.menuFile.addAction("New...", self.newWithSize, "Ctrl+Shift+N")
        self.menuFile.addAction("Open", self.openImage, "Ctrl+O")
        self.menuFile.addAction("Save", self.saveImage, "Ctrl+S")
        self.menuFile.addAction("Save As..", self.saveImageAs, "Ctrl+Shift+S")
        self.menuFile.addAction("Quit", win.close, "Ctrl+Q")
        self.menuEdit.addAction("Undo", self.canvas.undo, "Ctrl+Z")
        self.menuEdit.addAction("Redo", self.canvas.redo, "Ctrl+Y")
        self.menuEdit.addAction("Expand Canvas", self.expandCanvas)
        self.menuEdit.addAction("Reset Palette", self.palette.resetPalette)
        self.menuTransform.addAction("Resize", self.resizeImage)
        self.menuTransform.addAction("Rotate Left", self.rotateLeft)
        self.menuTransform.addAction("Rotate Right", self.rotateRight)
        self.menuTransform.addAction("Rotate by...", self.rotateAnyAngle)
        self.menuTransform.addAction("Flip", self.flipImage)
        self.menuTransform.addAction("Flop", self.flopImage)
        # Add buttons to button group
        self.btnGroup = QButtonGroup(win)
        for button in [self.pencilBtn, self.brushBtn, self.floodfillBtn, self.lineBtn,
                   self.rectBtn, self.ovalBtn, self.arcBtn, self.polylineBtn, self.polygonBtn,
                   self.textBtn, self.eraserBtn, self.splineBtn, self.roundedrectBtn,
                   self.circleBtn, self.sprayBtn]:
            self.btnGroup.addButton(button)
        # Connect Shapes/brushes with signals
        self.btnGroup.buttonPressed.connect(self.onBtnClick)
        self.canvas.mouseClicked.connect(self.onClick)
        self.canvas.mouseMoved.connect(self.onClick)
        self.canvas.mouseMoved.connect(self.setStatus)
        self.canvas.mouseReleased.connect(self.onRelease)
        self.palette.colorSelected.connect(self.setColor)
        self.color_picker.colorSelected.connect(self.setColor)
        self.checkEditColors.toggled.connect(self.toggleColorEdit)
        self.btnLineColor.clicked.connect(self.setLineColor)
        self.btnFillColor.clicked.connect(self.setFillColor)
        self.pattern_grid.patternSelected.connect(self.setPattern)
        self.brushSlider.valueChanged.connect(self.setBrushSize)
        self.lineSlider.valueChanged.connect(self.setLineWidth)
        self.opacitySlider.valueChanged.connect(self.setFillOpacity)
        self.zoomSlider.valueChanged.connect(self.setZoom)
        self.undoBtn.clicked.connect(self.canvas.undo)
        self.redoBtn.clicked.connect(self.canvas.redo)
        # This will be after connecting signal of that button
        self.pencilBtn.setChecked(True)
        self.setWindowTitle("Ankita - " + __version__)
    def onBtnClick(self, button):
        """ Initializes all on brush button change"""
        if self.btnMode == "polygon":
            self.drawpolygon(0,0,True)
            self.canvas.updateHistory()
        if self.btnMode == "polyline":
            self.canvas.updateHistory()
        if self.textBtn.isChecked():
            for widget in [self.labelText, self.textEdit, self.labelTextFont,
                           self.fontComboBox, self.labelFontSize, self.fontSizeSlider]:
                self.gridLayout_3.removeWidget(widget)
                widget.deleteLater()
        elif self.eraserBtn.isChecked():
            for widget in [self.labelEraser, self.eraserSizeSlider]:
                self.gridLayout_3.removeWidget(widget)
                widget.deleteLater()
        elif self.splineBtn.isChecked():
            self.finishspline()
        elif self.roundedrectBtn.isChecked():
            for widget in [self.labelRoundness, self.roundnessSlider]:
                self.gridLayout_3.removeWidget(widget)
                widget.deleteLater()
        elif self.sprayBtn.isChecked():
            for widget in [self.labelSpraySize, self.spraySizeSlider, self.labelSprayDensity, self.sprayDensitySlider]:
                self.gridLayout_3.removeWidget(widget)
                widget.deleteLater()
        self.canvas.update()
        self.btnMode = None
        self.points = []
        if self.btnGroup.id(button)==-2: # Pen
            self.btnMode = "pencil"
            self.pen.setWidth(0)
            self.linecolorBtn.setChecked(True)
            self.canvas.setCursor(QCursor(QPixmap(":/cursor_pencil.png")))
        elif self.btnGroup.id(button)==-3: # Brush
            self.btnMode = "pencil"
            self.pen.setWidth(self.brush_size)
            self.linecolorBtn.setChecked(True)
            self.canvas.setCursor(brush_cursor(self.brush_size*self.canvas.scale))
        elif self.btnGroup.id(button)==-12: # Eraser
            self.btnMode = "pencil"
            self.canvas.setCursor(brush_cursor(self.eraser_size*self.canvas.scale))
            self.labelEraser = QLabel("Eraser Size : %i"%self.eraser_size)
            self.eraserSizeSlider = QSlider(Qt.Horizontal, self.frameOptions)
            self.eraserSizeSlider.setMinimum(4)
            self.eraserSizeSlider.setMaximum(64)
            self.eraserSizeSlider.setValue(self.eraser_size)
            self.eraserSizeSlider.setPageStep(1)
            self.gridLayout_3.addWidget(self.labelEraser, 0,0)
            self.gridLayout_3.addWidget(self.eraserSizeSlider, 1,0)
            self.eraserSizeSlider.valueChanged.connect(self.setEraserSize)
        elif self.btnGroup.id(button)==-4: # Floodfill
            self.fillcolorBtn.setChecked(True)
            self.canvas.setCursor(QCursor(QPixmap(":/cursor_plus.png")))
        elif self.btnGroup.id(button)==-11: # Draw Text
            self.linecolorBtn.setChecked(True)
            self.labelText = QLabel("Enter Text :")
            self.textEdit = QLineEdit(self.frameOptions)
            self.textEdit.setMaximumWidth(111)
            self.labelTextFont = QLabel("Text Font :", self.frameOptions)
            self.fontComboBox = QFontComboBox(self.frameOptions)
            self.fontComboBox.setMaximumWidth(111)
            self.fontComboBox.setEditable(False)
            self.labelFontSize = QLabel("Font Size : 24", self.frameOptions)
            self.fontSizeSlider = QSlider(Qt.Horizontal, self.frameOptions)
            self.fontSizeSlider.setMinimum(6)
            self.fontSizeSlider.setMaximum(72)
            self.fontSizeSlider.setValue(24)
            self.fontSizeSlider.setPageStep(1)
            self.gridLayout_3.addWidget(self.labelText, 0,0)
            self.gridLayout_3.addWidget(self.textEdit, 1,0)
            self.gridLayout_3.addWidget(self.labelTextFont, 2,0)
            self.gridLayout_3.addWidget(self.fontComboBox, 3,0)
            self.gridLayout_3.addWidget(self.labelFontSize, 4,0)
            self.gridLayout_3.addWidget(self.fontSizeSlider, 5,0)
            self.textEdit.textChanged.connect(self.drawCursorText)
            self.fontComboBox.currentFontChanged.connect(self.drawCursorText)
            self.fontSizeSlider.valueChanged.connect(self.updateFontSize)
        elif self.btnGroup.id(button)==-13: # curve
            self.cp1, self.cp2 = [], []
            self.pen.setWidth(self.line_width)
            self.canvas.setCursor(QCursor(QPixmap(":/cursor_plus.png")))
        elif self.btnGroup.id(button)==-14: # Rounded rect
            self.canvas.setCursor(QCursor(QPixmap(":/cursor_plus.png")))
            self.labelRoundness = QLabel("Roundness : {}%".format(self.corner_roundness))
            self.roundnessSlider = QSlider(Qt.Horizontal, self.frameOptions)
            self.roundnessSlider.setMinimum(4)
            self.roundnessSlider.setMaximum(80)
            self.roundnessSlider.setValue(self.corner_roundness)
            self.roundnessSlider.setPageStep(1)
            self.gridLayout_3.addWidget(self.labelRoundness, 0,0)
            self.gridLayout_3.addWidget(self.roundnessSlider, 1,0)
            self.roundnessSlider.valueChanged.connect(self.setCornerRoundness)
            self.pen.setWidth(self.line_width)
        elif self.btnGroup.id(button)==-16: # Spray
            self.btnMode = "pencil"
            self.pen.setWidth(0)
            self.linecolorBtn.setChecked(True)
            self.canvas.setCursor(brush_cursor(self.spray_size*self.canvas.scale))
            self.labelSpraySize = QLabel("Spray Size : {}".format(self.spray_size))
            self.spraySizeSlider = QSlider(Qt.Horizontal, self.frameOptions)
            self.spraySizeSlider.setMinimum(16)
            self.spraySizeSlider.setMaximum(64)
            self.spraySizeSlider.setValue(self.spray_size)
            self.spraySizeSlider.setPageStep(1)
            self.labelSprayDensity = QLabel("Density : {}".format(self.spray_density))
            self.sprayDensitySlider = QSlider(Qt.Horizontal, self.frameOptions)
            self.sprayDensitySlider.setMinimum(1)
            self.sprayDensitySlider.setMaximum(6)
            self.sprayDensitySlider.setValue(self.spray_density)
            self.sprayDensitySlider.setPageStep(1)
            self.gridLayout_3.addWidget(self.labelSpraySize, 0,0)
            self.gridLayout_3.addWidget(self.spraySizeSlider, 1,0)
            self.gridLayout_3.addWidget(self.labelSprayDensity, 2,0)
            self.gridLayout_3.addWidget(self.sprayDensitySlider, 3,0)
            self.spraySizeSlider.valueChanged.connect(self.setSpraySize)
            self.sprayDensitySlider.valueChanged.connect(self.setSprayDensity)
        else:
            self.pen.setWidth(self.line_width)
            self.canvas.setCursor(QCursor(QPixmap(":/cursor_plus.png")))
    def onClick(self, pos, clicked=False):
        """ It is called when mouse is moved or clicked over canvas"""
        if self.btnGroup.checkedId()==-2:
            self.drawbypencil(pos, clicked)
        elif self.btnGroup.checkedId()==-3:
            self.drawbybrush(pos, clicked)
        elif self.btnGroup.checkedId()==-4:
            self.floodfill(pos, clicked)
        elif self.btnGroup.checkedId()==-5:
            self.drawline(pos, clicked)
        elif self.btnGroup.checkedId()==-6:
            self.drawrect(pos, clicked)
        elif self.btnGroup.checkedId()==-7:
            self.drawoval(pos, clicked)
        elif self.btnGroup.checkedId()==-8:
            self.drawarc(pos, clicked)
        elif self.btnGroup.checkedId()==-9:
            self.drawpolyline(pos, clicked)
        elif self.btnGroup.checkedId()==-10:
            self.drawpolygon(pos, clicked)
        elif self.btnGroup.checkedId()==-11:
            self.drawText(pos, clicked)
        elif self.btnGroup.checkedId()==-12:
            self.erase(pos, clicked)
        elif self.btnGroup.checkedId()==-13:
            self.drawspline(pos, clicked)
        elif self.btnGroup.checkedId()==-14:
            self.drawroundedrect(pos, clicked)
        elif self.btnGroup.checkedId()==-15:
            self.drawcenteredcircle(pos, clicked)
        elif self.btnGroup.checkedId()==-16:
            self.spray(pos, clicked)
    def onRelease(self):
        if self.btnMode == "pencil":
            self.canvas.updateHistory()
            self.painter.end()

    def drawbypencil(self, pos, clicked):
        """ Draw non-straight line with pencil """
        if clicked:
            self.points = [pos]
            self.beginPainter(self.canvas.pixmap)
        if self.canvas.mouse_pressed:
            if len(self.points)==1:
                self.painter.drawLine(self.points[0], pos)
                self.canvas.update()
                self.points = [pos]

    def drawbybrush(self, pos, clicked):
        """ Paint with thick brush """
        if clicked:
            self.points = [pos]
            self.beginPainter(self.canvas.pixmap)
        if self.canvas.mouse_pressed:
            if len(self.points)==1:
                self.painter.drawLine(self.points[0], pos)
                self.canvas.update()
                self.points = [pos]

    def erase(self, pos, clicked):
        if clicked:
            self.points = [pos]
            self.painter.begin(self.canvas.pixmap)
            pen = QPen(Qt.white)
            pen.setCapStyle(Qt.RoundCap)
            pen.setWidth(self.eraser_size)
            self.painter.setPen(pen)
        if self.canvas.mouse_pressed:
            if len(self.points)==1:
                self.painter.drawLine(self.points[0], pos)
                self.canvas.update()
                self.points = [pos]
    def setEraserSize(self, size):
        self.eraser_size = size
        self.canvas.setCursor(brush_cursor(self.eraser_size*self.canvas.scale))
        self.labelEraser.setText("Eraser Size : %i"%size)

    def drawline(self, pos, clicked):
        """ Draw Straight line"""
        if clicked:
            self.points.append(pos)
            if len(self.points) == 2:
                self.beginPainter(self.canvas.pixmap)
                self.painter.drawLine(self.points[0], pos)
                self.painter.end()
                self.canvas.update()
                self.points = []
                self.canvas.updateHistory()
        else:
            if len(self.points)==1:
                pm = self.canvas.pixmap.copy()
                self.beginPainter(pm)
                self.painter.drawLine(self.points[0], pos)
                self.painter.end()
                self.canvas.setPixmap(pm)

    def drawspline(self, pos, clicked):
        if clicked:
            self.points.append(pos)
            if len(self.points) >= 3:
                x = len(self.points)-3
                calcspline(self.points, self.cp1, self.cp2)
                path = QPainterPath(self.points[x])
                path.cubicTo(self.cp1[x], self.cp2[x], self.points[x+1])
                self.painter.begin(self.canvas.pixmap)
                self.painter.setPen(self.pen)
                self.painter.drawPath(path)
                self.painter.end()
                self.canvas.update()
                self.canvas.updateHistory()
        else:
            x = len(self.points)-2
            if x == -2 : return
            path = QPainterPath(self.points[x])
            if x > -1:
                points = self.points[:] + [pos]
                cp1, cp2 = self.cp1[:], self.cp2[:]
                calcspline(points, cp1, cp2)
                path.cubicTo(cp1[x], cp2[x], self.points[x+1])
                path.cubicTo(cp1[x+1], cp2[x+1], pos)
            else:
                path.lineTo(pos)
            pm = self.canvas.pixmap.copy()
            self.painter.begin(pm)
            self.painter.setPen(self.pen)
            self.painter.drawPath(path)
            self.painter.end()
            self.canvas.setPixmap(pm)
    def finishspline(self):
        x = len(self.points)-2
        if x<0 : return
        path = QPainterPath(self.points[x])
        if x == 0:
            path.lineTo(self.points[1])
        else:
            path.cubicTo(self.cp1[x], self.cp2[x], self.points[x+1])
        self.painter.begin(self.canvas.pixmap)
        self.painter.setPen(self.pen)
        self.painter.drawPath(path)
        self.painter.end()
        self.canvas.update()
        self.canvas.updateHistory()

    def drawrect(self, pos, clicked=False):
        """ Draw Rectangle """
        if clicked:
            self.points.append(pos)
            if len(self.points) == 2:
                x = self.points[0].x()
                y = self.points[0].y()
                self.beginPainter(self.canvas.pixmap)
                self.painter.drawRect(x,y, pos.x()-x,pos.y()-y)
                self.painter.end()
                self.canvas.update()
                self.points = []
                self.canvas.updateHistory()
        else:
            if len(self.points)==1:
                x = self.points[0].x()
                y = self.points[0].y()
                pm = self.canvas.pixmap.copy()
                self.beginPainter(pm)
                self.painter.drawRect(x,y, pos.x()-x,pos.y()-y)
                self.painter.end()
                self.canvas.setPixmap(pm)

    def drawroundedrect(self, pos, clicked):
        if clicked:
            self.points.append(pos)
            if len(self.points) == 2:
                x = self.points[0].x()
                y = self.points[0].y()
                if x > pos.x() : x = pos.x()
                if y > pos.y() : y = pos.y()
                w = abs(pos.x()-self.points[0].x())
                h = abs(pos.y()-self.points[0].y())
                self.beginPainter(self.canvas.pixmap)
                self.painter.drawRoundedRect(x,y, w, h, self.corner_roundness, self.corner_roundness, 1)
                self.painter.end()
                self.canvas.update()
                self.points = []
                self.canvas.updateHistory()
        else:
            if len(self.points)==1:
                x, y = self.points[0].x(), self.points[0].y()
                if x > pos.x() : x = pos.x()
                if y > pos.y() : y = pos.y()
                w = abs(pos.x()-self.points[0].x())
                h = abs(pos.y()-self.points[0].y())
                pm = self.canvas.pixmap.copy()
                self.beginPainter(pm)
                self.painter.drawRoundedRect(x,y, w, h, self.corner_roundness, self.corner_roundness, 1)
                self.painter.end()
                self.canvas.setPixmap(pm)
    def setCornerRoundness(self, value):
        self.corner_roundness = value
        self.labelRoundness.setText("Roundness : {}%".format(value))

    def drawpolyline(self, pos, clicked):
        """ Draw Poly Line"""
        if clicked:
            self.points.append(pos)
            self.btnMode = "polyline"
            if len(self.points) > 1:
                self.beginPainter(self.canvas.pixmap)
                apply(self.painter.drawPolyline, self.points)
                self.painter.end()
                self.canvas.update()
        else:
            if len(self.points)!=0:
                pm = self.canvas.pixmap.copy()
                self.beginPainter(pm)
                points = self.points[:]
                points.append(pos)
                apply(self.painter.drawPolyline, points)
                self.painter.end()
                self.canvas.setPixmap(pm)

    def drawpolygon(self, pos, clicked, finaldraw=False):
        """ Draw Polygon"""
        if finaldraw:
            if len(self.points)>1:
                self.beginPainter(self.canvas.pixmap)
                apply(self.painter.drawPolygon, self.points)
                self.painter.end()
                return
        if clicked:
            self.points.append(pos)
            self.btnMode = "polygon"
        else:
            if len(self.points)!=0:
                pm = self.canvas.pixmap.copy()
                self.beginPainter(pm)
                points = self.points[:]
                points.append(pos)
                apply(self.painter.drawPolygon, points)
                self.painter.end()
                self.canvas.setPixmap(pm)
                
    def drawoval(self, pos, clicked=False):
        """ Draw Oval """
        if clicked:
            self.points.append(pos)
            if len(self.points) == 2:
                x = self.points[0].x()
                y = self.points[0].y()
                self.beginPainter(self.canvas.pixmap)
                self.painter.drawEllipse(x,y, pos.x()-x,pos.y()-y)
                self.painter.end()
                self.canvas.update()
                self.points = []
                self.canvas.updateHistory()
        else:
            if len(self.points)==1:
                x = self.points[0].x()
                y = self.points[0].y()
                pm = self.canvas.pixmap.copy()
                self.beginPainter(pm)
                self.painter.drawEllipse(x,y, pos.x()-x,pos.y()-y)
                self.painter.end()
                self.canvas.setPixmap(pm)

    def drawcenteredcircle(self, pos, clicked):
        if clicked:
            self.points.append(pos)
            if len(self.points) == 2:
                r = sqrt((pos.x()-self.points[0].x())**2 + (pos.y()-self.points[0].y())**2)
                x = self.points[0].x()-r
                y = self.points[0].y()-r
                self.beginPainter(self.canvas.pixmap)
                self.painter.drawEllipse(x,y, 2*r+1,2*r+1)
                self.painter.end()
                self.canvas.update()
                self.points = []
                self.canvas.updateHistory()
        else:
            if len(self.points)==1:
                r = sqrt((pos.x()-self.points[0].x())**2 + (pos.y()-self.points[0].y())**2)
                x = self.points[0].x()-r
                y = self.points[0].y()-r
                pm = self.canvas.pixmap.copy()
                self.beginPainter(pm)
                self.painter.drawEllipse(x,y, 2*r+1,2*r+1)
                self.painter.end()
                self.canvas.setPixmap(pm)

    def drawarc(self, pos, clicked=False):
        """ Draw Arc """
        if clicked:
            self.points.append(pos)
            if len(self.points) == 3:
                x1 = self.points[0].x()
                y1 = self.points[0].y()
                x2 = self.points[1].x()
                y2 = self.points[1].y()
                x,y,r,start_ang,extent_ang = calc_arc(x1,y1,x2,y2,pos.x(),pos.y())
                self.beginPainter(self.canvas.pixmap)
                self.painter.drawArc(x-r,y-r, 2*r,2*r, start_ang*16,extent_ang*16)
                self.painter.end()
                self.canvas.update()
                self.points = []
                self.canvas.updateHistory()
        else:
            if len(self.points)==1:
                pm = self.canvas.pixmap.copy()
                self.beginPainter(pm)
                self.painter.drawLine(self.points[0], pos)
                self.painter.end()
                self.canvas.setPixmap(pm)
            elif len(self.points)==2:
                x1 = self.points[0].x()
                y1 = self.points[0].y()
                x2 = self.points[1].x()
                y2 = self.points[1].y()
                x,y,r,start_ang,extent_ang = calc_arc(x1,y1,x2,y2,pos.x(),pos.y())
                pm = self.canvas.pixmap.copy()
                self.beginPainter(pm)
                self.painter.drawArc(x-r,y-r, 2*r,2*r, start_ang*16,extent_ang*16)
                self.painter.end()
                self.canvas.setPixmap(pm)

    def spray(self, pos, clicked):
        if not self.canvas.mouse_pressed: return
        if clicked : 
            self.beginPainter(self.canvas.pixmap)
        size = self.spray_size/2
        points = []
        for i in range(size*self.spray_density):
          x = randint(-size, +size)
          y = randint(-size, +size)
          if x*x + y*y < size*size: # for circular area spray
            points.append(QPoint(x+pos.x(), y+pos.y()))
        apply(self.painter.drawPoints, points)
        self.canvas.update()
    def setSpraySize(self, value):
        self.spray_size = value
        self.labelSpraySize.setText("Spray Size : %i"%value)
        self.canvas.setCursor(brush_cursor(self.spray_size*self.canvas.scale))
    def setSprayDensity(self, value):
        self.spray_density = value
        self.labelSprayDensity.setText("Density : %i"%value)

    def floodfill(self, pos, clicked):
        """ Floodfill using python-pil"""
        if not clicked: return
        color = self.brush_color
        if color == QColor(0,0,0,0): color.setAlpha(255)
        image = self.canvas.pixmap.toImage()
        if image.pixel(pos) == color.rgba(): return
        rgba = (color.red(), color.green(), color.blue(), color.alpha())
        # Convert QImage to PIL image
        bytes = image.bits().asstring(image.numBytes())
        pil_img = Image.fromstring("RGBA",(image.width(), image.height()), bytes, "raw", "BGRA")
        # Floodfill and revert PIL Image to QImage
        ImageDraw.floodfill(pil_img, (pos.x(),pos.y()), rgba)
        image = ImageQt.ImageQt(pil_img)
        self.canvas.pixmap = QPixmap.fromImage(image)
        self.canvas.update()
        self.canvas.updateHistory()

    def drawText(self, pos, clicked):
        """ Fixes text when clicked"""
        if clicked:
            text = self.textEdit.text()
            font = self.fontComboBox.currentFont()
            font.setPixelSize(self.fontSizeSlider.value())
            fontmetrics = QFontMetrics(font)
            w = fontmetrics.width(text)
            h = fontmetrics.height()
            self.painter.begin(self.canvas.pixmap)
            self.painter.setPen(self.pen)
            self.painter.setFont(font)
            self.painter.drawText(pos.x(),pos.y(), w,h, Qt.AlignLeft|Qt.AlignVCenter, text)
            self.painter.end()
            self.canvas.update()
            self.canvas.updateHistory()
    def drawCursorText(self):
        """ Draws cursor when text, font or size is changed """
        text = self.textEdit.text()
        font = self.fontComboBox.currentFont()
        font.setPixelSize(self.fontSizeSlider.value())
        fontmetrics = QFontMetrics(font)
        w = fontmetrics.width(text)
        h = fontmetrics.height()
        if w == 0 : w = 1
        pixmap = QPixmap(w*2, h*2)
        pixmap.fill(QColor(0,0,0,0))
        self.painter.begin(pixmap)
        self.painter.setPen(self.pen)
        self.painter.setFont(font)
        self.painter.drawText(w,h, w,h, Qt.AlignLeft|Qt.AlignVCenter, text)
        self.painter.end()
        self.canvas.setCursor(QCursor(pixmap))
    def updateFontSize(self, size):
        self.labelFontSize.setText("Font Size : %i"%size)
        self.drawCursorText()

    def setZoom(self, factor):
        self.canvas.scale = factor
        self.canvas.update()
        self.labelZoom.setText("  Zoom :   %ix"%factor)
        if self.brushBtn.isChecked():
            self.canvas.setCursor(brush_cursor(self.brush_size*self.canvas.scale))
        elif self.eraserBtn.isChecked():
            self.canvas.setCursor(brush_cursor(self.eraser_size*self.canvas.scale))
        elif self.sprayBtn.isChecked():
            self.canvas.setCursor(brush_cursor(self.spray_size*self.canvas.scale))
    def setBrushSize(self, size):
        self.brush_size = size
        self.labelBrush.setText("Brush Size : %i"%size)
        if self.brushBtn.isChecked():
            self.pen.setWidth(self.brush_size)
            self.canvas.setCursor(brush_cursor(self.brush_size*self.canvas.scale))
    def setFillOpacity(self, alpha):
        self.labelOpacity.setText("Fill Opacity : %i"%alpha)
        if self.brush_color != QColor(0,0,0,0): # To avoid set alpha of null color
            self.brush_color.setAlpha(alpha)
            self.brush.setColor(self.brush_color)
    def setLineWidth(self, width):
        self.line_width = width
        self.labelLineWidth.setText("Line Width : %i"%width)
        if self.btnMode != "pencil":
            self.pen.setWidth(width)

    def setLineColor(self):
        color = QColorDialog.getColor(self.pen.color(), self.centralwidget.window())
        if color.isValid():
            self.linecolorBtn.setChecked(True)
            self.setColor(color)
    def setFillColor(self):
        color = QColorDialog.getColor(self.brush_color, self.centralwidget.window())
        if color.isValid():
            self.fillcolorBtn.setChecked(True)
            self.setColor(color)
    def setColor(self, color):
        if self.linecolorBtn.isChecked():
            self.btnLineColor.setStyleSheet("QPushButton{background-color: %s;}"%color.name())
            self.pen.setColor(color)
            if color.alpha() == 0:
                self.btnLineColor.setText("x")
            else:
                self.btnLineColor.setText("")
        else:
            self.btnFillColor.setStyleSheet("QPushButton{background-color: %s;}"%color.name())
            if color.alpha() == 0:
                self.brush_color = QColor(0,0,0,0)
                self.btnFillColor.setText("x")
            else:
                self.brush_color = color
                self.brush_color.setAlpha(self.opacitySlider.value())
                self.btnFillColor.setText("")
            self.brush.setColor(self.brush_color)
    def toggleColorEdit(self, checked):
        if checked:
            self.palette.edit_colors = True
        else:
            self.palette.edit_colors = False

    def setPattern(self, pattern):
        self.brush_pattern = pattern
        self.labelPattern.setPixmap(pattern)

    def setStatus(self, pos):
        self.status.setText( "Pointer : %i, %i"%(pos.x(),pos.y()) )

    def beginPainter(self, pixmap):
        self.painter.begin(pixmap)
        self.painter.setBrush(self.brush)
        self.painter.setPen(self.pen)
        if self.brushBtn.isChecked() and self.checkPattern.isChecked():
            pen = self.painter.pen()
            pen.setBrush(QBrush(self.brush_pattern))
            self.painter.setPen(pen)
################################       Edit     #############################################
    def expandCanvas(self):
        dialog = QDialog(self.centralwidget.window())
        dialog.setWindowTitle("Expand Canvas")
        gridLayout = QGridLayout(dialog)
        label = QLabel("Expand each side by (pixel) :", dialog)
        expansionEdit = QLineEdit(dialog)
        buttonBox = QDialogButtonBox(dialog)
        buttonBox.setOrientation(Qt.Horizontal)
        buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        gridLayout.addWidget(label)
        gridLayout.addWidget(expansionEdit)
        gridLayout.addWidget(buttonBox)
        buttonBox.accepted.connect(dialog.accept)
        buttonBox.rejected.connect(dialog.reject)
        if dialog.exec_() == QDialog.Accepted:
            try : expansion = int(expansionEdit.text())
            except : return
            pm = QPixmap(self.canvas.pixmap.width()+2*expansion, self.canvas.pixmap.height()+2*expansion)
            pm.fill()
            self.painter.begin(pm)
            self.painter.drawPixmap(expansion, expansion, self.canvas.pixmap)
            self.painter.end()
            self.canvas.pixmap = pm
            self.canvas.update()
            self.canvas.updateHistory()
################################    Transform   #############################################
    def resizeImage(self):
        dialog = ResizeImageDialog(self.centralwidget.window())
        if dialog.exec_() == QDialog.Accepted:
            w = dialog.widthEdit.text()
            h = dialog.heightEdit.text()
            if not w.isEmpty():
                try : width = int(w)
                except : return
            if not h.isEmpty():
                try : height = int(h)
                except : return
            if not w.isEmpty() and not h.isEmpty():
                self.canvas.pixmap = self.canvas.pixmap.scaled(width, height, 0, 1)
            elif not w.isEmpty():
                self.canvas.pixmap = self.canvas.pixmap.scaledToWidth(width, 1)
            elif not h.isEmpty():
                self.canvas.pixmap = self.canvas.pixmap.scaledToHeight(height, 1)
            else: return
            self.canvas.update()
            self.canvas.updateHistory()
    def rotateLeft(self):
        transform = QTransform().rotate(270)
        self.canvas.pixmap = self.canvas.pixmap.transformed(transform)
        self.canvas.update()
        self.canvas.updateHistory()
    def rotateRight(self):
        transform = QTransform().rotate(90)
        self.canvas.pixmap = self.canvas.pixmap.transformed(transform)
        self.canvas.update()
        self.canvas.updateHistory()
    def rotateAnyAngle(self):
        dialog = QDialog(self.centralwidget.window())
        dialog.setWindowTitle("Angle of rotation")
        gridLayout = QGridLayout(dialog)
        label = QLabel("Enter Angle (degree) :", dialog)
        angleEdit = QLineEdit(dialog)
        buttonBox = QDialogButtonBox(dialog)
        buttonBox.setOrientation(Qt.Horizontal)
        buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        gridLayout.addWidget(label)
        gridLayout.addWidget(angleEdit)
        gridLayout.addWidget(buttonBox)
        buttonBox.accepted.connect(dialog.accept)
        buttonBox.rejected.connect(dialog.reject)
        if dialog.exec_() == QDialog.Accepted:
            try : angle = int(angleEdit.text())
            except : return
            transform = QTransform().rotate(angle)
            self.canvas.pixmap = self.canvas.pixmap.transformed(transform)
            self.canvas.update()
            self.canvas.updateHistory()
    def flipImage(self):
        transform = QTransform().rotate(180, 1)
        self.canvas.pixmap = self.canvas.pixmap.transformed(transform)
        self.canvas.update()
        self.canvas.updateHistory()
    def flopImage(self):
        transform = QTransform().rotate(180, 0)
        self.canvas.pixmap = self.canvas.pixmap.transformed(transform)
        self.canvas.update()
        self.canvas.updateHistory()
################################  File Options  ##############################################
    def newImage(self):
        self.canvas.pixmap = QPixmap(self.canvas.pixmap.width(),self.canvas.pixmap.height())
        self.canvas.pixmap.fill()
        self.canvas.update()
        self.canvas.updateHistory()
        self.filename = ""
        self.setWindowTitle("Ankita - " + __version__)
    def newWithSize(self):
        dialog = NewImageDialog(self.centralwidget.window())
        if dialog.exec_() == QDialog.Accepted:
            width = dialog.widthEdit.text()
            height = dialog.heightEdit.text()
            try :
                width = int(width)
                height = int(height)
            except : return
            self.canvas.pixmap = QPixmap(width, height)
            self.canvas.pixmap.fill()
            self.canvas.update()
            self.canvas.updateHistory()
            self.filename = ""
            self.setWindowTitle("Ankita - " + __version__)

    def openImage(self):
        filename = QFileDialog.getOpenFileName(self.centralwidget.window(),
                                      "Select Image to Open", "",
                                      "Image Files (*.jpg *.png *.jpeg)" )
        if not filename.isEmpty():
            self.loadImage(filename)

    def loadImage(self, filename):
        self.canvas.pixmap = QPixmap(filename)
        self.canvas.update()
        self.canvas.updateHistory()
        self.filename = filename
        self.setWindowTitle(filename)

    def saveImage(self):
        if self.filename != "":
            self.canvas.pixmap.save(self.filename)
        else:
            self.saveImageAs()
    def saveImageAs(self):
        filename = QFileDialog.getSaveFileName(self.centralwidget.window(),
                                      "Set FileName to Save", self.filename,
                                      "Image Files (*.jpg *.png *.jpeg)" )
        if not filename.isEmpty():
          if not (filename.endsWith(".jpg",0) or filename.endsWith(".png",0) or filename.endsWith(".jpeg",0)):
            filename += ".png"
          self.canvas.pixmap.save(filename)
          self.filename = filename
          self.setWindowTitle(filename)

###############################################################################################
    def closeEvent(self, event):
        self.settings.setValue("ColorPalette", clr_array)
        self.settings.setValue("CanvasWidth", self.canvas.pixmap.width())
        self.settings.setValue("CanvasHeight", self.canvas.pixmap.height())
        return QMainWindow.closeEvent(self, event)
###############################################################################################



##############################################################################################
class ColorPicker(QLabel):
    colorSelected = pyqtSignal(QColor)
    def __init__(self, parent):
        super(ColorPicker, self).__init__(parent)
        self.setFrameShadow(0x0020)
        self.setFrameShape(0x0002)
        self.setToolTip("Color Picker")
        self.setSizePolicy(0, 0) #QSizePolicy.Fixed
        self.setPixmap(QPixmap(":/color_picker.png"))
        self.grab_mode = False
    def mousePressEvent(self, ev):
        if self.grab_mode:
            x = self.mapToGlobal(ev.pos()).x()
            y = self.mapToGlobal(ev.pos()).y()
            image = QPixmap.grabWindow(QApplication.desktop().winId(),x,y,1,1).toImage()
            color = QColor(image.pixel(0,0))
            self.colorSelected.emit(color)
    def mouseReleaseEvent(self, ev):
        if self.grab_mode: 
            self.grab_mode = False
            self.releaseMouse()
            self.unsetCursor()
            return
        self.grabMouse()
        self.grab_mode = True
        self.setCursor(QCursor(QPixmap(":/cursor_plus.png")))

class NewImageDialog(QDialog):
    def __init__(self, parent):
        super(NewImageDialog, self).__init__(parent)
        self.setWindowTitle("New Canvas")
        self.resize(250, 120)

        self.gridLayout = QGridLayout(self)
        self.widthEdit = QLineEdit("800", self)
        self.gridLayout.addWidget(self.widthEdit, 1, 0, 1, 1)
        self.labelX = QLabel(self)
        self.labelX.setText("x")
        self.gridLayout.addWidget(self.labelX, 1, 1, 1, 1)
        self.heightEdit = QLineEdit("600", self)
        self.gridLayout.addWidget(self.heightEdit, 1, 2, 1, 1)
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 3)
        self.label = QLabel(self)
        self.label.setText("<b>New Image Size :</b>")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 3)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

class ResizeImageDialog(QDialog):
    def __init__(self, parent):
        super(ResizeImageDialog, self).__init__(parent)
        self.setWindowTitle("Resize Image")
        self.resize(250, 120)

        self.gridLayout = QGridLayout(self)
        self.widthEdit = QLineEdit(self)
        self.gridLayout.addWidget(self.widthEdit, 2, 0, 1, 1)
        self.labelX = QLabel(self)
        self.labelX.setText("x")
        self.gridLayout.addWidget(self.labelX, 2, 1, 1, 1)
        self.heightEdit = QLineEdit(self)
        self.gridLayout.addWidget(self.heightEdit, 2, 2, 1, 1)
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 3)
        self.label = QLabel(self)
        self.label.setText("<b>Image Size (WxH) :</b>")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 3)
        self.label_2 = QLabel(self)
        self.label_2.setText("Enter both or any one value")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 3)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)


from math import sqrt, atan, degrees
def calc_arc(x1,y1, x2,y2, x3,y3):
    """ Calculates position of center of a circle, and the radius when three points
        on the circle are given """
    for each in [x1,y1, x2,y2, x3,y3]: # convert to float for accuracy
        each = float(each)
    if x1 == x2 : x2 += 0.000001
    if x3 == x2 : x3 += 0.000001
    if y1 == y2 : y2 += 0.000001
    try:
        mr = float(y2-y1)/(x2-x1)
        mt = float(y3-y2)/(x3-x2)
        # coordinate of center is (x,y)
        x = (mr*mt*(y3-y1)+mr*(x2+x3)-mt*(x1+x2))/(2*(mr-mt)) 
        y = -(1/mr)*(x-(x1+x2)/2)+(y1+y2)/2
        r = int(round(sqrt((x1-x)**2 + (y1-y)**2), 0))   # Radius of circle
        # Angle between x-axis and line connecting center and (x1,y1)
        ang1 = degrees(atan((y-y1)/(x1-x))) 
        if x > x1: ang1 += 180
        ang2 = degrees(atan((y-y2)/(x2-x)))
        if x > x2: ang2 += 180
        ang3 = degrees(atan((y-y3)/(x3-x)))
        if x > x3: ang3 += 180
    except ZeroDivisionError: return 0, 0, 0, 0, 0
    for each in ang1, ang2, ang3:
        if each < 0: each += 360
    if ang1 > ang2:
        ang1, ang2 = ang2, ang1
    start_ang = ang1
    extent_ang = ang2-ang1
    if not (ang3 < ang2 and ang3 > ang1):
        start_ang = ang2
        extent_ang = 360-extent_ang
    return x, y, r, start_ang, extent_ang

def calcspline(points, cp1, cp2):
    """ Takes points-list 'points' of atleast 3 points, appends control points to cp1, cp2"""
    n = len(points)-1 # points[n] is last point
    ax, ay, r = 0.0, 0.0, 0.0
    for i in range(n-2, n) :
        s = r
        bx = ax
        by = ay
        ax = points[i+1].x() - points[i].x()
        ay = points[i+1].y() - points[i].y()
        r = ax*ax + ay*ay + 1E-9
        ax = ax/r; ay = ay/r
        r = sqrt(r)/3.0
        if (i == n-1):
            cx = (ax+bx)/2.0
            cy = (ay+by)/2.0
            t = sqrt(cx*cx + cy*cy + 1E-9)
            cx = cx/t
            cy = cy/t
            cp1_x = points[i].x() + (r*cx) 
            cp1_y = points[i].y() + (r*cy)
            cp2_x = points[i].x() - (s*cx)
            cp2_y = points[i].y() - (s*cy)
            cp1.append(QPoint(cp1_x, cp1_y)) # cp1[i]
            cp2.append(QPoint(cp2_x, cp2_y)) # cp2[i-1]
            # Evaluate control_point1 near first knot point
            if i==1 :
              t = 3.0*s*s;
              cp1_x = cp2[0].x() - (t*bx)
              cp1_y = cp2[0].y() - (t*by)
              cp1.insert(0, QPoint(cp1_x, cp1_y)) # cp1[0]
            # Evaluate control_point2 near last knot point
            t = 3.0*r*r
            cp2_x = cp1[i].x() + (t*ax)
            cp2_y = cp1[i].y() + (t*ay)
            cp2.append(QPoint(cp2_x, cp2_y)) # cp2[i]
    if len(cp2) > 3: cp2.pop(-3)
    return cp1, cp2

def main():
    app = QApplication(sys.argv)
    app.setOrganizationName("Ankita")
    app.setApplicationName("ankita")
    win = Window()
    win.resize(1200, 700)
    if len(sys.argv)>1 and os.path.exists( os.path.abspath(sys.argv[-1]) ):
        win.loadImage(os.path.abspath(sys.argv[-1]))
    win.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
