
import chess.pgn
from Board import Board
from UR5Robot import UR5Robot
import asyncdgt
import asyncio
import chess
from stockfish import Stockfish
from ChessGameEnvironment import ChessGameEnvironment
import time

#board = chess.Board(fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
import asyncio
import chess
import chess.engine

"""async def main() -> None:
    transport, engine = await chess.engine.popen_uci(r"/home/rocotics/Desktop/Ur5CessBot/Ur5ChessBot/Rebuild/stockfish-ubuntu-x86-64-sse41-popcnt/stockfish/src/stockfish") 

    board = chess.Board()
    while not board.is_game_over():
        result = await engine.play(board, chess.engine.Limit(time=0.1))
        board.push(result.move)

    await engine.quit()

asyncio.run(main())"""

engine = chess.engine.SimpleEngine.popen_uci(r"/home/rocotics/Desktop/Ur5CessBot/Ur5ChessBot/Rebuild/stockfish-ubuntu-x86-64-sse41-popcnt/stockfish/src/stockfish") 

board = chess.Board()
while not board.is_game_over():
    print(board)
    result = engine.play(board, chess.engine.Limit(time=0.1))
    print(type(result.move))
    board.push(result.move)

print(board)
engine.quit()