import numpy as np
import scapy.all as scapy
import ctypes as ct

# Clevo_11:50:24	Broadcast	ARP	42	Who has 192.168.1.102? Tell 192.168.1.1
# spoofed= scapy.ARP(op=2 , pdst="192.168.1.102", psrc="192.168.1.1", hwdst="")
# scapy.send(spoofed, verbose= True)
# rez = scapy.srp(spoofed, timeout=5 , verbose= False)[0][0][1].hwsrc
# rez = spoofed


# Clevo_11:50:24	Broadcast	ARP	42	Who has 192.168.1.102? Tell 192.168.1.1
# Clevo_11:50:24	Broadcast	ARP	42	192.168.1.1 is at 80:fa:5b:11:50:24
# packet= scapy.ARP(op=2 , hwsrc="80:FA:5B:11:50:24" , psrc="192.168.1.1", hwdst="E8:98:C2:76:C1:EE" , pdst="192.168.1.102")
# rez = scapy.send(packet, verbose=False)


# arppacket= scapy.Ether(dst="ff:ff:ff:ff:ff:ff")/scapy.ARP(op=1 , pdst="192.168.1.1")
# targetmac= scapy.srp(arppacket, timeout=5, verbose= False)[1][0][1].hwsrc
#
# print(targetmac)

# item = 54533
# len = round(100 / 2)
# print(ct.c_int16(item).value)

# def revers16(value):
#     item = 0
#     for i in range(16):
#         if value & (1 << i):
#             item |= 1 << (15 - i)
#     return item
#
#
# print(revers16(8))

length = 96

for i in range(0, length, 2):
    print(i)






print("end")
