#!/usr/bin/python3
from argparse import ArgumentParser

from maze_solver.maze import Maze


def parse_args():
    parser = ArgumentParser(description="Labitynth solver")
    parser.add_argument("width", nargs="?", type=int, default=10)
    parser.add_argument("height", nargs="?", type=int, default=10)
    return parser.parse_args()


def main():
    args = parse_args()
    m = Maze(args.width, args.height)
    print(m)


if __name__ == "__main__":
    main()