import numpy as np
import math
from map import Map


class GameState:
    def __init__(self, map: Map, position, character):
        """
        Game state
        :param map: current game map
        :param position: current player position
        :param character: current character
        """
        self.map = map
        self.position = position
        self.character = 'Vampire' if map.role == 0 else 'Werewolf'

    def is_valid_move(self, x, y):
        """
        Check if the move is valid
        :param x, y: (x, y) position
        :return: bool
        """
        flag = True
        if x > self.map.a or x < 0:
            flag = False
        if y > self.map.b or y < 0:
            flag = False
        return flag

    def is_terminal(self):
        """
        Check if the game is over
        :return: bool
        """
        ##
        return True

    def evaluate(self):
        """
        Evaluate the cost
        :return: evaluation
        """
        ## !important
        wh = 0.7  # weight human
        we = 0.3  # weight enemy
        eval = 0
        human_cluster = self.map.GET_INFO().get("h")
        num_human_cluster = human_cluster.shape()[0]
        if self.character == "Vampire":
            enemy_cluster = self.map.GET_INFO().get("v")
            num_enemy_cluster = enemy_cluster.shape()[0]
        elif self.character == "Werewolf":
            enemy_cluster = self.map.GET_INFO().get("w")
            num_enemy_cluster = enemy_cluster.shape()[0]
        for i in range(num_human_cluster):
            ratio = self.map[self.position[0]][self.position[1]] / human_cluster[i]# human number of cluster
            ratio -= 1.5
            distance = np.linalg.norm(self.position, (human_cluster[i][0], human_cluster[i][1]))
            temp = np.abs(1 / np.abs(ratio) + 0.00001)
            eval += wh * temp / distance

        for i in range(num_enemy_cluster):
            ratio = self.map[self.position[0]][self.position[1]] / enemy_cluster[i]# human number of cluster
            ratio -= 1.5
            distance = np.linalg.norm(self.position, (enemy_cluster[i][0], enemy_cluster[i][1]))
            temp = np.abs(1 / np.abs(ratio) + 0.00001)
            eval += we * temp / distance

        return eval


def alpha_beta(state, depth, alpha, beta, maximizing_player):
    """
    α-β剪枝搜索
    :param state: 当前状态
    :param depth: 当前深度
    :param alpha: 当前 α 值
    :param beta: 当前 β 值
    :param maximizing_player: 是否是最大化玩家
    :return: 当前最佳评估值
    """
    if depth == 0 or state.is_terminal():
        return state.evaluate()

    if maximizing_player:
        max_eval = float('-inf')
        for child in state.generate_moves():
            eval = alpha_beta(child, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  # β剪枝
        return max_eval
    else:
        min_eval = float('inf')
        for child in state.generate_moves():
            eval = alpha_beta(child, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break  # α剪枝
        return min_eval


def find_best_move(game_state):
    """
    Find the best move
    :param game_state: current game state
    :return: best move
    """
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, -1), (-1, 1), (1, 1)]
    best_move = None
    # Vampire MAX玩家  Werewolf MIN玩家
    best_eval = float('-inf') if game_state.character == 'Vampire' else float('inf')
    for x, y in directions:
        new_x = game_state.position[0] + x
        new_y = game_state.position[1] + y
        if game_state.is_valid_move(new_x, new_y):
            new_map = game_state.map
            new_map[game_state.position[0]][game_state.position[1]] = 0  # 可能有分裂
            new_map[new_x][new_y] = 2 if game_state.character == 'Vampire' else 3
            new_character = 'Vampire' if new_map.role == 0 else 'Werewolf'
            new_state = GameState(new_map, (new_x, new_y), new_character)
            # depth的设置
            # eval = alpha_beta(new_state, depth=10, alpha=float('-inf'), beta=float('inf'), maximizing_player=(game_state.character == 'Vampire'))
            eval = alpha_beta(new_state, depth=10, alpha=float('-inf'), beta=float('inf'), maximizing_player=True)
            # 若为MAX玩家
            # if game_state.character == 'Vampire' and eval > best_eval:
            #     best_move = (x, y)
            #     best_eval = eval
            # elif game_state.character == 'Werewolf' and eval < best_eval:
            #     best_move = (x, y)
            #     best_eval = eval
            # else:
            #     print('No valid move!')
            #     best_move = (0, 0)
            if eval > best_eval:
                best_eval = eval
                best_move = (x, y)
            else:
                print('No valid move!')
                best_move = (0, 0)
    if best_move is None:
        print('Wrong map!')
    next_x = game_state.position[0] + best_move[0]
    next_y = game_state.position[1] + best_move[1]
    return next_x, next_y
