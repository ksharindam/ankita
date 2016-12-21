#!/usr/bin/env python
"""
Name = Ankita
version = 1.0
Dependency = python-qt4, python-pil
Description = A well designed Paint program in PyQt4

   Copyright (C) 2016 Arindam Chaudhuri <ksharindam@gmail.com>
  
   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.
  
   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.
  
   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import sys
import ui_ankita
from PIL import Image, ImageDraw, ImageQt

from PyQt4.QtCore import pyqtSignal, QPoint, Qt
from PyQt4.QtGui import QApplication, QMainWindow, QLabel, QHBoxLayout, QPixmap, QButtonGroup
from PyQt4.QtGui import QPainter, QPen, QBrush, qRgb, QColor, QCursor
from PyQt4.QtGui import QFileDialog

clr_array = [
"#ffffff", "#ffffff", "#cccccc", "#999999", "#666666", "#000000",
"#e066ff", "#d15fee", "#9b30ff", "#912cee", "#7d26cd", "#551a8b",
"#4169e1", "#3a5fcd", "#0000ff", "#0000ee", "#0000cd", "#00008b",
"#c0ffc0", "#80ff80", "#00ff00", "#00ee00", "#00cd00", "#008b00",
"#ff6a6a", "#ff3030", "#ff0000", "#ee0000", "#cd0000", "#8b0000",
"#ffff00", "#ffa500", "#00ffff", "#008b8b", "#ff00ff", "#8b008b"
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
    def __init__(self, parent):
        super(Label, self).__init__(parent)
        self.setSizePolicy(0, 0) #QSizePolicy.Fixed
        self.pixmap = QPixmap(640,480)
        self.pixmap.fill()
        self.setMouseTracking(True)
        self.mouse_pressed = False
        self.history = []
        self.current_index = -1
        self.scale = 1
        self.setCursor(QCursor(QPixmap(":/cursor_pencil.png")))
        #self.setCursor(brush_cursor(8))
        self.update()
    def mousePressEvent(self, ev):
        self.mouse_pressed = True
        self.mouseClicked.emit(QPoint(ev.x()/self.scale, ev.y()/self.scale), True)
        #print "%ix%i"%(ev.x(),ev.y())
    def mouseMoveEvent(self, ev):
        self.mouseMoved.emit(QPoint(ev.x()/self.scale, ev.y()/self.scale))
    def mouseReleaseEvent(self, ev):
        self.mouse_pressed = False
        self.mouseReleased.emit(QPoint(ev.x()/self.scale, ev.y()/self.scale))
    def setPixmap(self, pixmap):
        if self.scale != 1:
            pixmap = pixmap.scaledToWidth(self.pixmap.width()*self.scale)
        super(Label, self).setPixmap(pixmap)
    def update(self):
        self.setPixmap(self.pixmap)
    def updateHistory(self):
        """ Appends current pixmap to undo list """
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

    def redo(self):
        if self.current_index==len(self.history)-1:
            return
        self.pixmap = self.history[self.current_index+1].copy()
        self.update()
        self.current_index += 1

class ColorGrid(QLabel):
    """ Color Palette that holds many colors. Emit signal with QColor when a color is clicked"""
    colorSelected = pyqtSignal(QColor)
    def __init__(self, parent):
        super(ColorGrid, self).__init__(parent)
        self.column = 6
        self.row = 3
        self.pixmap = QPixmap(self.column*24+1,self.column*24+1)
        self.pixmap.fill()
        painter = QPainter()
        painter.begin(self.pixmap)
        for index,color in enumerate(clr_array):
            painter.setBrush(QBrush(QColor(color)))
            painter.drawRect((index%self.column)*24,(index//self.column)*24, 24,24)
        painter.drawLine(0,0,24,24)
        painter.drawLine(0,24,24,0)
        painter.end()
        self.setPixmap(self.pixmap)
    def mousePressEvent(self, ev):
        if ev.x() == 0 or ev.y() == 0: return
        index = ((ev.y()-1)//24) * self.column + (ev.x()-1)//24
        if index >= len(clr_array): return
        color = QColor(clr_array[index])
        if index == 0:
            color.setAlpha(0)
        self.colorSelected.emit(color)

class Window(ui_ankita.Ui_MainWindow):
    """ This class creates main window and all child widgets """
    def __init__(self):
        super(Window, self).__init__()
        self.filename = ""
        self.points = []
        self.btnMode = None
        self.brush_color = QColor(255,255,255,0)
        self.painter = QPainter()
        self.pen = QPen()
        self.pen.setCapStyle(0x20) # Qt.RountCap
        self.brush = QBrush(self.brush_color)
    def setupUi(self, win):
        super(Window, self).setupUi(win)
        # Change some widget property
        self.labelLine.setStyleSheet("QLabel{background-color: #000000;}")
        self.gridLayout.setRowStretch(4,1)
        # Add additional widgets
        self.canvas = Label(win)
        hLayout = QHBoxLayout(self.scrollWidget)
        hLayout.addWidget(self.canvas)
        self.palette = ColorGrid(win)
        self.gridLayout.addWidget(self.palette,3,0,1,2)
        # Create Menu Actions
        self.menuFile.addAction("Save", self.saveImage, "Ctrl+S")
        self.menuFile.addAction("Quit", win.close, "Ctrl+Q")
        self.menuEdit.addAction("Undo", self.canvas.undo, "Ctrl+Z")
        self.menuEdit.addAction("Redo", self.canvas.redo, "Ctrl+Y")
        # Add buttons to button group
        self.btnGroup = QButtonGroup(win)
        for button in [self.pencilBtn, self.brushBtn, self.floodfillBtn, self.lineBtn,
                   self.rectBtn, self.ovalBtn, self.arcBtn, self.polylineBtn, self.polygonBtn]:
            self.btnGroup.addButton(button)
        # Connect Shapes/brushes with signals
        self.btnGroup.buttonPressed.connect(self.onBtnClick)
        self.canvas.mouseClicked.connect(self.onClick)
        self.canvas.mouseMoved.connect(self.onClick)
        self.canvas.mouseMoved.connect(self.setStatus)
        self.canvas.mouseReleased.connect(self.onRelease)
        self.palette.colorSelected.connect(self.setColor)
        self.zoominBtn.clicked.connect(self.zoomIn)
        self.zoomoutBtn.clicked.connect(self.zoomOut)
        # This will be after connecting signal of that button
        self.pencilBtn.setChecked(True)
    def onBtnClick(self, button):
        """ Initializes all on brush button change"""
        if self.btnMode == "polygon":
            self.drawpolygon(0,0,True)
            self.canvas.updateHistory()
        if self.btnMode == "polyline":
            self.canvas.updateHistory()
        self.canvas.update()
        self.btnMode = None
        self.points = []
        self.pen.setWidth(0)
        if self.btnGroup.id(button)==-2:
            self.canvas.setCursor(QCursor(QPixmap(":/cursor_pencil.png")))
        elif self.btnGroup.id(button)==-3:
            self.pen.setWidth(8)
            self.canvas.setCursor(brush_cursor(8*self.canvas.scale))
        else:
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
    def onRelease(self):
        if self.btnMode == "pencil":
            self.canvas.updateHistory()
            self.painter.end()

    def drawbypencil(self, pos, clicked):
        """ Draw non-straight line with pencil """
        if clicked:
            self.points = [pos]
            self.btnMode = "pencil"
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
            self.btnMode = "pencil"
            self.beginPainter(self.canvas.pixmap)
        if self.canvas.mouse_pressed:
            if len(self.points)==1:
                self.painter.drawLine(self.points[0], pos)
                self.canvas.update()
                self.points = [pos]

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
            if len(self.points)==2:
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
    def floodfill(self, pos, clicked):
        if not clicked: return
        image = self.canvas.pixmap.toImage()
        rgb = (self.brush_color.red(), self.brush_color.green(), self.brush_color.blue())
        if image.pixel(pos) == self.brush_color.rgb(): return
        #image.convertToFormat(5)
        bytes = image.bits().asstring(image.numBytes())
        pil_img = Image.fromstring("RGBA",(image.width(), image.height()), bytes)
        r, g, b, a = pil_img.split()
        pil_img = Image.merge("RGBA", (b, g, r, a))
        ImageDraw.floodfill(pil_img, (pos.x(),pos.y()), rgb)
        image = ImageQt.ImageQt(pil_img)
        self.canvas.pixmap = QPixmap.fromImage(image)
        self.canvas.update()
        self.canvas.updateHistory()
    def zoomIn(self):
        if self.canvas.scale == 8: return
        self.canvas.scale += 1
        self.canvas.update()
    def zoomOut(self):
        if self.canvas.scale == 1: return
        self.canvas.scale -= 1
        self.canvas.update()
        
    def setColor(self, color):
        if self.linecolorBtn.isChecked():
            self.pen.setColor(color)
            self.labelLine.setStyleSheet("QLabel{background-color: %s;}"%color.name())
            if color.alpha() == 0:
                self.labelLine.setText("Empty")
            else:
                self.labelLine.setText("")
        else:
            self.brush_color = color
            self.brush.setColor(color)
            self.labelFill.setStyleSheet("QLabel{background-color: %s;}"%color.name())
            if color.alpha() == 0:
                self.labelFill.setText("Empty")
            else:
                self.labelFill.setText("")
    def setStatus(self, pos):
        self.statusbar.showMessage( "Pointer : %ix%i"%(pos.x(),pos.y()) )

    def beginPainter(self, pixmap):
        self.painter.begin(pixmap)
        self.painter.setPen(self.pen)
        self.painter.setBrush(self.brush)
    def saveImage(self):
        filename = QFileDialog.getSaveFileName(self.canvas,
                                      "Select Image to Save", self.filename,
                                      "Image Files (*.jpg *.png *.jpeg)" )
        if not filename.isEmpty():
          if not (filename.endsWith(".jpg",0) or filename.endsWith(".png",0) or filename.endsWith(".jpeg",0)):
            filename += ".png"
          self.canvas.pixmap.save(filename)
          self.filename = filename
    """def floodfill(self, pos, clicked):
        # Fully working but discarded because very slow
        # Concept source : wikipedia- floodfill #Alternative_implementations
        if not clicked: return
        image = self.canvas.pixmap.toImage()
        img_width = self.canvas.pixmap.width()
        img_height = self.canvas.pixmap.height()
        target_color = image.pixel(pos)
        replacing_color = qRgb(150,150,150)
        if target_color == replacing_color: return
        fill_list = []
        fill_list.append(pos)
        for point in fill_list:
            line_points = []
            w = e = point
            while 1:
                if w.x() == 0: break 
                w = QPoint(w.x()-1, w.y())
                if image.pixel(w) != target_color: break
                line_points.append(w)
            while 1:
                if e.x() == img_width-1: break
                e = QPoint(e.x()+1, e.y())
                if image.pixel(e) != target_color: break
                line_points.append(e)
            for point in line_points:
                image.setPixel(point, replacing_color)
                if point.y() != 0:
                    n = QPoint(point.x(), point.y()-1)
                    if image.pixel(n) == target_color:
                        fill_list.append(n)
                if point.y() != img_height-1:
                    s = QPoint(point.x(), point.y()+1)
                    if image.pixel(s) == target_color:
                        fill_list.append(s)
        image.setPixel(pos, replacing_color)
        self.canvas.pixmap = QPixmap.fromImage(image)
        self.canvas.update()
        self.canvas.updateHistory()"""

from math import sqrt, atan, degrees
def calc_arc(x1,y1, x2,y2, x3,y3):
    """ Calculates position of center of a circle, and the radius when three points
        on the circle are given """
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

app = QApplication(sys.argv)
win = QMainWindow()
gui = Window()
gui.setupUi(win)

win.resize(860, 600)
win.show()
sys.exit(app.exec_())