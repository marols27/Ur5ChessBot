class ToolCenterPoint(object):
    # A Tool Center Point or TCP for short consists of 6 values [x, y, z, rx, ry, rz].
    # The first 3 values (x, y, and z), are kartesian position values measured in meters,
    # and the remaining (xr, xy, and xz), are angle values measured in radiants.

    # Fields:
    #  - TCP: List of floating points, containing the TCP

    # Constructor:
    #  - __init__(self, [x, y, z, xr, xy, xz]):
    
    # Functions:
    #  - getPosition(self):
    #       Returns the first 3 values determining the location of the Tool Point as an array of 3 floating points.
    #
    #  - getAngle_(self):
    #       Returns the last 3 values determining the orientation of the Tool Point as an array of 3 floating points.


    # Constructor:
    def __init__(self, TCP: 'list[float]') -> None:
        self.TCP = TCP

    # Methods:
    def Position(self) -> 'list[float]':
        return self.TCP[:3]

    def Orientation(self) -> 'list[float]':
        return self.TCP[3:]

    def __str__(self) -> str:
        TCP = self.TCP
        return f"[{TCP[0]}, {TCP[1]}, {TCP[2]}, {TCP[3]}, {TCP[4]}, {TCP[5]}]"
    
# Point = ToolCenterPoint(0, 0, 0, 0, 0, 0)