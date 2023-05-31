import select
import bluetooth
import sys
from time import time

# Define the game board and other necessary variables
game_board = [[' ' for _ in range(7)] for _ in range(6)]
current_player = 'X'  # Player X starts

def print_game_board(game_state):
    # Print the received game state
    game_board = [list(game_state[i:i+7]) for i in range(0, len(game_state), 7)]
    pass


def send_request_response(code):
    # Send request or response code to the server
    server_sock.send(code.encode())

def receive_request_response():
    # Receive request or response code from the server
    data = server_sock.recv(3).decode()
    return data

def send_player_move(column):
    # Send player's move (column number) to the server
    server_sock.send(column.encode())

def receive_game_state():
    # Receive the updated game state from the server
    game_state = server_sock.recv(42).decode()  # Assuming the game state is always 42 characters long
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
    client_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    client_sock.connect((host, port))
    
    print("Connected to server at", server_address)

    # Send request to the server to choose the game mode 
    request = input("Enter 100 for human mode or 101 for AI mode. Do you accept the game? (yes/no):")
    send_request_response(request)

    # Receive the response from the server
    response = receive_request_response()

    if response == "102":
        print("Game request accepted. Starting the game...")

        if request == "100":
            print("Start of the human mode")
            response = input("Do you want to play yourself or with your AI? (player/ai): ")

            if response.lower() == "player":
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
                        start_time = time()
                        ready, _, _ = select.select([client_sock], [], [], 60)
                        # Check if timeout occurred
                        if not ready:
                            print("Timeout occurred. Player took too long to make a move.")
                            break
                        game_state = receive_game_state()
                        print("Updated game board:")
                        # Stop the timer
                        elapsed_time = time() - start_time
                        print("Elapsed time for the move:", elapsed_time)
                        # Update game board and display
                        print_game_board(game_state)

                        # Check for game end conditions (win or draw or quit)
                        if check_win(row, column):
                            print("Player", current_player, "wins!")
                            break
                        elif check_draw():
                            print("It's a draw!")
                            break
                        elif column == "201":
                            print("Player requested to quit the game.")
                            break
                    else:
                        print("Invalid column number. Please try again.")
           
            elif response.lower() == "ai":
                print("Waiting for the game board...")

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
                        start_time = time()
                        ready, _, _ = select.select([client_sock], [], [], 60)
                        # Check if timeout occurred
                        if not ready:
                            print("Timeout occurred. Player took too long to make a move.")
                            break
                        game_state = receive_game_state()
                        print("Updated game board:")
                        # Stop the timer
                        elapsed_time = time() - start_time
                        print("Elapsed time for the move:", elapsed_time)
                        # Update game board and display
                        print_game_board(game_state)
                        # Check for game end conditions (win or draw or quit)
                        if check_win(row, column):
                            print("Player", current_player, "wins!")
                            break
                        elif check_draw():
                            print("It's a draw!")
                            break
                        elif column == "201":
                            print("Player requested to quit the game.")
                            break
                    else:
                        print("Invalid column number. Please try again.")    
    
        elif request == "101":
            print("AI mode")
            response = input("Do you want to play yourself or with your AI? (player/ai): ")

            if response.lower() == "player":
                print("Waiting for the game board...")

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
                        start_time = time()
                        ready, _, _ = select.select([client_sock], [], [], 60)
                        # Check if timeout occurred
                        if not ready:
                            print("Timeout occurred. Player took too long to make a move.")
                            break
                        game_state = receive_game_state()
                        print("Updated game board:")
                        # Stop the timer
                        elapsed_time = time() - start_time
                        print("Elapsed time for the move:", elapsed_time)
                        # Update game board and display
                        print_game_board(game_state)
                        # Check for game end conditions (win or draw or quit)
                        if check_win(row, column):
                            print("Player", current_player, "wins!")
                            break
                        elif check_draw():
                            print("It's a draw!")
                            break
                        elif column == "201":
                            print("Player requested to quit the game.")
                            break
                    else:
                        print("Invalid column number. Please try again.")


            elif response.lower() == "ai":
                print("Waiting for the game board...")

                # Receive the initial game state from the server
                game_state = receive_game_state()
                print("Initial game board:")
                print_game_board(game_state)

                # Game loop 
                while True:
                    # AI playing 
                    ai_move = generate_ai_move()
                    send_player_move(ai_move)
                    start_time = time()
                    ready, _, _ = select.select([client_sock], [], [], 60)
                    # Check if timeout occurred
                    if not ready:
                        print("Timeout occurred. Player took too long to make a move.")
                        break
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
            print("Invalid request code.")

    elif response == "103":
        print("Game request refused by the server.")

    else:
        print("Invalid response received from the server.")

   

    # Clean up
    client_sock.close()
    print("Connection closed.")

if __name__ == "__main__":
    main()

