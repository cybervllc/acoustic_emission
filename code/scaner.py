import scapy.all as scapy

#My code
print("Scanning...")
arp_request=scapy.ARP(pdst='192.168.1.1')
brodcast=scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
arp=brodcast/arp_request
tmp=scapy.srp(arp, timeout=5,verbose=False)

answered = tmp[0]
data = answered



for element in answered:
    print("IP:{}".format(element[1].psrc))
    print("MAC address: {}\n".format(element[1].hwsrc))

print('end')
