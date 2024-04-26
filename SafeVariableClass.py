#from testChess import chessMoveClass
class SafeVariableClass:
    tcp_orientation =  [ 0.49136627, 0.00694196628, -0.027585285, -2.14870471, 2.2550925, 0.020063739] # Used to collect the three last indexes
    file_name_for_calibration = r"recalibratin_point.txt"
    

    def make_new_motherpoint(self, robot_rtde_r): #Recalibration method
        filename = self.file_name_for_calibration
        need_recalibration = input("Need recalibration? 'y' or 'n': ")
        if need_recalibration =='y':
            new_content = robot_rtde_r.getActualTCPPose() # Gets the real time tcp-position

            for index in range(len(new_content)-3):
                self.tcp_orientation[index]=new_content[index] 

            new_data = input("Is this new point for ur5 arm? 'y' or 'n': " )

            if new_data.lower() == 'y':
                    try:
                        with open(filename, 'r', encoding='utf-8') as file:
                            existing_content = file.read()
                    except FileNotFoundError:
                        existing_content = ""

                    if existing_content != self.tcp_orientation:
                        with open(filename, 'w', encoding='utf-8') as file:
                            file.write(str(self.tcp_orientation))
            else:
                print("No changes done!")
        else:
            print("Continues with previous joint-values")


    def read_file_and_convert_to_int(file_name_for_calibration):
        try:
            with open(file_name_for_calibration, 'r', encoding='utf-8') as file:
                content = file.read()
            # Fjerner klammeparentesene før splitting
            content = content.strip().replace('[', '').replace(']', '')
            points = content.split(',')
            # Konverterer hvert punkt til int
            list_of_int_points = [float(point.strip()) for point in points]
        except:
            print("There is nothing in the file for points")
        return list_of_int_points

    # NB! When you are going to make a new point, place the robotgripper fingers as near the chessboard as possible! If there are any exctentions to the gripper, remove and prosceed
    # Denne posisjonen her er helt nede i brettet, kanten helt nede i venstre hjørne. Den må heises opp og flyttes 4 ruter til øyre og kanskje litt til.
    # Alle bevegelser skal baseres rundt dette punktet her
    # If the chessboard ever is moved, this point has to be renewed:
    """[    +frem-tibake,   +venstre-høyre,     +opp-ned,   rx,     ry,     rz    ]"""
    mother_point_h8_tip_low = read_file_and_convert_to_int("recalibratin_point.txt")# So this point will never be used, just a referencepoint

    # The variable over is at the edge for the chessboard. It slightly touches the board.

    one_square_lenght = 0.055 #m
    xyz = 0.08
    down = 0.2
    forward = 0.005
    right = 0.0035
    sligtly_ut_to_not_hit_the_board_with_gripper_fingers = 0.015

    h8__sentrum_kingheight = [
        mother_point_h8_tip_low[0]+(one_square_lenght/2), 
        mother_point_h8_tip_low[1]-(one_square_lenght/2), 
        mother_point_h8_tip_low[2]+0.055, 
        mother_point_h8_tip_low[3], 
        mother_point_h8_tip_low[4], 
        mother_point_h8_tip_low[5]
        ]
    
    h8_high = [
        mother_point_h8_tip_low[0]+(one_square_lenght/2),   #Tilbake og frem 
        mother_point_h8_tip_low[1]-(one_square_lenght/2),   # Venstre og høyre
        mother_point_h8_tip_low[2]+0.145414714+0.045,   # Ned og opp 
        mother_point_h8_tip_low[3],               # Rx
        mother_point_h8_tip_low[4],               # Ry
        mother_point_h8_tip_low[5]                # Rz
        ]


    sentrum_whole_board = [
        mother_point_h8_tip_low[0]+(one_square_lenght/2)*6,   #Tilbake og frem 
        mother_point_h8_tip_low[1]-(one_square_lenght/2)*6,   # Venstre og høyre
        mother_point_h8_tip_low[2]+0.145414714,   # Ned og opp 
        mother_point_h8_tip_low[3],               # Rx
        mother_point_h8_tip_low[4],               # Ry
        mother_point_h8_tip_low[5]                # Rz
        ]

    lower_highten_var       =   0.2 #meters
    right_left_var          =   0.225
    forward_reverse_var     =   0.07
    # Må ikke endre noe på variablene over, det kan skape en kjedereaksjon med alle funksjonene
    standard_pos_idle =  [  
        mother_point_h8_tip_low[0]-forward_reverse_var,             #Tilbake og frem    
        mother_point_h8_tip_low[1]-right_left_var,        # Venstre og høyre
        mother_point_h8_tip_low[2]+lower_highten_var+0.055,     # Ned og opp # Pluss 5 cm slik at den ikke knuser brikkene med gripperbasen
        mother_point_h8_tip_low[3],                               # Rx
        mother_point_h8_tip_low[4],                               # Ry
        mother_point_h8_tip_low[5]                                # Rz
        ]

    trashcan = [
    mother_point_h8_tip_low[0]+(one_square_lenght/2)+0.05,   #Tilbake og frem 
    mother_point_h8_tip_low[1]+0.12,   # Venstre og høyre
    mother_point_h8_tip_low[2]+0.145414714+0.1,   # Ned og opp 
    mother_point_h8_tip_low[3],               # Rx
    mother_point_h8_tip_low[4],               # Ry
    mother_point_h8_tip_low[5]                # Rz
    ]                            
    