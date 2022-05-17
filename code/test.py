import scapy.all as scapy
from scapy.layers.l2 import Ether, ARP
from scapy.sendrecv import srp


class scan:
    def Arp(self, ip):
        self.ip = ip
        print(ip)
        arp_r = scapy.ARP(pdst=ip)
        br = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
        request = br/arp_r
        # answered, unanswered = scapy.srp(request, timeout=1)
        answered, unanswered = srp(Ether(dst="FF:FF:FF:FF:FF:FF") / ARP(pdst=ip), timeout=1, iface='enth0', inter=0.1)
        print('\tIP\t\t\t\t\tMAC')
        print('_' * 37)
        for i in answered:
            ip, mac = i[1].psrc, i[1].hwsrc
            print(ip, '\t\t' + mac)
            print('-' * 37)

arp = scan() # create an instance of the class
arp.Arp('192.168.1.102/7176')