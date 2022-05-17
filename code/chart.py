import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation



# Построение графика
fig, [ax1, ax2] = plt.subplots(nrows=2, ncols=1)
ax1.set_xlabel('time (s)')
ax2.set_xlabel('freq (MHz)')
ax1.grid()
ax2.grid()







def updateChart(i):
    Fs = 2400000  # Частота дискритизации устройства 2.4Mhz
    tstep = 1 / Fs  # Время выборки одной точки или время между точками
    N = 960  # Количество элементов в выборке

    # Сигнал
    y = np.ndarray((960,), buffer=np.array([
        0, 20, 22, 23, 22, 21, 18, 18, 17, 14, 9, 4, 1, -4, -7, -9, -13, -17, -18, -17, -20, -18, -12, -10, -6, -4, 0,
        9, 11, 17, 21, 25, 25, 27, 24, 22, 18, 15, 9, 3, -3, -9, -17, -21, -24, -28, -30, -29, -25, -23, -18, -15, -9,
        -3, 4, 9, 12, 16, 19, 24, 26, 23, 21, 21, 16, 11, 9, 4, -2, -6, -11, -14, -18, -18, -21, -19, -17, -15, -11, -8,
        -4, 0, 5, 8, 15, 16, 19, 21, 23, 23, 20, 17, 15, 12, 5, 0, -4, -7, -8, -12, -14, -14, -14, -16, -14, -13, -13,
        -9, -6, -4, -3, -1, 2, 5, 4, 6, 7, 9, 5, 5, 3, 1, 2, -1, -2, -3, -1, -1, 1, 0, 2, 4, 4, 7, 12, 10, 11, 11, 11,
        12, 11, 13, 11, 7, 5, 3, 1, -4, -7, -14, -15, -16, -15, -17, -18, -16, -15, -15, -11, -8, -6, -2, 0, 4, 5, 12,
        11, 12, 14, 15, 15, 16, 18, 13, 12, 12, 8, 5, 0, -2, -3, -7, -9, -14, -13, -14, -14, -15, -14, -13, -10, -7, -7,
        -2, 4, 7, 8, 10, 17, 19, 18, 19, 21, 20, 20, 20, 17, 12, 11, 4, -1, -6, -11, -17, -20, -26, -27, -27, -26, -23,
        -23, -18, -16, -6, 0, 3, 9, 13, 17, 18, 20, 22, 20, 17, 15, 11, 8, 3, -2, -5, -8, -10, -13, -15, -12, -14, -12,
        -10, -6, -6, -7, -4, -2, 3, 3, 5, 7, 8, 10, 10, 12, 9, 11, 13, 12, 10, 11, 10, 6, 4, 3, 0, -3, -5, -10, -13,
        -13, -16, -20, -20, -18, -17, -16, -14, -12, -8, -4, 0, 3, 7, 10, 13, 16, 16, 18, 17, 15, 11, 8, 2, -1, -5, -9,
        -10, -11, -11, -10, -8, -7, -3, 2, 5, 12, 10, 12, 15, 15, 14, 12, 10, 7, 1, -6, -10, -15, -15, -21, -24, -23,
        -21, -18, -17, -13, -8, -2, 3, 9, 16, 18, 22, 26, 27, 27, 24, 22, 17, 13, 7, 1, -3, -11, -16, -19, -23, -26,
        -26, -25, -23, -22, -16, -10, -7, -3, 5, 10, 13, 17, 20, 22, 22, 22, 19, 17, 15, 12, 9, 3, 1, -1, -2, -7, -10,
        -12, -13, -14, -15, -15, -16, -16, -14, -15, -14, -12, -9, -7, -4, 0, 3, 6, 8, 9, 11, 11, 12, 11, 11, 8, 6, 2,
        2, -2, -5, -10, -13, -12, -14, -15, -16, -16, -12, -9, -6, 0, 4, 12, 17, 17, 24, 25, 28, 26, 24, 22, 18, 12, 8,
        2, -7, -13, -19, -24, -27, -27, -28, -27, -23, -18, -13, -5, 2, 7, 13, 19, 20, 23, 24, 23, 21, 16, 13, 9, 3, -3,
        -6, -10, -14, -17, -20, -21, -22, -21, -21, -17, -12, -9, -5, 0, 5, 10, 14, 16, 20, 19, 18, 17, 16, 16, 14, 7,
        4, 2, -3, -5, -10, -13, -15, -15, -15, -14, -14, -11, -9, -6, 0, 4, 5, 9, 11, 12, 13, 14, 16, 18, 12, 10, 7, 3,
        -1, -4, -9, -12, -14, -15, -16, -19, -20, -17, -18, -16, -11, -11, -7, -2, 2, 4, 9, 11, 17, 18, 20, 22, 21, 21,
        17, 14, 10, 6, 3, -3, -9, -12, -17, -21, -23, -23, -24, -21, -18, -15, -11, -7, 1, 7, 13, 17, 23, 24, 25, 25,
        22, 20, 18, 12, 3, -2, -9, -13, -18, -23, -24, -26, -26, -24, -21, -16, -12, -7, 0, 3, 8, 15, 18, 21, 22, 23,
        21, 22, 18, 15, 11, 6, 1, -4, -10, -12, -15, -18, -20, -19, -19, -21, -19, -17, -12, -9, -6, -1, 4, 9, 10, 12,
        15, 16, 16, 15, 15, 13, 9, 6, 4, 0, -2, -4, -8, -12, -15, -14, -15, -14, -15, -13, -11, -7, -7, -5, -3, 1, 3, 7,
        8, 11, 13, 14, 15, 16, 16, 14, 14, 11, 8, 5, 2, -1, -7, -11, -12, -18, -18, -20, -20, -20, -17, -14, -11, -7,
        -3, 4, 8, 13, 19, 20, 22, 23, 21, 20, 16, 10, 7, 1, -5, -10, -16, -19, -20, -21, -23, -25, -21, -16, -11, -8,
        -3, 1, 3, 10, 12, 14, 17, 16, 13, 14, 14, 13, 10, 10, 8, 5, 3, -1, -1, -3, -4, -4, -7, -9, -12, -13, -14, -14,
        -14, -11, -12, -10, -6, -6, -2, 2, 5, 7, 8, 13, 17, 16, 17, 16, 17, 13, 9, 3, 1, -3, -6, -10, -15, -16, -20,
        -24, -21, -20, -19, -15, -10, -6, -3, 4, 11, 13, 15, 22, 24, 23, 19, 19, 16, 16, 11, 6, 0, -7, -11, -16, -19,
        -25, -26, -25, -24, -20, -17, -11, -5, -1, 5, 12, 21, 25, 26, 28, 29, 25, 21, 17, 11, 5, -5, -9, -14, -21, -26,
        -30, -33, -31, -28, -23, -16, -13, -7, 1, 6, 12, 18, 24, 29, 32, 34, 32, 28, 22, 19, 15, 9, 2, -4, -9, -14, -16,
        -20, -20, -21, -22, -22, -20, -17, -12, -9, -5, -1, 3, 7, 11, 14, 18, 21, 25, 27, 24, 25, 24, 20, 14, 9, 3, -3,
        -7, -12, -17, -24, -27, -33, -34, -34, -33, -29, -26, -20, -14, -6, 6, 14, 19, 30, 36, 38, 40, 43, 39, 34, 28,
        22, 12, 3, -8, -20, -29, -35, -41, -43, -45, -45, -40, -34, -28, -19, -8, 4, 16, 25, 34, 40, 46, 48, 51, 48, 41,
        34, 26, 14, 5, -7, -17, -25, -33, -39, -45, -45, -43, -39, -35, -27, -19, -12, -3, 8, 15, 24, 30, 36, 41, 40,
        41, 38, 33, 31, 26, 17, 11, 5, -3, -12, -20, -25, -31, -32, -38, -39, -35, -33, -27, -19, -12, -4, 4
    ]), offset=np.int_().itemsize, dtype=int)

    # Быстрое преобразование фурье
    X = np.fft.fft(y)
    X_mag = np.abs(X) / N  # По модулю и выравниваем по амплитуде

    fstep = Fs / N
    f = np.linspace(0, (N - 1) * fstep, N)
    f_plot = f[0:int(N / 2 + 1)]  # Берем левую половину
    X_mag_plot = 5 * X_mag[0:int(N / 2 + 1)]  # Амплитуда для построения
    t = np.linspace(0, (N - 1) * tstep, N)  # Время выборки каждой точки, с интервалом tstep

    ax1.cla()
    ax2.cla()

    ax1.plot(t, y, '.-')
    ax2.plot(f_plot, X_mag_plot, '.-')



anim = FuncAnimation(fig, updateChart, frames=100, interval=200, repeat=False)
plt.show()


