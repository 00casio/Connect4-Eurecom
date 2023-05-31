import os
import bluetooth
from time import time

# Define the game board and other necessary variables
game_board = [[' ' for _ in range(7)] for _ in range(6)]
current_player = 'X'  # Player X starts

def initialize_game():
    # Clear the game board
    for row in game_board:
        for i in range(7):
            row[i] = ' '

def print_game_board():
    # Print the current game board
    pass


def send_request_response(code):
    # Send request or response code to the client
    client_sock.send(code.encode())

def receive_request_response():
    # Receive request or response code from the client
    data = client_sock.recv(3).decode()
    return data

def send_game_state():
    # Convert game board to a string representation
    game_state = ""
    for row in game_board:
        for cell in row:
            game_state += cell
    game_state += "\n"

    # Send game state to the client
    client_sock.send(game_state.encode())

def receive_player_move():
    # Receive player move from the client
    data = client_sock.recv(3).decode()
    column = int(data)
    return column

def get_next_empty_row(column):
    # Find the next empty row in the specified column
    pass

def check_win(row, column):
    pass


def check_draw():
    # Check if the game is a draw (all cells are filled)
    pass

def play_game():
    global current_player

    # Send initial game state to the client
    send_game_state()

    while True:
        try:
            # Receive player move from the client
            column = receive_player_move()
            row = get_next_empty_row(column)
        except bluetooth.btcommon.BluetoothError:
            print("Player took too long to make a move. Timeout occurred.")
            break

        # Update the game board
        game_board[row][column] = current_player

        # Send updated game state to the client
        send_game_state()

        # Check for a win or draw or quit 
        if check_win(row, column):
            print("Player", current_player, "wins!")
            break
        elif check_draw():
            print("It's a draw!")
            break
        elif column == "201":
            print("Player requested to quit the game.")
            break

        # Switch to the other player
        current_player = 'O' if current_player == 'X' else 'X'


def main():

    os.system("bluetoothctl discoverable on")
    os.system("bluetoothctl pairable on")       
    # Set up Bluetooth server socket
    server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    server_sock.bind(("", bluetooth.PORT_ANY))
    server_sock.listen(1)

    port = server_sock.getsockname()[1]

    uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

    bluetooth.advertise_service(server_sock, "connect4-4", service_id=uuid,
                                service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
                                profiles=[bluetooth.SERIAL_PORT_PROFILE])

    print("Waiting for connection on RFCOMM channel", port)

    client_sock, client_info = server_sock.accept()
    print("Accepted connection from", client_info)

    # Game initialization
    initialize_game()

    # Set the timeout for receiving player's move to 60 seconds
    client_sock.settimeout(60)

    # Receive the request from the client to choose the game mode  
    request = receive_request_response()

    if request == "100":
        print("Start the game in human mode.")
        # Send the response to the client
        send_request_response(client_sock, "102")
        print_game_board()  # Launch of the board 

        # Play the game
        play_game()
    elif request == "101":
        print("Start the game in AI mode.")
        # Send the response to the client
        send_request_response(client_sock, "102")
        # Start the game in AI mode
        play_game()
    else:
        # Request was refused
        print("Client refused the game request.")
        send_request_response(client_sock, "103")

    # Clean up
    client_sock.close()
    server_sock.close()
    print("All done.")

if __name__ == "__main__":
    main()