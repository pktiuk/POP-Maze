import enum, time, math, random, sys
from os import environ
from collections import Counter

from anytree import AnyNode

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

import __future__

# Randomized Kruskal's algorithm implementation


class TileType(enum.IntEnum):
    EMPTY = 0
    WALL = 1
    CHECKED = 2
    CURRENT = 3
    FINAL_PATH = 4


class Maze:
    def __init__(self, width, height, visualisation=False, init=True):
        self.h = int(
            height / 2
        )  # size of walkable tiles is two times smaller, because of edge spacing
        self.w = int(width / 2)
        if visualisation:
            self.visual = MazeVisualizer(height + 1, width + 1)
        else:
            self.visual = None

        self.nodes = self.__create_nodes(
        )  # generate tree nodes for every walkable tile
        self.edges = self.__create_edges()  # generate edges of nodes
        if init:
            self.generate()  # generate maze data
        else:
            self._fill_zeroes()

        self.current_tile = None

    def __str__(self):
        result = ""
        for y in range(len(self.data)):
            for x in range(len(self.data[0])):
                if self.data[y][x] == TileType.WALL:
                    result += "X"
                elif self.data[y][x] == TileType.EMPTY:
                    result += " "
                elif self.data[y][x] == TileType.CHECKED:
                    result += "."
                elif self.data[y][x] == TileType.FINAL_PATH:
                    result += "+"
                else:
                    result += "?"
            result += "\n"
        return result

    def __create_nodes(self):
        nodes = []
        for i in range(self.h):
            for j in range(self.w):
                nodes.append(AnyNode(
                    id=i * self.w +
                    j))  # id is assigned numerically: 0,1,2,3,..., n*m - 1
        return nodes

    def __create_edges(self):
        edges = []
        for i in range(self.h):
            for j in range(self.w):
                if j != self.w - 1:
                    edges.append(
                        (i * self.w + j, i * self.w + j + 1))  # vertical edge
                if i != self.h - 1:
                    edges.append((i * self.w + j,
                                  (i + 1) * self.w + j))  # horizontal edge
        # random.shuffle(edges) # randomized list of edges
        return edges

    # maze generation
    def generate(self):
        self.__zero()

        edges_temp = self.edges.copy(
        )  # copy edge list - edges are popped from list so we have to copy it to have it saved
        random.shuffle(edges_temp)
        while (edges_temp):

            id_1 = edges_temp[-1][0]  # id of first node
            id_2 = edges_temp[-1][1]  # id of second node
            node_1 = next(x for x in self.nodes
                          if x.id == id_1)  # search for first node variable
            node_2 = next(x for x in self.nodes
                          if x.id == id_2)  # search for second node variable

            if not node_1.is_root:
                node_1 = node_1.ancestors[0]  # root of first node
            if not node_2.is_root:
                node_2 = node_2.ancestors[0]  # root of second node
            if node_1.id == node_2.id:  # check if nodes are in same tree
                x, y = self.__get_cords(id_1, id_2)
                self.set_wall(x + 1, y +
                              1)  # nodes are connected, so we save this edge
            else:  # nodes are not connected, because we assigned 0 values before we do not change any maze value
                temp = list(node_1.children)  # save first node children
                temp.append(node_2)  # add second node as first node's child
                node_1.children = temp
            edges_temp.pop()  # remove checked edge

        for i in range(2 * self.h + 1):  # fill bouding box and corners
            for j in range(2 * self.w + 1):
                if i == 0 or i == 2 * self.h or j == 0 or j == 2 * self.w or (
                        i % 2 == 0 and j % 2 == 0):
                    self.set_wall(j, i)

    def _fill_zeroes(self):
        self.data = [[0] * (2 * self.w + 1) for x in range(2 * self.h + 1)
                     ]  # generate maze array with zeros

    def _set_tile(self, x, y, type: TileType):
        self.data[y][x] = type
        if self.visual is not None:
            self.visual.draw_cell(x, y, self.visual.TILE_COLORS.get(type),
                                  0.01)

    def get_tile(self, x, y) -> TileType:
        return self.data[y][x]

    def set_wall(self, x, y):
        self._set_tile(x, y, TileType.WALL)

    def set_empty(self, x, y):
        self._set_tile(x, y, TileType.EMPTY)

    def set_checked(self, x, y):
        self._set_tile(x, y, TileType.CHECKED)

    def set_path(self, x, y):
        self._set_tile(x, y, TileType.FINAL_PATH)

    def set_current(self, x, y):
        if self.current_tile is not None:
            prev_x, prev_y = self.current_tile
            self.set_checked(prev_x, prev_y)
        self._set_tile(x, y, TileType.CURRENT)
        self.current_tile = (x, y)

    # finding cordinates of edge between two nodes in maze array
    def __get_cords(self, id_1, id_2):
        if id_2 - id_1 == 1:  # vertical edge
            x = (id_1 % self.w) * 2 + 1
            y = int(id_1 / self.w) * 2
        else:  # horizontal edge
            x = (id_1 % self.w) * 2
            y = int(id_1 / self.w) * 2 + 1
        return x, y

    def show(self):
        if self.visual is not None:
            self.visual.show(self.data)
        else:
            self.visual = MazeVisualizer(2 * self.h + 1, 2 * self.w + 1)
            self.visual.show(self.data)

    def __zero(self):
        self._fill_zeroes()
        for i in range(self.h):
            for j in range(self.w):
                self.nodes[i * self.w + j].parent = None

    # restarts labirynth state (useful for trying different solvers)
    def restart(self):
        for y in range(self.h):
            for x in range(self.w):
                self.nodes[x * self.w + y].parent = None
                if self.data[y][x] != TileType.WALL:
                    self.data[y][x] = TileType.EMPTY

    def get_tiles_count(self, tile_type: TileType = TileType.CHECKED):
        l = [cell for row in self.data for cell in row]
        return Counter(l)[tile_type]


class MazeVisualizer:
    LIGHT_GRAY = (224, 224, 224)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    WIDTH = 800
    HEIGHT = 800

    TILE_COLORS = {
        TileType.WALL: BLACK,
        TileType.CHECKED: GREEN,
        TileType.CURRENT: RED,
        TileType.FINAL_PATH: BLUE,
    }

    def __init__(self, n, m, title="maze"):
        self.n = self.HEIGHT / n
        self.m = self.WIDTH / m
        if self.m < self.n:
            self.n = self.m
        self.padding = (self.HEIGHT - self.n * n) / 2
        self.display = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.display.fill(self.LIGHT_GRAY)
        pygame.display.set_caption(title)

    def draw_cell(self, x, y, color=None, delay=0, update=True):
        x = x * self.m
        y = self.padding + (y * self.n)
        w = self.m
        h = self.n
        if not w.is_integer():
            w = math.ceil(w)
        if not h.is_integer():
            h = math.ceil(h)
        if color is None:
            color = self.LIGHT_GRAY
        pygame.draw.rect(self.display, color, pygame.Rect(x, y, w, h))
        if update:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()
        if delay != 0:
            time.sleep(delay)

    def show(self, data):
        self.display.fill(self.LIGHT_GRAY)
        for i in range(len(data)):
            for j in range(len(data[i])):
                self.draw_cell(j, i, self.TILE_COLORS.get(data[i][j]), 0,
                               False)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                break