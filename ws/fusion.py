import socket
ClientMultiSocket = socket.socket()
host = '127.0.0.1'
port = 2004
print('Waiting for connection response')

try:
    ClientMultiSocket.connect((host, port))
except socket.error as e:
    print(str(e))
else:
    ClientMultiSocket.send(str.encode("fusion"))

    while True:
        res = ClientMultiSocket.recv(1024)
        print(res.decode('utf-8'))

        if not res:
            break

    ClientMultiSocket.close()