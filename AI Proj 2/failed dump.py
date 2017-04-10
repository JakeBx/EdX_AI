from BaseAI import BaseAI
from Grid_3 import Grid
from time import clock
import numpy as np

class PlayerAI(BaseAI):
    def __init__(self):
        self.max_depth = int
        #self.idx = {}
        self.snake_index = 0

    def getMove(self, grid):
        timeout = allowance + clock()

        alpha_in = {'score': float("-inf"), 'direction': -1}
        beta_in = {'score': float("inf"), 'direction': -1}
        moves = grid.getAvailableMoves()
        result = {'score': float('-inf'), 'direction': -1}

        empty_tiles = 0
        for row in grid.map:
            empty_tiles += row.count(0)

        # if empty_tiles >= 7:
        #     self.max_depth = 1
        if empty_tiles >= 4:
            self.max_depth = 1
        else:
            self.max_depth = 6

        print(self.max_depth)

        for move in moves:
            new_grid = grid.clone()
            new_grid.move(move)
            move_score = self.max(new_grid, self.max_depth, alpha_in, beta_in, move, timeout)

            if move_score['score'] > result['score']:
                result = move_score
                result['direction'] = move

        self.snake_index = result['snake']

        return result['direction']

    def mini(self, grid, depth, alpha, beta, last_move, timeout):
        if clock() > timeout:
            return {'score': float("inf"), 'direction': -1}
        if depth == 0:
            score, which_snake = self.get_heuristic(grid)
            return {'score': score, 'direction': last_move, 'snake': which_snake}

        if not grid.canMove():
            score, which_snake = self.get_heuristic(grid)
            return {'score': score, 'direction': last_move, 'snake': which_snake}

        score_dir = {'score': float("inf"), 'direction': -1, 'snake': -1}

        inserts = grid.getAvailableCells()

        for available in inserts:
            new_grid = grid.clone()
            new_grid.insertTile(available, 2)  # just assuming new tile is a two, may be a 4

            alt = self.max(new_grid, depth - 1, alpha, beta, last_move, timeout)
            # print("min", score_dir, alt)
            # print(score_dir['score'], alt['score'])
            score_dir = min(score_dir, alt, key=lambda x: x['score'])  # returns the smaller value from tge max selection or the move
            # update beta
            if score_dir['score'] <= alpha['score']:
                return score_dir
            if beta['score'] > score_dir['score']:
                beta = score_dir


        return score_dir

    def max(self, grid, depth, alpha, beta, last_move, timeout):
        if clock() > timeout:
            return {'score': float("-inf"), 'direction': -1}
        if depth == 0:
            score, which_snake = self.get_heuristic(grid)
            return {'score': score, 'direction': last_move, 'snake': which_snake}

        if not grid.canMove():
            score, which_snake = self.get_heuristic(grid)
            return {'score': score, 'direction': last_move, 'snake': which_snake}

        score_dir = {'score': float("-inf"), 'direction': -1, 'snake': -1}

        moves = grid.getAvailableMoves()  # TODO: break this out cells and inserts for min, moves and moves for max

        for move in moves:
            new_grid = grid.clone()
            new_grid.move(move)  # just assuming new tile is a two, may be a 4
            alt = self.mini(new_grid, depth - 1, alpha, beta, move, timeout)
            # print("max", score_dir, alt)
            # print(score_dir['score'], alt['score'])
            score_dir = max(score_dir, alt, key=lambda x: x['score'])  # returns the smaller value from the max selection or the move
            # update alpha
            if score_dir['score'] >= beta['score']:
                return score_dir
            if alpha['score'] < score_dir['score']:
                alpha = score_dir


        return score_dir


    def get_heuristic_long(self, grid):
        # grid_id = id(grid.map)
        # if grid_id in self.idx:
        #     return self.idx[grid_id]

        score = 0
        for y, snake in enumerate(snake_weights):
            which_snake = 0
            empty_count = 0
            snake_score = 0
            for i, row in enumerate(grid.map):
                snake_row = snake[i]
                for j in range(grid.size):
                    element = row[j]
                    snake_score += element * snake_row[j]
                    if element == 0:
                        empty_count += 1
                    if element == 2048:
                        snake_score += 100

            if empty_count == 0:
                snake_score -= 200

            if snake_score > score:
                score = snake_score
                which_snake = y

        # self.idx[grid_id] = score

        return score, which_snake


    def get_heuristic_short(self, grid):
        grid_id = id(grid.map)
        # if grid_id in self.idx:
        #     return self.idx[grid_id]

        # empty_count = 0
        snake_score = 0
        for each, row in enumerate(grid.map):
            snake_row = snake_weights[self.snake_index][each]
            for j in range(grid.size):
                element = row[j]
                snake_score += element * snake_row[j]
                # if element == 0:
                #     empty_count += 1
                # if element == 2048:
                #     snake_score += 100

        # if empty_count == 0:
        #     snake_score -= 200


        # self.idx[grid_id] = score

        return snake_score

    def get_heuristic(self, grid):
        if self.max_depth == 1:
            return self.get_heuristic_long(grid)
        else:
            return self.get_heuristic_short(grid), self.snake_index


snake_path_first = np.array([[15, 8, 7, 0],
                             [14, 9, 6, 1],
                             [13, 10, 5, 2],
                             [12, 11, 4, 3]])
snake_path = []
np.array(snake_path)
snake_path.append(np.flipud(np.fliplr(snake_path_first)))
snake_path.append(snake_path_first.T)

allowance = 0.08

snake_weights = []
for snake in snake_path:
    snake_weights.append([[pow(0.25, y) for y in x] for x in snake])

# print(snake_weights)


#
# if __name__ == '__main__':
#     snake_path_first = np.array([[15, 8, 7, 0],
#                                  [14, 9, 6, 1],
#                                  [13, 10, 5, 2],
#                                  [12, 11, 4, 3]])
#     print(snake_path)
#     snake_path = []
#     np.array(snake_path)
#     snake_path.append(np.fliplr(snake_path_first))
#     snake_path.append(snake_path_first.T)
#     print(snake_path)
#     snake_path_first = np.array([[15,  8,  7,  0],
#        [14,  9,  6,  1],
#        [13, 10,  5,  2],
#        [12, 11,  4,  3]])
#     snake_path = []
#     np.array(snake_path)
#     snake_path.append(snake_path_first)
#     snake_path.append(snake_path_first.T)
#     snake_path.append(np.fliplr(snake_path_first))
#     snake_path.append(np.fliplr(snake_path_first.T))
#     snake_path.append(np.flipud(snake_path_first))
#     snake_path.append(np.flipud(snake_path_first.T))
#     snake_path.append(np.flipud(np.fliplr(snake_path_first)))
#     snake_path.append(np.flipud(np.fliplr(snake_path_first.T)))
#     print(snake_path)
#     test = Grid()
#     test.map = [[0, 0, 4, 2],[4, 4, 0, 0],[0, 4, 2, 0],[0, 8, 0, 2]]
#     goon = PlayerAI()
#     alpha = {'score': float("-inf"), 'direction': -1}
#     beta = {'score': float("inf"), 'direction': -1}
#     temp = goon.search(test)
#     print(temp)





# 1. Build minimax search tree (AB pruning)
# 2. Calc heuristic at terminal nodes
#         2a. tuning of parameters for heuristic
# 3. Enforce time limit at 0.1s