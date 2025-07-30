import argparse       # To parse command-line arguments.
import os             # Runs OS commands (imported for CD command).
import socket         # Provides low-level networking interfaces.
import shlex          # Tokenizes strings using shell-like syntax.
import subprocess     # Run and interact with system commands.
import sys            # Interact with the Python interpreter.
import textwrap       # Formats long strings, especially for console output.
import threading      # Run tasks with concurrent execution.


def execute(cmd):
    cmd = cmd.strip() # Remove any blank spaces.
    if not cmd:
        return None
    output = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)
    # Prints output of command executed, and redirect any errors of the command to standard output
    # shlex.sploit(cmd) safely splits the string "commands" into a list avoiding possible shell injections (Not for us)
    return output.decode()


class NetCat:
    def __init__(self, args, buffer=None):
        self.args = args # Stores the argument object so other methods (like send() or listen()) can access flags
                         # like args.listen, args.target, etc.
        self.buffer = buffer
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   # Additional options to make passing
                                                                                  # information easier back & forth.

    def run(self):  # This is the entry point that controls whether the tool should act as a server or a client
        if self.args.listen:  # Checks if the listen argument was set, otherwise goes into client mode.
            self.listen()
        else:
            self.send()

    def send(self):
        self.socket.connect((self.args.target, self.args.port))
        if self.buffer:
            self.socket.send(self.buffer)
        try:
            while True:
                recv_len = 1
                response = ''
                while recv_len:
                    data = self.socket.recv(4096)
                    recv_len = len(data)
                    response += data.decode()
                    if recv_len < 4096:
                        break
                if response:          # This handles the prompt appearance as it was ugly before.
                    # If the prompt is at the end, handle it separately
                    if response.endswith('<Npy: #> '):
                        # Print output before the prompt (if any)
                        output = response[:-len('<Npy: #> ')] # Removing the prompt (<Npy: #> ) from the end of the
                                                              # response string, so that only the command output is
                                                              # printed to the screen
                        if output:
                            print(output, end='')
                            # By default, print() adds a newline (\n) at the end. If we let it do that, we’d get an
                            # extra blank line between the command output and the shell prompt. Using end='' ensures
                            # the next line (your prompt: <Npy: #> ) starts immediately after the output

                        buffer = input('<Npy: #> ')
                    else:
                        print(response, end='')
                        buffer = input()
                    buffer += '\n'
                    self.socket.send(buffer.encode())
        except KeyboardInterrupt:
            print('User terminated.')
            self.socket.close()
            sys.exit()

    def listen(self):
        self.socket.bind((self.args.target, self.args.port))
        self.socket.listen(5)
        while True:
            client_socket, _ = self.socket.accept()
            client_thread = threading.Thread(
                target=self.handle, args=(client_socket,)
            )
            client_thread.start()

    def handle(self, client_socket):
        if self.args.execute:     # Execute a specific command
            output = execute(self.args.execute)
            client_socket.send(output.encode())

        elif self.args.upload:     # Upload a file
            file_buffer = b''
            while True:
                data = client_socket.recv(4096)    # If file being uploaded is big, adjust this line.
                if data:
                    file_buffer += data
                else:
                    break

            with open(self.args.upload, 'wb') as f:   # WB is for Writing Bytes.
                f.write(file_buffer)
            message = f'Saved fie {self.args.upload}'
            client_socket.send(message.encode())

        elif self.args.command:    # Create a Shell
            cmd_buffer = b''
            while True:
                try:
                    client_socket.send(b'<Npy: #> ')
                    while '\n' not in cmd_buffer.decode():
                        cmd_buffer += client_socket.recv(64)

                    command = cmd_buffer.decode().strip()    # Handles CD command as it broke the server.
                    if command.startswith('cd '):
                        try:
                            path = command[3:].strip()
                            os.chdir(path)
                            response = f'Changed directory to {os.getcwd()}\n'
                        except Exception as e:
                            response = f'Failed to change directory: {e}\n'
                    else:
                        response = execute(command) or ''
                    if response:
                        client_socket.send(response.encode())

                    cmd_buffer = b''
                except Exception as e:
                    print(f'server killed {e}')
                    self.socket.close()
                    sys.exit()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='A Very Basic Python NetCat',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''Example:
            netcat.py -t 192.168.10.50 -p 5555 -l -c # Command shell
            netcat.py -t 192.168.10.50 -p 5555 -l -u=mytest.txt # Upload to file
            netcat.py -t 192.168.10.50 -p 5555 -l -e=\"cat /etc/passwd" # Execute command
            echo 'ABC' | ./netcat.py -t 192.168.10.50 -p 135 # Echo text to server port 135
            netcat.py -t 192.168.10.50 -p 5555 # Connect to server
        '''))

    parser.add_argument('-c', '--command', action='store_true', help='Command shell')
    parser.add_argument('-e', '--execute', help='Execute specified command')
    parser.add_argument('-l', '--listen', action='store_true', help='Listen')
    parser.add_argument('-p', '--port',type=int, default=5555, help='Specified port')
    parser.add_argument('-t', '--target', default='192.168.10.50', help='Specified IP')
    parser.add_argument('-u', '--upload', help='Upload file')
    # action='store_true' means:
    # If you include the flag (e.g., -l), it becomes True.
    # If you don't include it, it stays False.

    args = parser.parse_args()
    # Parses all flags passed to the script by the user and stores the results in an args object.

    if args.listen:
        buffer = ''
    else:
        buffer = sys.stdin.read()
    # The if statement above checks whether you're in listen mode (server), the buffer is empty or If you're in client
    # mode (connecting to another host), it reads from standard input. Example:
    # echo "hello" | python netcat.py -t 10.0.0.1 -p 5555
    # In that case, buffer becomes "hello\n"

    nc = NetCat(args, buffer.encode())
    # Creates NetCat instance and passes args from CLI and encoded buffer in case of text.
    nc.run()
