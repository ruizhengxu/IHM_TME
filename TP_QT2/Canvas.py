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
        self.setMinimumSize(WIDTH, HEIGHT)
        
        self.list_elems = []
        
        self.drawing = True
        self.draw_mode = Shape.FREE
        self.pen_color = Qt.black
        self.brush_color = Qt.transparent
        
        self.pix = QPixmap(self.rect().size())
        self.pix.fill(Qt.white)
        
        self.begin = QPoint()
        self.end = QPoint()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(QPoint(), self.pix)
        painter.setPen(QPen(self.pen_color))
        painter.setBrush(self.brush_color)
        
        for elem in self.list_elems:
            if type(elem) == QLine:
                painter.drawLine(elem)
            elif type(elem) == QRect:
                painter.drawRect(elem)
            elif type(elem) == QRectF:
                painter.drawEllipse(elem)
        # if self.drawing and not self.begin.isNull() and not self.end.isNull():
        #     if self.draw_mode == Shape.FREE:
        #         pass
        #     elif self.draw_mode == Shape.RECT:
        #         painter.drawRect(QRect(self.begin, self.end))
        #     elif self.draw_mode == Shape.ELLIPSE:
        #         painter.drawEllipse(QRectF(self.begin, self.end))
        
    def mousePressEvent(self, event):
        print("Mouse clicked at :", event.pos())
        if self.drawing and Qt.LeftButton:
            self.begin = event.pos()
            self.end = event.pos()
            self.update()
    
    def mouseMoveEvent(self, event):
        print("Mouse real-time position :", event.pos())
        if self.drawing and Qt.LeftButton:
            painter = QPainter(self.pix)
            painter.setPen(QPen(self.pen_color))
            painter.setBrush(self.brush_color)
            
            if self.draw_mode == Shape.FREE:
                painter.drawLine(self.end, event.pos())
            elif self.draw_mode == Shape.RECT:
                pass
            elif self.draw_mode == Shape.ELLIPSE:
                pass
            self.end = event.pos()
            self.update()
        
    def mouseReleaseEvent(self, event):
        if self.drawing and Qt.LeftButton:
            print("Mouse released at :", event.pos())
            painter = QPainter(self.pix)
            painter.setPen(QPen(self.pen_color))
            painter.setBrush(self.brush_color)
            
            if self.draw_mode == Shape.FREE:
                line = QLine(self.end, event.pos())
                self.list_elems.append(line)
                painter.drawLine(line)
            elif self.draw_mode == Shape.RECT:
                rect = QRect(self.begin, self.end)
                self.list_elems.append(rect)
                painter.drawRect(rect)
            elif self.draw_mode == Shape.ELLIPSE:
                ellipse = QRectF(self.begin, self.end)
                self.list_elems.append(ellipse)
                painter.drawEllipse(ellipse)
            self.begin, self.end = QPoint(), QPoint()
            self.update()
            

    def reset(self):
        print("reset")

    def add_object(self):
        print("add object")
        
    def set_drawing(self, drawing):
        self.drawing = drawing
        
    def set_shape(self, shape):
        self.draw_mode = shape
        print(self.draw_mode)

    def set_pen_color(self, color ):
        print("set pen color")
        self.pen_color = color
        
    def set_brush_color(self, color ):
        print("set brush color")
        self.brush_color = color