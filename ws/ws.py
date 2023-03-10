
import asyncio
import websockets

import socket
ClientMultiSocket = socket.socket()
host = '192.168.177.125'
port = 2004
print('Waiting for connection response')

try:
    ClientMultiSocket.connect((host, port))
except socket.error as e:
    print(str(e))
print("SOCKET SERVER RUNNING")
ClientMultiSocket.send(str.encode("web"))

async def echo(websocket):
    print("CLIENT DETECTED!")
    async for message in websocket:
        print(message)
        await asyncio.sleep(1)
        ClientMultiSocket.send(message.encode("utf-8"))

async def main():
    async with websockets.serve(echo, "localhost", 8765):
        print("WEB SOCKET RUNNING")
        await asyncio.Future()  # run forever

asyncio.run(main())