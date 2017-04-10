# Jake's code
# Attempt 2

# import, initialize method
import os
import argparse
from copy import copy
from collections import deque
from heapq import heappop, heappush
from time import time
try:
    import resource
    def mem():
        return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024
except:
    def mem():
        return 0

End = [0, 1, 2, 3, 4, 5, 6, 7, 8]

class Node:
    move_priority = ['Up', 'Down', 'Left', 'Right']

    def __init__(self, start_board):
        self.Tiles = start_board
        self.Previous = None
        self.PrevMove = ''
        self.Depth = 0
        self.Key = self.reference()
        self.Last = ''

    # methods for node
    # def hasher :
    # TODO

    # returns heuristic score for board
    def calc_heur(self):
        dist = 0
        for goal_pos, tile in enumerate(self.Tiles):
            if tile != 0:
                # How distant is each tile from correct position.
                dist += abs(tile // 3 - goal_pos // 3)  # rows
                dist += abs(tile % 3 - goal_pos % 3)  # columns
        return dist

    def solved(self):
        return self.Tiles == End

    def swap(self, row1, col1, row2, col2):
        stored = self.get(row1, col1)
        self.put(row1, col1, self.get(row2, col2))
        self.put(row2, col2, stored)

    def empty(self):
        empty_index = self.Tiles.index(0)
        return (empty_index // 3, empty_index % 3)

    def pos_moves(self):
        moves = []
        empty_row, empty_col = self.empty()
        if empty_row > 0:
            moves.append('Up')
        if empty_row < 2:
            moves.append('Down')
        if empty_col > 0:
            moves.append('Left')
        if empty_col < 2:
            moves.append('Right')
        return moves

    def move(self, direction):
        empty_row, empty_col = self.empty()
        if direction == 'Up':
            swap_row, swap_col = (empty_row - 1, empty_col)
        elif direction == 'Down':
            swap_row, swap_col = (empty_row + 1, empty_col)
        elif direction == 'Left':
            swap_row, swap_col = (empty_row, empty_col - 1)
        elif direction == 'Right':
            swap_row, swap_col = (empty_row, empty_col + 1)
        self.swap(empty_row, empty_col, swap_row, swap_col)
        self.Last = direction
        self.Key = self.reference()

    def new_child(self):
        new_inst = copy(self)
        new_inst.Tiles = self.Tiles[:]
        new_inst.Previous = self
        new_inst.Depth = self.Depth + 1
        new_inst.Key = self.reference()
        return new_inst

    def path_to_goal(self):
        node = self
        path = []
        while node.Previous:
            path.append(node.Last)
            node = node.Previous
        path.reverse()
        return path

    def get(self, row, col):
        return self.Tiles[row * 3 + col]

    def put(self, row, col, value):
        self.Tiles[row * 3 + col] = value

    def reference(self):
        i = 0
        for value in self.Tiles:
            i = i * 10 + value
        return i

    def priority_tuple(self):
        if self.Previous:
            tie_breaker = (str(self.move_priority.index(self.Last) + 1) + '-' +
                           str(self.Previous.Key))
        else:
            tie_breaker = 'Root'
        return (self.Depth + self.calc_heur(), tie_breaker, self.Key)


# In[ ]:

# dfs/bf solver function


# In[ ]:
def bfs(board):
    root = Node(board)
    frontier_nodes = deque()
    frontier_nodes.append(root)
    explored_keys = set()
    frontier_keys = set()
    frontier_keys.add(copy(root.Key))
    start_time = time()
    nodes_expanded = 0
    max_depth = root.Depth
    max_f_size = 0

    while frontier_nodes:

        fringe_size = len(frontier_keys)
        if fringe_size > max_f_size:
            max_f_size = fringe_size

        
        current = frontier_nodes.popleft()
        frontier_keys.remove(current.Key)

        explored_keys.add(copy(current.Key))  # refacotor into the above methods with a pop of frontier keys

        if current.solved():
            fringe_size = len(frontier_keys)
            end_time = time()
            total_time = end_time - start_time
            return True, current, fringe_size, max_f_size, nodes_expanded, max_depth, total_time

        possible_moves = current.pos_moves()

        nodes_expanded += 1

        for this in possible_moves:
            new_node = current.new_child()
            new_node.move(this)
            if new_node.Key not in explored_keys:
                if new_node.Key not in frontier_keys:
                    frontier_nodes.append(new_node)
                    frontier_keys.add(new_node.Key)
                    if new_node.Depth > max_depth:
                        max_depth = new_node.Depth

    return False, count


def dfs(board):
    root = Node(board)
    frontier_nodes = deque()
    frontier_nodes.append(root)
    explored_keys = set()
    frontier_keys = set()
    frontier_keys.add(copy(root.Key))
    start_time = time()
    nodes_expanded = 0
    max_depth = root.Depth
    max_f_size = 0

    while frontier_nodes:

        fringe_size = len(frontier_keys)
        if fringe_size > max_f_size:
            max_f_size = fringe_size

        current = frontier_nodes.pop()
        frontier_keys.remove(current.Key)

        explored_keys.add(copy(current.Key))  # refacotor into the above methods with a pop of frontier keys

        if current.solved():
            fringe_size = len(frontier_keys)
            end_time = time()
            total_time = end_time - start_time
            return True, current, fringe_size, max_f_size, nodes_expanded, max_depth, total_time

        possible_moves = current.pos_moves()
        possible_moves.reverse()

        nodes_expanded += 1

        for this in possible_moves:
            new_node = current.new_child()
            new_node.move(this)
            if new_node.Key not in explored_keys:
                if new_node.Key not in frontier_keys:
                    frontier_nodes.append(new_node)
                    frontier_keys.add(new_node.Key)
                    if new_node.Depth > max_depth:
                        max_depth = new_node.Depth

    return False


def astar(board):
    root = Node(board)
    frontier_nodes = {}
    frontier_nodes[root.Key] = root
    explored_keys = set()
    frontier_keys = set()
    cancelled_idx = set()
    frontier_keys.add(root.Key)
    nodes_order = []
    heappush(nodes_order, root.priority_tuple())
    start_time = time()
    nodes_expanded = 0
    max_depth = root.Depth
    max_f_size = 0

    while frontier_keys:

        fringe_size = len(frontier_keys)
        if fringe_size > max_f_size:
            max_f_size = fringe_size

        heuristic_cost, tie_breaker, key = heappop(nodes_order)

        if (key, heuristic_cost) in cancelled_idx:
            cancelled_idx.remove((key, heuristic_cost))
            continue

        current = frontier_nodes[key]
        explored_keys.add(key)
        frontier_keys.remove(key)  # change to pop

        if current.solved():
            fringe_size = len(frontier_keys)
            end_time = time()
            total_time = end_time - start_time
            return True, current, fringe_size, max_f_size, nodes_expanded, max_depth, total_time

        possible_moves = current.pos_moves()
        nodes_expanded += 1

        for this in possible_moves:
            new_node = current.new_child()
            new_node.move(this)
            new_key = new_node.Key
            if new_key not in explored_keys:
                if new_key not in frontier_keys:
                    heappush(nodes_order, new_node.priority_tuple())
                    frontier_nodes[new_key] = new_node
                    frontier_keys.add(new_key)
                    if new_node.Depth > max_depth:
                        max_depth = new_node.Depth
                else:
                    new_heur_score = new_node.Depth + new_node.calc_heur()
                    exists_node = frontier_nodes[new_key]
                    exists_heur_score = exists_node.Depth + exists_node.calc_heur()
                    if new_heur_score < exists_heur_score:
                        cancelled_idx.add((new_key, exists_heur_score))
                        heappush(nodes_order, new_node.priority_tuple())
                        frontier_nodes[new_key] = new_node
                        if new_node.Depth > max_depth:
                            max_depth = new_node.Depth


def ida(board):
    start_time = time()
    max_depth = 0
    max_f_size = 0
    threshold = 0

    while True:

        root = Node(board)
        nodes_expanded = 0

        frontier_nodes = {}
        frontier_nodes[root.Key] = root
        explored_keys = set()
        frontier_keys = set()
        cancelled_idx = set()
        frontier_keys.add(root.Key)
        nodes_order = []
        heappush(nodes_order, root.priority_tuple())

        threshold += 1

        while frontier_keys:

            fringe_size = len(frontier_keys)
            if fringe_size > max_f_size:
                max_f_size = fringe_size

            heuristic_cost, tie_breaker, key = heappop(nodes_order)

            if (key, heuristic_cost) in cancelled_idx:
                cancelled_idx.remove((key, heuristic_cost))
                continue

            current = frontier_nodes[key]
            explored_keys.add(key)
            frontier_keys.remove(key)  # change to pop

            if current.solved():
                fringe_size = len(frontier_keys)
                end_time = time()
                total_time = end_time - start_time
                return True, current, fringe_size, max_f_size, nodes_expanded, max_depth, total_time

            possible_moves = current.pos_moves()
            nodes_expanded += 1

            for this in possible_moves:
                new_node = current.new_child()
                new_node.move(this)
                new_key = new_node.Key
                new_heur_score = new_node.Depth + new_node.calc_heur()
                if new_key not in explored_keys and new_heur_score < threshold:  # change in function from ast
                    if new_key not in frontier_keys:
                        heappush(nodes_order, new_node.priority_tuple())
                        frontier_nodes[new_key] = new_node
                        frontier_keys.add(new_key)
                        if new_node.Depth > max_depth:
                            max_depth = new_node.Depth
                    else:
                        exists_node = frontier_nodes[new_key]
                        exists_heur_score = exists_node.Depth + exists_node.calc_heur()

                        if new_heur_score < exists_heur_score:
                            cancelled_idx.add((new_key, exists_heur_score))
                            heappush(nodes_order, new_node.priority_tuple())
                            frontier_nodes[new_key] = new_node
                            if new_node.Depth > max_depth:
                                max_search_depth = new_node.Depth


file_name = 'output.txt'


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('method', choices=['bfs', 'dfs', 'ast', 'ida'])
    parser.add_argument('tiles')
    args = parser.parse_args()

    if args and args.method and args.tiles:
        tiles_list = [int(x) for x in args.tiles.split(",")]
        if args.method == 'ast':
            (result, node, fringe_size,
             max_fringe_size, nodes_expanded,
             max_search_depth, running_time) = astar(tiles_list)
        elif args.method == 'ida':
            (result, node, fringe_size,
             max_fringe_size, nodes_expanded,
             max_search_depth, running_time) = ida(tiles_list)
        elif args.method == 'dfs':
            (result, node, fringe_size,
             max_fringe_size, nodes_expanded,
             max_search_depth, running_time) = dfs(tiles_list)
        else:
            (result, node, fringe_size,
             max_fringe_size, nodes_expanded,
             max_search_depth, running_time) = bfs(tiles_list)

        if result:

            with open(file_name, "w") as fo:
                fo.write("path_to_goal: {}\n".format(node.path_to_goal()))
                fo.write("cost_of_path: {}\n".format(node.Depth))
                fo.write("nodes_expanded: {}\n".format(nodes_expanded))
                fo.write("fringe_size: {}\n".format(fringe_size))
                fo.write("max_fringe_size: {}\n".format(max_fringe_size))
                fo.write("search_depth: {}\n".format(node.Depth))
                fo.write("max_search_depth: {}\n".format(max_search_depth))
                fo.write("running_time: {}\n".format(round(running_time, 8)))
                fo.write("max_ram_usage: {}\n".format(round(mem(), 8)))
            #
            with open(file_name, "r") as f:
                print(f.read(), end="")

        else:
            print("-1")



# main('ida','1,2,5,3,4,8,0,6,7')
# print(dfsbfs([1,2,5,3,4,8,0,6,7],'bfs'))
# print(ida([1,2,5,3,4,8,0,6,7]))
#
# (result, node, fringe_size,
#          max_fringe_size, nodes_expanded,
#          max_search_depth, running_time) = astar([1,2,5,3,4,8,0,6,7])
#
# print("path_to_goal: {}\n".format(node.path_to_goal()))
# print("cost_of_path: {}\n".format(node.Depth))
# print("nodes_expanded: {}\n".format(nodes_expanded))
# print("fringe_size: {}\n".format(fringe_size))
# print("max_fringe_size: {}\n".format(max_fringe_size))
# print("search_depth: {}\n".format(node.Depth))
# print("max_search_depth: {}\n".format(max_search_depth))
# print("running_time: {}\n".format(round(running_time,8)))
# print("max_ram_usage: {}\n".format(round(memory_usage(),8)))
