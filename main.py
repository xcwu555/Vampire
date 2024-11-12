import time
from client import ClientSocket

from map import Map


def play_game():
    client_socket = ClientSocket()
    # client_socket = ClientSocket(args.ip, args.port)
    client_socket.send_nme("Our AI")
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
        # send our move
        print("To be Done......")
        map.SEND_MOVE(client_socket)

        message  = client_socket.get_message()
        time_message_received = time.time()
        message_flag = message[0]
        if message_flag == "upd":
            # receive upd information
            map.UPDATE_GAME_STATE(message)
        elif message_flag == "end":
            break
        elif message_flag == "bye":
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
