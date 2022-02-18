import pickle, math
from shutil import move
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from zmq import SHARED
from Enum import *

DEFAULT_SCALE = 1
DEFAULT_OFFSET = 0

class Canvas(QWidget):

    def __init__(self, parent = None):
        # print("class Canvas")
        QWidget.__init__(self, parent)
        # self.setMinimumSize(WIDTH, HEIGHT)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet('background-color: white;')
        # self.setMouseTracking(True)
        
        self.list_elems = []
        self.list_properties = []
        self.list_size = 0
        
        self.move_canvas = False
        self.offset_x, self.offset_y = DEFAULT_OFFSET, DEFAULT_OFFSET
        self.scale = DEFAULT_SCALE
        
        self.drawing = True
        self.draw_mode = Shape.FREE
        
        self.select = False
        self.selected_shape = None
        
        self.lasso = False
        self.lasso_poly = QPolygon()
        self.lasso_selected_shape = []
        
        self.pen_color = Qt.black
        self.pen_width = 5
        self.brush_color = Qt.transparent
        
        self.begin = QPoint()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.translate(QPoint(self.offset_x, self.offset_y))
        painter.scale(self.scale, self.scale)
        
        if self.lasso and self.lasso_poly.count() != 0: 
            pen = QPen(Qt.gray)
            pen.setStyle(Qt.DashLine)
            pen.setWidth(2)
            painter.setPen(pen)
            painter.drawPolygon(self.lasso_poly)
        
        for i, elem in enumerate(self.list_elems):
            properties = self.list_properties[i]
            pen = QPen(properties[0])
            pen.setWidth(properties[1])
            brush = QBrush(properties[2])
            if i == self.selected_shape or i in self.lasso_selected_shape:
                pen.setStyle(Qt.DashLine)
            
            painter.setPen(pen)
            painter.setBrush(brush)
            if type(elem) == list:
                painter.drawPolyline(QPolygon(elem))
            elif type(elem) == QLine:
                painter.drawLine(elem)
            elif type(elem) == QRect:
                painter.drawRect(elem)
            elif type(elem) == QRectF:
                painter.drawEllipse(elem)
        
    def mousePressEvent(self, event):
        self.begin = event.pos()
        # LASSO
        if self.lasso and Qt.LeftButton and self.lasso_poly.count() != 0:
            self.lasso_poly.clear()
            self.lasso_selected_shape.clear()
        # SELECT
        if self.select and Qt.LeftButton:
            for i in range(len(self.list_elems)-1, -1, -1):
                shape = self.list_elems[i]
                if type(shape) == QLine:
                    if self.line_contains_point(shape, self.begin):
                        self.selected_shape = i
                        break
                elif type(shape) == list:
                    for j in range(len(shape)-1):
                        if self.line_contains_point(QLine(shape[j], shape[j+1]), self.begin): 
                            self.selected_shape = i
                            break
                else:
                    if shape.contains(self.begin):
                        self.selected_shape = i
                        break
        # DRAW
        if self.drawing and self.draw_mode != None and Qt.LeftButton:
            self.list_properties.append([self.pen_color, self.pen_width, self.brush_color, self.draw_mode])
            if self.draw_mode == Shape.FREE:
                self.list_elems.append([])
            else:
                self.list_elems.append(None)
        
        self.update()
    
    def mouseMoveEvent(self, event):
        # LASSO
        if self.lasso and Qt.LeftButton:
            self.lasso_poly.append(event.pos())
        # MOVE
        if self.move_canvas and Qt.LeftButton:
            self.offset_x += int((event.pos().x() - self.begin.x())/15) # /15 to move slower
            self.offset_y += int((event.pos().y() - self.begin.y())/15)
        # DRAW
        elif self.drawing and self.draw_mode != None and Qt.LeftButton:
            if self.draw_mode == Shape.FREE:
                pt = QPoint(event.pos().x(), event.pos().y())
                self.list_elems[self.list_size].append(pt)
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
        # LASSO
        if self.lasso and self.lasso_poly != [] and Qt.LeftButton:
            self.lasso_poly.append(event.pos())
            for i, elem in enumerate(self.list_elems):
                if type(elem) == QLine:
                    if self.poly_contains_point(self.get_all_points_from_lines(elem)):
                        self.lasso_selected_shape.append(i)
                elif type(elem) == list:
                    if self.poly_contains_point(elem):
                        self.lasso_selected_shape.append(i)
                else:
                    tl, tr, bl, br = elem.topLeft(), elem.topRight(), elem.bottomLeft(), elem.bottomRight()
                    if type(elem) == QRectF:
                        tl, tr, bl, br = tl.toPoint(), tr.toPoint(), bl.toPoint(), br.toPoint()
                    if self.poly_contains_point([tl, tr, bl, br]):
                        self.lasso_selected_shape.append(i)
        # DRAW
        if self.drawing and self.draw_mode != None and Qt.LeftButton:
            self.list_size += 1
        
        self.update()
        
    def get_all_points_from_lines(self, line: QLine):
        a, b = line.p1(), line.p2()
        slope = None if a.x() == b.x() else (b.y() - a.y())/(b.x() - a.x())
        intercept =  a.x() if slope == None else a.y() - slope * a.x()
        return [QPoint(x, int(slope * x + intercept)) for x in range(a.x(), b.x())]
        
    def line_contains_point(self, line : QLine, pt : QPoint):
        a, b = line.p1(), line.p2()
        dis_a_pt = int(math.sqrt((a.x() - pt.x())**2 + (a.y() - pt.y())**2))
        dis_pt_b = int(math.sqrt((pt.x() - b.x())**2 + (pt.y() - b.y())**2))
        dis_a_b = int(math.sqrt((a.x() - b.x())**2 + (a.y() - b.y())**2))
        return dis_a_pt + dis_pt_b == dis_a_b
    
    def poly_contains_point(self, l_pt : list):
        for pt in l_pt:
            if self.lasso_poly.containsPoint(pt, Qt.OddEvenFill): return True
        return False
            
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
        
    def set_mode(self, mode):
        if mode == Mode.MOVE:
            QApplication.setOverrideCursor(Qt.SizeAllCursor)
            self.move_canvas = True
            self.drawing = False
            self.select = False
            self.selected_shape = None
            self.lasso = False
            self.lasso_poly.clear()
            self.update_elems(zoom=True)
            self.scale = DEFAULT_SCALE
        elif mode == Mode.DRAW:
            QApplication.setOverrideCursor(Qt.ArrowCursor)
            self.drawing = True
            self.move_canvas = False
            self.select = False
            self.selected_shape = None
            self.lasso = False
            self.lasso_poly.clear()
            self.lasso_selected_shape.clear()
            self.update_elems(move=True, zoom=True)
            self.offset_x, self.offset_y = DEFAULT_OFFSET, DEFAULT_OFFSET
            self.scale = DEFAULT_SCALE
        elif mode == Mode.SELECT:
            QApplication.setOverrideCursor(Qt.ArrowCursor)
            self.move_canvas = False
            self.drawing = False
            self.select = True
            self.lasso = False
            self.lasso_poly.clear()
            self.lasso_selected_shape.clear()
            self.update_elems(move=True, zoom=True)
            self.offset_x, self.offset_y = DEFAULT_OFFSET, DEFAULT_OFFSET
            self.scale = DEFAULT_SCALE
        elif mode == Mode.LASSO:
            QApplication.setOverrideCursor(Qt.CrossCursor)
            self.move_canvas = False
            self.drawing = False
            self.select = False
            self.selected_shape = None
            self.lasso = True
            self.update_elems(move=True, zoom=True)
            self.offset_x, self.offset_y = DEFAULT_OFFSET, DEFAULT_OFFSET
            self.scale = DEFAULT_SCALE
        self.update()
        
    def update_elems(self, move=False, zoom=False):
        if move:
            for elem in self.list_elems:
                if type(elem) == list:
                    for e in elem:
                        e.setX(e.x() + self.offset_x)
                        e.setY(e.y() + self.offset_y)
                else:
                    elem.translate(self.offset_x, self.offset_y)
        if zoom:
            for i, elem in enumerate(self.list_elems):
                if type(elem) == list:
                    self.list_elems[i] = [QPoint(int(p.x()*self.scale), int(p.y()*self.scale)) for p in elem]
                else:
                    if type(elem) == QLine:
                        l = self.list_elems[i]
                        self.list_elems[i] = QLine(QPoint(int(l.x1()*self.scale), int(l.y1()*self.scale)),
                                                   QPoint(int(l.x2()*self.scale), int(l.y2()*self.scale)),)
                    else:
                        coordinates = elem.getCoords()
                        x, y, w, h = coordinates[0]*(self.scale), coordinates[1]*(self.scale),\
                                     (coordinates[2]-coordinates[0])*(self.scale),\
                                     (coordinates[3]-coordinates[1])*(self.scale)
                        if type(elem) == QRect: x, y, w, h = int(x), int(y), int(w)+1, int(h)+1
                        self.list_elems[i].setRect(x, y, w, h)
                self.list_properties[i][1] = int(self.list_properties[i][1] * self.scale) # Change width after scaling
        
    def zoom(self, scale):
        self.scale += scale
        self.update()
        
    def set_shape(self, shape):
        self.draw_mode = shape
        print(self.draw_mode)
        
    def change_shape_property(self, prop, index_shape, index_prop):
        property = self.list_properties[index_shape]
        property[index_prop] = prop
        self.list_properties[index_shape] = property
        
    def set_pen_width(self, width):
        self.pen_width = width

    def set_pen_color(self, color ):
        print("set pen color")
        self.pen_color = color
        if self.select and self.selected_shape != None:
            self.change_shape_property(color, self.selected_shape, 0)
        if self.lasso and len(self.lasso_selected_shape) != 0:
            for i in self.lasso_selected_shape: self.change_shape_property(color, i, 0)
        
    def set_brush_color(self, color ):
        print("set brush color")
        self.brush_color = color
        if self.select and self.selected_shape != None:
            self.change_shape_property(color, self.selected_shape, 2)
        if self.lasso and len(self.lasso_selected_shape) != 0:
            for i in self.lasso_selected_shape: self.change_shape_property(color, i, 2)
            
    def get_drawing(self):
        drawing = []
        for i in range(self.list_size):
            elem = self.list_elems[i]
            if type(elem) == list:
                drawing.append([elem, self.list_properties[i]])
            elif type(elem) == QLine:
                drawing.append([(elem.x1(), elem.y1(), elem.x2(), elem.y2()), self.list_properties[i]])
            else:
                drawing.append([elem.getCoords(), self.list_properties[i]])
        return drawing
            
    def load_canvas(self, file_name):
        try:
            with open(file_name, "rb") as fp:
                data = pickle.load(fp)

            self.list_elems.clear()
            self.list_properties.clear()
            self.list_size = 0
            self.selected_shape = None
            self.lasso_poly = QPolygon()
            self.lasso_selected_shape = []
            for d in data:
                coordinates = d[0]
                prop = d[1]
                if prop[3] == Shape.FREE:
                    self.list_elems.append([c for c in coordinates])
                elif prop[3] == Shape.LINE:
                    self.list_elems.append(QLine(QPoint(coordinates[0], coordinates[1]), QPoint(coordinates[2], coordinates[3])))
                elif prop[3] == Shape.RECT:
                    self.list_elems.append(QRect(coordinates[0], coordinates[1], 
                                                 coordinates[2]-coordinates[0]+1, coordinates[3]-coordinates[1]+1))
                else:
                    self.list_elems.append(QRectF(coordinates[0], coordinates[1], 
                                                  coordinates[2]-coordinates[0], coordinates[3]-coordinates[1]))
                self.list_properties.append(prop)
                self.list_size += 1
            self.update()
            return 1
        except:
            return 0
            
    def save_canvas(self, file_name):
        data = self.get_drawing()
        try:
            with open(file_name, "wb") as fp:
                pickle.dump(data, fp)
        except:
            return 0
