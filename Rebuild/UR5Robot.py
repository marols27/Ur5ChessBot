import rtde_control #import RTDEControlInterface as RTDEControl
import rtde_receive #import RTDEReceiveInterface as RTDEReceive
from robotiq_gripper_control import RobotiqGripper
import copy


#import Getuci
#import SafeVariableClass

class UR5Robot:
    # CLASS DOCUMENTATION:
    # This is a class containing the  UR5 robots conections, settings and methods for moving the robot.
    
    # Fields:
    # - controll:   Interface for driving the robot
    # - info:       Interface for getting the robots current information
    # - gripper:    Interface for driving the gripper
    # - speed:      Robot driving speed
    # - acceleration:   Robot driving acceleration
    # - travelHeight:   Robot driving height above the chess board

    # Constructor:
    #  - __init__(
    #           travelHeight, 
    #           conectionIP: str = "172.31.1.144", 
    #           gripperForce: float = 50, 
    #           gripperSpeed: float = 100, 
    #           speed: float = 0.09, 
    #           acceleration: float = 0.1
    # ): Constructs a robot conected object, 
    
    # Functions:
    # - recalibrateFeature(): Robot functionality for feature recalibration. Returns 3 Tool center points.
    # - moveByUCI(uciMove): Performs any chess move by the uci string.
    #
    # # BASIC MOVEMENT:
    # - goto(pos): Makes the robot make a simple move to the specified pos.
    # - grab(): Makes the robot close the gripper to pick upp a piece.
    # - drop(): Makes the robot open the gripper to drop a piece.
    #
    # # COMBINED MOVEMENT:
    # - movePiece(fromPos, toPos): Makes a ordinary chess piece move.
    # - capturePiece(fromPos, toPos, capturePos): Captures a piece, and makes an ordinary chess piece move afterwords.
    #
    # 


    # Fields:
    

    # Constructor:
    def __init__(self, travelHeight, conectionIP: str = "172.31.1.144", gripperForce: float = 50, gripperSpeed: float = 100, speed: float = 0.25, acceleration: float = 0.1):
        print("Connecting to robot...")
        self.controll = rtde_control.RTDEControlInterface(conectionIP)
        self.info = rtde_receive.RTDEReceiveInterface(conectionIP)
        self.gripper = RobotiqGripper(self.controll)
        print("Connected sucsessfuly to robot!")
        self.gripper.set_force(gripperForce)  # from 0 to 100 %
        self.gripper.set_speed(gripperSpeed)  # from 0 to 100 %
        self.speed = speed
        self.acceleration = acceleration
        self.travelHeight = travelHeight
        # Må ikke endre noe på variablene over, det kan skape en kjedereaksjon med alle funksjonene


    # Methodes:
    def recalibrateFeature(self):
        self.drop()
        self.controll.teachMode()
        input("Move the robot to the first calibration point and press enter...")
        originPose = self.info.getActualTCPPose()
        input("Move the robot to the seccond calibration point and press enter...")
        xAxisPose = self.info.getActualTCPPose()
        input("Move the robot to the third calibration point and press enter...")
        xyplanePose = self.info.getActualTCPPose()
        input("Move the robot away and press enter to finish calibration...")
        self.controll.endTeachMode()
        return [originPose, xAxisPose, xyplanePose]
    
    def moveByUCI(self, uciMove):
        uci = [uciMove[:2], uciMove[2:4]]
        if len(uciMove) == 4:
            uci.append(None)
        else:
            uci.append(uciMove[4])
        print(uci)
    
    def goto(self, pos): # Move to specified position 
        self.controll.moveL(pos, self.speed, self.acceleration)

    def grab(self): # Grab piece 
        self.gripper.move(6)

    def drop(self): # Let go of piece
        self.gripper.move(37)

    def home(self): # Move to a presett home pose
        self.goto([-0.01502896027794896, 0.16225169818269464, 0.4566147854450882, -1.456142795245294, -2.760610691602006, -0.04964717445743023])

    def movePiece(self, fromPos, toPos, home = True): # Move a piece on the board from fromPos to toPos
        aboveFromPos = copy.deepcopy(fromPos)
        aboveFromPos[2] += self.travelHeight
        aboveToPos = copy.deepcopy(toPos)
        aboveToPos[2] += self.travelHeight
        self.goto(aboveFromPos)
        self.goto(fromPos)
        self.grab()
        self.goto(aboveFromPos)
        self.goto(aboveToPos)
        self.goto(toPos)
        self.drop()
        self.goto(aboveToPos)
        if home:
            self.home()

    def capturePiece(self, fromPos, toPos, capturePos): # Capture a piece at the toPos pose and move a piece on the board from fromPos to toPos
        self.movePiece(toPos, capturePos, False)
        self.movePiece(fromPos, toPos)
    
    def enPassent(self, fromPos, toPos, targetPos, capturePos):
        self.movePiece(fromPos, toPos, False)
        self.movePiece(targetPos, capturePos)

    def castle(self, fromPosKing, toPosKing, fromPosRook, toPosRook):
        self.movePiece(fromPosKing, toPosKing, False)
        self.movePiece(fromPosRook, toPosRook)

    if __name__ == '__main__':
        pass