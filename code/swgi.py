import socket
from ping3 import verbose_ping
import scapy.all as scapy
import ctypes as ct
from matplotlib import pyplot
from matplotlib.animation import FuncAnimation

# spoofed = scapy.ARP(op=2, pdst="192.168.1.102", psrc="192.168.1.1", hwdst="")
# scapy.send(spoofed, verbose=False)

# verbose_ping('192.168.1.102', count=1, ttl=128)

s_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
s_udp.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 20)
text = "\x5a\x44\x43\x50\x00\x01\x00\x00"
s_udp.sendto(text.encode('utf-8'), ('239.192.71.76', 7176))

s_76 = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
s_76.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
s_76.setsockopt(socket.IPPROTO_TCP, 0x10, 3)
s_76.connect(("192.168.1.102", 7176))

s_77 = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
s_77.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
s_77.setsockopt(socket.IPPROTO_TCP, 0x10, 3)
s_77.connect(("192.168.1.102", 7177))

data = s_76.recv(1024)
# print(data)

data = s_77.recv(1024)
# print(data)

myData = list()

x_data, y_data = [], []
figure = pyplot.figure()
line, = pyplot.plot_date(x_data, y_data, '-')

# fp = open('myData.csv', 'w')
# fp_1 = open('myData_1.csv', 'w')

# ---------------------------

dataMed = list()
dataMed.append(0)
dataMed.append(0)
dataMed.append(0)
countMed = 7

def median(value):
    global dataMed
    global countMed
    dataMed.append(value)
    if len(dataMed) > countMed:
        dataMed.pop(0)
    arr = list()
    for i in range(len(dataMed)):
        arr.append(dataMed[i])
    flag = True
    while flag:
        flag = False
        for i in range(len(dataMed) - 1):
            if arr[i] > arr[i + 1]:
                flag = True
                tmp = arr[i]
                arr[i] = arr[i + 1]
                arr[i + 1] = tmp
    num = round(len(dataMed) / 2)
    return arr[num]

def revers16(value):
    item = 0
    for i in range(16):
        if value & (1 << i):
            item |= 1 << (15 - i)
    return item

# ---------------------------

def update(frame):
    global myData
    global fp
    data = bytearray(s_77.recv(1024))
    length = len(data)
    if length > 1:
        length = round(length / 2)
        # print(length)
        if length > 0:
            # fp.write(f"{length * 100000}\n")
            for i in range(0, length, 12):
                item_1_1 = ct.c_int16((data[i + 1] << 8) | data[i]).value
                item_1_2 = ct.c_int16((data[i + 3] << 8) | data[i + 2]).value
                print(item_1_2)
                item_2_1 = (data[i + 5] << 8) | data[i + 4]
                item_2_2 = (data[i + 7] << 8) | data[i + 6]
                item_2_3 = (data[i + 9] << 8) | data[i + 8]
                item_2_4 = (data[i + 11] << 8) | data[i + 10]

                # fp_1.write(f"{item_1_1};{item_1_2}\n")
                #
                # fp.write(f"{item_2_1}\n")
                # fp.write(f"{item_2_2}\n")
                # fp.write(f"{item_2_3}\n")
                # fp.write(f"{item_2_4}\n")

                if item_2_1 & 32768:
                    item_2_1 -= 65536
                if item_2_2 & 32768:
                    item_2_2 -= 65536
                if item_2_3 & 32768:
                    item_2_3 -= 65536
                if item_2_4 & 32768:
                    item_2_4 -= 65536

                myData.append(item_2_1)
                myData.append(item_2_2)
                myData.append(item_2_3)
                myData.append(item_2_4)
                # myData.append(item)
                while len(myData) > 500:
                    myData.pop(0)
    x_data.clear()
    y_data.clear()
    for count in range(len(myData)):
        x_data.append(count)
        y_data.append(myData[count])
    line.set_data(x_data, y_data)
    figure.gca().relim()
    figure.gca().autoscale_view()
    return line,


animation = FuncAnimation(figure, update, interval=250)

pyplot.show()

# fp.close()
# fp_1.close()

print('end')
