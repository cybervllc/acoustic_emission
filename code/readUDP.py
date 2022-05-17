import socket


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

sock.bind(('239.192.71.76', 7176))

while True:
    data, addr = sock.recvfrom(1024)
    print("received message: %s" % data)