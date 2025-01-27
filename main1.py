import time
from client import ClientSocket
# import copy
from map import Map
from GameState import *
import config

def send_our_moves(map, client_socket):
    # 创建 GameState 实例
    our_position = map.get_our_position()[0]
    tuple_postition = tuple([our_position[0], our_position[1]])
    game_state = GameState(map, tuple_postition, 'Vampire')
    # 测试: 生成移动
    print("Valid moves from position (2, 2):")
    moves = game_state.generate_moves()
    for idx, move in enumerate(moves):
        print(f"Move {idx + 1}: Position {move.position}, Character {move.character}")
        move.map.GET_INFO()
    # 测试: 评估函数
    # print("--------------------------------------")
    # evaluation = game_state.evaluate()
    # print("\nEvaluation of the current state:", evaluation)

    # 测试: α-β剪枝和最佳移动
    print("--------------------------------------")
    # eval_finc=2: Alphabeta
    best_x, best_y = find_best_move(game_state, eval_func=1)
    print(f"\nBest move for the current state: ({best_x}, {best_y})")
    # print("PAUSE")
    # import time
    # time.sleep(1000)
    map.SEND_MOVE(client_socket, best_x, best_y)


def play_game():
    # ip & port
    client_socket = ClientSocket(config.SERVER_IP, config.SERVER_PORT)
    # client_socket = ClientSocket(args.ip, args.port)
    client_socket.send_nme("Your AI")
    map = Map()
    # set message
    message = client_socket.get_message()
    map.UPDATE_GAME_STATE(message)

    # hum message
    message = client_socket.get_message()
    map.UPDATE_GAME_STATE(message)

    # hme message
    message = client_socket.get_message()
    map.UPDATE_GAME_STATE(message)

    # map message
    message = client_socket.get_message()
    map.UPDATE_GAME_STATE(message)

    message_flag = "error"
    # start of the game
    while True:
        # # send our move
        # print("To be Done......")
        # send_our_moves(map=map, client_socket=client_socket)
        #
        # map.GET_INFO()

        print("waiting  message")
        message = client_socket.get_message()
        time_message_received = time.time()
        message_flag = message[0]
        # receive upd information
        map.UPDATE_GAME_STATE(message)
        print("receiving 2")
        if message_flag == "upd":
            print("receiving upd")
            send_our_moves(map=map, client_socket=client_socket)
            # map.UPDATE_GAME_STATE(message)
        elif message_flag == "end":
            print("receiving end")
            break
        elif message_flag == "bye":
            print("receiving bye")
            break
        else:
            print("udp/end/bye error!")
        print("one round")

    return message_flag

if __name__ == '__main__':

    while(True):
        message_flag = play_game()
        if message_flag == "bye":
            break
