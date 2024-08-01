import chess.pgn
from UR5Feature import UR5Feature
from ToolCenterPoint import ToolCenterPoint as TCP
import chess

class Board():
    # CLASS DOCCUMENTATION:
    # Fields:
    # - boardSize: The board length and with measured in meter.
    # - boardHeight: The board height measured in meter.
    # - squareSize: The boards squares with and length measured in meter.
    # - kingHeight: The height of the tallest piece on the board measured in meter.
    # - loop: (Not quite sure) Some kind of asyncronus task processing variable.
    # - dgtBoard: The asyncronus connection task to the physical board.
    # - feature: A feature object for keeping track of the boards pose relative to the robot.
    #            "this is used to in a more easy way calculate the pieces' positions on the board during playtime."
    # - board: A viritual clone of the board, keeping track of the physical state of the board. (Might not be nessecary).
    # - history: A list keeping track of every leegal move don since the start of the program. (need to be resett whith each new game)
    # - previousState: Keeps track of the previous legal move done on the board.
    
    # Constructor:
    # __init__(startFen, featureOriginTCP, featureXAxisTCP, featureXYPlaneTCP): 
    #       Creates a new Board object, and populates the history, and previousState with the startFen, 
    #       and initializes the feature using the 3 TCP objects passed in the constructor.

    # Event handlers:
    # - on_connected(port): Feedback for the dgt board connection.
    # - on_disconnected(): Feedback for the dgt board disconnection.
    # - on_board_change(): Feed for uppdating the board state in the program based on updates from the board.

    # Methods:
    # - getSquareTCP(pos): Expects a string of 2 caracters (file letters and rank numbers) in the format "[a-h][1-8]" 
    #                      and returns the position coordinates for the square for the robot to move to.
    # - getUCI(board): Returns a Universal Chess Interface move string, by comparing a new board layout with the current.
    # - push(UCI): Updates the board with the new move.
    # - getPGN(): Returns a PGN list of moves as a history of moves for a game.




    # Fields:
    

    # Constructor:
    def __init__(
            self, startFen: str,
            boardSize: float = 0.54, 
            boardHeight: float = 0.02,
            squareSize: float = 0.055,
            tallestPieceHeight: float = 0.098,
            featureOriginTCP: TCP = TCP([0.030438048986547096, 0.41930054103456266, 0.15122225475964543, -1.3275419080602613, -2.840664168295585, 0.04405738075098039]),
            featureXaxisTCP: TCP = TCP([0.25330442778386353, 0.11336284736003377, 0.14728839080090772, -1.3783928523104927, -2.8187597113837213, -0.05747344058811938]),
            featureXYPlaneTCP: TCP = TCP([0.33428968912697665, 0.6475493468855537, 0.15513260502163922, -0.9816732580188312, 2.963418514873813, -0.016564578264027296])
        ):
        self.boardSize = boardSize      # m
        self.boardHeight = boardHeight  # m
        self.squareSize = squareSize    # m
        self.tallestPieceHeight = tallestPieceHeight    # m
        self.feature: UR5Feature = UR5Feature(featureOriginTCP, featureXaxisTCP, featureXYPlaneTCP)
        self.board: chess.Board = chess.Board(fen=startFen)
        
        legalMoves: "list[chess.Move]" = list(self.board.legal_moves)
        self.legalMoves: "list[str]" = []
        for i in legalMoves:
            x = str(i)
            x.replace("Move.from_uci('", "")
            x.replace("')", "")
            self.legalMoves.append(x)

    # Methods
    def getSquareTCP(self, boardPos: str) -> TCP:
        if boardPos[0].lower() == "a":
            file = 1
        elif boardPos[0].lower() == "b":
            file = 2
        elif boardPos[0].lower() == "c":
            file = 3 # returns the final SAN
        elif boardPos[0].lower() == "d":
            file = 4
        elif boardPos[0].lower() == "e":
            file = 5
        elif boardPos[0].lower() == "f":
            file = 6
        elif boardPos[0].lower() == "g":
            file = 7
        elif boardPos[0].lower() == "h":
            file = 8
        rank = int(boardPos[1])
        return self.feature.getFeatureRelativeTCP(self.squareSize * (file - 1), self.squareSize * (rank - 1), 0)
    
    # Not finished, to do list:
    # - Implement the casteling case.
    def getUCI(self, toBoard: str) -> str:
        files = {1:"a", 2:"b", 3:"c", 4:"d", 5:"e", 6:"f", 7:"g", 8:"h"}

        fromBoard = str(self.board).split("\n")
        for i in range(len(fromBoard)):
            fromBoard[i] = fromBoard[i].split(" ")
        
        toBoard = toBoard.split("\n")
        for i in range(len(toBoard)):
            toBoard[i] = toBoard[i].split(" ")
        

        # List of dictionaries in the form {file, rank, before, after}
        changedSquares: "list[dict]" = []
        for x in range(1, 8):
            for y in range(1, 8):
                if fromBoard[8-y][x-1] != toBoard[8-y][x-1]:
                    changedSquares.append({"file":x, "rank":y, "before":fromBoard[8-y][x-1], "after":toBoard[8-y][x-1]})


        uci = ""
        # Picked upp piece case
        if len(changedSquares) == 1:
            return changedSquares[0]

        # Normal move case (with promotion handling)
        if len(changedSquares) == 2:
            # Checking spechial non complete move cases
            movingPawn = changedSquares[0]["before"].lower() == "p" or changedSquares[1]["before"].lower() == "p"
            changingFiles = changedSquares[0]["file"] != changedSquares[1]["file"]
            enPassentMove = changedSquares[0]["before"] == changedSquares[1]["after"] and changedSquares[0]["after"] == changedSquares[1]["before"]

            notCompletedMoveCases = [
                changedSquares[0]["after"] == changedSquares[1]["after"], # "During a capture, both squares has to be emptied during piece moving"
                movingPawn and changingFiles and enPassentMove
            ]
            if True in notCompletedMoveCases:
                return None

            if changedSquares[0]["after"] == ".":
                uci += files[changedSquares[0]["file"]]
                uci += str(changedSquares[0]["rank"])
                uci += files[changedSquares[1]["file"]]
                uci += str(changedSquares[1]["rank"])
                movedPieceIsPawn = changedSquares[0]["before"].lower() == "p"
                movedPieceWasPromoted = changedSquares[1]["after"].lower() != "p"
                if movedPieceIsPawn and movedPieceWasPromoted:
                    uci += changedSquares[1]["after"].lower()
            else:
                uci += files[changedSquares[1]["file"]]
                uci += str(changedSquares[1]["rank"])
                uci += files[changedSquares[0]["file"]]
                uci += str(changedSquares[0]["rank"])
                movedPieceIsPawn = changedSquares[1]["before"].lower() == "p"
                movedPieceWasPromoted = changedSquares[0]["after"].lower() != "p"
                if movedPieceIsPawn and movedPieceWasPromoted:
                    uci += changedSquares[0]["after"].lower()
            return uci
        
        # En passent move case
        if len(changedSquares) == 3:
            fromRank = []
            moveToSquare = None
            assaultingSquare = None
            for i in changedSquares:
                if i["before"].lower() == "p":
                    fromRank.append(i)
                else:
                    moveToSquare = i
            
            if fromRank.len != 2:
                return None
            
            fromRankACheck = fromRank[0]["before"].lower() == "p" and fromRank[0]["after"] == "."
            fromRankBCheck = fromRank[1]["before"].lower() == "p" and fromRank[1]["after"] == "."
            moveToSquareCheck = moveToSquare["before"] == "." and moveToSquare["after"].lower() == "p"
            enPassentMove = fromRankACheck and fromRankBCheck and moveToSquareCheck
            if not enPassentMove:
                return None # "ERROR: 3 Changes on the board was made, but no en passent move detected!"
            else:
                assaultingSquare = fromRank[0] if fromRank[0]["file"] != moveToSquare["file"] else fromRank[1]
                uci += files[assaultingSquare["file"]]
                uci += str(assaultingSquare["rank"])
                uci += files[moveToSquare["file"]]
                uci += str(moveToSquare["rank"])
                return uci
                
            

        # Castle move case
        if len(changedSquares) == 4:
            pass
        return None

    def push(self, uci):
        self.board.push(uci)
        legalMoves: "list[chess.Move]" = list(self.board.legal_moves)
        self.legalMoves: "list[str]" = []
        for i in legalMoves:
            x = str(i)
            x.replace("Move.from_uci('", "")
            x.replace("')", "")
            self.legalMoves.append(x)

    def getPGN(self):
        return chess.pgn.Game()