import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

"""
Game of Life - Rules

Start with some distribution of cells on square grid

If a live cell has less than two live neigbors, it dies
If a live cell has two or three neighbors, it stays alive
If a live cell has more than three neighbors, it dies
If empty cell has more than three live neighbors, it becomes alive
"""

# Grid values
ON = 255
OFF = 0
vals = [ON, OFF]

# function to create initial grid with given probability of cell being alive


def initGrid(N: int, prob: float = 0.1):
    return np.random.choice(vals, N*N, p=[prob, 1-prob]).reshape(N, N)

# function to update grid


def updateGrid(frame, img, grid, N: int):
    # use periodic boundary conditions
    temp = grid.copy()
    for x in range(N):
        for y in range(N):
            # calculate the sum of neighboring cells
            nsum = int((grid[x, (y-1) % N] + grid[x, (y+1) % N] +
                        grid[(x-1) % N, (y-1) % N] + grid[(x-1) % N, y % N] + grid[(x-1) % N, (y+1) % N] +
                        grid[(x+1) % N, (y-1) % N] + grid[(x+1) % N, y] + grid[(x+1) % N, (y+1) % N])/255)

            if grid[x, y] == ON:
                if nsum < 2 or nsum > 3:
                    temp[x, y] = OFF
            else:
                if nsum == 3:
                    temp[x, y] = ON

    img.set_data(temp)
    grid[:] = temp[:]
    return img


def main(args: list) -> int:

    N = int(args[0])
    p = float(args[1])
    framerate = int(args[2])

    print("Starting game of life with parameters", N, p, framerate)
    grid = initGrid(N, p)
    print("Grid initialized, size ", N)
    print(grid)

    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest')

    # show animation of the grid
    ani = animation.FuncAnimation(fig, updateGrid, fargs=(
        img, grid, N, ), frames=10, interval=framerate, save_count=50)

    plt.show()


def parse_args() -> list:
    # get argument parser object
    ap = argparse.ArgumentParser()
    N = 100
    p = 0.2
    framerate = 50

    # add arguments to the parser
    ap.add_argument("-N", "--grid_size", required=False,
                    help="Creates N*N grid for the game, default {N}")
    ap.add_argument("-p", "--probability", required=False,
                    help="Probability of a random cell being alive, should float [0,1[, default {p}")
    ap.add_argument("-f", "--framerate", required=False,
                    help="Framerate for the plot")

    # parse command line arguments
    args = ap.parse_args()
    # convert namespace object to dictionary
    arg_dict = vars(args)
    arg_list = []

    if args.grid_size:
        arg_list.append(arg_dict['grid_size'])
    else:
        arg_list.append(N)

    if args.probability:
        arg_list.append(arg_dict['probability'])
    else:
        arg_list.append(p)

    if args.framerate:
        arg_list.append(arg_dict['framerate'])
    else:
        arg_list.append(framerate)

    return arg_list


# call main
if __name__ == '__main__':
    args = parse_args()
    main(args)
