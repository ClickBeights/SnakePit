import socket
import threading

IP = '0.0.0.0' # Can be left empty as well
PORT = 9998

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IP, PORT))
    server.listen(5)   # The 5 means it will allow up to 5 queued connections before refusing new ones.
    print(f'[*] Listening on {IP}:{PORT}')

    while True:
        client, address = server.accept()

        # The address variable is a tuple specifically, it’s a 2-item tuple: (IP, port). We can call each using a
        # numerical value.
        print (f'[*] Accepted connection from {address[0]}:{address[1]}')

        # The args parameter expects a tuple — a collection of arguments that will be passed to the target function
        # (handle_client in this case). Even if you're passing just one argument, it still needs to be a tuple.
        # In our case, this is a tuple with one element.
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()

def handle_client(client_socket):
    with client_socket as sock:     # (With...as) is a clean, safe way to use resources (like files or sockets)
                                    # that should be automatically closed or cleaned up — even if something goes wrong.
        request = sock.recv(1024)
        print(f'[*] Received: {request.decode("utf-8")}')
        # Send message to connecting client.
        sock.send(b'This is ACK sir!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

if __name__ == '__main__':
    main()
