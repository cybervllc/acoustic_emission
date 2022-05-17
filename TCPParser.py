import socket
import threading
import time

from ping3 import verbose_ping
import scapy.all as scapy
import ctypes as ct
from matplotlib import pyplot
from matplotlib.animation import FuncAnimation

spoofed = scapy.ARP(op=2, pdst="192.168.1.102", psrc="192.168.1.1", hwdst="")
scapy.send(spoofed, verbose=False)

verbose_ping('192.168.1.102', count=1, ttl=128)

# Запуск преобразования
s_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
s_udp.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 20)
text = "\x5a\x44\x43\x50\x00\x01\x00\x00"
s_udp.sendto(text.encode('utf-8'), ('239.192.71.76', 7176))

s_76 = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
s_76.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
s_76.setsockopt(socket.IPPROTO_TCP, 0x10, 3)
s_76.connect(("192.168.1.102", 7176))

s_77 = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
s_77.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 10)
s_77.setsockopt(socket.IPPROTO_TCP, 0x10, 3)
s_77.connect(("192.168.1.102", 7177))

data = s_76.recv(1024)
# print(data)

data = s_77.recv(1024)
# print(data)

myData = list()
myData_noze = list()
myData_amplifaer = list()

x_data, y_data = [], []
figure = pyplot.figure()
line, = pyplot.plot_date(x_data, y_data, '-')

val = input("Enter your value: ")

text_w = "_file_" + val
dir = "newtest/"
fp = open(dir + 'data'+text_w+'.csv', 'w')
fp_raw = open(dir + 'dataRaw'+text_w+'.csv', 'w')
fp_packet = open(dir + 'dataPacket'+text_w+'.csv', 'w')

allAddres = list()
allCmd = list()
flag = True

def thread_function():
    global myData
    global myData_noze
    global myData_amplifaer
    global fp
    while flag:
        time.sleep(0.00001)
        data = bytearray(s_77.recv(1200))
        length = len(data)
        if length > 0:
            fp_raw.write(f"\n\n")
            # Сохраняем все байты данных
            for i in range(length):
                fp_raw.write(f"{data[i]}\n")
            # print(length)
            #   Парсим пакеты
            #   Длина пакета 12 байт
            for i in range(0, length, 12):
                #   Номер устройства
                #   1 byte
                number = data[i]
                if number not in allAddres:
                    allAddres.append(number)

                # Форма сигнала
                if number == 207:  # 3 - форма сигнала | 4 - уровень шума | 5 - параметрический канал
                    #   Номер команды
                    #   1 byte
                    command = data[i + 1]
                    # Проверка
                    if command != 6:
                        continue
                    #   Количество байт данных
                    #   2 byte
                    lenData = (data[i + 3] << 8) | data[i + 2]  # High Low
                    #   Парсим данные
                    items = list()
                    for j in range(0, lenData, 2):
                        value = (data[i + j + 5] << 8) | data[i + j + 4]
                        items.append(value)
                    #   Если это пакет не данные
                    if (items[0] == 32768) and (items[1] == 36864) : #and (items[3] == 60):
                        if (items[2] == 0) and (items[3] != 60):
                            fp.write(f"0\n-8192\n8192\n0\n")
                            # myData.clear()
                            myData.append(0)
                            myData.append(0)
                            myData.append(0)
                            myData.append(0)
                        # print(f"{items[2] & 0xFF} _ {items[2] >> 8}")
                        for k in range(0, 12):
                            fp_packet.write(f"{data[i + k]}\n")
                        continue

                    # for j in range(0, 12):
                    #     fp_packet.write(f"{data[i + j]}\n")
                    #   Сохраняем данные
                    for j in range(len(items)):
                        valueSing = ct.c_int16(items[j]).value
                        fp.write(f"{valueSing}\n")
                        myData.append(valueSing)
                    while len(myData) > 1000:
                        myData.pop(0)
                """
                # Шум
                if number == 208:  # 3 - форма сигнала | 4 - уровень шума | 5 - параметрический канал
                    #   Номер команды
                    #   1 byte
                    command = data[i + 1]
                    # if command not in allCmd:
                    #     allCmd.append(command)
                    # Проверка
                    if command != 6:
                        continue
                    #   Количество байт данных
                    #   2 byte
                    lenData = (data[i + 3] << 8) | data[i + 2]  # High Low
                    #   Парсим данные
                    items = list()
                    for j in range(0, lenData, 2):
                        value = (data[i + j + 4] << 8) | data[i + j + 5]
                        items.append(value)
                    #   Сохраняем данные
                    for j in range(len(items)):
                        valueSing = ct.c_int16(items[j]).value
                        myData_noze.append(valueSing)
                    while len(myData_noze) > 1000:
                        myData_noze.pop(0)

                # Амплитуда
                if number == 212:  # 20 - | 21 -
                    #   Номер команды
                    #   1 byte
                    command = data[i + 1]
                    # if command not in allCmd:
                    #     allCmd.append(command)
                    # Проверка
                    # if command != 6:
                    #     continue
                    #   Количество байт данных
                    #   2 byte
                    lenData = (data[i + 3] << 8) | data[i + 2]  # High Low
                    #   Парсим данные
                    items = list()
                    for j in range(0, lenData, 2):
                        value = (data[i + j + 4] << 8) | data[i + j + 5]
                        items.append(value)
                    #   Сохраняем данные
                    for j in range(len(items)):
                        valueSing = ct.c_int16(items[j]).value
                        myData_amplifaer.append(valueSing)
                    while len(myData_amplifaer) > 1000:
                        myData_amplifaer.pop(0)
                """
        else:
            fp.write(f"0\n")
            myData.append(0)
    return 0


def update(frame):
    global myData
    global myData_noze
    global myData_amplifaer

    x_data.clear()
    y_data.clear()
    for count in range(len(myData)):
        x_data.append(count)
        y_data.append(myData[count])
    line.set_data(x_data, y_data)
    figure.gca().relim()
    figure.gca().autoscale_view()
    return line,


x = threading.Thread(target=thread_function)
x.start()

animation = FuncAnimation(figure, update, interval=1)
pyplot.show()

flag = False
x.join()

fp.close()
fp_raw.close()
fp_packet.close()


print("ADDRES:")
print(allAddres)
print("COMMAND:")
print(allCmd)

print('end')
