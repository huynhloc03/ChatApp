import socket
import threading

HOST = '127.0.0.1'
PORT = 3000
LISTENER_CAPACITY = 10
current_clients = []

def messageListener(client, username):
    while True:
        msg = client.recv(1024).decode('utf-8')
        if msg =='':
            print ('Message is empty')
        else:
            sentMessage= username + ': ' + msg
            sendMessageAll(sentMessage)

def sendMessageClient(client, message):
    client.sendall(message.encode('utf-8'))

def sendMessageAll(message):
    for users in current_clients:
        sendMessageClient(users[1], message)

def clientHandler(client):
    while True:
        username = client.recv(1024).decode('utf-8')
        if username =='':
            print('Client name is empty')
        else:
            current_clients.append((username,client))
            break
    threading.Thread(target=messageListener, args=(client, username)).start()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"Server started on {HOST}:{PORT}")
    try:
        server.bind((HOST, PORT))
    except:
        print('Error: Port already in use')

    server.listen(LISTENER_CAPACITY)

    while True:
        client, address = server.accept()
        print('Connected with ' + address[0] + ':' + str(address[1]))
        threading.Thread(target=clientHandler, args=(client,)).start()

if __name__ == '__main__':
    main()
