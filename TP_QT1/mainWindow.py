import sys, resources
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

class MainWindow(QMainWindow):
    
    def __init__(self):
        # print("constructeur de la class MainWindow")
        super().__init__(None)
        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)
        self.menuBar = self.menuBar()
        # bar.setNativeMenuBar(False) # D'ont use OS native bar
        self.statusBar = self.statusBar()
        
        fileMenu = self.menuBar.addMenu("File")
        
        # Create different actions
        fileOpenAct = QAction(QIcon(":/images/open.png"), "Open", self)
        fileOpenAct.setShortcut(QKeySequence("Ctrl+O"))
        fileOpenAct.setToolTip("Open File")
        fileOpenAct.setStatusTip("Open a file")
        fileOpenAct.triggered.connect(self.openFile) # Connect the action to the slot (function)
        fileMenu.addAction(fileOpenAct) # Add action to "File" menu
        
        fileSaveAct = QAction(QIcon(":/images/save.png"), "Save", self)
        fileSaveAct.setShortcut(QKeySequence("Ctrl+S"))
        fileSaveAct.setToolTip("Save File")
        fileSaveAct.setStatusTip("Save to file")
        fileSaveAct.triggered.connect(self.saveFile)
        fileMenu.addAction(fileSaveAct)
        
        fileQuitAct = QAction(QIcon(":/images/quit.png"), "Quit", self)
        fileQuitAct.setShortcut(QKeySequence("Ctrl+Q"))
        fileQuitAct.setToolTip("Quit File")
        fileQuitAct.setStatusTip("Quit Application")
        fileQuitAct.triggered.connect(self.quitFile)
        fileMenu.addAction(fileQuitAct)
        
    def openFile(self):
        fileName = QFileDialog.getOpenFileName(self, "Open File", "", "Text files (*.txt *.html)")[0]
        self.statusBar.showMessage("Open " + fileName, 6000)
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
        
    def quitFile(self):
        response = QMessageBox.question(self, "Confirm exit", 
                                        "Are you sure you want to exit ?")
        if response == QMessageBox.Yes:
            sys.exit()
        
        
def main(args):
    # print("Hello World")
    app = QApplication(args)
    
    win = MainWindow()
    win.show()
    win.resize(800, 600)
    
    app.exec()
    
if __name__ == "__main__":
    main(sys.argv)