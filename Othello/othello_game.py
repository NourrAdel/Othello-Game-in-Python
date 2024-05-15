import tkinter as tk  # Import the tkinter library and alias it as tk
from tkinter import ttk  # Import the ttk module from tkinter for themed widgets

# Constants
BOARD_SIZE = 8  # Define the size of the Othello board (8x8)
SQUARE_SIZE = 60  # Define the size of each square on the board


class OthelloGUI:
    def __init__(self, root):
        """Constructor method for initializing the GUI."""
        self.root = root  # Set the root window
        self.root.title("Othello")  # Set the title of the root window to "Othello"
        self.current_player = 'B'  # Initialize the current player to Black ('B')
        self.game_over = False  # Initialize the game over flag to False

        # Create welcome message
        self.welcome_label = tk.Label(root, text="Welcome to Othello!\nChoose your game mode to start.",
                                      font=("Helvetica", 16))
        self.welcome_label.pack()  # Pack the welcome label into the root window

        # Create mode selection buttons
        self.mode_label = tk.Label(root, text="Select Mode:", font=("Helvetica", 14))
        self.mode_label.pack()  # Pack the mode label into the root window
        self.two_player_button = tk.Button(root, text="Two Player Mode", command=self.start_two_player_mode)
        self.two_player_button.pack()  # Pack the button for two player mode into the root window
        self.vs_ai_button = tk.Button(root, text="Player vs AI Mode", command=self.start_vs_ai_mode)
        self.vs_ai_button.pack()  # Pack the button for player vs AI mode into the root window

        # Variables for mode and difficulty
        self.mode = None  # Initialize mode to None
        self.difficulty_var = None  # Initialize difficulty variable to None

    def start_two_player_mode(self):
        # Method to start the game in two player mode
        self.mode = "Two Player"  # Set the mode to "Two Player"
        self.initialize_game()  # Call the method to initialize the game

    def start_vs_ai_mode(self):
        # Method to start the game in player vs AI mode
        self.mode = "Player vs AI"  # Set the mode to "Player vs AI"
        self.initialize_game()  # Call the method to initialize the game

    def initialize_game(self):
        # Method to initialize the game based on selected mode
        # Clear mode selection interface
        self.welcome_label.pack_forget()  # Remove the welcome label from the root window
        self.mode_label.pack_forget()  # Remove the mode label from the root window
        self.two_player_button.pack_forget()  # Remove the two player mode button from the root window
        self.vs_ai_button.pack_forget()  # Remove the player vs AI mode button from the root window
        if self.mode == "Two Player":
            # If the selected mode is two player mode
            self.start_two_player_game()  # Call the method to start the game in two player mode
        elif self.mode == "Player vs AI":
            # If the selected mode is player vs AI mode
            self.start_vs_ai_game()  # Call the method to start the game in player vs AI mode

    def start_two_player_game(self):
        # Method to start the game in two player mode
        self.create_game_interface()  # Call the method to create the game interface
        self.current_player = 'B'  # Set the current player to Black ('B')
        self.turn_label.config(text="Black's Turn")  # Set the turn label text to indicate Black's turn

    def start_vs_ai_game(self):
        # Method to start the game in player vs AI mode
        # Create difficulty selection dropdown
        self.difficulty_label = tk.Label(self.root, text="Select Difficulty:", font=("Helvetica", 14))
        # Create a label for difficulty selection
        self.difficulty_label.pack()  # Pack the difficulty label into the root window
        self.difficulty_var = tk.StringVar(self.root)  # Create a StringVar for the difficulty
        self.difficulty_var.set("Medium")  # Set the default difficulty to "Medium"
        self.difficulty_menu = ttk.Combobox(self.root, textvariable=self.difficulty_var,
                                            values=["Easy", "Medium", "Hard"])
        # Create a dropdown menu for difficulty selection
        self.difficulty_menu.pack()  # Pack the difficulty menu into the root window

        self.create_game_interface()  # Call the method to create the game interface

        # Start the AI's move immediately if it's the AI's turn
        if self.current_player == 'B':  # If it's the AI's turn (Black)
            self.ai_move()  # Call the method for AI to move immediately



    def create_game_interface(self):
        # Method to create the game interface
        # Set background color
        self.root.configure(background='#097969')

        # Create canvas for the board
        self.canvas = tk.Canvas(self.root, width=BOARD_SIZE * SQUARE_SIZE, height=BOARD_SIZE * SQUARE_SIZE, bg='#097969')
        # Create a canvas widget with the specified width, height, and background color
        self.canvas.pack()  # Pack the canvas into the root window

        # Initialize game state and starting discs
        self.board = [[' ' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        # Initialize the game board with empty cells
        self.board[3][3] = 'W'  # Place initial white discs
        self.board[3][4] = 'B'  # Place initial black discs
        self.board[4][3] = 'B'  # Place initial black discs
        self.board[4][4] = 'W'  # Place initial white discs

        # Initialize count labels
        self.black_count_label = tk.Label(self.root, text="Black: 2", font=("Helvetica", 14), bg='#097969')
        # Create a label to display the count of black discs
        self.black_count_label.pack()  # Pack the label for black count into the root window
        self.white_count_label = tk.Label(self.root, text="White: 2", font=("Helvetica", 14), bg='#097969')
        # Create a label to display the count of white discs
        self.white_count_label.pack()  # Pack the label for white count into the root window

        # Initialize player turn label
        self.turn_label = tk.Label(self.root, text="", font=("Helvetica", 14), bg='#097969')
        # Create a label to display the current player's turn
        self.turn_label.pack()  # Pack the turn label into the root window

        self.draw_board()  # Call the method to draw the game board

        # Bind mouse click event to canvas
        self.canvas.bind("<Button-1>", self.handle_click)
        # Bind the left mouse click event to the handle_click method

    def draw_board(self):
        # Method to draw the game board
        self.canvas.delete("all")  # Clear the canvas

        # Draw grid lines
        for i in range(BOARD_SIZE):
            self.canvas.create_line(0, i * SQUARE_SIZE, BOARD_SIZE * SQUARE_SIZE, i * SQUARE_SIZE)
            # Draw horizontal lines
            self.canvas.create_line(i * SQUARE_SIZE, 0, i * SQUARE_SIZE, BOARD_SIZE * SQUARE_SIZE)
            # Draw vertical lines

        # Draw discs and legal moves
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.board[i][j] == 'B':  # If the cell contains a black disc
                    x = j * SQUARE_SIZE + SQUARE_SIZE // 2  # Calculate x-coordinate for the center of the disc
                    y = i * SQUARE_SIZE + SQUARE_SIZE // 2  # Calculate y-coordinate for the center of the disc
                    # Draw a black disc at the calculated position
                    self.canvas.create_oval(x - SQUARE_SIZE // 2 + 5, y - SQUARE_SIZE // 2 + 5,
                                            x + SQUARE_SIZE // 2 - 5, y + SQUARE_SIZE // 2 - 5,
                                            fill='black')
                elif self.board[i][j] == 'W':  # If the cell contains a white disc
                    x = j * SQUARE_SIZE + SQUARE_SIZE // 2  # Calculate x-coordinate for the center of the disc
                    y = i * SQUARE_SIZE + SQUARE_SIZE // 2  # Calculate y-coordinate for the center of the disc
                    # Draw a white disc at the calculated position
                    self.canvas.create_oval(x - SQUARE_SIZE // 2 + 5, y - SQUARE_SIZE // 2 + 5,
                                            x + SQUARE_SIZE // 2 - 5, y + SQUARE_SIZE // 2 - 5,
                                            fill='white')

        # Draw legal moves
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.is_valid_move(i, j):  # If the move is valid
                    x = j * SQUARE_SIZE + SQUARE_SIZE // 2  # Calculate x-coordinate for the center of the square
                    y = i * SQUARE_SIZE + SQUARE_SIZE // 2  # Calculate y-coordinate for the center of the square
                    # Draw an 'X' at the calculated position to indicate a legal move
                    self.canvas.create_text(x, y, text="X", font=("Helvetica", 16))

        # Highlight current player's discs
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.board[i][j] == self.current_player:  # If the disc belongs to the current player
                    x = j * SQUARE_SIZE + SQUARE_SIZE // 2  # Calculate x-coordinate for the center of the disc
                    y = i * SQUARE_SIZE + SQUARE_SIZE // 2  # Calculate y-coordinate for the center of the disc
                    # Draw a yellow outline around the disc to highlight it
                    self.canvas.create_oval(x - SQUARE_SIZE // 2 + 5, y - SQUARE_SIZE // 2 + 5,
                                            x + SQUARE_SIZE // 2 - 5, y + SQUARE_SIZE // 2 - 5,
                                            outline="yellow", width=2)

    def handle_click(self, event):
        # Method to handle mouse clicks based on the game mode
        if self.mode == "Two Player":
            self.handle_click_two_player(event)
        elif self.mode == "Player vs AI":
            self.handle_click_vs_ai(event)

    def handle_click_two_player(self, event):
        # Method to handle mouse clicks in Two Player mode
        if self.game_over:
            return  # If the game is over, ignore clicks

        col = event.x // SQUARE_SIZE  # Calculate the column index of the clicked square
        row = event.y // SQUARE_SIZE  # Calculate the row index of the clicked square

        # Make a move if it's a valid move
        if self.is_valid_move(row, col):
            self.make_move(row, col)  # Make the move
            self.draw_board()  # Redraw the game board

    def handle_click_vs_ai(self, event):
        # Method to handle mouse clicks in Player vs AI mode
        if self.game_over:
            return  # If the game is over, ignore clicks

        col = event.x // SQUARE_SIZE  # Calculate the column index of the clicked square
        row = event.y // SQUARE_SIZE  # Calculate the row index of the clicked square

        # Make a move if it's a valid move
        if self.is_valid_move(row, col):
            self.make_move(row, col)  # Make the move
            self.draw_board()  # Redraw the game board

            # AI player's turn
            if self.current_player == 'B' and not self.game_over:  # If it's the AI's turn and the game is not over
                self.ai_move()  # Start the AI's move immediately

    def is_valid_move(self, row, col, board=None):
        # Method to check if a move is valid
        if board is None:
            board = self.board  # If no board is provided, use the current game board

        if board[row][col] != ' ':  # If the cell is not empty
            return False  # The move is invalid

        # Check in all four directions for valid moves
        # Define directions: up, down, right, left
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dr, dc in directions:  # Loop through each direction
            r, c = row + dr, col + dc  # Calculate the next cell in the direction
            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] != self.current_player and board[r][
                c] != ' ':  # If the next cell belongs to the opponent
                while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:  # Loop until the end of the board
                    if board[r][c] == self.current_player:  # If a disc belonging to the current player is found
                        return True  # The move is valid
                    elif board[r][c] == ' ':  # If an empty cell is found
                        break  # Break the loop
                    r += dr  # Move to the next cell in the same direction
                    c += dc
        return False  # No valid move found

    def make_move(self, row, col, board=None, player=None):
        # Method to make a move on the game board
        if board is None:
            board = self.board  # If no board is provided, use the current game board
        if player is None:
            player = self.current_player  # If no player is provided, use the current player

        board[row][col] = player  # Place the player's disc at the specified position

        # Flip discs in all four directions
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Define directions: right, left, down, up
        for dr, dc in directions:  # Loop through each direction
            r, c = row + dr, col + dc  # Calculate the next cell in the direction
            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] != player and board[r][
                c] != ' ':  # If the next cell belongs to the opponent
                discs_to_flip = []  # Initialize a list to store discs to flip
                while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:  # Loop until the end of the board
                    if board[r][c] == player:  # If a disc belonging to the current player is found
                        for flip_row, flip_col in discs_to_flip:  # Iterate over the discs to flip
                            board[flip_row][flip_col] = player  # Flip the discs
                        break  # Break the loop
                    elif board[r][c] == ' ':  # If an empty cell is found
                        break  # Break the loop
                    discs_to_flip.append((r, c))  # Add the opponent's disc to the list
                    r += dr  # Move to the next cell in the same direction
                    c += dc

        # Update counts and labels
        black_count = sum(row.count('B') for row in board)  # Count black discs
        white_count = sum(row.count('W') for row in board)  # Count white discs
        self.black_count_label.config(text=f"Black: {black_count}")  # Update black count label
        self.white_count_label.config(text=f"White: {white_count}")  # Update white count label

        # Switch players
        self.current_player = 'B' if player == 'W' else 'W'  # Switch current player

        # Update player turn label
        self.turn_label.config(text=f"{self.current_player.capitalize()}'s Turn")

        # Check for game end
        if self.check_game_over():  # If the game is over
            if not self.game_over:  # Check if game is already over
                self.display_winner()  # Display the winner
                self.game_over = True  # Set game_over flag to True

    def ai_move(self):
        # Function to make a move for the AI player using the alpha-beta pruning algorithm
        def alpha_beta_pruning(board, player, alpha, beta, depth):
            # Check if depth limit reached or game over
            if depth == 0 or not any(self.is_valid_move(row, col, board=board)
                                     for row in range(BOARD_SIZE) for col in range(BOARD_SIZE)):
                return self.evaluate(board, player)  # Evaluate the board state

            if player == 'B':  # Maximize for Black player
                max_eval = float('-inf')
                for row in range(BOARD_SIZE):
                    for col in range(BOARD_SIZE):
                        if self.is_valid_move(row, col, board=board):
                            new_board = [row[:] for row in board]  # Create a copy of the board
                            self.make_move(row, col, board=new_board, player=player)  # Make the move
                            # Recursively call alpha-beta pruning for the opponent
                            eval_score = alpha_beta_pruning(new_board, 'W', alpha, beta, depth - 1)
                            max_eval = max(max_eval, eval_score)  # Update the max evaluation score
                            alpha = max(alpha, eval_score)  # Update alpha
                            if beta <= alpha:
                                break  # Beta cutoff
                return max_eval

            else:  # Minimize for White player
                min_eval = float('inf')
                for row in range(BOARD_SIZE):
                    for col in range(BOARD_SIZE):
                        if self.is_valid_move(row, col, board=board):
                            new_board = [row[:] for row in board]  # Create a copy of the board
                            self.make_move(row, col, board=new_board, player=player)  # Make the move
                            # Recursively call alpha-beta pruning for the opponent
                            eval_score = alpha_beta_pruning(new_board, 'B', alpha, beta, depth - 1)
                            min_eval = min(min_eval, eval_score)  # Update the min evaluation score
                            beta = min(beta, eval_score)  # Update beta
                            if beta <= alpha:
                                break  # Alpha cutoff
                return min_eval

        # Difficulty Levels: Retrieve selected difficulty from dropdown menu
        difficulty = self.difficulty_var.get()

        depth = 3  # Default depth for medium difficulty
        if difficulty == "Easy":
            depth = 1  # Easy level
        elif difficulty == "Hard":
            depth = 5  # Hard level

        # Find the best move for the computer player
        best_move = None
        best_eval = float('-inf')
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.is_valid_move(row, col):
                    new_board = [row[:] for row in self.board]  # Create a copy of the board
                    self.make_move(row, col, board=new_board, player=self.current_player)  # Make the move
                    # Call alpha-beta pruning to evaluate the move
                    eval_score = alpha_beta_pruning(new_board, 'W', float('-inf'), float('inf'), depth)
                    # If the evaluation score is better than the best evaluation score so far
                    if eval_score > best_eval:
                        best_eval = eval_score  # Update the best evaluation score
                        best_move = (row, col)  # Update the best move

        # Make the best move found by the algorithm
        if best_move:
            self.make_move(best_move[0], best_move[1])  # Make the best move
            self.draw_board()  # Redraw the game board

    # Function to evaluate the current state of the game board
    def evaluate(self, board, player):
        # Simple evaluation function: the difference between the number of player's disks and opponent's disks
        player_count = sum(row.count(player) for row in board)  # Count the number of player's disks
        opponent_count = sum(row.count('B' if player == 'W' else 'W') for row in board)  # Count the opponent's disks
        return player_count - opponent_count  # Return the evaluation score

    # Function to check if the game is over
    def check_game_over(self):
        # Check if there are valid moves for either player
        black_moves = any(self.is_valid_move(r, c) for r in range(BOARD_SIZE) for c in range(BOARD_SIZE))
        white_moves = any(self.is_valid_move(r, c) for r in range(BOARD_SIZE) for c in range(BOARD_SIZE))
        # Return True if no valid moves for both players or if a player runs out of pieces, indicating game over
        return not (black_moves or white_moves)

    # Function to display the winner of the game
    def display_winner(self):
        # Count the number of black and white discs on the board
        black_count = sum(row.count('B') for row in self.board)
        white_count = sum(row.count('W') for row in self.board)

        # Determine the winner based on the disc count
        if black_count > white_count:
            winner_text = "Black Won!"
        elif black_count < white_count:
            winner_text = "White Won!"
        else:
            winner_text = "Draw!"

        # Display the winner text with background matching the canvas/board
        winner_label = tk.Label(self.root, text=winner_text, font=("Helvetica", 16), bg='#097969')
        winner_label.pack()

# Initialize the Tkinter root window and start the game
root = tk.Tk()
# Create an instance of the OthelloGUI class, passing the root window as an argument
game = OthelloGUI(root)
# Start the Tkinter event loop, which waits for user input and responds accordingly
root.mainloop()
