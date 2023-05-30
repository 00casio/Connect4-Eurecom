import sys

import bluetooth

def print_game_board(game_state):
    # Print the received game state
    game_board = [list(game_state[i:i+7]) for i in range(0, len(game_state), 7)]
    pass

def send_request_response(code):
    # Send request or response code to the server
    sock.send(code.encode())

def receive_request_response():
    # Receive request or response code from the server
    data = sock.recv(3).decode()
    return data

def send_player_move(column):
    # Send player's move (column number) to the server
    sock.send(column.encode())

def receive_game_state():
    # Receive the updated game state from the server
    game_state = sock.recv(42).decode()  # Assuming the game state is always 42 characters long
    return game_state

def check_win(row, column):
    pass


def check_draw():
    # Check if the game is a draw (all cells are filled)
    pass


def main():
    addr = None

    if len(sys.argv) < 2:
        print("No device specified. Searching all nearby bluetooth devices for "
          "the SampleServer service...")
    else:
        addr = sys.argv[1]
        print("Searching for SampleServer on {}...".format(addr))

    # search for the SampleServer service
    uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
    service_matches = bluetooth.find_service(uuid=uuid, address=addr)

    if len(service_matches) == 0:
        print("Couldn't find the SampleServer service.")
        sys.exit(0)

    first_match = service_matches[0]
    port = first_match["port"]
    name = first_match["name"]
    host = first_match["host"]

    print("Connecting to \"{}\" on {}".format(name, host))

    # Create the client socket
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((host, port))
    
    print("Connected to server at", server_address)

    # Receive request from the server
    request = receive_request_response()

    if request == "100":
        print("Received request to play in human mode.")
        response = input("Do you accept the game? (yes/no): ")

        if response.lower() == "yes":
            send_request_response("102")  # Accept the game
            print("Game request accepted. Waiting for the game board...")

            # Receive the initial game state from the server
            game_state = receive_game_state()
            print("Initial game board:")
            print_game_board(game_state)

            # Game loop
            while True:
                # Prompt the player for a move
                column = input("Enter the column number (0-6) to place your token: ")
                if column.isdigit() and 0 <= int(column) <= 6:
                    send_player_move(column)
                    game_state = receive_game_state()
                    print("Updated game board:")
                    print_game_board(game_state)
                else:
                    print("Invalid column number. Please try again.")

                # Check for game end conditions (win or draw)
                if check_win(row, column):
                    print("Player", current_player, "wins!")
                    break
                elif check_draw():
                    print("It's a draw!")
                    break

        else:
            send_request_response("103")  # Refuse the game
            print("Game request refused.")
    
    elif request == "101":
        print("Received request to play in AI mode.")
        response = input("Do you want to play yourself or the AI? (player/ai): ")

        if response.lower() == "player":
            send_request_response("102")  # Accept the game with player mode
            print("Game request accepted. Waiting for the game board...")

            # Receive the initial game state from the server
            game_state = receive_game_state()
            print("Initial game board:")
            print_game_board(game_state)

            # Game loop
            while True:
                # Prompt the player for a move
                column = input("Enter the column number (0-6) to place your token: ")
                if column.isdigit() and 0 <= int(column) <= 6:
                    send_player_move(column)
                    game_state = receive_game_state()
                    print("Updated game board:")
                    print_game_board(game_state)
                else:
                    print("Invalid column number. Please try again.")

                # Check for game end conditions (win or draw)
                if check_win(row, column):
                    print("Player", current_player, "wins!")
                    break
                elif check_draw():
                    print("It's a draw!")
                    break

        elif response.lower() == "ai":
            send_request_response("102")  # Accept the game with AI mode
            print("Game request accepted. Waiting for the game board...")

            # Receive the initial game state from the server
            game_state = receive_game_state()
            print("Initial game board:")
            print_game_board(game_state)

            # Game loop 
            while True:
                # AI playing 
                ai_move = generate_ai_move()
                send_player_move(ai_move)
                game_state = receive_game_state()
                print("Updated game board:")
                print_game_board(game_state)

                # Check for game end conditions (win or draw)
                if check_win(row, column):
                    print("Player", current_player, "wins!")
                    break
                elif check_draw():
                    print("It's a draw!")
                    break

        else:
            send_request_response("103")  # Refuse the game
            print("Game request refused.")
    else:
        print("Invalid request received.")
   

    # Clean up
    sock.close()

if __name__ == "__main__":
    main()

