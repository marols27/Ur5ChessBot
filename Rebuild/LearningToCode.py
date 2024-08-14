import chess
import chess.pgn

game = chess.pgn.Game()
game.headers["Event"] = "Chess Game"
node = game.add_variation(chess.Move.from_uci("e2e4"))
node = node.add_variation(chess.Move.from_uci("e7e5"))
print(str(node.game()))