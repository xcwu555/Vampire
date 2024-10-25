import time

import config
from client import ClientSocket

def play_game():
    client_socket = ClientSocket(config.ip, config.port).py
    client_socket.send_nme("AIAI")
    # set message
    message = client_socket.get_message()
    print(message)
    UPDATE_GAME_STATE(message)
    # hum message
    message = client_socket.get_message()
    UPDATE_GAME_STATE(message)
    # hme message
    message = client_socket.get_message()
    UPDATE_GAME_STATE(message)
    # map message
    message = client_socket.get_message()
    UPDATE_GAME_STATE(message)

    # start of the game
    while True:
        message  = client_socket.get_message()
        time_message_received = time.time()
        UPDATE_GAME_STATE(message)
        if message[0] == "upd":
            nb_moves, moves = COMPUTE_NEXT_MOVE(GAME_STATE)
            client_socket.send_mov(nb_moves, moves)


if __name__ == '__main__':
    play_game()
