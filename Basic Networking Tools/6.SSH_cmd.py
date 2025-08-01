import paramiko

# This functions makes an SSH connection to a server and runs a single command
def ssh_command(ip, port, user, passwd, cmd):
    client = paramiko.SSHClient()
    # This line Tells Paramiko what to do when the SSH server's host key is not in the known hosts list
    # (i.e., first-time connection). It then automatically accept unknown host keys without prompting.
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port=port, username=user, password=passwd)
    # We are using underscore instead of stdin because we want to ignore it (The following method expects 3 values).
    _, stdout, stderr = client.exec_command(cmd)
    output = stdout.readlines() + stderr.readlines()
    if output:
        print('---Output---')
        for line in output:
            print(line.strip())

if __name__ == '__main__':
    # Allows interaction with passwords.
    import getpass
    # This line autopopulates username based on user who ran the script.
    # user = getpass.getuser()
    user = input('Enter username: ')
    # The password is hidden so no shoulder surfing.
    password = getpass.getpass()
    # Anything after 'or' is default values. You can test with "bandit.labs.overthewire.org" instead of.
    ip = input('Enter server IP or Domain: ') or '192.168.10.50'
    port = input('Enter port or <CR>: ') or 2220
    cmd = input('Enter command or <CR>: ') or 'id'
    ssh_command(ip, port, user, password, cmd)

# Paramiko supports authentication with keys and or passwords (Preferred over simple passwords)
