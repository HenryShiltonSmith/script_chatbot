import os
import sys
import base64

from tkinter import E
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from pathlib import Path

from chat import chatbot

pixmap = "" 
        
class Ui_MainWindow(object):                                                     
    def setupUi(self, MainWindow, firstSetup):
        # Create main window
        MainWindow.setObjectName("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        # Create chat label
        self.lblChat = QtWidgets.QTextEdit(self.centralwidget)
        self.lblChat.setAutoFillBackground(False)
        self.lblChat.setObjectName("lblChat")
        self.lblChat.setAlignment(Qt.AlignBottom)
        # self.lblChat.setWordWrap(True)
        self.lblChat.setGeometry(QtCore.QRect(20, 70, 750, 410))
        self.lblChat.setReadOnly(True)
        self.lblChat.setFontPointSize(12)
        self.lblChat.setAlignment(QtCore.Qt.AlignBottom)
        
        # Create input button
        self.btnSend = QtWidgets.QPushButton(self.centralwidget)
        self.btnSend.setObjectName("btnSend")
        
        # Create input text box
        self.tbInput = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.tbInput.setObjectName("tbInput")
        
        
        # Create agent image
        self.lblImage = QtWidgets.QLabel(self.centralwidget)
        self.lblImage.setObjectName("lblImage")
        self.lblImage.setGeometry(QtCore.QRect(20, 10, 55, 55))
        
        # Create agent name label
        self.lblName = QtWidgets.QLabel(self.centralwidget)
        self.lblName.setObjectName("lblName")
        self.lblName.setGeometry(QtCore.QRect(90, 10, 241, 61)) 
        self.lblName.setText("Place holder")      
                
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setObjectName("menubar")
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow, firstSetup)
        
    def retranslateUi(self, MainWindow, firstSetup):           
        _translate = QtCore.QCoreApplication.translate      
        MainWindow.setWindowTitle(_translate("MainWindow", "Generic Inc. Chatbot"))
        self.btnSend.setText(_translate("MainWindow", "SEND"))
        self.tbInput.setPlaceholderText(_translate("MainWindow", "Please enter your message."))
        self.lblImage.setText(_translate("MainWindow", "Placeholder"))
          
        pixmap = QPixmap("chetan_bot")
        self.lblImage.setPixmap(pixmap)  
        self.lblImage.setGeometry(QtCore.QRect(20, 10, 55, 55))
        self.lblName.setGeometry(QtCore.QRect(90, 10, 241, 61))
        self.btnSend.setGeometry(QtCore.QRect(662, 500, 111, 41))
        self.tbInput.setGeometry(QtCore.QRect(20, 500, 621, 41))
        
        # Set Chatbot Name Label
        self.lblName.setText("Chetan B.")
        
        # Set Default First Message
        self.lblChat.setText("Chetan: Hello. My name is Chetan Bot. How can I help you today?")
        
        app.setStyleSheet("QLabel{font-size: 12pt;}")
        
        # connect button to function on_click
        self.btnSend.clicked.connect(lambda: self.on_click())
        

    # Function ran by clicking submit button
    def on_click(self):
        censor = False
        chat_input = str(self.tbInput.toPlainText()).replace("\n","")
        
        holder = str(self.lblChat.toHtml()).count('<p ')
        
        # Open and decrypt blacklist.txt
        data = open("blacklist.txt", "r").read()
        blacklist_dc = str(base64.b64decode(data))
        blacklist = blacklist_dc.split(r"\n")
        
        # Check if input is in blacklist if is astrix out the censored word and set bolean to true
        for word in chat_input.split():
            if word.lower() in blacklist:
                chat_input = chat_input.replace(word, "*" * len(word))
                censor = True
         
        # If bolean true
        if censor == True:
            # add input (With astrik replacement) to chatlog       
            self.lblChat.setText(str(self.lblChat.toHtml()) + "<p align='right'>" + "You: " + chat_input + "</p>")
            
            font = QtGui.QFont()
            font.setPointSize(12)
            self.lblChat.setFont(font)
            # Add hard coded please watch language outpitu to chatlog
            self.lblChat.setText(str(self.lblChat.toHtml()) + "<p align='left'>" + "Chetan: Please mind your langauge" + \
                "</p>")
            # refresh input text box
            self.tbInput.setPlainText("")
        else: # If not censoring
            self.lblChat.setText(str(self.lblChat.toHtml()) + "<p align='right'>" + "You: " + chat_input + "</p>")
            font = QtGui.QFont()
            font.setPointSize(12)
            self.lblChat.setFont(font)
            
            # Set chat_returns to the return of chatbot function when given input
            chat_returns = chatbot(chat_input)
            
            try:
                # If return a goodbye
                if chat_returns[0] == "goodbye":
                    self.lblChat.setText(str(self.lblChat.toHtml()) + "<p align='left'>" + "Chetan: " + chat_returns[1] + "</p>")
                    self.tbInput.setPlainText("")
                    self.tbInput.setReadOnly(True)
                    self.tbInput.setPlaceholderText("Please exit the program")
                else:
                    # If return isn't goodbye clear input and prepare for new input
                    self.lblChat.setText(str(self.lblChat.toHtml()) + "<p align='left'>"  + "Chetan: " + chat_returns[1] + "</p>")
                    self.tbInput.setPlainText("")
            except:
                # If no return respond that chatbot doesn't understand
                self.lblChat.setText(str(self.lblChat.toHtml()) + "<p align='left'>"  + "Chetan: I am not sure what you mean. </p>")
                self.tbInput.setPlainText("")
            
            font = QtGui.QFont()
            font.setPointSize(12)
            self.lblChat.setFont(font)

class Window(QtWidgets.QMainWindow):
    def  __init__(self, parent=None):
        super(Window, self).__init__(parent=parent)
        self.setWindowTitle("TEST")
        self.setFixedSize(800, 601)
        ui = Ui_MainWindow()
        ui.setupUi(self, True)

if __name__ == "__main__":
    import sys
    os.chdir(Path(__file__).parent)
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = Window()
    MainWindow.show()
    sys.exit(app.exec_())