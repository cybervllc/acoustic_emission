import socket
import threading
import time
import ctypes as ct
from matplotlib import pyplot
from matplotlib.animation import FuncAnimation

# Запуск преобразования
s_76 = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
s_76.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
s_76.setsockopt(socket.IPPROTO_TCP, 0x10, 3)
s_76.connect(("192.168.1.102", 7176))
# Подключение к устройству
s_77 = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
s_77.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 10)
s_77.setsockopt(socket.IPPROTO_TCP, 0x10, 3)
s_77.connect(("192.168.1.102", 7177))
# Данные для отображения на графике
myData = list()
x_data, y_data = [], []
figure = pyplot.figure()
line, = pyplot.plot_date(x_data, y_data, '-')
# Запись данных в файл
text_w = '102'
fp = open('data/file_'+text_w+'.csv', 'w')

# Поток для получения данных
flag = True
def thread_function():
    global myData
    global myData_noze
    global myData_amplifaer
    global fp
    while flag:
        # Прием данных
        data = bytearray(s_77.recv(1200))
        length = len(data)
        if length >= 12:
            #   Длина пакета 12 байт
            for i in range(0, length, 12):
                #   Номер устройства
                #   1 byte
                number = data[i]
                # Форма сигнала
                if number == 207:  # форма сигнала
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
                        # value = ct.c_int16((data[i + j + 4] << 8) | data[i + j + 5]).value
                        value = (data[i + j + 5] << 8) | data[i + j + 4]
                        items.append(value)
                    #   Если это пакет не данные
                    if (items[0] == 32768) and (items[1] == 36864) and (items[3] == 60):
                        continue
                    #   Сохраняем данные
                    for j in range(len(items)):
                        valueSing = ct.c_int16(items[j]).value
                        fp.write(f"{valueSing}\n")
                        myData.append(valueSing)
                    while len(myData) > 1000:
                        myData.pop(0)
        else:
            fp.write(f"0\n")
            myData.append(0)
        time.sleep(0.00001)

# Отображение графика
def update(frame):
    global myData
    x_data.clear()
    y_data.clear()
    for count in range(len(myData)):
        x_data.append(count)
        y_data.append(myData[count])
    line.set_data(x_data, y_data)
    figure.gca().relim()
    figure.gca().autoscale_view()
    return line,

# Запуск потока
x = threading.Thread(target=thread_function)
x.start()
# Отображение графика
animation = FuncAnimation(figure, update, interval=1)
pyplot.show()
# Закрытие потока и файла
flag = False
x.join()
fp.close()
