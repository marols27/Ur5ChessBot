import asyncio
import asyncdgt
import ChessEngine as ce
import chess
import time
import Getuci as gu

## This is a class with many different methods and functions. Not everything here is in use
class chessMoveClass:

    getuci=gu.Getuci()

    def __init__(self):
        self.virtualBoard=chess.Board()#Creates a viritual board which follows every moves and gets updatet whenever a move is beeing taken. 
        #This makes it posible to get a overview over the legal moves and these sorts of thing on the way. 


    def compare_two_values(self, gammelt_svar, nytt_svar): #Compares two inputs. This is to make the counter go up, since we want it to break the while loop after 2 itterations.
        if gammelt_svar != nytt_svar:
            return True
        else:
            return False


    def checks_if_board_has_been_reset(self, board1, fen_string):
        for i, j in zip(str(board1), str(fen_string)):
            if i != j:
                return False

        return True


    # This function makes sure the move you make isn't mistaken, in case you wanted to move the piece to another spot.
    def get_safe_move(self, input1, input2): #Wait's 3 seconds before getting the UCI
        self.input1 = input1
        self.input2 = input2
        loop = asyncio.get_event_loop()
        dgt = asyncdgt.auto_connect(loop, ["/dev/ttyACM*"])
        # b_old = loop.run_until_complete(dgt.get_board()) 
        self.input1 = loop.run_until_complete(dgt.get_board()) 

        while True:
            last_change_time = time.time()
            while True:
                self.input2 = loop.run_until_complete(dgt.get_board()) 
                last_input2 = self.input2

                if self.input1 != last_input2:
                    last_change_time = time.time()
                    self.input1 = last_input2
                
                #Wait's three seconds before confirming the move.
                elif self.input1==last_input2 and time.time() - last_change_time >= 1.5: 
                    #Checks if the piece has been in the same place for 3 seconds or more
                    boardStatusLast = loop.run_until_complete(dgt.get_board()) 
                    return boardStatusLast


    def reads_human_uci(self): #Returns UCI. 
        loop = asyncio.get_event_loop()
        dgt = asyncdgt.auto_connect(loop, ["/dev/ttyACM*"]) #Gets the board status. 
        counter = 1
        # Get board twice
        b_old = loop.run_until_complete(dgt.get_board()) 
        B_old = loop.run_until_complete(dgt.get_board())

        while counter%3 !=0: #Ends when player gives two different board states.
            b_new = loop.run_until_complete(dgt.get_board())


            if self.compare_two_values(b_old,b_new) ==True:
                b_old=b_new
                counter+=1
                
            elif self.compare_two_values(B_old,b_old)==False: #This compares the two boards, old and new, and if there is a difference, the whileloop will loop once!.
                # When the board is changed, for instance: a piece has been picked up, it loop's once.
                counter=1
                
            time.sleep(0.01)
        b_old=B_old
        uci = self.getuci.get_uci(b_old, self.get_safe_move(b_old,b_new))#uses class Getuci.py to calculate the uci. 
        print("uci from reads_human_uci:",uci)
        #Also it takes in the  function get_safe_move ^. This makes it posible to slide the pieces. 
        if uci!="":

            # print(uci) #Print's out the uci, 'b2b4'
            if len(uci)>5:

                print('To long string')
            else:
                return uci 
        b_old=b_new

        
    def fen(self):
        loop = asyncio.get_event_loop()
        dgt = asyncdgt.auto_connect(loop, ["/dev/ttyACM*"]) #Gets the board status. 
        return loop.run_until_complete(dgt.get_board()) 


    def sanMove(self): 
        # returns the final SAN
        return self.uci_move_to_san(self.reads_human_uci())


    #NB!: Need's to check up against legal moves before executing
    def uci_move_to_san(self,uci_move): #Takes in the UCI and transform it to SAN value
        self.testUCI = uci_move
        fra = self.testUCI[:2] # Splits the uci-value into two, so we can put it in the move variable. The chess.Move() takes in two inputs, from-square and to-square.
        til = self.testUCI[2:]
        move=chess.Move(fra,til)
        print("")
        move=move.from_uci(self.testUCI)
        san = self.virtualBoard.san(move) # This is the san value which we use to feed the chess engine.
        return san
    

    def make_uci_first_pos(self, startUCI): #Splits the uci to get start square
        self.startuci=startUCI
        fra = self.startuci[:2]
        return fra
    

    def make_uci_last_pos(self,sluttUCI):#Splits the uci to get end square
        self.sluttuci = sluttUCI
        til= self.sluttuci[2:]
        return til
    

    def robotmakesmoveDone(self, firstBoard, secondBaord):
        self.firstBoard = firstBoard
        self.secondboard = secondBaord
        uci = self.getuci.get_uci(self.firstBoard,self.secondboard)
        san = self.uci_move_to_san(uci)
        self.virtualBoard.push_san(san)
        print(self.virtualBoard.push_san(san))
    

    def is_position_occupied(self, position):
        # Sjekk om en bestemt posisjon er opptatt ved å se på brettet
        piece = self.virtualBoard.piece_at(chess.SQUARE_NAMES.index(position))
        return piece is not None


    def execute_move(self, start_pos, end_pos):
        # Sjekk om målposisjonen er opptatt
        if self.is_position_occupied(end_pos):
            print(f"Målposisjon {end_pos} er opptatt. Fjerner brikken.")
            # Kode for å fysisk fjerne brikken fra brettet med robotarmen

        # Kode for å flytte brikken fra start_pos til end_pos med robotarmen
        print(f"Flytter brikke fra {start_pos} til {end_pos}.")


    def legal_moves_to_readable_list(self, legal_moves: object):
        
        legal_move_str = str(legal_moves)
        if legal_move_str is None:
            return []
        legal_move_str = legal_move_str.split('(')[1]
        legal_move_str = legal_move_str.split(')')[0]
        legal_move_str = legal_move_str.split(',')
        cleaned_moves = [move.strip() for move in legal_move_str]
        return cleaned_moves
        # Skriver ut den rensede listen og hvert element i listen


    def temp_solution_to_uci_problem(self, disfunctional_uci):
        
        uci = disfunctional_uci[2:]+disfunctional_uci[:2]
        return uci






    if __name__=='__main__':
        pass



