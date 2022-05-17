from datetime import datetime
from matplotlib import pyplot
from matplotlib.animation import FuncAnimation

x_data, y_data = [], []
data = 0

figure = pyplot.figure()
line, = pyplot.plot_date(x_data, y_data, '-')


def update(frame):
    global data
    x_data.append(datetime.now())
    y_data.append(data)
    line.set_data(x_data, y_data)
    figure.gca().relim()
    figure.gca().autoscale_view()
    data = data + 1
    return line,


animation = FuncAnimation(figure, update, interval=1)

pyplot.show()
