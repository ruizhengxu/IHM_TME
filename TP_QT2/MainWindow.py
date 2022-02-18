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
        actBrush = colorMenu.addAction(QIcon(":/icons/brush.png"), "&Brush color", self.brush_color, QKeySequence("Ctrl+B"))

        colorToolBar = QToolBar("Color")
        self.addToolBar( colorToolBar )
        colorToolBar.addAction( actPen )
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
            sys.exit()
        return response
    
    def pen_color(self):
        color = QColorDialog.getColor()
        self.canvas.set_pen_color(color)
        self.log_action("Pen Color :" + str(color.getRgb()))

    def brush_color(self):
        color = QColorDialog.getColor()
        self.canvas.set_brush_color(color)
        self.log_action("Brush Color :" + str(color.getRgb()))
        
    def erase_last(self):
        self.canvas.erase()
    
    def erase_all(self):
        response = QMessageBox.question(self, "Confirm erase", 
                                        "Are you sure you want to erase all figures ?")
        if response == QMessageBox.Yes:
            self.canvas.erase(all=True)

    def free_drawing(self):
        self.log_action("Shape Mode: free drawing")
        self.canvas.set_shape(Shape.FREE)
        
    def line(self):
        self.log_action("Shape Mode: line")
        self.canvas.set_shape(Shape.LINE)
        
    def rectangle(self):
        self.log_action("Shape Mode: rectangle")
        self.canvas.set_shape(Shape.RECT)

    def cercle(self):
        self.log_action("Shape Mode: cercle")
        self.canvas.set_shape(Shape.CERCLE)

    def ellipse(self):
        self.log_action("Shape Mode: ellipse")
        self.canvas.set_shape(Shape.ELLIPSE)

    def move(self):
        self.log_action("Mode: move")
        self.canvas.set_mode(Mode.MOVE)

    def draw(self):
        self.log_action("Mode: draw")
        self.canvas.set_mode(Mode.DRAW)
        
    def select(self):
        self.log_action("Mode: select")
        self.canvas.set_mode(Mode.SELECT)
        
    def lasso(self):
        self.log_action("Mode: lasso")
        self.canvas.set_mode(Mode.LASSO)
        
    def zoom_in(self):
        self.log_action("Tool: zoom in")
    
    def zoom_out(self):
        self.log_action("Tool: zoom out")
        
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
