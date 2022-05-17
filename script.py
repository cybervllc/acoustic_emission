import socket
import threading
import time

import numpy as np
import pandas as pd
from ping3 import verbose_ping
import scapy.all as scapy
import ctypes as ct
from matplotlib import pyplot, pyplot as plt
from matplotlib.animation import FuncAnimation

# Поиск доступного устройства
spoofed = scapy.ARP(op=2, pdst="192.168.1.102", psrc="192.168.1.1", hwdst="")
scapy.send(spoofed, verbose=False)
# Проверка доступности
verbose_ping('192.168.1.102', count=1, ttl=128)
# Запуск преобразования
s_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
s_udp.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 20)
text = "\x5a\x44\x43\x50\x00\x01\x00\x00"
s_udp.sendto(text.encode('utf-8'), ('239.192.71.76', 7176))

# Открываем порт для команд
s_76 = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
s_76.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
s_76.setsockopt(socket.IPPROTO_TCP, 0x10, 3)
s_76.connect(("192.168.1.102", 7176))

def thread_function_port7176():
    while True:
        time.sleep(0.1)
        pass
        # Здесь посылать каждые 0,1 или 1 секунду команды для проверки готовности данных
    return 0

# Открываем порт для получения данных. Следующий +1
s_77 = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
s_77.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 10)
s_77.setsockopt(socket.IPPROTO_TCP, 0x10, 3)
s_77.connect(("192.168.1.102", 7177))

def thread_function_port7177():
    global threadContinue_0, df, fp_raw, fp_packet, dataChart
    newLine = False # Начало преобразования данных
    currentData = list() # Принимаемые данные от начала до конца преобразования
    row = 0
    # DEBUG START
    allNumbers = list()
    allCommand = list()
    # DEBUG END
    while threadContinue_0:
        time.sleep(0.00001)
        data = bytearray(s_77.recv(1200)) # Ожидать приема данных
        length = len(data)  # Размер принятых данных
        try:
            # DEBUG START
            # Сохраняем все байты данных в потоковый файл
            # for j in range(length):
            #     fp_raw.write(f"{data[j]}\n")
            # DEBUG END
            # Разбор пакетов. Длина пакета 12 байт.
            for i in range(0, length, 12):
                packet = data[i:i+12]
                #   Номер устройства - 1 byte / 192 + number(2 .. 63)
                number = packet[0] & 0x3F
                # DEBUG START
                if number not in allNumbers:
                    allNumbers.append(number)
                # DEBUG END
                # 15 - форма сигнала | 16 - уровень шума | 17 - параметрический канал
                if number == 15:
                    #   Номер команды - 1 byte
                    command = packet[1]
                    # DEBUG START
                    if command not in allCommand:
                        allCommand.append(command)
                    # DEBUG END
                    if command != 6:
                        continue
                    #   Количество байт данных - 2 byte (8 byte)
                    lenData = (packet[3] << 8) | packet[2]  # High Low
                    #   Данные
                    items = list()
                    for j in range(0, lenData, 2):
                        value = (packet[j + 5] << 8) | packet[j + 4]
                        items.append(value)
                    #   Данные нумирации пакетов
                    if (items[0] == 32768) and (items[1] == 36864) and (items[2] > 0) and (items[3] == 60):
                        continue
                    #   Данные начала пакетов
                    if (items[0] == 32768) and (items[1] == 36864) and (items[2] == 0) and (items[3] != 60):
                        if newLine:
                            newLine = False
                            if (len(currentData) > 960):
                                currentData = currentData[:960] # костыль
                            df[str(row)] = currentData
                            row += 1
                            dataChart.clear()
                            for j in range(len(currentData)):
                                dataChart.append(currentData[j])
                            currentData.clear()
                        continue
                    # Данные сигнала
                    for j in range(len(items)):
                        valueSing = ct.c_int16(items[j]).value
                        currentData.append(valueSing)
                        newLine = True
        except ArithmeticError:
            pass
    name = input("Enter name: ")
    df.to_csv('newtest/out_'+name+'.csv')
    # DEBUG START
    print("_____ _____ _____ INFO _____ _____ _____")
    print("numbers:")
    allNumbers.sort()
    print(allNumbers)
    print("command:")
    allCommand.sort()
    print(allCommand)
    # print(df)
    print("_____ _____ _____ _____ _____ _____ _____")
    # DEBUG END


threadContinue_0 = True
threadContinue_1 = True
df = pd.DataFrame() # Таблица всех принятых данных по пакетам

dataChart = list()

# Построение графика
figure, [ax1, ax2] = plt.subplots(nrows=2, ncols=1)
ax1.set_xlabel('time (s)')
ax2.set_xlabel('freq (MHz)')
ax1.grid()
ax2.grid()

text_w = "0" # input("Enter your value: ")
dir = "newtest/"
fp_raw = open(dir + 'dataRaw'+text_w+'.csv', 'w') # Файл с принятыми данными байтами (Не обработанный поток)
fp_packet = open(dir + 'dataPacket'+text_w+'.csv', 'w')


x = threading.Thread(target=thread_function_port7177)
x.start()


def updateChart(i):
    global dataChart
    data = list()
    Fs = 2400000  # Частота дискритизации устройства 2.4Mhz
    tstep = 1 / Fs  # Время выборки одной точки или время между точками
    N = 960  # Количество элементов в выборке
    if len(dataChart) < N:
        return
    data.append(0)
    for i in range(N):
        data.append(dataChart[i])
    data.append(0)
    # Сигнал
    y = np.ndarray((N,), buffer=np.array(data), offset=np.int_().itemsize, dtype=int)
    # Быстрое преобразование фурье
    X = np.fft.fft(y)
    X_mag = np.abs(X) / N  # По модулю и выравниваем по амплитуде
    #
    fstep = Fs / N
    f = np.linspace(0, (N - 1) * fstep, N)
    f_plot = f[0:int(N / 6 + 1)]  # Берем левую половину
    X_mag_plot = 5 * X_mag[0:int(N / 6 + 1)]  # Амплитуда для построения
    t = np.linspace(0, (N - 1) * tstep, N)  # Время выборки каждой точки, с интервалом tstep
    #
    ax1.cla()
    ax2.cla()
    #
    ax1.plot(t, y, '.-')
    ax2.plot(f_plot, X_mag_plot, '.-')
    #
    figure.gca().relim()
    figure.gca().autoscale_view()

animation = FuncAnimation(figure, updateChart, interval=100)
plt.show()


threadContinue_0 = False
x.join()


fp_raw.close()
fp_packet.close()



print('end')
