from Game import Game
from Board import Board
from DGTBoard import DGTBoard
from UR5Robot import UR5Robot
import chess
import chess.engine
import chess.pgn
import Settings
from PoseConfigure import PoseConfigure
from guiMain import GUI

# robot = UR5Robot(Settings.TRAVEL_HEIGHT, Settings.HOME, Settings.CONNECTION_IP, Settings.ACCELERATION, Settings.SPEED, Settings.GRIPPER_SPEED, Settings.GRIPPER_FORCE)
# dgt = DGTBoard(Settings.PORT)
# board = Board(Settings.START_FEN, Settings.BOARD_FEATURE, Settings.BOARD_SIZE, Settings.SQUARE_SIZE)
# engine = chess.engine.SimpleEngine.popen_uci(Settings.STOCKFISH_PATH)
# gameInfo = chess.pgn.Game()
# capturePos = Settings.CAPTURE_POSE
# timeout = Settings.TIMEOUT
gui = GUI()

#game = Game(robot, dgt, board, engine, gameInfo, capturePos, timeout, 10, False)

#game.runGameLoop()

#print(game.gameInfo)