import sys, resources

from PyQt5.QtCore import *
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
        self.createWidgets()
        self.initMenuBar()
        self.initStatusBar()
        self.initToolBar()
    
    def initUI(self):
        self.setWindowTitle('newFile.txt')
        self.center()
        self.show()
        
        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)
    
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
        
        self.fontFamilyAct = QAction(QIcon(":/images/font_family.png"), "Font family", self)
        
        self.fontSizeAct = QAction(QIcon(":/images/font_size.png"), "Font size", self)
        
        self.fontColorAct = QAction(QIcon(":/images/font_color.png"), "Font color", self)
        self.fontColorAct.triggered.connect(self.fontColor)
        
        self.highlightAct = QAction(QIcon(":/images/highlight.png"), "Highlight", self)
        self.highlightAct.triggered.connect(self.highlight)
        
        self.fontBoldAct = QAction(QIcon(":/images/bold.png"), "Bold", self)
        self.fontBoldAct.setShortcut(QKeySequence("Ctrl+B"))
        self.fontBoldAct.setToolTip("Bold")
        self.fontBoldAct.setStatusTip("Bold")
        self.fontBoldAct.triggered.connect(self.bold)
        
        self.fontItalicAct = QAction(QIcon(":/images/italic.png"), "Italic", self)
        self.fontItalicAct.setShortcut(QKeySequence("Ctrl+I"))
        self.fontItalicAct.setToolTip("Italic")
        self.fontItalicAct.setStatusTip("Italic")
        self.fontItalicAct.triggered.connect(self.italic)
        
        self.fontUnderlineAct = QAction(QIcon(":/images/underline.png"), "Underline", self)
        self.fontUnderlineAct.setShortcut(QKeySequence("Ctrl+U"))
        self.fontUnderlineAct.setToolTip("Underline")
        self.fontUnderlineAct.setStatusTip("Underline")
        self.fontUnderlineAct.triggered.connect(self.underline)
        
    def createWidgets(self):
        self.fontBox = QFontComboBox(self)
        self.fontBox.currentFontChanged.connect(self.fontFamily)
        
        self.fontSizeBox = QComboBox(self)
        self.fontSizeBox.setEditable(True)
        # Minimum number of chars displayed
        self.fontSizeBox.setMinimumContentsLength(3)
        self.fontSizeBox.activated.connect(self.fontSize)
        # Typical font sizes
        fontSizes = ['6','7','8','9','10','11','12','13','14',
                    '15','16','18','20','22','24','26','28',
                    '32','36','40','44','48','54','60','66',
                    '72','80','88','96']
        for i in fontSizes:
            self.fontSizeBox.addItem(i)
    
    def initMenuBar(self):
        self.menuBar = self.menuBar()
        # bar.setNativeMenuBar(False) # D'ont use OS native bar
        fileMenu = self.menuBar.addMenu("File")
        
        fileMenu.addAction(self.openAct) # Add action to "File" menu
        fileMenu.addAction(self.saveAct)
        fileMenu.addSeparator()
        fileMenu.addAction(self.quitAct)
        
    def initStatusBar(self):
        self.statusBar = self.statusBar()
        
    def initToolBar(self):
        editToolBar = self.addToolBar("Edit")
        editToolBar.addAction(self.cutAct)
        editToolBar.addAction(self.copyAct)
        editToolBar.addAction(self.pasteAct)
        fontToolBar = self.addToolBar("Font")
        fontToolBar.addAction(self.fontFamilyAct)
        fontToolBar.addWidget(self.fontBox)
        fontToolBar.addAction(self.fontSizeAct)
        fontToolBar.addWidget(self.fontSizeBox)
        fontToolBar.addAction(self.fontColorAct)
        fontToolBar.addAction(self.highlightAct)
        fontToolBar.addSeparator()
        fontToolBar.addAction(self.fontBoldAct)
        fontToolBar.addAction(self.fontItalicAct)
        fontToolBar.addAction(self.fontUnderlineAct)
      
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
        
    def cut(self):
        clipboard = QApplication.clipboard()
        cursor = self.textEdit.textCursor()
        s, e = cursor.position(), cursor.position() + len(cursor.selectedText())
        selectedText = cursor.selectedText()
        if selectedText != "":
            clipboard.setText(selectedText)
            curText = self.textEdit.toPlainText()
            if self.windowTitle().split(".")[1] == "html":
                self.textEdit.setHtml(curText[0:s] + curText[e:len(curText)])
            else:
                self.textEdit.setPlainText(curText[0:s] + curText[e:len(curText)])
            cursor.setPosition(s)
            self.textEdit.setTextCursor(cursor)
           
    def copy(self):
        clipboard = QApplication.clipboard()
        cursor = self.textEdit.textCursor()
        s, e = cursor.position(), cursor.position() + len(cursor.selectedText())
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
    
    def fontFamily(self,font):
      self.textEdit.setCurrentFont(font)
 
    def fontSize(self):
        self.textEdit.setFontPointSize(int(self.fontSizeBox.currentText()))
    
    def fontColor(self):
        # Get a color from the text dialog
        color = QColorDialog.getColor()
        # Set it as the new text color
        self.textEdit.setTextColor(color)
    
    def highlight(self):
        color = QColorDialog.getColor()
        self.textEdit.setTextBackgroundColor(color)

    def bold(self):
        if self.textEdit.fontWeight() == QFont.Bold: 
            self.textEdit.setFontWeight(QFont.Normal)
        else:
            self.textEdit.setFontWeight(QFont.Bold)
        
    def italic(self):
        state = self.textEdit.fontItalic()
        self.textEdit.setFontItalic(not state)
    
    def underline(self):
        state = self.textEdit.fontUnderline()
        self.textEdit.setFontUnderline(not state)
    
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