
for i in range(1, 268):
    text_N = str(i)
    fpFIL = open('dataFilter/data1_4mm_P6M5_300kHz_'+text_N+'.csv', 'w')

    with open('data/data1_4mm_P6M5_300kHz_'+text_N+'.csv', 'rb') as f:
        for line in f:
            value = int(line)
            if value not in [1737, 1735, 1481, 1479, 1465, 1493, 1297, 2245, 2246, 2227, 1399, 1366, 1345, 586, 587, 1416, 1417, 1418, 1419, 1268, 1568]:
                # if value < 400 and value > -400:
                fpFIL.write(f"{value}\n")
    fpFIL.close()


print("end")