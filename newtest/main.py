import ctypes as ct
from matplotlib import pyplot
from matplotlib.animation import FuncAnimation

myData = list()
address = list()
cmd = list()

addr = 192 + 15

text_w = "_file_1"
path = 'dataPacket'+text_w+'.csv'

fp = open('packets_'+str(addr)+'_6_data.csv', 'w')
fpRaw = open('packetsRAW_'+str(addr)+'_6_data.csv', 'w')

def run_code():
    print("start")
    data = bytearray()
    with open(path, 'r') as fdata:
        for line in fdata:
            data.append(int(line))
    length = len(data)
    print(length)
    if length > 0:
        # for i in range(480, 1200, 12):
        for i in range(0, length, 12):
            # 1 - 16
            # 198(6) - 5 6 7
            # 199(7) - 0
            # 200(8) - 0 5 6 7
            # 212(20) - 5 7
            # 213(21) - 5 6 7
            if (data[i] != addr) or (data[i+1] != 6):
                continue
            # 1 byte - address
            if data[i] not in address:
                address.append(data[i])
            # 1 byte - command
            # print(data[i+1])
            if data[i + 1] not in cmd:
                cmd.append(data[i + 1])
            # 2 byte - len data in byte
            lenData = (data[i + 3] << 8) | data[i + 2]
            items = list()
            for j in range(0, lenData, 2):

                # item = ct.c_int16((data[i + j + 4] << 8) | data[i + j + 5]).value

                item = (data[i + j + 5] << 8) | data[i + j + 4]
                item = ct.c_int16(item).value

                items.append(item)

            if (items[0] == 128) and (items[1] == 144) and (items[3] == 15360):
                continue

            for j in range(0, 12, 1):
                fpRaw.write(f"{data[i + j]}\n")

            for j in range(len(items)):
                fp.write(f"{items[j]}\n")
                myData.append(items[j])

    print("Все адреса:")
    print(address)
    print("Все команды:")
    print(cmd)
    fp.close()
    fpRaw.close()
    print("end")


if __name__ == '__main__':
    run_code()


