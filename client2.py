import socket
import threading
import sys
import re
import time

from PyQt5 import QtCore as core
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

host = 'localhost'
port = 9898
username = 'Default'
back_bottle_id = 0


class Client(QTabWidget):
    def __init__(self, parent=None):
        super(Client, self).__init__(parent)
        self.setWindowTitle('drift_bottle')

        # name widget
        self.setNameWidget = QWidget()
        self.btnSet =QPushButton('Set')
        self.name = QLineEdit()
        self.label = QLabel('name:')

        # chat widget
        self.setChatWidget = QWidget()
        self.btnSend = QPushButton('send')
        self.chat = QTextEdit()
        self.input = QLineEdit()

        # bottle Widget
        self.setBottleWidget = QWidget()
        # self.btlInputLabel = QLabel('message:')
        self.btlInput = QTextEdit()
        # self.btlTagLabel = QLabel('tag:')
        # self.btlTag = QLineEdit()
        self.btlBtnSent = QPushButton('throw')

        #get bottle Widget
        self.setBackBottleWidget = QWidget()
        # self.bkbtlFind = QLineEdit()
        self.bkbtlBtnFind = QPushButton('fish up a bottle')
        self.bkbtlText = QTextEdit()
        self.bkbtlReply = QTextEdit()
        self.bkbtlBtnReply = QPushButton('reply')

        #my bottle widget
        self.setMybottleWidget = QWidget()
        self.mybtnfind = QPushButton('find my bottles')
        self.mybtls = QTextEdit()

        #chat with server
        self.CSwidget = QWidget()
        self.CSin = QLineEdit()
        self.CSinf = QTextEdit()
        self.CSsend = QPushButton('send')

        self.addTab(self.setChatWidget, "chat room")
        self.addTab(self.setBottleWidget,"throw bottles")
        self.addTab(self.setBackBottleWidget,"get bottles")
        self.addTab(self.setMybottleWidget,"My bottles")
        # self.addTab(self.CSwidget,'chat with Aquaman')
        # self.addTab(self.setFirstWidget,"name")

        self.timer = core.QTimer()
        self.timer2 = core.QTimer()
        self.timer3 = core.QTimer()
        self.timer4 = core.QTimer()
        self.messages = []
        self.bottles = ""
        self.mymsgs = []
        self.bkbtlid = ""
        self.bkbtlusr = ""
        self.Btlmsg = []
        self.CSmsgs = []

        self.tab1UI()
        self.tab2UI()
        self.tab3UI()
        self.tab4UI()
        # self.tab5UI()
        # self.build()
        self.resize(600,400)
        self.createAction()

        recvThread = threading.Thread(target=self.recvFromServer)
        # recvThread.setDaemon(True)
        recvThread.start()

    #chat with server
    # def tab5UI(self):
    #     layout = QFormLayout()
    #     layout.addRow(self.CSinf)
    #     layout.addRow(self.CSin)
    #     layout.addRow(self.CSsend)
    #     self.CSwidget.setLayout(layout)

    # my bottle
    def tab4UI(self):
        layout = QFormLayout()

        layout.addRow(self.mybtnfind)
        layout.addRow(self.mybtls)
        self.setMybottleWidget.setLayout(layout)

    #get bottle
    def tab3UI(self):
        layout = QFormLayout()
        layout.addRow(self.bkbtlBtnFind)
        layout.addRow('bottle',self.bkbtlText)
        layout.addRow('reply',self.bkbtlReply)
        layout.addRow(self.bkbtlBtnReply)
        self.setBackBottleWidget.setLayout(layout)

    # throw bottle
    def tab2UI(self):
        layout = QFormLayout()
        layout.addRow('input',self.btlInput)
        layout.addRow('throw',self.btlBtnSent)
        self.setBottleWidget.setLayout(layout)

    # chat
    def tab1UI(self):
        layout = QFormLayout()
        layout.addRow('room',self.chat)
        layout.addRow('input',self.input)
        layout.addRow(self.btnSend)
        self.setChatWidget.setLayout(layout)



    #throw bottle to server
    def throwBottle(self):
        print('send bottle to server...')
        global username
        btlText = self.btlInput.toPlainText()
        self.btlInput.setText('')
        print(btlText)
        print(type(btlText))
        # btlTag = self.btlTag.text()
        # self.btlTag.setText('')
        try:

            msg = "send bottle:"+str(len(username))+"#"+str(len(btlText))+"#"+username+btlText
            s.send(msg.encode('utf-8'))
            print('bottle been sent')
        except:
            print('send bottle error')
            self.exit()

    # find bottle
    def findBottle(self):
        global username
        # global back_bottle_id
        # btlid = str(self.bkbtlid.text())
        # back_bottle_id = int(btlid)
        # self.bkbtlid.setText('')
        try:
            print('try to find bottle...')
            msg = "try to find bottle:"
            s.send(msg.encode('utf-8'))
        except:
            print('find bottle error')
            self.exit()

    # send back bottle
    def send_back_bottle(self):
        global username
        # global back_bottle_id
        btlreply = str(self.bkbtlReply.toPlainText())
        self.bkbtlReply.setText('')
        try:
            print('try to send back bottle...')
            msg = "back bottle reply:"+str(len(self.bkbtlusr))+"#"+str(len(btlreply))+"#"+str(self.bkbtlid)+"#"+self.bkbtlusr+btlreply
            s.send(msg.encode('utf-8'))
        except:
            print('send back bottle error')
            self.exit()

    # check my bottles
    def checkMybottle(self):
        global username
        try:
            self.mybtls.setText("")
            msg = "find my bottles:"+username
            s.send(msg.encode('utf-8'))
        except:
            print('check error')
            self.exit()

    # send message to Server
    def sendToServer(self):
        global username
        msg = str(self.input.text())
        self.input.setText('')
        if msg.strip() == '':
            return
        try:
            print('try to send message')
            msg2 = "send message: "+username+":"+msg
            s.send(msg2.encode('utf-8'))
            print ('send success')
        except:
            print('send message error')
            self.exit()

    #chat with Aquaman
    def ChatWithServer(self):
        global username
        msg = str(self.CSin.text())
        self.CSin.setText('')
        if msg.strip() == '':
            return
        try:
            print('try to chat:')
            msg2 = "chat:"+msg
            s.send(msg2.encode('utf-8'))
            print ('send success')
        except:
            print('send message error')
            self.exit()

    def recvFromServer(self):
        while 1:
            try:
                print('try to receive...')
                data = str(s.recv(1024))[2:-1]
                # print(str(data,'utf8'))
                print(data)
                if re.match(r'message:(.*)',data):
                    message = re.match(r'message:([\d\D]*)',data).group(1)
                    self.messages.append(message)
                elif re.match(r'fish up bottle:([\d\D]*)',data):

                    tre = re.match(r'fish up bottle:(\d*)#(\d*)#(\d*)#([\d\D]*)',data)
                    print("fish up")
                    id = tre.group(3)

                    lMsg = int(tre.group(1))
                    lUsr = int(tre.group(2))
                    rStr = tre.group(4)
                    Cmsg = "bottle:"+rStr[0:lMsg]
                    Cusr = rStr[lMsg:lMsg+lUsr]
                    if Cusr == username:
                        self.Btlmsg.append("fail in dredging bottles, please try again.")
                    else:
                        self.bkbtlusr = Cusr
                        print(Cmsg)
                        self.Btlmsg.append(Cmsg)
                        self.bkbtlid = id
                elif re.match("my bottles:([\d\D]*)",data):
                    tre = re.match(r'my bottles:([\d\D]*)#!@([\d\D]*)#!@([\d\D]*)',data)
                    print(tre)
                    id = tre.group(1)
                    mybtl = tre.group(2)
                    ans = tre.group(3)
                    self.mymsgs.append(id)
                    self.mymsgs.append(mybtl)
                    self.mymsgs.append(ans)
                    print(self.mymsgs)
                elif re.match("Aquaman:([\d\D]*)", data):
                    print(data.encode('utf-8'))
                    self.CSmsgs.append(data)

            except:
                return

    def showBottlefind(self):
        for m in self.Btlmsg:
            self.bkbtlText.append(m)
        self.Btlmsg = []

    def showBottle(self):
        for m in self.mymsgs:
            self.mybtls.append(m)
        self.mymsgs = []


    def showChat(self):
        for m in self.messages:
            self.chat.append(m)
        self.messages = []

    def showAquaman(self):
        for m in self.CSmsgs:
            self.CSinf.append(m)
        self.CSmsgs = []


    # def slotExtension(self):
    #     global username
    #     name = str(self.name.text())
    #     if name.strip() != '':
    #         username = name
    #         print (username)
    #     s.send(username.encode('utf-8'))
    #     self.setNameWidget.hide()

    def exit(self):
        s.close()
        sys.exit()

    # def build(self):
        # self.layout.addWidget(self.chat, 0, 0, 1, 4)
        # self.layout.addWidget(self.input, 2, 0, 1, 4)
        # self.layout.addWidget(self.btnSend, 2, 4)
        #
        # self.setNameLayout.addWidget(self.label, 0, 0)
        # self.setNameLayout.addWidget(self.name, 0, 1)
        # self.setNameLayout.addWidget(self.btnSet, 0, 2)
        # self.layout.addWidget(self.setNameWidget, 3, 0)
        # #bottle layout
        # self.layout.addWidget(self.setBottleWidget,8,0)
        # self.setBottleLayout.addWidget(self.btlInputLabel,0,0)
        # self.setBottleLayout.addWidget(self.btlInput,0,1)
        # self.setBottleLayout.addWidget(self.btlTagLabel,0,4)
        # self.setBottleLayout.addWidget(self.btlTag,0,5)
        # self.setBottleLayout.addWidget(self.btlBtnSent,0,6)
        #
        # #get bottle layout
        # self.layout.addWidget(self.setBackBottleWidget, 10, 0)
        # self.setBackBottleLayout.addWidget(self.bkbtlid, 0, 0)
        # self.setBackBottleLayout.addWidget(self.bkbtlFind, 0, 1)
        # self.setBackBottleLayout.addWidget(self.bkbtlBtnFind, 0, 4)
        # self.setBackBottleLayout.addWidget(self.bkbtlTextLbl, 1, 0)
        # self.setBackBottleLayout.addWidget(self.bkbtlText, 2, 0, 1, 1)
        # self.setBackBottleLayout.addWidget(self.bkbtlReplyLbl, 1, 1)
        # self.setBackBottleLayout.addWidget(self.bkbtlReply, 2, 1,1,1)
        # self.setBackBottleLayout.addWidget(self.bkbtlBtnReply, 3, 0)
        # self.layout.setSizeConstraint(QLayout.SetFixedSize)
        # self.showMaximized()

    def createAction(self):
        self.btnSend.clicked.connect(self.sendToServer)
        # self.btnSet.clicked.connect(self.slotExtension)
        self.bkbtlBtnFind.clicked.connect(self.findBottle)
        self.btlBtnSent.clicked.connect(self.throwBottle)
        self.mybtnfind.clicked.connect(self.checkMybottle)
        self.bkbtlBtnReply.clicked.connect(self.send_back_bottle)
        self.CSsend.clicked.connect(self.ChatWithServer)
        self.timer.timeout.connect(self.showBottle)
        self.timer2.timeout.connect(self.showBottlefind)
        # self.timer.timeout.connect(self.showCSchat)
        self.timer3.timeout.connect(self.showChat)
        self.timer4.timeout.connect(self.showAquaman)
        self.timer.start(1000)
        self.timer2.start(1000)
        self.timer3.start(1000)
        self.timer4.start(1000)


class logindialog(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('login')
        self.resize(200, 200)
        # self.setFixedSize(self.width(), self.height())
        self.setWindowFlags(Qt.WindowCloseButtonHint)

        self.frame = QFrame(self)
        self.verticalLayout = QVBoxLayout(self.frame)

        self.lineEdit_account = QLineEdit()
        self.lineEdit_account.setPlaceholderText("username")
        self.verticalLayout.addWidget(self.lineEdit_account)


        self.pushButton_enter = QPushButton()
        self.pushButton_enter.setText("login")
        self.verticalLayout.addWidget(self.pushButton_enter)

        self.pushButton_quit = QPushButton()
        self.pushButton_quit.setText("cancel")
        self.verticalLayout.addWidget(self.pushButton_quit)

        self.pushButton_enter.clicked.connect(self.on_pushButton_enter_clicked)
        self.pushButton_quit.clicked.connect(QCoreApplication.instance().quit)

    def on_pushButton_enter_clicked(self):
        global username
        if self.lineEdit_account.text() == "":
            return
        else:
            name = str(self.lineEdit_account.text())
            if name.strip() != '':
                username = name
            print (username)
            s.send(username.encode('utf-8'))
        # if self.lineEdit_password.text() == "":
        #     return
        self.accept()

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect((host, port))
# s.send(username.encode('utf-8'))
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
print ('[%s] connect' % username)

app = QApplication(sys.argv)
dialog = logindialog()
if  dialog.exec_()==QDialog.Accepted:
    c = Client()
    c.show()
    sys.exit(app.exec_())
