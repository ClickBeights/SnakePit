# To add: try catch to eliminate ugly errors...
import socket # This gives you tools to create a network connection.

target_host = "127.0.0.1"
target_port = 9999

# You create a socket object, which is like a virtual plug to connect to another computer.
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# This line makes the actual connection to Google's web server.
client.connect((target_host, target_port))

# You're manually sending an HTTP GET request, just like a browser would.
client.send(b"GET / HTTP/1.1\r\nHost: google.com\r\n\r\n")

# This line reads up to 4,069 bytes of data from the server.
response = client.recv(4069)

# The server sends raw bytes, so you need to convert (decode) it into a readable string.
print(response.decode())

# This disconnects the socket — like hanging up a phone call.
client.close()
