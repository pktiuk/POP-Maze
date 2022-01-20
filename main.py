#!/usr/bin/python3
from argparse import ArgumentParser

from maze_solver.maze import Maze
from maze_solver.solver import Solver


def parse_args():
    parser = ArgumentParser(description="Labitynth solver")
    parser.add_argument("width", nargs="?", type=int, default=10)
    parser.add_argument("height", nargs="?", type=int, default=10)
    parser.add_argument("-v",
                        "--visualize",
                        action="store_true",
                        dest="visualize")
    return parser.parse_args()


def main():
    args = parse_args()
    m = Maze(args.width, args.height, args.visualize)
    start = (1, len(m.data) - 2)
    end = (len(m.data[0]) - 2, 1)
    solver = Solver(m, start, end)
    print(m)
    print("Press Enter to exit")
    input()


if __name__ == "__main__":
    main()