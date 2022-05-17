import matplotlib.pyplot as plt
import numpy as np

plt.ion() ## Note this correction
fig=plt.figure()
plt.axis([0, 500, -40000, 40000])

myData = list()

while True:
    myData.clear()
    for i in range(500):
        item = 65535 * np.random.random() - 32767
        myData.append(item)
    for i in range(500):
        plt.scatter(i, myData[i])
        plt.pause(0.0001)
    plt.show()







