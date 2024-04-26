import ChessEngine as ce
import chess as ch
import chessMoveClass 
import Getuci 
import URClass as ur
import SafeVariableClass as safe_v

urclass = ur.URClass()
getuci = Getuci.Getuci()
chess_move_class_object = chessMoveClass.chessMoveClass()
safe_var_class = safe_v.SafeVariableClass()
class mainforChessengine:

    

    def __init__(self, board=chess_move_class_object.virtualBoard):
        self.board = board
        self.board_in_starting_pos = chess_move_class_object.fen()
        self.retry_limit = 10  # Sett en grense for antall rekursive forsøk
        self.moves_history = [None]
        self.white = False
        self.counter = 0
    

    #play human move
    def playHumanMove(self, retry_count=0):
        print("----------------HUMANS TURN------------------")
        if retry_count >= self.retry_limit:
            print("Maximum number of attempts reached. Terminating attempt to make a human move.")
            return
        san = chess_move_class_object.sanMove()  # Start checking if human makes move.

        try:
            
            legal_move_list = chess_move_class_object.legal_moves_to_readable_list(self.board.legal_moves)
            if san not in legal_move_list:
                print("Not a legal move, try again")
                self.playHumanMove(retry_count + 1)
                return
            else:
                self.counter += 1
                # The move is legal
                retry_count = 0
                self.board.push_san(san)
                print(f"Human move done, counter: {self.counter}")
            
                if self.moves_history is not None or self.white==False:
                    self.white = True
                    if self.moves_history[0] == None:
                        self.moves_history.clear()
                    self.moves_history.append(f"'w': {san}")
                else:
                    self.moves_history.append(f"'b': {san}") #Husk å legge til move når menneske spiller svart
                    self.board.push_san(san)
                    

            if legal_move_list is None:
                print("No legal moves was found")
            
            
            
            print("----------------HUMANS DONE------------------")

        except Exception as e:
            print(f"Some error occured: {e}")
            if retry_count < self.retry_limit - 1:  # Prøv på nytt bare hvis vi ikke har nådd grensen
                self.playHumanMove(retry_count + 1)
        
    
        

    #play engine move
    def playEngineMove(self, maxDepth, color):
        engine = ce.Engine(self.board, maxDepth, color)
        return engine
        
    def getEngineMove(self, maxDepth, color): #This return's a UCI!
        engine = ce.Engine(self.board, maxDepth, color)
        bestMove=engine.getBestMove()
        return bestMove


    #start a game
    def startGame(self):
        urclass.moveSimple(urclass.safe_standard_pos)

        current_board_state_fen = str(self.board_in_starting_pos)
        reset = chess_move_class_object.checks_if_board_has_been_reset(self.board,current_board_state_fen)

        # Checks if the board is in startposition
        if reset == True:
            #get human player's color
            color=None

            while(color!="b" and color!="w"):
                color = input("""Play as (type "b" or "w"): """).lower()
            maxDepth=None
            
            while not isinstance(maxDepth, int):
                try:
                    maxDepth = int(input("Choose depth: "))
                except ValueError:
                    print("Please enter a valid integer for depth.")

        
            if color=="b":
                while (self.board.is_checkmate()==False):
                    print("The engine is thinking...")
                    uciForRobot = self.getEngineMove(maxDepth, ch.WHITE) 
                    print(uciForRobot)
                    self.scanBoard1 = chess_move_class_object.fen()
                    from_square=chess_move_class_object.make_uci_first_pos(str(uciForRobot)) #Split's uci into two pieces and grabs the start square
                    to_square=chess_move_class_object.make_uci_last_pos(str(uciForRobot))
                    urclass.moverob(from_square,to_square,'w')
                    self.scanBoard2 = chess_move_class_object.fen()
                    uci = getuci.get_uci(self.scanBoard1,self.scanBoard2)
                    san = chess_move_class_object.uci_move_to_san(uci)
                    self.board.push_san(san)
                    print(f'board rett etter roboten har bevegd seg:\n {self.board}')
                    # print(self.playEngineMove(maxDepth, ch.WHITE)) #This playes the move from the robot engine.
                    self.playHumanMove()
                print(self.board.outcome())    
            
            elif color=="w": #If the human player is 'white', the robot will play as black, and this is the black playerside.
                while (self.board.is_checkmate()==False):
                    safe_backup_fen = chess_move_class_object.fen()
                    try:
                        # When this variable and the board status in real time are the same, the game can continue after fail
                        self.playHumanMove()
                        uciForRobot =   self.getEngineMove(maxDepth, ch.BLACK) #This is the UCI that has to be split up and fed to the robotarm!!
                        print("!!!",uciForRobot)
                        from_square =   chess_move_class_object.make_uci_first_pos(str(uciForRobot)) #Split's uci into two pieces and grabs the start square
                        to_square   =   chess_move_class_object.make_uci_last_pos(str(uciForRobot))
                    except:
                        print(f"Not legal move, {from_square} to {to_square}")
                        print("Continues the game:")
                        break

                    print("----------------ROBOTS TURN-------------------")

                    scanBoard1 = chess_move_class_object.fen()
                    
                    if chess_move_class_object.is_position_occupied(to_square):
                        legal_move_list = chess_move_class_object.legal_moves_to_readable_list(self.board.legal_moves)
                        print("Lovlige trekk for svart:",legal_move_list)
                        self.counter += 1

                        print("rob captures:")
                        print(f"FromSquare: {from_square} and ToSquare: {to_square}")

                        # Captures the piece and moves it's own piece to the square
                        urclass.drop_off_captured_piece("b",from_square,to_square)
                        scanBoard2 = chess_move_class_object.fen()
                        #print(f"Robot move done, counter: {self.counter}")
                        #Need to find a way to push moves like 'Qxd5' which means 'Queen captures d5' and 'Kxf3+' which means Knight captures f3 and checks the king. 
                        uci_disfunctional = getuci.get_uci(scanBoard1, scanBoard2)
                        uci = chess_move_class_object.temp_solution_to_uci_problem(uci_disfunctional)
                        

                        san = chess_move_class_object.uci_move_to_san(uci)
                        print(" Fully working uci: ",uci)
                        print("San-value-robot-capture:",san)
                    else:
                        legal_move_list = chess_move_class_object.legal_moves_to_readable_list(self.board.legal_moves)
                        print("Lovlige trekk for svart:",legal_move_list)
                        self.counter += 1
                        urclass.moverob(from_square,to_square,'b') # Takes in from- and to-square and the robotarm preforms the movement
                        scanBoard2 = chess_move_class_object.fen()
                        #print(f"Robot move done, counter: {self.counter}")
                        uci = getuci.get_uci(scanBoard1,scanBoard2)
                        san = chess_move_class_object.uci_move_to_san(uci)
                        print("San-value-robot-move:",san)
                    
                    
                    #Need to find a way to push moves like 'Qxd5' which means 'Queen captures d5' and 'Kxf3+' which means Knight captures f3 and checks the king. 
                    
                    self.moves_history.append(f"'b': {san}")
                    
                    print(f"\nList og history: {self.moves_history}\n" )
                    self.board.push_san(san)
                    print("----------------ROBOTS DONE-------------------")


            print(self.board.outcome())
            #reset the board
            self.board.reset

            #start another game
            start_new_game = input('Nytt parti, "j" for ja og "n" for nei:')

            if start_new_game == 'j':
                
                curr_state_of_board = str(chess_move_class_object.fen())
                ideal_state_of_board = str(self.board_in_starting_pos)
                if curr_state_of_board == ideal_state_of_board:
                    self.startGame()
                else:
                    print("Fix the pieces")
                    
            elif start_new_game == 'n':
                print('Takk for kampen.')

        else:
            print("Put pieces back to the original position")



