import os

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

def play_game():
    global current_player

    # Send initial game state to the client
    send_game_state()

    while True:
        # Receive player move from the client
        column = receive_player_move()
        row = get_next_empty_row(column)

        # Update the game board
        game_board[row][column] = current_player

        # Send updated game state to the client
        send_game_state()

        # Check for a win or draw
        if check_win(row, column):
            print("Player", current_player, "wins!")
            break
        elif check_draw():
            print("It's a draw!")
            break

        # Switch to the other player
        current_player = 'O' if current_player == 'X' else 'X'

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

    # Send request to the client to choose the game mode 
    send_request_response("100") or send_request_response("101") 
    response = receive_request_response()

    if response == "102":
        print("Player accepted the game.")
        print_game_board()  # Launch of the board 

        # Play the game
        play_game()
    else:
        print("Player refused the game.")

     # Clean up
    client_sock.close()
    server_sock.close()
    print("All done.")


if __name__ == "__main__":
    main()

client_sock.close()
server_sock.close()
print("All done.")

