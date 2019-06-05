# Comments are not here. This is an application for private use.

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
from pypresence import Presence
import time
import queue
import sys
import random

class WebChat:
    def __init__(self, ip: str, port: int, top):
        global gui, client
        self.queue_in = queue.Queue()
        self.top = top
        gui = Graphic(top, self.queue_in, self.end_app)
        self.bufsize = 1024
        discord.update(state='Connecting...')
        client = socket(AF_INET, SOCK_STREAM)
        client.connect((ip, port))
        discord.update(state='Connected', details='ipICT Chat #1')

        self.running = 1
        receiver = Thread(target=self.receive)
        receiver.start()

        self.periodic_call()

    def receive(self):
        while self.running:
            try:
                msg = client.recv(self.bufsize).decode('utf-8')
                self.queue_in.put(msg)
            except OSError:
                break

    def end_app(self):
        self.running = 0

    def send(self):
        msg = gui.message.get()
        gui.message.set("")
        client.send(bytes(msg, 'utf-8'))
        if msg == '{quit}':
            gui.message.set("Chat disabled.")
            client.close()
            self.top.quit()

    def periodic_call(self):
        gui.process_incoming()
        if not self.running:
            sys.exit(1)
        self.top.after(200, self.periodic_call)


class Graphic:
    def __init__(self, top, queue_in, end_command):
        self.queue_in = queue_in
        self.top = top
        self.top.title("FGN Chat")

        self.messages_frame = tkinter.Frame(self.top)
        self.message = tkinter.StringVar()
        self.message.set("")
        self.scrollbar = tkinter.Scrollbar(self.messages_frame)

        self.msg_list = tkinter.Listbox(self.messages_frame, height=20, width=100, yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
        self.msg_list.pack()
        self.messages_frame.pack()

        self.entry_field = tkinter.Entry(self.top, textvariable=self.message)
        self.entry_field.bind("<Return>", WebChat.send)
        self.entry_field.pack()
        self.send_button = tkinter.Button(self.top, text="Send", command='Webchat.send')
        self.send_button.pack()

        self.top.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        self.message.set('{quit}')
        chat.send()

    def process_incoming(self):
        try:
            msg = self.queue_in.get(0)
            self.msg_list.insert(tkinter.END, msg)
        except queue.Empty:
            pass


class DiscordPresence:
    def __init__(self, client_id: str):
        self.RPC = Presence(client_id=client_id)
        self.RPC.connect()
        self.RPC.update(start=int(time.time()), state='In lobby')

    def update(self, state: str, details: str = None):
        self.RPC.update(state=state, details=details)

    def close(self):
        self.RPC.close()

if __name__ == '__main__':
    discord = DiscordPresence("585447447824826378")
    top = tkinter.Tk()
    chat = WebChat('85.214.78.168', 1111, top)
    top.mainloop()
