from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Enum import *

class Canvas(QWidget):

    def __init__(self, parent = None):
        print("class Canvas")
        QWidget.__init__(self, parent)
        # self.setMinimumSize(WIDTH, HEIGHT)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet('background-color: white;')
        # self.setMouseTracking(True)
        
        self.list_elems = []
        self.list_properties = []
        self.list_size = 0
        
        self.move_canvas = False
        self.offset_x, self.offset_y = 0, 0
        self.drawing = True
        self.draw_mode = Shape.FREE
        self.pen_color = Qt.black
        self.brush_color = Qt.transparent
        
        self.begin = QPoint()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.translate(QPoint(self.offset_x, self.offset_y))
        
        for i, elem in enumerate(self.list_elems):
            pen_brush = self.list_properties[i]
            painter.setPen(QPen(pen_brush[0]))
            painter.setBrush(QBrush(pen_brush[1]))
            if type(elem) == list:
                for pt in elem:
                    painter.drawLine(pt)
            elif type(elem) == QLine:
                painter.drawLine(elem)
            elif type(elem) == QRect:
                painter.drawRect(elem)
            elif type(elem) == QRectF:
                painter.drawEllipse(elem)
        
    def mousePressEvent(self, event):
        # print("Mouse clicked at :", event.pos())
        self.begin = event.pos()
        if self.drawing and self.draw_mode != None and Qt.LeftButton:
            self.list_properties.append((self.pen_color, self.brush_color))
            if self.draw_mode == Shape.FREE:
                self.list_elems.append([])
            else:
                self.list_elems.append(None)
            self.update()
    
    def mouseMoveEvent(self, event):
        # print("Mouse moved at :", event.pos())
        if self.move_canvas and Qt.LeftButton:
            self.offset_x += int((event.pos().x() - self.begin.x())/15) # /15 to move slower
            self.offset_y += int((event.pos().y() - self.begin.y())/15)
            self.update()
        elif self.drawing and self.draw_mode != None and Qt.LeftButton:
            if self.draw_mode == Shape.FREE:
                tmp = self.list_elems[self.list_size]
                new_point = QPoint(event.pos().x(), event.pos().y())
                if len(tmp) != 0:
                    last_point = tmp[len(tmp)-1].p2()
                else: 
                    last_point = new_point
                line = QLine(last_point, new_point)
                self.list_elems[self.list_size].append(line)
            elif self.draw_mode == Shape.LINE:
                line = QLine(self.begin, event.pos())
                self.list_elems[self.list_size] = line
            elif self.draw_mode == Shape.RECT:
                rect = QRect(self.begin.x(), self.begin.y(),
                            event.pos().x() - self.begin.x(), event.pos().y() - self.begin.y())
                self.list_elems[self.list_size] = rect
            elif self.draw_mode == Shape.CERCLE:
                diameter = max(event.pos().x() - self.begin.x(), event.pos().y() - self.begin.y())
                cercle = QRectF(self.begin.x(), self.begin.y(),
                                diameter, diameter)
                self.list_elems[self.list_size] = cercle
            elif self.draw_mode == Shape.ELLIPSE:
                ellipse = QRectF(self.begin.x(), self.begin.y(),
                                event.pos().x() - self.begin.x(), event.pos().y() - self.begin.y())
                self.list_elems[self.list_size] = ellipse
            self.end = event.pos()
            self.update()
        
    def mouseReleaseEvent(self, event):
        # print("Mouse released at :", event.pos())
        if self.drawing and self.draw_mode != None and Qt.LeftButton:
            print(self.list_elems)
            self.list_size += 1
            self.update()
            
    def erase(self, all=False):
        if self.list_size == 0:
            return
        if all == True:
            self.list_elems.clear()
            self.list_properties.clear()
            self.list_size = 0
        else:
            last_property = self.list_properties[self.list_size-1]
            last_elem = self.list_elems[self.list_size-1]
            self.list_properties.remove(last_property)
            self.list_elems.remove(last_elem)
            self.list_size -= 1
        self.update()

    def add_object(self):
        print("add object")
        
    def set_mode(self, mode):
        if mode == Mode.MOVE:
            QApplication.setOverrideCursor(Qt.SizeAllCursor)
            self.move_canvas = True
            self.drawing = False
        elif mode == Mode.DRAW:
            QApplication.restoreOverrideCursor()
            self.drawing = True
            self.move_canvas = False
            self.update_elems()
            self.offset_x, self.offset_y = 0, 0
        elif mode == Mode.SELECT:
            QApplication.setOverrideCursor(Qt.CrossCursor)
            self.move_canvas = False
            self.drawing = False
        
    def update_elems(self):
        for elem in self.list_elems:
            elem.translate(self.offset_x, self.offset_y)
    
    def set_move(self, move):
        self.move = move
        QApplication.setOverrideCursor(Qt.SizeAllCursor)
        if move: self.drawing = False
        
    def set_drawing(self, drawing):
        QApplication.restoreOverrideCursor()
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