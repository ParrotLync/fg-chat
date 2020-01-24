from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import os

class ChatServer:
    def __init__(self, ip: str, port: int):
        self.clients = {}
        self.addresses = {}
        self.bufsize = 1024
        self.server = socket(AF_INET, SOCK_STREAM)
        self.server.bind((ip, port))
        print(">> Now listening on", ip, "with port", port)
        
        self.server.listen(5)
        print("Waiting for a connection...")
        ACCEPT_THREAD = Thread(target=self.accept_incoming_connections)
        ACCEPT_THREAD.start()
        ACCEPT_THREAD.join()
        self.server.close()

    def accept_incoming_connections(self):
        while True:
            client, address = self.server.accept()
            print("New Connection:", address)
            client.send(bytes("> Hey there! You succesfully connected! Please type your nickname and press enter!", "utf-8"))
            self.addresses[client] = address
            Thread(target=self.handle_client, args=(client,)).start()

    def handle_client(self, client):
        nickname = client.recv(self.bufsize).decode("utf-8")
        msg = "> Welcome %s! If you want to quit, just close the chat window." % nickname
        self.private(client, msg)
        self.broadcast(nickname + " has joined the chat!")
        self.clients[client] = nickname
        
        while True:
            msg = client.recv(self.bufsize).decode('utf-8')
            if msg != '{quit}':
                self.broadcast(str(nickname) + ': ' + str(msg))
            else:
                self.broadcast(nickname + ' has left the chat!')
                self.private(client, '> You left the chat!')
                client.close()
                del self.clients[client]
                break

    def private(self, client, msg):
        client.send(bytes(msg, 'utf-8'))

    def broadcast(self, msg):
        for sock in self.clients:
            sock.send(bytes(msg, 'utf-8'))

if __name__ == '__main__':
    os.system('clear')
    chat = ChatServer('85.214.78.168', 1111)