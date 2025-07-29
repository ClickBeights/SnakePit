import socket

target_host = "127.0.0.1"
target_port = 9997

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

client.sendto(b"AAABBBCCC", (target_host, target_port))

# This line uses two variables (data and addr) because the recvfrom() function returns two pieces of information.
data, addr = client.recvfrom(4096)

print(data.decode())
client.close()
