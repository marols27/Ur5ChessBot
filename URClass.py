import rtde_control #import RTDEControlInterface as RTDEControl
import rtde_receive #import RTDEReceiveInterface as RTDEReceive
from robotiq_gripper_control import RobotiqGripper
import Getuci
import SafeVariableClass

class URClass:
    getuci = Getuci.Getuci()
    object_safeMoveChess = SafeVariableClass.SafeVariableClass()
    safe_standard_pos =object_safeMoveChess.standard_pos_idle # Waiting position
    safe_var = SafeVariableClass.SafeVariableClass()

    def __init__(self):
        self.rtde_c = rtde_control.RTDEControlInterface("172.31.1.144")
        self.rtde_r = rtde_receive.RTDEReceiveInterface("172.31.1.144")
        self.gripper = RobotiqGripper(self.rtde_c)
        self.gripper.set_force(50)  # from 0 to 100 %
        self.gripper.set_speed(100)  # from 0 to 100 %
        self.speed = 0.09
        self.acceleration = 0.1
        self.gripper.move(30) 
        self.senke_høyne_variabel   =   self.object_safeMoveChess.h8__sentrum_kingheight[2]
        # Må ikke endre noe på variablene over, det kan skape en kjedereaksjon med alle funksjonene
        

    def moveSimple(self, pos):
        idlePos = self.rtde_c.moveL(pos)


    def moverob(self, a, b, color):
        self.color = color
        self.gripper.move(30)
        self.startSquare = a
        self.endSquare = b
        
        self.rtde_c.moveL(self.safe_standard_pos,self.speed,1.2,False)
        if self.color=='w':
            sjakkbrikke = self.getPositionForWhite(self.startSquare)
        elif self.color == 'b':
            sjakkbrikke = self.getPositionForBlack(self.startSquare)

        self.rtde_c.moveL(sjakkbrikke,self.speed,1.2,False)
        sjakkbrikke[2] = self.object_safeMoveChess.h8__sentrum_kingheight[2]+0.01 # index 2 is the height of the king, and adds 0.05 so the gripperfingers dont crush the table
        self.rtde_c.moveL(sjakkbrikke,self.speed,1.2,False)
        self.gripper.move(8)
        sjakkbrikke[2]=self.object_safeMoveChess.h8_high[2]
        self.rtde_c.moveL(sjakkbrikke,self.speed,1.2,False)
        
        if self.color == 'w':
            sjakkbrikke = self.getPositionForWhite(self.endSquare)
        elif self.color == 'b':
            sjakkbrikke = self.getPositionForBlack(self.endSquare)

        self.rtde_c.moveL(sjakkbrikke,self.speed,1.2,False)
        sjakkbrikke[2] = self.object_safeMoveChess.h8__sentrum_kingheight[2]+self.safe_var.sligtly_ut_to_not_hit_the_board_with_gripper_fingers # A little higher than the pickup so it doesnt crush the piece into the board
        self.rtde_c.moveL(sjakkbrikke,self.speed,1.2,False)
        self.gripper.move(30)
        sjakkbrikke[2] = self.object_safeMoveChess.h8_high[2]
        self.rtde_c.moveL(sjakkbrikke,self.speed,1.2,False)
        self.rtde_c.moveL(self.safe_standard_pos,self.speed,1.2,False)
    

    def drop_off_captured_piece(self, color, piece_to_be_moved, captured_piece):
            # Startposisjon for slipp-punkt, basert på h8's posisjon, men 15cm (0.15m) til venstre
            # og litt forhøyet for å sikre at brikken slippes trygt.
            # Anta at h8's x- og y-posisjon er startpunktet.
            dropoff_point = SafeVariableClass.SafeVariableClass.trashcan
            dropoff_point[2] = self.object_safeMoveChess.h8_high[2]+0.15
            if color=='b':
                # This uses the 'safe_v.h8_sentrum_høy' variable in SafeVariableClass
                sjakkbrikke = self.getPositionForBlack(captured_piece)
                black_piece_hover = self.getPositionForBlack(piece_to_be_moved)

            self.rtde_c.moveL(sjakkbrikke,self.speed,1.2,False)
            sjakkbrikke[2] = self.object_safeMoveChess.h8__sentrum_kingheight[2]+0.01 # lower to pick up piece
            self.rtde_c.moveL(sjakkbrikke,self.speed,1.2,False)
            self.gripper.move(8)
            sjakkbrikke[2]=self.object_safeMoveChess.h8_high[2]
            self.rtde_c.moveL(sjakkbrikke,self.speed,1.2,False)
            self.rtde_c.moveL(dropoff_point, self.speed, 1.2, False)
            # Åpne gripperen for å slippe brikken
            self.gripper.move(30)  # Juster verdi basert på gripperens åpningsgrad for å slippe brikken
            black_piece_hover[2] = self.object_safeMoveChess.h8_high[2]
            self.rtde_c.moveL(black_piece_hover,self.speed,1.2,False)
            
            # Returnere til sikkerhetsposisjon etter slipp
            if color == 'b':
                sjakkbrikke = self.getPositionForBlack(piece_to_be_moved)

            sjakkbrikke[2] = self.object_safeMoveChess.h8__sentrum_kingheight[2]+0.01
            self.rtde_c.moveL(sjakkbrikke,self.speed,1.2,False)
            self.gripper.move(8)
            sjakkbrikke[2]=self.object_safeMoveChess.h8_high[2]
            self.rtde_c.moveL(sjakkbrikke,self.speed,1.2,False)

            if color == 'b':
                sjakkbrikke = self.getPositionForBlack(captured_piece)

            self.rtde_c.moveL(sjakkbrikke,self.speed,1.2,False)
            sjakkbrikke[2] = self.object_safeMoveChess.h8__sentrum_kingheight[2]+self.safe_var.sligtly_ut_to_not_hit_the_board_with_gripper_fingers #So the robot doesnt break the board
            self.rtde_c.moveL(sjakkbrikke,self.speed,1.2,False)
            self.gripper.move(30)
            sjakkbrikke[2] = self.object_safeMoveChess.h8_high[2]
            self.rtde_c.moveL(sjakkbrikke,self.speed,1.2,False)
            self.rtde_c.moveL(self.safe_standard_pos,self.speed,1.2,False)





    #+ frem, - tibake      
    #+ venstre, - høyre        
    #+ opp, - ned 
    #This gets the positions if the robotarm plays as 'white'
    def getPositionForWhite(self, brikkePos):        
        self.chess_orgin = self.object_safeMoveChess.h8_high
        self.length = 0.055
        self.chessboard_dict ={}
        list_pos = ['a','b','c','d','e','f','g','h']
        #Creating a 8x8 chess map

        for i in range(8):
            for j in range(8):
                postion = f"{list_pos[i]}{j+1}"
                x = self.chess_orgin[0]+j*self.length
                y = self.chess_orgin[1]-i*self.length
                z = self.chess_orgin[2]
                Rx= self.chess_orgin[3]
                Ry= self.chess_orgin[4]
                Rz= self.chess_orgin[5]
                self.chessboard_dict[postion] = [x,y,z,Rx,Ry,Rz]
        pos_a1 = self.chessboard_dict.get(brikkePos)
        return pos_a1
    
    
    #This gets the positions if the robotarm plays as 'black'
    def getPositionForBlack(self, brikkePos):
        self.chess_orgin = self.object_safeMoveChess.h8_high 
        self.length = 0.055
        self.chessboard_dict ={}
        list_pos = ['a','b','c','d','e','f','g','h']        # [+ frem, - tibake   ,   + venstre, - høyre    ,    + opp, - ned , ... ,]
        #Creating a 8x8 chess map
        for i in range(8):
            for j in range(8):
                postion = f"{list_pos[7-i]}{8-j}"
                x = self.chess_orgin[0]+j*self.length
                y = self.chess_orgin[1]-i*self.length
                z = self.chess_orgin[2]
                Rx= self.chess_orgin[3]
                Ry= self.chess_orgin[4]
                Rz= self.chess_orgin[5]
                self.chessboard_dict[postion] = [x,y,z,Rx,Ry,Rz]
        pos_a1 = self.chessboard_dict.get(brikkePos)
        return pos_a1


    if __name__ == '__main__':
        pass