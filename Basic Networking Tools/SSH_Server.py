import os
import paramiko
import socket
import sys
import threading

CWD = os.path.dirname(os.path.realpath(__file__))
# Provide a host key for authentication to the connecting client.
# The key mentioned in the line below must exist at the same directory as the python server.
HOSTKEYS = paramiko.RSAKey(filename=os.path.join(CWD, 'test_rsa.key'))
# The class below is a solid template of paramiko that can be used in other programs as well, it would be wise to
# encrypt credentials or read them from a remote database.
class Server (paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        # Hard coded credentials in the server file found below.
        if (username == 'py') and (password == 'thon'):
            return paramiko.AUTH_SUCCESSFUL

if __name__ == '__main__':
    server = '192.168.1.7'
    ssh_port = 2222

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((server, ssh_port))
        sock.listen(100)
        print('[+] Listening for connection...')
        client, addr = sock.accept()
    except Exception as e:
        print('[-] Listen failed: ' + str(e))
        sys.exit(1)
    else:
        print('[+] Got a connection!', client, addr)
    # The section below facilitates the session using Paramiko functions.
    cSession = paramiko.Transport(client)
    cSession.add_server_key(HOSTKEYS)
    server = Server()
    cSession.start_server(server=server)

    channel = cSession.accept(20)
    if channel is None:
        print('*** No channel.')
        sys.exit()

    print('[+] Authenticated!')
    print(channel.recv(1024))
    channel.send('Welcome to the custom ssh session')
    try:
        while True:
            command = input("Enter command: ")
            if command != 'exit':
                channel.send(command)
                receive = channel.recv(8192)
                print(receive.decode())
            else:
                channel.send('exit')
                print('Exiting...')
                cSession.close()
                break
    except KeyboardInterrupt:
        cSession.close()
