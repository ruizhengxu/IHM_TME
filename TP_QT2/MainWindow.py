import sys
from datetime import datetime
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Canvas import *
from Enum import *
import resources

WIDTH = 1280
HEIGHT = 720
LOG_FNAME = "log.txt"

class MainWindow(QMainWindow):

    def __init__(self, parent = None ):
        QMainWindow.__init__(self, parent )
        
        screen = QApplication.primaryScreen()
        self.setGeometry(int(screen.size().width()/2)-int(WIDTH/2),
                         int(screen.size().height()/2)-int(HEIGHT/2), 
                         WIDTH, HEIGHT)

        self.file_name = ""
        
        self.v_layout = QVBoxLayout()
        self.textEdit = QTextEdit()
        self.textEdit.setMaximumHeight(int(HEIGHT/10))
        self.canvas = Canvas()
        self.v_layout.addWidget(self.textEdit)
        self.v_layout.addWidget(self.canvas)
        self.container = QWidget()
        self.container.setLayout(self.v_layout)
        self.setCentralWidget(self.container)

        bar = self.menuBar()
        fileMenu = bar.addMenu("File")
        openAct = fileMenu.addAction(QIcon(":/images/open.png"), "&Open File", self.open_file, QKeySequence("Ctrl+O"))
        saveAct = fileMenu.addAction(QIcon(":/images/save.png"), "&Save File", self.save_file, QKeySequence("Ctrl+S"))
        quitAct = fileMenu.addAction(QIcon(":/images/quit.png"), "&Quit", self.quit, QKeySequence("Ctrl+Q"))

        colorMenu = bar.addMenu("Color")
        actPen = colorMenu.addAction(QIcon(":/icons/pen.png"), "&Pen color", self.pen_color, QKeySequence("Ctrl+P"))
        actPenWidth = colorMenu.addAction(QIcon(":/icons/pen_width.png"), "&Pen width")
        pen_vbox = QVBoxLayout()
        self.pen_width_value = QLabel("2")
        self.pen_width_slider = QSlider(Qt.Horizontal)
        self.pen_width_slider.setMinimum(1)
        self.pen_width_slider.setMaximum(18)
        self.pen_width_slider.setValue(2)
        self.pen_width_slider.valueChanged.connect(self.pen_width_show)
        self.pen_width_slider.sliderReleased.connect(self.set_pen_width)
        pen_vbox.addWidget(self.pen_width_slider)
        pen_vbox.addWidget(self.pen_width_value)
        pen_vbox.setAlignment(self.pen_width_value, Qt.AlignCenter)
        pen_width_container = QWidget()
        pen_width_container.setLayout(pen_vbox)
        actBrush = colorMenu.addAction(QIcon(":/icons/brush.png"), "&Brush color", self.brush_color, QKeySequence("Ctrl+B"))

        colorToolBar = QToolBar("Color")
        self.addToolBar( colorToolBar )
        colorToolBar.addAction( actPen )
        colorToolBar.addAction( actPenWidth )
        colorToolBar.addWidget(pen_width_container)
        colorToolBar.addAction( actBrush )
        
        eraseMenu = bar.addMenu("Eraser")
        actEraseLast = eraseMenu.addAction(QIcon(":/icons/eraser1.png"), "&Erase last", self.erase_last, QKeySequence("Backspace"))
        actEraseAll = eraseMenu.addAction(QIcon(":/icons/eraser2.png"), "&Erase all", self.erase_all, QKeySequence("Ctrl+Backspace"))
        
        eraseToolBar = QToolBar("Eraser")
        self.addToolBar(eraseToolBar)
        eraseToolBar.addAction(actEraseLast)
        eraseToolBar.addAction(actEraseAll)

        shapeMenu = bar.addMenu("Shape")
        actFree = shapeMenu.addAction(QIcon(":/icons/free.png"), "&Free drawing", self.free_drawing)
        actLine = shapeMenu.addAction(QIcon(":/icons/line.png"), "&Line", self.line)
        actRectangle = shapeMenu.addAction(QIcon(":/icons/rectangle.png"), "&Rectangle", self.rectangle )
        actCercle = shapeMenu.addAction(QIcon(":/icons/cercle.png"), "&Cercle", self.cercle)
        actEllipse = shapeMenu.addAction(QIcon(":/icons/ellipse.png"), "&Ellipse", self.ellipse)
        
        shapeToolBar = QToolBar("Shape")
        self.addToolBar( shapeToolBar )
        shapeToolBar.addAction( actFree )
        shapeToolBar.addAction( actLine )
        shapeToolBar.addAction( actRectangle )
        shapeToolBar.addAction( actCercle )
        shapeToolBar.addAction( actEllipse )

        modeMenu = bar.addMenu("Mode")
        actMove = modeMenu.addAction(QIcon(":/icons/move.png"), "&Move", self.move)
        actDraw = modeMenu.addAction(QIcon(":/icons/draw.png"), "&Draw", self.draw)
        actSelect = modeMenu.addAction(QIcon(":/icons/select.png"), "&Select", self.select)
        actLasso = modeMenu.addAction(QIcon(":/icons/lasso.png"), "&Lasso", self.lasso)
        
        modeToolBar = QToolBar("Navigation")
        self.addToolBar(Qt.LeftToolBarArea, modeToolBar)
        modeToolBar.addAction( actMove )
        modeToolBar.addAction( actDraw )
        modeToolBar.addAction( actSelect )
        modeToolBar.addAction( actLasso )
        
        toolMenu = bar.addMenu("Tool")
        actZoomIn = toolMenu.addAction(QIcon(":/icons/zoom-in.png"), "&Zoom in", self.zoom_in)
        actZoomOut = toolMenu.addAction(QIcon(":/icons/zoom-out.png"), "&Zoom out", self.zoom_out)
        
        toolsToolBar = QToolBar("Tools")
        self.addToolBar(Qt.LeftToolBarArea, toolsToolBar )
        toolsToolBar.addAction( actZoomIn )
        toolsToolBar.addAction( actZoomOut )
        
        self.log_action("==============================\n"\
                        "Application launched at " + str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")))


    ##############
    def open_file(self):
        file_name = QFileDialog.getOpenFileName(self, "Open File")[0]
        if file_name != "":
            res = self.canvas.load_canvas(file_name)
            if res:
                self.log_action("File opened : " + file_name)
                self.file_name = file_name
                self.windowTitle = self.file_name
            else:
                self.log_action("Tried to open invalid file : " + file_name)
    
    def save_file(self):
        if self.file_name != "":
            self.canvas.save_canvas(self.file_name)
            self.log_action("File saved : " + self.file_name)
        else:
            file_name = QFileDialog.getSaveFileName(self, "Save File")[0]
            if file_name != "":
                self.canvas.save_canvas(file_name)
                self.file_name = file_name
            self.log_action("File saved : " + file_name)
        
    def quit(self):
        response = QMessageBox.question(self, "Confirm exit", 
                                        "Are you sure you want to exit ?")
        if response == QMessageBox.Yes:
            self.log_action("Application termianted at " + str(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))\
                    + "\n==============================\n")
            sys.exit()
        return response
    
    def pen_color(self):
        color = QColorDialog.getColor()
        self.canvas.set_pen_color(color)
        self.log_action("Pen Color :" + str(color.getRgb()))
        
    def pen_width_show(self):
        self.pen_width_value.setText(str(self.pen_width_slider.value()))
        
    def set_pen_width(self):
        width = self.pen_width_slider.value()
        self.canvas.set_pen_width(width)
        self.log_action("Pen Width : " + str(width))

    def brush_color(self):
        color = QColorDialog.getColor()
        self.canvas.set_brush_color(color)
        self.log_action("Brush Color :" + str(color.getRgb()))
        
    def erase_last(self):
        self.canvas.erase()
        self.log_action("Erase last shape")
    
    def erase_all(self):
        response = QMessageBox.question(self, "Confirm erase", 
                                        "Are you sure you want to erase all figures ?")
        if response == QMessageBox.Yes:
            self.canvas.erase(all=True)
            self.log_action("Erase All")

    def free_drawing(self):
        self.canvas.set_shape(Shape.FREE)
        self.log_action("Shape Mode: free drawing")
        
    def line(self):
        self.canvas.set_shape(Shape.LINE)
        self.log_action("Shape Mode: line")
        
    def rectangle(self):
        self.canvas.set_shape(Shape.RECT)
        self.log_action("Shape Mode: rectangle")

    def cercle(self):
        self.canvas.set_shape(Shape.CERCLE)
        self.log_action("Shape Mode: cercle")

    def ellipse(self):
        self.canvas.set_shape(Shape.ELLIPSE)
        self.log_action("Shape Mode: ellipse")

    def move(self):
        self.canvas.set_mode(Mode.MOVE)
        self.log_action("Mode: move")

    def draw(self):
        self.canvas.set_mode(Mode.DRAW)
        self.log_action("Mode: draw")
        
    def select(self):
        self.canvas.set_mode(Mode.SELECT)
        self.log_action("Mode: select")
        
    def lasso(self):
        self.canvas.set_mode(Mode.LASSO)
        self.log_action("Mode: lasso")
        
    def zoom_out(self):
        self.canvas.zoom(-0.1)
        # self.log_action("Tool: zoom in")
    
    def zoom_in(self):
        self.canvas.zoom(0.1)
        # self.log_action("Tool: zoom out")
        
    def log_action(self, str):
        content = self.textEdit.toPlainText()
        self.textEdit.setPlainText( content + "\n" + str)
        self.textEdit.moveCursor(QTextCursor.End)
        
        with open(LOG_FNAME, "a+") as f:
            f.write(str + "\n")
            
    def closeEvent(self, event):
        response = self.quit()
        if response == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

if __name__=="__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    app.exec_()
