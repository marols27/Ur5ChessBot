import chessMoveClass as tc
import Getuci as gu
import mainforChessengine
import chess as ch
import SafeVariableClass as safe_v
import Rebuild.UR5Robot as ur                                    #Comment out if you want to run the chess program

chessMoveClass = tc.chessMoveClass()
mainEngine= mainforChessengine.mainforChessengine()
getUciandSan = tc.chessMoveClass()
urclass = mainforChessengine.urclass                    #Else if you want to test or run simple programs from URClass, uncomment




#NB!NB!NB! For recalibration!#
"""The two lines under are only for recalibration, dont try this!"""
instance_of_class = safe_v.SafeVariableClass()
calibrate_new_position = instance_of_class.make_new_motherpoint(urclass.info)
#NB!NB!NB!#





game = mainforChessengine.mainforChessengine()
startGame = game.startGame()



#urclass.moverob('h8','h3', 'b')
#urclass.drop_off_captured_piece("b",'f5','f4')
#urclass.moveSimple(safe_v.SafeVariableClass.standardPosition_high)
#urclass.moveSimple(safe_v.SafeVariableClass.trashcan)




