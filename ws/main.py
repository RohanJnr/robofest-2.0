import socket
from _thread import *



ServerSideSocket = socket.socket()
host = '127.0.0.1'
port = 2004
ThreadCount = 0
try:
    ServerSideSocket.bind((host, port))
except socket.error as e:
    print(str(e))
print('Socket is listening..')
ServerSideSocket.listen(5)

conn = {}

def multi_threaded_client(connection):
    connection.send(str.encode('Server is working:'))
    while True:
        data = connection.recv(2048)
        data = data.decode("utf-8")

        if data == "fusion":
            print("Fusion 360 client.")
            conn["fusion"] = connection

        elif data == "web":
            print("WEB it is")
            conn["web"] = connection


        else:
            conn["fusion"].sendall(data.encode("utf-8"))

        if not data:
            break
    connection.close()
while True:
    Client, address = ServerSideSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(multi_threaded_client, (Client, ))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))
ServerSideSocket.close()