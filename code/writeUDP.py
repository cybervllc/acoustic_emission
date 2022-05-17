import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 20)
# 0x5a, 0x44, 0x43, 0x50, 0x00, 0x01, 0x00, 0x00
text = "\x5a\x44\x43\x50\x00\x01\x00\x00"

s.sendto("text".encode('utf-8'), ('239.192.71.76', 7176))

print("end")