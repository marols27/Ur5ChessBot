from Board import Board
import chess
import chess.engine
from DGTBoard import DGTBoard
import json
from ToolCenterPoint import ToolCenterPoint as TCP
from UR5Robot import UR5Robot

class ChessGameEnvironment():
    # This class consist of the underlying elements that we are using in our settup.
    # this might get changed in the future to be personalizable to the settups that others might have,
    # but for now it consists of the board, robot, captured pieces spot.
    # The plan is to make this class the overall object / class of the entire settup, and make this class
    # handle al the logic between the different elements in the chess playin environments, including the GUI interface
    # we plan to have on a touch screen, next to and included in our system settup.

    # DOCUMENTATION:
    # Fields: 
    # - Board:      
    #       An object that keeps track of the board related components of the environments, 
    #       like the position of the pieces and, legal moves.
    # - Robot:
    #       An object that keep track of all info acording the UR5 Robot, 
    #       and the movement functions for easier use in the environment.  
    # - capturePos:
    #       Currently a TCP for dropping of captured pieces. 
    #       The plan is to create a table class to keep track of captured pieces and add pawn promotion functionality for the robot.

    # Constructor:
    # __init__():
    #   currently empty constructor. 




    # Fields
    engine = chess.engine.SimpleEngine.popen_uci(r"/home/rocotics/Desktop/Ur5CessBot/Ur5ChessBot/Rebuild/stockfish-ubuntu-x86-64-sse41-popcnt/stockfish/src/stockfish") 

    # Constructor:
    def __init__(self, startingFen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1") -> None:
        self.dgtBoard = DGTBoard()
        self.startingFen = self.strBoardToFenBoard(self.dgtBoard.getCurentBoard()) + " w KQkq - 0 1"
        while self.startingFen != startingFen:
            input("Please place your peces in the corect starting setup and confirm setup...")
            self.startingFen = self.strBoardToFenBoard(self.dgtBoard.getCurentBoard()) + " w KQkq - 0 1"
        print("Board settup has been verified")
        self.board = Board(startFen=self.startingFen)
        self.robot = UR5Robot(self.board)
        self.capturePos = TCP([0.5309219723931501, 0.02908272224209137, 0.4360150516473804, 2.147942236187428, 2.199250328744319, 0.1209011611924127])


        #Event Handlers:
        @self.dgtBoard.dgtConnection.on("connected")
        def onConnection(port):
            print(f"Board connected at {port}")

        @self.dgtBoard.dgtConnection.on("disconnected")
        def onDisconnection():
            print("Board disconnected")

        @self.dgtConnection.on("board")
        def onBoardChange(board):
            print(str(board))
            self.updatingDGTBoard = str(board)
            self.updatingUCI = self.getUCI(self.dgtBoard, self.updatingDGTBoard)
            move = {
                "dgtBoardFEN": self.strBoardToFenBoard(str(board)),
                "isLegal": self.updatingUCI in self.legalMoves,
                "turn": self.turn
            }
            print(json.dumps(move)) # send 
            if self.updatingUCI in self.legalMoves:
                cmd = input("Confirm y or n?\n")
                if cmd == "y":
                    print("Confirmed")
                    onConfirmMove()
                else:
                    print("Denied")

        #@userFeedback.on("confirmMove")
        def onConfirmMove():
            self.turn = not self.turn
            self.dgtBoard = self.updatingDGTBoard
            self.board.push(chess.Move.from_uci(self.updatingUCI))
            legalMoves: "list[chess.Move]" = list(self.board.legal_moves)
            self.legalMoves = []
            for i in legalMoves:
                x = str(i)
                x.replace("Move.from_uci('", "")
                x.replace("')", "")
                self.legalMoves.append(x)
            history = chess.pgn.Game()
            self.pgnStory = history
            pgn = {"pgn": history}
            # socket.emit("pgn")


    #Methods:
    def strBoardToFenBoard(self, strBoard: str) -> str:
        strBoard = strBoard.split("\n")
        for i in range(len(strBoard)):
            strBoard[i] = strBoard[i].split(" ")

        fen = ""
        emptySpacesCounter = 0
        for y in range(len(strBoard)):
            for x in range(len(strBoard[y])):
                if strBoard[y][x] != ".":
                    if emptySpacesCounter > 0:
                        fen += str(emptySpacesCounter)
                        emptySpacesCounter = 0
                    fen += strBoard[y][x]
                else:
                    emptySpacesCounter += 1
                    if x == 7:
                        fen += str(emptySpacesCounter)
                        emptySpacesCounter = 0
            if y < 7:
                fen += "/"
        return fen
    
    def playRobotMove(self):
        result = self.engine.play(self.board, chess.engine.Limit(time=0.1))
        self.board.push(result.move)


