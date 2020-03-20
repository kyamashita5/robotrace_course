import numpy as np
import matplotlib.pyplot as plt


def plot_points(points_path):
    points = np.loadtxt(points_path)

    plt.axes().set_aspect('equal')
    plt.plot(points[:,0], points[:,1])
    plt.grid()
    plt.show()

if __name__ == '__main__':
    import sys
    points_path = 'real/2019alljapan_points.txt'
    argv = sys.argv    
    if len(argv) >= 2:
        points_path = argv[1]
    plot_points(points_path)