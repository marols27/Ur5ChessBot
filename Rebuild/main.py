import chess.engine
import chess.pgn
from ChessGameEnvironment import ChessGameEnvironment
from UR5Robot import UR5Robot
from DGTBoard import DGTBoard
from Board import Board
import chess
import Settings
from Game import Game

# If you wish to change any of the settings, it is recommended to change them in the Settings.py file.
#socket = Settings.SOCKET
robot = UR5Robot(travelHeight=Settings.TRAVEL_HEIGHT, homePose=Settings.HOME, connectionIP=Settings.CONNECTION_IP, acceleration=Settings.ACCELERATION, speed=Settings.SPEED, gripperSpeed=Settings.GRIPPER_SPEED, gripperForce=Settings.GRIPPER_FORCE)
dgtBoard = DGTBoard(port=Settings.PORT)
board = Board(startFen=Settings.START_FEN, feature=Settings.BOARD_FEATURE, boardSize=Settings.BOARD_SIZE, squareSize=Settings.SQUARE_SIZE)
engine = chess.engine.SimpleEngine.popen_uci(Settings.STOCKFISH_PATH)
gameInfo = chess.pgn.Game()
capturePos = Settings.CAPTURE_POSE
timeout = Settings.TIMEOUT

chessGame = Game(socket=True, robot=robot, dgtBoard=dgtBoard, board=board, engine=engine, gameInfo=gameInfo, capturePos=capturePos, timeout=timeout)
conditions = {
    "difficulty": Settings.DIFFICULTY,
    "color": chess.BLACK
}
robot.home()
chessGame.on_conditions(conditions)
chessGame.on_start()
chessGame.runGameLoop()

"""
# Event handlers:
@robot.control.on("connect")
def on_robot_connection():
    socket.emit("robot_connected")

@robot.control.on("disconnect")
def on_robot_disconnection():
    socket.emit("robot_disconnected")

@robot.info.on("connect")
def on_robot_info_connection():
    socket.emit("robot_info_connected")

@robot.info.on("disconnect")
def on_robot_info_disconnection():
    socket.emit("robot_info_disconnected")

@robot.gripper.on("connect")
def on_robot_gripper_connection():
    socket.emit("robot_gripper_connected")

@robot.gripper.on("disconnect")
def on_robot_gripper_disconnection():
    socket.emit("robot_gripper_disconnected")

@dgtBoard.dgtConnection.on("connect")
def on_dgt_connection():
    socket.emit("dgt_connected")

@dgtBoard.dgtConnection.on("disconnect")
def on_dgt_disconnection():
    socket.emit("dgt_disconnected")

"""
