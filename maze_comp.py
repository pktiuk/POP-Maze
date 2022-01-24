#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import math, time, random, csv, os, sys
from timeit import default_timer as timer
from tqdm import tqdm
from maze_solver.maze import Maze, TileType
from maze_solver.solver import Solver


def create_folder(name):
    parent_dir = os.getcwd()
    path = os.path.join(parent_dir, name)
    os.makedirs(path, exist_ok=True)


def test_size(start_size, end_size, iterations, heuristic, jump):
    folder_name = 'results'
    create_folder(folder_name)
    filename = str(start_size) + "-" + str(end_size) + "_" + str(
        iterations) + "_" + "_" + str(heuristic) + ".csv"
    filename = os.path.join(folder_name, filename)
    with open(filename, 'w', newline="") as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=",")

        csvwriter.writerow([
            'iteration', 'size', 'time [ms]', 'path length',
            'visited tiles [%]'
        ])
        for size in tqdm(range(start_size, end_size + 1, jump)):

            avg_time = 0
            avg_path_length = 0
            avg_visited_tiles = 0

            for _ in range(iterations):
                maze = Maze(size, size)
                path = Solver(maze, (1, len(maze.data) - 2),
                              (len(maze.data[0]) - 2, 1),
                              init=False,
                              heuristic_type=heuristic)

                start = timer()
                path.search()
                end = timer()

                data = path.calculate_data()

                avg_time += round((end - start) * 1000, 2)
                avg_path_length += data[4]
                avg_visited_tiles += round(
                    100 * (data[2] + data[3] + data[4]) /
                    (data[0] + data[2] + data[3] + data[4]), 2)

            avg_time /= iterations
            avg_path_length /= iterations
            avg_visited_tiles /= iterations

            csvwriter.writerow([(size - start_size) / jump + 1, size, avg_time,
                                avg_path_length, avg_visited_tiles])

        print(chr(27) + "[2J")


def make_time_plot(start_size, end_size, iterations):
    folder_name = 'plots'
    create_folder(folder_name)
    file_name = str(start_size) + "-" + str(end_size) + "_" + str(
        iterations) + ".jpg"
    file_name = os.path.join(folder_name, file_name)

    column_names = [
        'iteration', 'size', 'time [ms]', 'path length', 'visited tiles [%]'
    ]

    fig, axs = plt.subplots(nrows=4,
                            ncols=3,
                            tight_layout=True,
                            figsize=(10, 10))
    fig.suptitle(
        'Average time [ms], path length and visited tiles [%] for sqare maze from size '
        + str(start_size) + ' to size ' + str(end_size) + '.')

    for heuristic in range(4):
        data = pd.read_csv('results/' + str(start_size) + '-' + str(end_size) +
                           '_' + str(iterations) + '__' + str(heuristic) +
                           '.csv')

        for i in range(2, 5):
            axs[heuristic][i - 2].plot(data['size'], data[column_names[i]])
            axs[heuristic][i - 2].set_ylabel('average ' + column_names[i],
                                             rotation=90)

    # plt.show()
    plt.savefig(file_name)


def analysis_average_data(start_size=30, end_size=50, iterations=50, jump=1):
    for heuristic in range(4):
        test_size(start_size, end_size, iterations, heuristic, jump)
    make_time_plot(start_size, end_size, iterations)


if __name__ == "__main__":
    random.seed(578)
    # analysis_average_data(20, 50, 50)
    if len(sys.argv) > 4:
        analysis_average_data(int(sys.argv[1]), int(sys.argv[2]),
                              int(sys.argv[3]), int(sys.argv[4]))
    elif len(sys.argv) == 4:
        analysis_average_data(int(sys.argv[1]), int(sys.argv[2]),
                              int(sys.argv[3]))
    elif len(sys.argv) == 3:
        analysis_average_data(int(sys.argv[1]), int(sys.argv[2]))
    else:
        analysis_average_data()
