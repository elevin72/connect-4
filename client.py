import socket
import player

CLIENT_HOST = ''
CLIENT_PORT = 4000
SERVER_HOST = ''
SERVER_PORT = 4001

class RemotePlayer:

    def send_to():
        pass

    def recv_from():
        pass

def Main():

    host = CLIENT_HOST #client ip
    port = CLIENT_PORT
    
    server = (SERVER_HOST, SERVER_PORT)
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host,port))

    sock.connect(server)


    
    message = input(" ")
    while message !='q':
        sock.sendall(message.encode('utf-8'))
        data, addr = sock.recvfrom(1024)
        data = data.decode('utf-8')
        print("Received from server: " + data)
        message = input("-> ")
    sock.close()

if __name__=='__main__':
    Main()

