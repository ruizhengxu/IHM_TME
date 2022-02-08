from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Shape import *

WIDTH = 600
HEIGHT = 500

class Canvas(QWidget):

    def __init__(self, parent = None):
        print("class Canvas")
        QWidget.__init__(self, parent)
        self.set_color(Qt.white)
        self.setMinimumSize(WIDTH, HEIGHT)
        
        self.drawing = Shape.FREE
        self.pix = QPixmap(self.rect().size())
        self.pix.fill(Qt.white)
        
        self.begin = QPoint()
        self.end = QPoint()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(QPoint(), self.pix)
    
        if not self.begin.isNull() and not self.end.isNull():
            if self.drawing == Shape.FREE:
                pass
            elif self.drawing == Shape.RECT:
                painter.drawRect(QRect(self.begin, self.end))
            elif self.drawing == Shape.ELLIPSE:
                painter.drawEllipse(QRectF(self.begin, self.end))
        
    def mousePressEvent(self, event):
        print("Mouse clicked at :", event.pos())
        if Qt.LeftButton:
            self.begin = event.pos()
            self.end = event.pos()
            self.update()
    
    def mouseMoveEvent(self, event):
        print("Mouse real-time position :", event.pos())
        if Qt.LeftButton:
            painter = QPainter(self.pix)
            if self.drawing == Shape.FREE:
                painter.drawLine(self.end, event.pos())
            elif self.drawing == Shape.RECT:
                pass
            elif self.drawing == Shape.ELLIPSE:
                pass
            self.end = event.pos()
            self.update()
        
    def mouseReleaseEvent(self, event):
        pass
        if Qt.LeftButton:
            print("Mouse released at :", event.pos())
            painter = QPainter(self.pix)
            if self.drawing == Shape.FREE:
                painter.drawLine(self.end, event.pos())
            elif self.drawing == Shape.RECT:
                painter.drawRect(QRect(self.begin, self.end))
            elif self.drawing == Shape.ELLIPSE:
                painter.drawEllipse(QRectF(self.begin, self.end))
            self.begin, self.end = QPoint(), QPoint()
            self.update()
            

    def reset(self):
        print("reset")

    def add_object(self):
        print("add object")
        
    def set_shape(self, shape):
        self.drawing = shape
        print(self.drawing)

    def set_color(self, color ):
        print("set color")