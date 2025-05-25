import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


plt.style.use('fivethirtyeight')

def animate(i):
    with open("data.txt", "r") as f:
        data = [float(line.strip()) for line in f]
        
    y = data
    x = [item for item in range(len(y))]

    plt.cla()
    plt.plot(x, y, label='yield')
    plt.legend(loc='upper left')
    plt.tight_layout()



def main():
    ani = FuncAnimation(plt.gcf(), animate, interval=20000, cache_frame_data=False)
    plt.tight_layout()
    plt.show()

main()
