import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
import random

FONT = ('Arial', 18)
MSGFONT = ('Arial', 14)
BTNFONT = ('Arial', 16)
BLACK = '#222831'
TEAL = '#76ABAE'
GREY = '#31363F'
LIGHT_GREY = '#EEEEEE'
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = '127.0.0.1'
PORT = 3000


root = tk.Tk()
root.title('Chat App')
root.geometry('800x800')
root.resizable(False, False)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=6)
root.grid_rowconfigure(2, weight=1)

def createMsg(msg, color='#000000'): 
    msg_box.config(state=tk.NORMAL)
    msg_box.insert(tk.END, msg + '\n', color)
    msg_box.tag_configure(color, foreground=color)
    msg_box.config(state=tk.DISABLED)


def get_random_color():
    return f'#{random.randint(0, 255):02X}{random.randint(0, 255):02X}{random.randint(0, 255):02X}'


def connect():
    try:
        client.connect((HOST, PORT))
        print('Connected to server')
        createMsg('[Server] Connected to server')
    except:
        messagebox.showerror('Unable to connect','Error: Connection refused')

    username = usernameTextbox.get()
    if username == '':
        messagebox.showerror('Empty username','Username cannot be empty')
        exit(1)
    else:
        client.sendall(username.encode('utf-8'))

    threading.Thread(target=messageListenerFromServer, args=(client,)).start()
    usernameTextbox.config(state=tk.DISABLED)
    username_btn.config(state=tk.DISABLED)

def sendMessage():
    msg = msg_textbox.get()
    if msg == '':
        messagebox.showerror('Empty message','Message cannot be empty')
        exit(1)
    else:
        client.sendall(msg.encode('utf-8'))
        msg_textbox.delete(0, len(msg))


topFrame = tk.Frame(root, width=800, height=100, bg = BLACK)
topFrame.grid(row=0, column=0, sticky=tk.NSEW)

middleFrame = tk.Frame(root, width=800, height=600, bg = GREY)
middleFrame.grid(row=1, column=0, sticky=tk.NSEW)

bottomFrame = tk.Frame(root, width=800, height=100, bg = BLACK)
bottomFrame.grid(row=2, column=0, sticky=tk.NSEW)

usernameLabel = tk.Label(topFrame, text='Username: ', font=FONT, bg = BLACK, fg = TEAL)
usernameLabel.pack(side=tk.LEFT, padx=10)

usernameTextbox = tk.Entry(topFrame, font=FONT, bg = GREY, fg = TEAL, width = 42)
usernameTextbox.pack(side=tk.LEFT)

username_btn = tk.Button(topFrame, text='Join', font=BTNFONT, bg = TEAL, fg = GREY, command = connect)
username_btn.pack(side=tk.LEFT, padx=15)

msg_textbox = tk.Entry(bottomFrame, font=FONT, bg = GREY, fg = TEAL, width = 52)
msg_textbox.pack(side=tk.LEFT, padx=10)

msg_btn = tk.Button(bottomFrame, text='Send', font=BTNFONT, bg = TEAL, fg = GREY, command = sendMessage)
msg_btn.pack(side=tk.LEFT, padx=10)

msg_box = scrolledtext.ScrolledText(middleFrame, font=MSGFONT, bg = GREY, fg = TEAL, width = 75, height = 33)
msg_box.config(state=tk.DISABLED)
msg_box.pack(side=tk.LEFT)


user_colors = {} 
def assign_color_to_user(username):
    if username not in user_colors:
        user_colors[username] = get_random_color()
    return user_colors[username]

def messageListenerFromServer(client):
    while True:
        msg = client.recv(1024).decode('utf-8')
        if msg:
            username = msg.split(':')[0]
            msgContent = msg.split(':')[1]
            
            user_color = assign_color_to_user(username)
            
            createMsg(f'{username}: {msgContent}', user_color)
        else:
            messagebox.showerror('Message empty','Message received is empty')


def main():

    root.mainloop()

if __name__ == '__main__': 
    main()