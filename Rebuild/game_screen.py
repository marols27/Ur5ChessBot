import tkinter as tk
from tkinter import messagebox
from components.chessboard import Chessboard  # Import the Chessboard component
from components.move_history import MoveHistory  # Import the MoveHistory component
from DGTBoard import DGTBoard
from UR5Robot import UR5Robot
from Board import Board
from Game import Game
import Settings
import chess
import chess.engine
import chess.pgn

def show_game_screen(root, selection_frame, color, difficulty):
    '''Show the game screen with the selected color and difficulty.'''
    
    robot = UR5Robot(Settings.TRAVEL_HEIGHT, Settings.HOME, Settings.CONNECTION_IP, Settings.ACCELERATION, Settings.SPEED, Settings.GRIPPER_SPEED, Settings.GRIPPER_FORCE)
    dgt = DGTBoard(Settings.PORT)
    board = Board(Settings.START_FEN, Settings.BOARD_FEATURE, Settings.BOARD_SIZE, Settings.SQUARE_SIZE)
    engine = chess.engine.SimpleEngine.popen_uci(Settings.STOCKFISH_PATH)
    gameInfo = chess.pgn.Game()
    capturePos = Settings.CAPTURE_POSE
    timeout = Settings.TIMEOUT
    game = Game(robot, dgt, board, engine, gameInfo, capturePos, timeout, 10, False)    # Destroy the selection screen
    selection_frame.destroy()

    # Create the main game frame
    game_frame = tk.Frame(root, bg="#1a237e")
    game_frame.pack(fill="both", expand=True)
    
    # Determine whether to flip the board based on the selected color
    flipped = (color == "black")
    
    # Chessboard frame
    board_frame = tk.Frame(game_frame, bg="#1a237e")
    board_frame.grid(row=0, column=0, padx=20, pady=20, sticky="n")

    # Define desired square size
    square_size = 100

    # Create the Chessboard component with the specified square size
    board_canvas = Chessboard(board_frame, square_size=square_size, flipped=flipped)
    board_canvas.pack()

    # Update the Chessboard with the starting position
    starting_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    board_canvas.update_board(starting_fen)
    
    # Move history frame
    history_frame = tk.Frame(game_frame, bg="#1a237e")
    history_frame.grid(row=0, column=1, padx=20, pady=20, sticky="n")

    # Create the MoveHistory component
    move_history = MoveHistory(history_frame, board_canvas, game)    
    move_history.grid(row=0, column=0, padx=20, pady=20, sticky="n")

    # Action buttons frame
    action_frame = tk.Frame(game_frame, bg="#1a237e")
    action_frame.grid(row=1, column=1, padx=20, pady=10, sticky="e")

    # Confirm Move Button
    confirm_move_button = tk.Button(
        action_frame,
        text="CONFIRM MOVE",
        font=("Helvetica", 20, "bold"),
        bg="#28a745",  # Green background
        fg="#252525",  # White text
        activebackground="#218838",  # Darker green when pressed
        activeforeground="white",  # White text when pressed
        padx=20,
        pady=10,
        state="normal"  # Ensure button is enabled
    )
    confirm_move_button.pack(side="left", padx=10)

    # Resign Button
    resign_button = tk.Button(
        action_frame,
        text="RESIGN",
        font=("Helvetica", 20, "bold"),
        bg="#dc3545",  # Red background
        fg="#252525",  # White text
        activebackground="#c82333",  # Darker red when pressed
        activeforeground="white",  # White text when pressed
        padx=20,
        pady=10,
        state="normal"  # Ensure button is enabled
    )
    
    resign_button.pack()
   
    # Example function to confirm move
    def confirm_move():
        move_history.reset_to_current()

        if not move_history.is_current:
            # If we're in history mode, reset to current before making a move

            # Confirm the player's move
            game.confirmMove()

            # Update the move history and board state in the GUI
            move_history.update_move_history()

            # Let the robot play its move
            game.playRobotMove()

            # Update the move history and board state in the GUI after the robot's move
            move_history.update_move_history()
        else:
            # If we're in history mode, reset to current before making a move
            move_history.reset_to_current()
            confirm_move()

    confirm_move_button.config(command=confirm_move)

    # Example function to resign the game
    def resign_game():
        messagebox.showinfo("Resign", "You have resigned the game.")
        game_frame.destroy()
    
        # Import inside the function to avoid circular import
        from home_screen import show_home_screen
        show_home_screen(root)
        
    resign_button.config(command=resign_game)
    
    if game.board.turn == True:
            game.playRobotMove()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Chess Game")
    root.geometry("1024x768")
    show_game_screen(root, tk.Frame(root), "white", "medium")
    root.mainloop()