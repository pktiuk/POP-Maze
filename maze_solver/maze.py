import random

from anytree import AnyNode

# Randomized Kruskal's algorithm implementation
# https://en.wikipedia.org/wiki/Kruskal's_algorithm


class Maze:
    def __init__(self, height, width, visualisation=False, init=True):
        self.h = int(
            height / 2
        )  # size of walkable tiles is two times smaller, because of edge spacing
        self.w = int(width / 2)

        self.nodes = self.__create_nodes(
        )  # generate tree nodes for every walkable tile
        self.edges = self.__create_edges()  # generate edges of nodes
        if init:
            self.generate()  # generate maze data
        else:
            self.data = []

    def __str__(self):
        #TODO fix orientation
        result = ""
        for line in self.data:
            for pixel in line:
                if pixel:
                    result += "X"
                else:
                    result += " "
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
        self.data = [[0] * (2 * self.w + 1) for x in range(2 * self.h + 1)
                     ]  # generate maze array with zeros

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
                x, y = self.__getCords(id_1, id_2)
                self.data[y + 1][
                    x + 1] = 1  # nodes are connected, so we save this edge
            else:  # nodes are not connected, because we assigned 0 values before we do not change any maze value
                temp = list(node_1.children)  # save first node children
                temp.append(node_2)  # add second node as first node's child
                node_1.children = temp
            edges_temp.pop()  # remove checked edge

        for i in range(2 * self.h + 1):  # fill bouding box and corners
            for j in range(2 * self.w + 1):
                if i == 0 or i == 2 * self.h or j == 0 or j == 2 * self.w or (
                        i % 2 == 0 and j % 2 == 0):
                    self.data[i][j] = 1

    # finding cordinates of edge between two nodes in maze array
    def __getCords(self, id_1, id_2):
        if id_2 - id_1 == 1:  # vertical edge
            x = (id_1 % self.w) * 2 + 1
            y = int(id_1 / self.w) * 2
        else:  # horizontal edge
            x = (id_1 % self.w) * 2
            y = int(id_1 / self.w) * 2 + 1
        return x, y

    def clean_nodes(self):
        for i in range(self.h):
            for j in range(self.w):
                self.nodes[i * self.w + j].parent = None
