import threading
import socket
from tkinter import *


class UiChatClient:
    ip = '127.0.0.1'
    port = 12345

    def __init__(self):
        self.connectedSocket = None
        self.window = None
        self.chatList = None
        self.messageEntry = None
        self.messageButton = None
        self.allChat =''

    def connect(self):
        self.connectedSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connectedSocket.connect((UiChatClient.ip, UiChatClient.port))

    def setWindow(self):
        self.window = Tk()
        self.window.title('PyChat')
        self.window.geometry('400x500')
        
        self.chatFrame = Frame(self.window)
        self.chatFrame.pack(side='top', fill='both', expand=True)

        self.xScrollbar = Scrollbar(self.chatFrame, orient=HORIZONTAL)
        self.yScrollbar = Scrollbar(self.chatFrame)
        self.xScrollbar.pack(side='bottom', fill='x')
        self.yScrollbar.pack(side='right', fill='y')

        self.chatList = Listbox(self.chatFrame, selectmode='extended', xscrollcommand=self.xScrollbar.set, yscrollcommand=self.yScrollbar.set)
        self.chatList.pack(side='left', fill='both', expand=True, padx=3, pady=3)
        self.xScrollbar.config(command=self.chatList.xview)
        self.yScrollbar.config(command=self.chatList.yview)
        

        self.messageFrame = Frame(self.window)        
        self.messageFrame.pack(side='bottom', fill='x')

        self.messageEntry = Entry(self.messageFrame)
        self.messageEntry.pack(side='left', fill='x', expand=True, padx=3, pady=3)
        self.messageEntry.bind('<Return>', self.sendMsgEvent)
        self.messageEntry.focus()

        self.messageButton = Button(self.messageFrame, width=10, text='전송', command=self.sendMsg)
        self.messageButton.pack(side='right', fill='x', padx=3, pady=3)



    def sendMsg(self):
        msg = self.messageEntry.get()
        self.messageEntry.delete(0, END)
        self.messageEntry.config(text='')
        msg = msg.encode(encoding='utf-8')
        self.connectedSocket.sendall(msg)

    def sendMsgEvent(self, e):
        self.sendMsg()

    def recvMsg(self):
        while True:
            msg = self.connectedSocket.recv(1024)
            msg = msg.decode()+'\n'
            self.chatList.insert(END, msg)
            # self.allChat += msg

            # self.chatList.config(text=self.allChat)

    def run(self):
        self.connect()
        self.setWindow()

        th2 = threading.Thread(target=self.recvMsg)
        th2.start()
        self.window.mainloop()

    def close(self):
        self.connectedSocket.close()


UiChatClient().run()