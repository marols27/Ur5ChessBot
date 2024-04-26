import URClass
import SafeVariableClass
import chessMoveClass

class Test:

    safe_v= SafeVariableClass.SafeVariableClass()
    urClass = URClass.URClass()
    test = chessMoveClass.chessMoveClass()
    def __init__(self) -> None:
        pass


    #a = urClass.getPositionForBlack('h8')
    
    #urClass.moveSimple(safe_v.h8__sentrum_kingheight)
    #TCP_posisjon = safe_v.mother_point_h8_tip_low
    #robot_ip_for_safe_v = urClass.rtde_r
    #new_point = safe_v.make_new_motherpoint(robot_ip_for_safe_v, TCP_posisjon)
    
    
    urClass.moverob('h8','h6', 'b')


    

    #print(test.visual_board_to_binary_grid())



