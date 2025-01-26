import copy

import numpy as np
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
        if x >= self.map.a or x < 0:
            flag = False
        if y >= self.map.b or y < 0:
            flag = False
        return flag

    def generate_moves(self):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, -1), (-1, 1), (1, 1)]
        next_states = []
        (current_species, current_num, _) = self.map[self.position[0], self.position[1]]
        attacker_species = 2 if self.character == 'Vampire' else 3
        for x, y in directions:
            new_x = self.position[0] + x
            new_y = self.position[1] + y
            if self.is_valid_move(new_x, new_y):
                (target_species, target_num, _) = self.map[new_x, new_y]
                new_map = copy.deepcopy(self.map)
                new_map[self.position[0], self.position[1]] = list([0, 0, 0])
                if target_species == 0:
                    new_map[new_x, new_y] = list([current_species, current_num, 0])
                else:
                    E1 = current_num  # attackers' number
                    E2 = target_num   # defenders' number
                    if E1 == E2:
                        P = 0.5
                    elif E1 < E2:
                        P = E1/(2*E2)
                    else:
                        P = (E1/E2) - 0.5

                    if target_species == 1:   # human
                        attacker_win_num = round((E1 + E2) * P)
                        defender_win_num = 0
                        attacker_lose_num = 0
                        defender_lose_num = round(E2 * (1 - P))

                        # 最终期望攻击者 = attacker_win_num + 0*(1-P) = (E1+E2)*P
                        final_attacker = attacker_win_num
                        # 最终期望防守者 = 0*P + E2*(1-P)*(1) = E2*(1-P)
                        final_defender = defender_lose_num

                        # 比较大小决定归属
                        if final_attacker > final_defender:
                            # 归攻击者种族
                            final_num = final_attacker - final_defender
                            if final_num > 0:
                                new_map[new_x, new_y] = list([attacker_species, final_num, 0])
                        else:
                            # 归人类
                            final_num = final_defender - final_attacker
                            if final_num > 0:
                                new_map[new_x, new_y] = list([1, final_num, 0])
                    else:
                        attacker_win_num = round(E1*P)
                        defender_win_num = 0
                        attacker_lose_num = 0
                        defender_lose_num = round(E2*(1-P))

                        final_attacker = attacker_win_num
                        final_defender = defender_lose_num

                        if final_attacker > final_defender:
                            new_map[new_x, new_y] = list([attacker_species, final_attacker - final_defender, 0])
                        elif final_attacker < final_defender:
                            new_map[new_x, new_y] = list([target_species, final_defender - final_attacker, 0])

                new_character = 'Vampire' if self.map.role == 0 else 'Werewolf'
                next_states.append(GameState(new_map, (new_x, new_y), new_character))

        return next_states



    def evaluate(self, previous_num_human_cluster):
        """
        Evaluate the cost
        :return: evaluation
        """
        ## !important
        wh = 10  # weight human
        we = 5  # weight enemy
        human_cluster = self.map.GET_INFO().get("h")
        num_human_cluster = len(human_cluster)
        if self.character == "Vampire":
            enemy_cluster = self.map.GET_INFO().get("w")
        else:
            enemy_cluster = self.map.GET_INFO().get("v")
        num_enemy_cluster = len(enemy_cluster)

        max_human = 0
        max_enemy = 0
        for i in range(num_human_cluster):
            difference_human = self.map[self.position[0], self.position[1]][1] - human_cluster[i][2]
            distance_human = np.linalg.norm(
                np.array(self.position) - np.array((human_cluster[i][0], human_cluster[i][1])))
            if difference_human > 0:
                if num_human_cluster < previous_num_human_cluster:
                    temp = np.inf
                else:
                    temp = wh / distance_human
                if max_human < temp:
                    max_human = temp

        distance_enemy = 0
        for i in range(num_enemy_cluster):
            difference_enemy = self.map[self.position[0], self.position[1]][1] - enemy_cluster[i][2]
            distance_enemy = np.linalg.norm(
                np.array(self.position) - np.array((enemy_cluster[i][0], enemy_cluster[i][1])))
            if difference_enemy > 0:
                if distance_enemy == 0:
                    temp = np.inf
                else:
                    temp = we / distance_enemy
                if max_enemy < temp:
                    max_enemy = temp
        eval = max(max_human, max_enemy)
        if eval == 0:
            for i in range(num_human_cluster):
                distance_human = np.linalg.norm(
                    np.array(self.position) - np.array((human_cluster[i][0], human_cluster[i][1])))
                if distance_human < 2:
                    eval -= np.inf
            eval += we / (distance_enemy + 0.01)

        return eval


    def evaluate_alphabeta(self):
        """
        Evaluate the cost
        :return: evaluation
        """
        ## !important
        wh = 10  # weight human
        we = 5  # weight enemy
        eval = 0
        human_cluster = self.map.GET_INFO().get("h")
        num_human_cluster = len(human_cluster)
        if self.character == "Vampire":
            enemy_cluster = self.map.GET_INFO().get("w")
        else:
            enemy_cluster = self.map.GET_INFO().get("v")
        num_enemy_cluster = len(enemy_cluster)

        for i in range(num_human_cluster):
            ratio = self.map[self.position[0], self.position[1]][1] / human_cluster[i][2]# human number of cluster
            ratio -= 1.5
            difference_human = self.map[self.position[0], self.position[1]][1] - human_cluster[i][2]
            distance_human = np.linalg.norm(
                np.array(self.position) - np.array((human_cluster[i][0], human_cluster[i][1])))
            temp = np.abs(1 / np.abs(ratio) + 0.00001) * difference_human
            eval += np.divide(wh * temp, distance_human, where=(distance_human!=0))  # ?

        for i in range(num_enemy_cluster):
            ratio = self.map[self.position[0], self.position[1]][1] / enemy_cluster[i][2]# enemy number of cluster
            ratio -= 1.5
            difference_enemy = self.map[self.position[0], self.position[1]][1] - enemy_cluster[i][2]
            distance_enemy = np.linalg.norm(
                np.array(self.position) - np.array((enemy_cluster[i][0], enemy_cluster[i][1])))
            temp = np.abs(1 / np.abs(ratio) + 0.00001) * difference_enemy
            eval += np.divide(we * temp, distance_enemy, where=(distance_enemy!=0))  # ?

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
    enemy_cluster = state.map.GET_INFO().get("v")
    num_enemy = 0
    for i in range(len(enemy_cluster)):
        num_enemy += enemy_cluster[i][2]
    if num_enemy == 0:
        return np.inf
    if len(state.map[state.position[0], state.position[1]]) == 0:
        return -np.inf
    if depth == 0:
        return state.evaluate_alphabeta()

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


def find_best_move(game_state, eval_func):
    """
    Find the best move
    :param game_state: current game state
    :return: best move
    """
    next_states = game_state.generate_moves()
    # directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, -1), (-1, 1), (1, 1), (0, 0)]
    best_move = None
    # Vampire MAX玩家  Werewolf MIN玩家
    best_eval = float('-inf')# if game_state.character == 'Vampire' else float('inf')
    for next_state in next_states:
        # print(next_state.map.GET_INFO())
        if eval_func == 1:  #
            num_human_cluster = len(game_state.map.GET_INFO().get("h"))
            eval = next_state.evaluate(num_human_cluster)
        if eval_func == 2:
            eval = alpha_beta(next_state, 3, alpha=float('-inf'), beta=float('inf'), maximizing_player=True)
        # print(f"{next_state.position[0], next_state.position[1]} Eval: {eval}")
        if eval > best_eval:
            best_eval = eval
            best_move = (next_state.position[0], next_state.position[1])

    if best_move is None:
        print('Wrong map!')
    next_x = best_move[0] - game_state.position[0]
    next_y = best_move[1] - game_state.position[1]
    return next_x, next_y


if __name__ == "__main__":
    # 创建 Map 实例
    game_map = Map()

    # 设置地图大小
    game_map.UPDATE_GAME_STATE(['set', [7, 7]])  # 5x5 地图

    # 初始化人类位置
    humans = [[6, 6], [0, 0], [3, 3]]  # 定义人类位置
    game_map.UPDATE_GAME_STATE(['hum', humans])

    # 设置玩家起始位置
    player_start = [4, 4]
    game_map.UPDATE_GAME_STATE(['hme', player_start])

    # 设置地图内容（包括人类、吸血鬼和狼人）
    map_content = [
        [6, 6, 2, 0, 0],  # 人类在 (1,1), 数量5
        [0, 0, 2, 0, 0],
        [3, 3, 10, 0, 0],
        [4, 4, 0, 14, 0],  # 吸血鬼在 (2,2), 数量6
        [2, 2, 0, 0, 14],  # 狼人在 (3,3), 数量7
    ]
    game_map.UPDATE_GAME_STATE(['map', map_content])
    game_map.GET_INFO()

    print("real init", tuple(game_map.hme))
    print("type of real init", type(game_map.hme))
    # 创建 GameState 实例
    initial_position = (4, 4)
    print("type of initial position", type(initial_position))
    game_state = GameState(game_map, initial_position, 'Vampire')

    # 测试: 生成移动
    # print("Valid moves from position (2, 2):")
    moves = game_state.generate_moves()
    for idx, move in enumerate(moves):
        print(f"Move {idx + 1}: Position {move.position}, Character {move.character}")
        move.map.GET_INFO()
    # 测试: 评估函数
    # print("--------------------------------------")
    # evaluation = game_state.evaluate()
    # print(game_state.map.GET_INFO())
    # print("\nEvaluation of the current state:", evaluation)

    # 测试: α-β剪枝和最佳移动
    print("--------------------------------------")
    best_x, best_y = find_best_move(game_state)
    print(f"\nBest move for the current state: ({best_x}, {best_y})")
