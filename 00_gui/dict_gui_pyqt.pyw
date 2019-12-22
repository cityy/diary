#here we import necessary things we need
import sys
from PyQt5 import QtWidgets, QtGui, QtCore, Qt
import importlib.util

# custom script to create the entry csv
spec = importlib.util.spec_from_file_location("entryMaker", "../00_tools/entryMaker.py")
entryMaker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(entryMaker)


# for high dpi displays
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

class MainWindow:
    def makeTextEdit(self, text, yPos, height):
        bgColor = '#232323'
        border = 'none'
        ident = text.split(' ')[0].lower()
        self.textEdit = QtWidgets.QTextEdit(self.window, tabChangesFocus=True, acceptRichText=False)
        self.textEdit.setObjectName(ident)
        self.textEdit.setGeometry(25,yPos,450,height)
        self.textEdit.setPlaceholderText(text)
        self.textEdit.setStyleSheet("background-color:" + bgColor + "; border: " + border + "; color:#8e8e8e; padding-top: 12px; font-size:10px; padding-left:10px")

    def closeProgram(self):
        self.app.quit()

    def addEntry(self):
        data = dict()
        data['keyword'] = self.window.findChild(QtWidgets.QTextEdit, 'keyword').toPlainText()
        data['quote'] = self.window.findChild(QtWidgets.QTextEdit, 'quote').toPlainText()
        data['authors'] = self.window.findChild(QtWidgets.QTextEdit, 'authors').toPlainText()
        data['chapter'] = self.window.findChild(QtWidgets.QTextEdit, 'chapter').toPlainText()
        data['book'] = self.window.findChild(QtWidgets.QTextEdit, 'book').toPlainText()
        data['year'] = self.window.findChild(QtWidgets.QTextEdit, 'year').toPlainText()
        data['pages'] = self.window.findChild(QtWidgets.QTextEdit, 'pages').toPlainText()
        data['tags'] = self.window.findChild(QtWidgets.QTextEdit, 'tag1').toPlainText()
        data['file'] = self.imagePathLabel.toPlainText()   
        # print(data)
        entryMaker.run(data)
        self.createBtn.setStyleSheet("background-color:#fedbD0; color:#121212;font-size:15px;")
        self.createBtn.setText("Success")
        # print( self.window.findChildren(QtWidgets.QTextEdit) )
       # entryMaker.run(data)

    def loadImage(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self.window, 'Open file', 'jpg,png,gif')
        self.imagePathLabel.setText(fname[0])

    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.window = QtWidgets.QMainWindow()
        # self.window.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        #self.imagePath = "./Graf_2004_499.jpg"

        self.initGUI()

        self.window.setWindowTitle("Add an entry to the Catalogue")
        self.window.setStyleSheet("background-color:#000000; font-family:Lucida Console;")
        self.window.setGeometry(500, 100, 500,755)
        self.window.setFixedSize(self.window.size()) # fix the window size
        self.window.show()
        sys.exit(self.app.exec_())

    def initGUI(self):


        self.makeTextEdit('Keyword', 25, 40 )
        self.makeTextEdit('Quote', 90, 80 )
        self.makeTextEdit('Authors (Name, Surname)', 195, 40 )
        self.makeTextEdit('Chapter / Article / ...', 260, 40 )
        self.makeTextEdit('Book / Magazine / Website', 325, 40 )
        self.makeTextEdit('Year', 390, 40 )
        self.makeTextEdit('Pages / URL', 455, 40 )
        self.makeTextEdit('Tag1 + Tag 2 + ...', 520, 80 )

        self.imageUpload = QtWidgets.QPushButton(self.window)
        self.imageUpload.setText("...")
        self.imageUpload.setGeometry(435, 625, 40, 40)
        self.imageUpload.setStyleSheet("background-color:#232323; color:#9a9a9a;font-size:10px; border:none;")
        self.imagePathLabel = QtWidgets.QTextEdit(self.window)
        self.imagePathLabel.setPlaceholderText('Image or Text File Path')
        self.imagePathLabel.setGeometry(25, 625, 409, 40)
        self.imagePathLabel.setStyleSheet("background-color: #232323; border:none; color:#8e8e8e; padding-top: 12px; font-size:10px; padding-left:10px")
        self.imageUpload.clicked.connect(lambda: self.loadImage())

        #create the create entry button
        self.createBtn = QtWidgets.QPushButton(self.window)
        self.createBtn.setText("Create Entry")
        self.createBtn.setGeometry(25, 690, 212.5, 40)
        self.createBtn.setStyleSheet("background-color:#8e8e8e; color:#242424;font-size:10px;")
        self.createBtn.clicked.connect(lambda: self.addEntry())

        #Button to end the Program
        self.quitBtn = QtWidgets.QPushButton(self.window)
        self.quitBtn.setText("Quit")
        self.quitBtn.setGeometry(262.5,690, 212.5, 40)
        self.quitBtn.setStyleSheet("background-color:#8e8e8e; color:#242424;font-size:10px;")
        self.quitBtn.clicked.connect(lambda: self.closeProgram())


#let's instantiate an object to the class MainWindow
main = MainWindow()