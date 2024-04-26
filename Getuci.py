
class Getuci:

    def __init__(self) -> None:
        pass
    

    #Transform the board to uci, chess.Board --> 'e2e4'
    def get_uci(self,board1, board2):

        nums = {1:"a", 2:"b", 3:"c", 4:"d", 5:"e", 6:"f", 7:"g", 8:"h"}

        str_board = str(board1).split("\n")
        str_board2 = str(board2).split("\n")
        move = ""
        who_moved = "w"
        flip = False
        if who_moved == "w":
            for i in range(8)[::-1]:
                for x in range(15)[::-1]:   
                    if str_board[i][x] != str_board2[i][x]:
                        if str_board[i][x] == "." and move == "":
                            flip = True
                        move+=str(nums.get(round(x/2)+1))+str(9-(i+1))
        else:
            for i in range(8):
                for x in range(15):
                    if str_board[i][x] != str_board2[i][x]:
                        if str_board[i][x] == "." and move == "":
                            flip = True
                        move+=str(nums.get(round(x/2)+1))+str(9-(i+1))
        if flip:
            move = move[2]+move[3]+move[0]+move[1]
        return move
