# Chess playing robot

##### This project's is about getting a UR5e robotarm to play chess against you. We have a DGT-board and a UR5e robot to disposition.
##### The code for this project is divided in two. We have the `chess-python` code and `ur5e-code`. 
#
### Program's I've been using
* Python
* Fusion 360
* VMware Workstation 16 Player
* Bambu Studio
#
### What the project is currently doing:
It can almost play chess by itself with a human opponent. 
* It can get the state of the DGT board and translate it into SAN and UCI values, which is very usefull to push a move or give instructions to robotarm. 
* The robotarm knows every chess-square, and can move to all of them and pick and place the pieces. The only input needed is the UCI, `b2b4`, which is beeing devided into two variables by two different function's.
+ Choose degree of difficulty (2 --> 10) and color ('white' or 'black').
+ You can play chess against the robot, but it can't capture pieces.
+ It has a gripper, but it need some improvement.
#
### What the project needs:
* Get a way to accept captures, and this is the same issue as the one over. This goes on in the same class, `testChess.py`. 
* Spesial moves: *En passant* and *castling* is not taken into account.
* A better gripper and more safe gripper, to pick up the pieces.
#
### What I'm thinking further
As in the topic "What the project needs", this section is pretty similar.
+ It needs safety parametre for the robot arm, so it doesn't bump into anything or damage anyone.
+ When illegal moves is preformed, the robot has to signilize someway that the move is illegal, maybe pointing at a piece of paper that says illegal, or print on the screen "Illegal move". Because chessplaying at boards, it's not always easy to see that you actually did a illegal move, especially if you are under pressure and have limited time to finish the move.
+ Need a basket for the captured pieces.

  
# Already have everything intsalled

## Do:
- Download the zip-file.
- Open the folder you just extracted to Visual Studio code.
- Type into termial: sudo apt update && sudo apt upgrade
- Type into termial: pip install python-chess
- Clone this repository: "https://github.com/niklasf/python-asyncdgt/tree/master" in the same place you have you'r project (zip-file)
- Type into terminal: pip3 install asyncdgt






