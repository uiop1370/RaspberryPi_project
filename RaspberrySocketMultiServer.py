from socket import *
from select import *
from threading import *
import pymysql


#DB설정
data1 = ""
data2 = ""
row = None #테이블의 행을 받아줌
sql = ""

conn = pymysql.connect(host='192.168.0.84', user='root', password='1234', db='mysql', charset='utf8') #접속정보
cur = conn.cursor()




HOST = 'localhost'
PORT = 9999
ADDR = (HOST, PORT)
users = []
serverSocket = socket(AF_INET, SOCK_STREAM)
usersNickname = []

class Waiting(Thread):
    global serverSocket
    global ADDR
    
    def __init__(self):
        super().__init__()
        serverSocket.bind(ADDR)
        serverSocket.listen(100)
        
    def run(self):
        try:
            while True:
                clientSocket, addr = serverSocket.accept()
                if not clientSocket:
                    continue
                t2 = RaspberryServer(clientSocket)
                t2.start()
        except:
            pass

class RaspberryServer(Thread):
    global ADDR
    global users
    global serverSocket
    global usersNickname
    
    def __init__(self, socket):
        super().__init__()
        users.append(socket)
        self.socket = socket

#     def nickname(self):
#         try:
#             while True:
#                 nickname = self.socket.recv(1024)
#                 if "nickname:" in nickname.decode():
#                     nickname = nickname.decode().split(":")[1]
#                     usersNickname.append(nickname)
#                     self.socket.sendall("Entered ChatRoom".encode())
#                     break
#         except:
#             pass
        
    def SELECT(self, add):
        cur.execute("SELECT * FROM PP WHERE NUM = "+add.decode())
        while (True):      
            row = cur.fetchone()
            if row == None:
                break
            data1 = row[0]
            data2 = row[1]
            print("%2s" % data2)
            return data2

    def run(self):
        print("sub thread start", len(users))
        print('Connected by', ADDR)
        print('client Socket', self.socket)
        try:
            while True:
                data = self.socket.recv(1024)
                if not data:
                    break
                print('Received from', ADDR, data.decode())
#                 num = data.decode()
                DBdata = self.SELECT(data)
                
                senderSocketIndex = users.index(self.socket)
                t3 = ServerSender(data, senderSocketIndex, DBdata)
                t3.start()
        finally:
            users.remove(self.socket)
            self.socket.close()
            serverSocket.close()
            
class ServerSender(Thread):
    global users
    
    def __init__(self, data, senderSocketIndex, DBdata):
        super().__init__()
        self.data = data
        self.senderSocketIndex = senderSocketIndex
        self.DBdata = DBdata

    def run(self):
        for i in range(len(users)):
            tempSocket = users[i]
#             newData = self.data.decode()
            tempSocket.sendall(self.DBdata.encode())

t1 = Waiting()
t1.start()
