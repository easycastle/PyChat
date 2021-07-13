import socket
import threading

class Room:
    def __init__(self):
        self.clients = []
        self.allChat=None

    def addClient(self, c):
        self.clients.append(c)

    def delClient(self, c):
        self.clients.remove(c)

    def sendMsgAll(self, msg):
        for i in self.clients:
            print(i)
            i.sendMsg(msg)


class ChatClient:
    def __init__(self, r, soc):
        self.room = r
        self.id = None
        self.soc = soc

    def readMsg(self):
        self.id = self.soc.recv(1024).decode()
        msg = self.id + '님이 입장하셨습니다'
        self.room.sendMsgAll(msg)

        while True:
            msg = self.soc.recv(1024).decode()
            msg = self.id+': '+ msg
            self.room.sendMsgAll(msg)
        self.room.sendMsgAll(self.id + '님이 퇴장하셨습니다.')

    def sendMsg(self, msg):
        print(type(msg))
        self.soc.sendall(msg.encode(encoding='utf-8'))


class ChatServer:
    ip = '127.0.0.1'
    port = 12345

    def __init__(self):
        self.server_soc = None
        self.room = Room()

    def open(self):
        self.server_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_soc.bind((ChatServer.ip, ChatServer.port))
        self.server_soc.listen()

    def run(self):
        self.open()
        print('Server Start!')

        while True:
            client_soc, addr = self.server_soc.accept()
            print(addr, '접속')
            c = ChatClient(self.room, client_soc)
            self.room.addClient(c)
            print('클라이언트:',self.room.clients)
            th = threading.Thread(target=c.readMsg)
            th.start()

        self.server_soc.close()


ChatServer().run()