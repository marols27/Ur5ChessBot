import rtde_control #import RTDEControlInterface as RTDEControl
import rtde_receive #import RTDEReceiveInterface as RTDEReceive
from robotiq_gripper_control import RobotiqGripper
import copy
from ToolCenterPoint import ToolCenterPoint as TCP


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
    travelHeight = None
    homePose = None
    connectionIP = None
    acceleration = None
    speed = None
    gripperSpeed = None
    gripperForce = None

    # Interfaces:
    control = None
    info = None
    gripper = None


    # Constructor:
    def __init__(self, travelHeight: float, homePose: TCP, connectionIP: str, acceleration: float, speed: float, gripperSpeed: float, gripperForce: float):
        self.travelHeight = travelHeight
        self.homePose = homePose
        self.connectionIP = connectionIP
        self.acceleration = acceleration
        self.speed = speed
        self.gripperSpeed = gripperSpeed
        self.gripperForce = gripperForce

        # Connection and setup:
        self.control = rtde_control.RTDEControlInterface(connectionIP)
        self.info = rtde_receive.RTDEReceiveInterface(connectionIP)
        self.gripper = RobotiqGripper(self.control)
        self.gripper.activate()
        self.gripper.set_force(gripperForce)  # from 0 to 100 %
        self.gripper.set_speed(gripperSpeed)  # from 0 to 100 %
        self.drop()


    # Methodes:
    def getPos(self):
        self.control.teachMode()
        input("Move the robot to the point and press enter to get the pose...")
        self.control.endTeachMode()
        pose = self.info.getActualTCPPose()
        return pose
        
    def goto(self, pos: "list[float]"):
        try:
            self.control.moveL(pos, self.speed, self.acceleration)
        except:
            if self.control.isConnected():
                self.control.disconnect()
            self.control.reconnect()
            if self.info.isConnected():
                self.info.disconnect()
            self.info.reconnect()
            self.control.moveL(pos, self.speed, self.acceleration)


    def grab(self):
        try:
            self.gripper.move(6)
        except:
            if self.control.isConnected():
                self.control.disconnect()
            self.control.reconnect()
            if self.info.isConnected():
                self.info.disconnect()
            self.info.reconnect()
            self.gripper.activate()
            self.gripper.set_force(self.gripperForce)  # from 0 to 100 %
            self.gripper.set_speed(self.gripperSpeed)  # from 0 to 100 %
            self.gripper.move(37)
            self.gripper.move(6)


    def drop(self):
        try:
            self.gripper.move(37)
        except:
            if self.control.isConnected():
                self.control.disconnect()
            self.control.reconnect()
            if self.info.isConnected():
                self.info.disconnect()
            self.info.reconnect()
            self.gripper.activate()
            self.gripper.set_force(self.gripperForce)  # from 0 to 100 %
            self.gripper.set_speed(self.gripperSpeed)  # from 0 to 100 %
            self.gripper.move(37)

    def home(self):
        self.goto(self.homePose.TCP)

    def movePiece(self, fromPos: "list[float]", toPos: "list[float]", home = True):
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

    def capturePiece(self, fromPos: "list[float]", toPos: "list[float]", capturePos: "list[float]"):
        aboveToPos = copy.deepcopy(toPos)
        aboveToPos[2] += self.travelHeight
        self.goto(aboveToPos)
        self.goto(toPos)
        self.grab()
        self.goto(aboveToPos)
        self.goto(capturePos)
        self.drop()
        self.movePiece(fromPos, toPos)
    
    def enPassent(self, fromPos: "list[float]", toPos: "list[float]", targetPos: "list[float]", capturePos: "list[float]"):
        self.movePiece(fromPos, toPos, False)
        self.movePiece(targetPos, capturePos)

    def castle(self, fromPosKing: "list[float]", toPosKing: "list[float]", fromPosRook: "list[float]", toPosRook: "list[float]"):
        self.movePiece(fromPosKing, toPosKing, False)
        self.movePiece(fromPosRook, toPosRook)
    
    def promotion(self, fromPos: "list[float]", capturePos: "list[float]"):
        self.movePiece(fromPos, capturePos)
        # Request piece promotion.
    
    def capturePromotion(self, fromPos: "list[float]", toPos: "list[float]", capturePos: "list[float]"):
        self.movePiece(fromPos, capturePos, False)
        self.movePiece(toPos, capturePos)
        # Request piece promotion.

    if __name__ == '__main__':
        pass