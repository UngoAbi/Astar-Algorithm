from math import inf as infinity
from collections.abc import Generator
from enum import Enum
import pygame
from consts import *


class NodeType(Enum):
    DEFAULT = pygame.transform.scale(pygame.image.load("../assets/graphics/default.png"), (NODE_SIZE, NODE_SIZE))
    WALL = pygame.transform.scale(pygame.image.load("../assets/graphics/wall.png"), (NODE_SIZE, NODE_SIZE))
    START = pygame.transform.scale(pygame.image.load("../assets/graphics/start.png"), (NODE_SIZE, NODE_SIZE))
    TARGET = pygame.transform.scale(pygame.image.load("../assets/graphics/target.png"), (NODE_SIZE, NODE_SIZE))
    OPEN = pygame.transform.scale(pygame.image.load("../assets/graphics/open.png"), (NODE_SIZE, NODE_SIZE))
    CLOSED = pygame.transform.scale(pygame.image.load("../assets/graphics/closed.png"), (NODE_SIZE, NODE_SIZE))
    PATH = pygame.transform.scale(pygame.image.load("../assets/graphics/path.png"), (NODE_SIZE, NODE_SIZE))


class Node:
    def __init__(self, position: tuple[int, int], node_type: NodeType = NodeType.DEFAULT) -> None:
        self.position = position
        self.x, self.y = position
        self.type = node_type
        self.rect = pygame.Rect((self.x * NODE_SIZE, self.y * NODE_SIZE), (NODE_SIZE, NODE_SIZE))

        self.parent = None      # where the node originates from
        self.g_cost = 0         # distance from the start node
        self.h_cost = infinity  # distance from the target node
        self.f_cost = infinity  # g_cost + h_cost


class Grid:
    def __init__(self) -> None:
        self.rows = ROWS
        self.columns = COLUMNS
        self.matrix = [[Node((x, y), NodeType.DEFAULT) for x in range(COLUMNS)] for y in range(ROWS)]
        self.start_node = self.matrix[START_NODE_Y][START_NODE_X]
        self.start_node.type = NodeType.START
        self.target_node = self.matrix[TARGET_NODE_Y][TARGET_NODE_X]
        self.target_node.type = NodeType.TARGET

        self.open = set()
        self.closed = set()
        self.current = None

        self.path = list()
        self.run = False

    def get_clicked_cell(self, mouse_pos: tuple[int, int]) -> Node | None:
        for row in self.matrix:
            for cell in row:
                if cell.rect.collidepoint(*mouse_pos):
                    return cell

    def set_current_node(self) -> None:
        self.current = next(iter(self.open))
        for node in self.open:
            if node.f_cost < self.current.f_cost or (node.f_cost == self.current.f_cost and node.h_cost < self.current.h_cost):
                self.current = node

    def get_neighbors(self, node: Node) -> Generator[Node]:
        x, y = node.position
        if CAN_GO_DIAGONAL:
            off_sets = ((-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1))
        else:
            off_sets = ((0, -1), (-1, 0), (1, 0), (0, 1))

        for new_x, new_y in off_sets:
            new_x += x
            new_y += y
            if is_in_bounds((new_x, new_y)):
                yield self.matrix[new_y][new_x]

    def find_path(self) -> None:
        if self.current is None:
            self.open.add(self.start_node)

        self.set_current_node()
        self.open.remove(self.current)
        self.add_to_closed(self.current)

        if self.current == self.target_node:
            self.add_node_and_parent_to_path(self.current)
            return

        for neighbor in self.get_neighbors(self.current):
            if neighbor.type == NodeType.WALL or neighbor in self.closed:
                continue

            new_cost = self.current.g_cost + get_distance(self.current.position, neighbor.position)
            if new_cost < neighbor.g_cost or neighbor not in self.open:
                neighbor.g_cost = new_cost
                neighbor.h_cost = get_distance(neighbor.position, self.target_node.position)
                neighbor.f_cost = neighbor.g_cost + neighbor.h_cost
                neighbor.parent = self.current
                if neighbor not in self.open:
                    self.add_to_open(neighbor)

    def add_node_and_parent_to_path(self, node: Node) -> None:
        if node.parent:
            self.path.append(node)
            self.add_node_and_parent_to_path(node.parent)

    def reveal_path(self) -> None:
        node = self.path.pop()
        if node.type not in [NodeType.START, NodeType.TARGET]:
            node.type = NodeType.PATH

        if node.type == NodeType.TARGET:
            self.run = None

    def add_to_open(self, node: Node) -> None:
        if node.type not in [NodeType.START, NodeType.TARGET]:
            node.type = NodeType.OPEN
        self.open.add(node)

    def add_to_closed(self, node: Node) -> None:
        if node.type not in [NodeType.START, NodeType.TARGET]:
            node.type = NodeType.CLOSED
        self.closed.add(node)

    def reset(self) -> None:
        self.rows = ROWS
        self.columns = COLUMNS
        self.matrix = [[Node((x, y), NodeType.DEFAULT) for x in range(COLUMNS)] for y in range(ROWS)]
        self.start_node = self.matrix[START_NODE_Y][START_NODE_X]
        self.start_node.type = NodeType.START
        self.target_node = self.matrix[TARGET_NODE_Y][TARGET_NODE_X]
        self.target_node.type = NodeType.TARGET

        self.open = set()
        self.closed = set()
        self.current = None

        self.path = list()
        self.run = False


def is_in_bounds(position: tuple[int, int]) -> bool:
    x, y = position
    return 0 <= x < COLUMNS and 0 <= y < ROWS


def get_distance(pos_1: tuple[int, int], pos_2: tuple[int, int]) -> int:
    x1, y1 = pos_1
    x2, y2 = pos_2
    delta_x = abs(x1 - x2)
    delta_y = abs(y1 - y2)
    if delta_x > delta_y:
        return 14 * delta_y + 10 * (delta_x - delta_y)
    return 14 * delta_x + 10 * (delta_y - delta_x)
