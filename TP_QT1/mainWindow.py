import sys, resources

from functools import partial
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

# Q1: Que faut il ne pas oublier pour que le code s’execute?
# 	app = Application(args)
#	app.exec()

# Q2: Pourquoi la fenêtre ne s’affiche pas? que faut il rajouter?
# 	QMainWindow.__init__(self) dans __init__() de la classe MainWindow

# Pour compiler resources.qrc :
#	pyrcc5 -o resources.py resources.qrc, puis importer la classe

# Q4: Comment connecter les actions aux slots ?
#	yourAction.triggered.connect(self.your_function)

HEIGHT = 720
WIDTH = 1280

class MainWindow(QMainWindow):
    
    def __init__(self):
        # print("constructeur de la class MainWindow")
        super().__init__(None)
        self.initUI()
        self.createAction()
        self.initMenuBar()
        self.initStatusBar()
        self.initToolBar()
        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)
    
    def initUI(self):
        self.setWindowTitle('File Editor')
        self.center()
        self.show()
    
    def createAction(self):
        # Create different actions
        self.openAct = QAction(QIcon(":/images/open.png"), "Open", self)
        self.openAct.setShortcut(QKeySequence("Ctrl+O"))
        self.openAct.setToolTip("Open File")
        self.openAct.setStatusTip("Open a file")
        self.openAct.triggered.connect(self.openFile) # Connect the action to the slot (function)
        
        self.saveAct = QAction(QIcon(":/images/save.png"), "Save", self)
        self.saveAct.setShortcut(QKeySequence("Ctrl+S"))
        self.saveAct.setToolTip("Save File")
        self.saveAct.setStatusTip("Save to file")
        self.saveAct.triggered.connect(self.saveFile)
        
        self.cutAct = QAction(QIcon(":/images/cut.png"), "Cut", self)
        self.cutAct.setShortcut(QKeySequence("Ctrl+X"))
        self.cutAct.setToolTip("Cut")
        self.cutAct.setStatusTip("Cut")
        self.cutAct.triggered.connect(self.cut)
        
        self.copyAct = QAction(QIcon(":/images/copy.png"), "Copy", self)
        self.copyAct.setShortcut(QKeySequence("Ctrl+C"))
        self.copyAct.setToolTip("Copy")
        self.copyAct.setStatusTip("Copy")
        self.copyAct.triggered.connect(self.copy)
        
        self.pasteAct = QAction(QIcon(":/images/paste.png"), "Paste", self)
        self.pasteAct.setShortcut(QKeySequence("Ctrl+V"))
        self.pasteAct.setToolTip("Paste")
        self.pasteAct.setStatusTip("Paste")
        self.pasteAct.triggered.connect(self.paste)
        
        self.quitAct = QAction(QIcon(":/images/quit.png"), "Quit", self)
        self.quitAct.setShortcut(QKeySequence("Ctrl+Q"))
        self.quitAct.setToolTip("Quit File")
        self.quitAct.setStatusTip("Quit Application")
        self.quitAct.triggered.connect(self.quitFile)
    
    def initMenuBar(self):
        self.menuBar = self.menuBar()
        # bar.setNativeMenuBar(False) # D'ont use OS native bar
        fileMenu = self.menuBar.addMenu("File")
        
        fileMenu.addAction(self.openAct) # Add action to "File" menu
        fileMenu.addAction(self.saveAct)
        fileMenu.addAction(self.quitAct)
        
    def initStatusBar(self):
        self.statusBar = self.statusBar()
        
    def initToolBar(self):
        editToolBar = self.addToolBar("Edit")
        editToolBar.addAction(self.cutAct)
        editToolBar.addAction(self.copyAct)
        editToolBar.addAction(self.pasteAct)
      
    def openFile(self):
        fileName = QFileDialog.getOpenFileName(self, "Open File", "", "Text files (*.txt *.html)")[0]
        self.statusBar.showMessage("Open " + fileName, 6000)
        self.setWindowTitle(fileName)
        # Read file
        if fileName != "":
            f = open(fileName, "r")
            if fileName.split(".")[1] == "html":
                self.textEdit.setHtml(f.read())
            else:
                self.textEdit.setPlainText(f.read())
            f.close()
        
    def saveFile(self):
        self.statusBar.showMessage("Save..")
        fileName = QFileDialog.getSaveFileName(self, "Save File", "", "Text files (*.txt *.html)")[0]
        # Save to file
        if fileName != "":
            f = open(fileName, "w")
            if fileName.split(".")[1] == "html":
                f.write(self.textEdit.toHtml())
            else:
                f.write(self.textEdit.toPlainText())
            self.statusBar.showMessage("Saved to " + fileName, 6000)
            f.close()
    
    def getSelectTextPos(self):
        cursor = self.textEdit.textCursor()
        start = int(cursor.selectionStart())
        end = int(cursor.selectionEnd())
        return start, end
        
    def cut(self):
        clipboard = QApplication.clipboard()
        s, e = self.getSelectTextPos()
        selectedText = self.textEdit.toPlainText()[s:e]
        if selectedText != "":
            clipboard.setText(selectedText)
            curText = self.textEdit.toPlainText()
            if self.windowTitle().split(".")[1] == "html":
                self.textEdit.setHtml(curText[0:s] + curText[e:len(curText)])
            else:
                self.textEdit.setPlainText(curText[0:s] + curText[e:len(curText)])
            self.textEdit.moveCursor(QTextCursor.position(s))
           
    def copy(self):
        clipboard = QApplication.clipboard()
        s, e = self.getSelectTextPos()
        if self.windowTitle().split(".")[1] == "html":
            selectedText = self.textEdit.toHtml()[s:e]
        else:
            selectedText = self.textEdit.toPlainText()[s:e]
        if selectedText != "": clipboard.setText(selectedText)
    
    def paste(self):
        clipboard = QApplication.clipboard()
        if self.windowTitle().split(".")[1] == "html":
            self.textEdit.insertHtml(clipboard.text())
        else:
            self.textEdit.insertPlainText(clipboard.text())
        
    def quitFile(self):
        response = QMessageBox.question(self, "Confirm exit", 
                                        "Are you sure you want to exit ?")
        if response == QMessageBox.Yes:
            sys.exit()
        return response
    
    def center(self):
        screen = QApplication.primaryScreen()
        self.setGeometry(int(screen.size().width()/2)-int(WIDTH/2),
                         int(screen.size().height()/2)-int(HEIGHT/2), 
                         WIDTH, HEIGHT)
        
    def closeEvent(self, event):
        response = self.quitFile()
        if response == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
        
def main(args):
    # print("Hello World")
    app = QApplication(args)
    win = MainWindow()
    win.resize(WIDTH, HEIGHT)
    app.exec()
    
if __name__ == "__main__":
    main(sys.argv)