# Tic-Tac-Toe board
board = [' ', ' ', ' ',
         ' ', ' ', ' ',
         ' ', ' ', ' ']

# Players
PLAYER_X = 'X'
PLAYER_O = 'O'

# Function to check if a player has won
def check_winner(player):
    # Check rows, columns, and diagonals
    for i in range(3):
        if all(board[i*3 + j] == player for j in range(3)):
            return True
        if all(board[j*3 + i] == player for j in range(3)):
            return True
    if all(board[i] == player for i in [0, 4, 8]) or all(board[i] == player for i in [2, 4, 6]):
        return True
    return False

# Function to check if the game is over
def is_game_over():
    return any(cell == ' ' for cell in board) or check_winner(PLAYER_X) or check_winner(PLAYER_O)

# Minimax algorithm
def minimax(depth, maximizing_player):
    if check_winner(PLAYER_X):
        return -1
    if check_winner(PLAYER_O):
        return 1
    if not any(cell == ' ' for cell in board):
        return 0

    if maximizing_player:
        max_eval = float('-inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = PLAYER_O
                eval = minimax(depth + 1, False)
                board[i] = ' '
                max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = PLAYER_X
                eval = minimax(depth + 1, True)
                board[i] = ' '
                min_eval = min(min_eval, eval)
        return min_eval

# Function to find the best move for the computer (Player O)
def find_best_move():
    best_move = -1
    best_eval = float('-inf')
    for i in range(9):
        if board[i] == ' ':
            board[i] = PLAYER_O
            eval = minimax(0, False)
            board[i] = ' '
            if eval > best_eval:
                best_eval = eval
                best_move = i
    return best_move

# Main game loop
def play_game():
    while not is_game_over():
        print_board()
        
        # Get user input for their move
        move = -1
        while move < 0 or move > 8 or board[move] != ' ':
            move = int(input("Enter your move (0-8): "))
            if move < 0 or move > 8 or board[move] != ' ':
                print("Invalid move. Try again.")
        
        board[move] = PLAYER_X
        
        if is_game_over():
            break
        
        print("Computer is making its move...")
        computer_move = find_best_move()
        board[computer_move] = PLAYER_O

    print_board()
    if check_winner(PLAYER_X):
        print("You win!")
    elif check_winner(PLAYER_O):
        print("Computer wins!")
    else:
        print("It's a draw!")

# Function to display the Tic-Tac-Toe board
def print_board():
    for i in range(0, 9, 3):
        print(board[i], '|', board[i + 1], '|', board[i + 2])
        if i < 6:
            print('-' * 9)

# Start the game
play_game()
