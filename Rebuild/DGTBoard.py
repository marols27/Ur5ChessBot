import asyncio
import asyncdgt

class DGTBoard():
    # CLASS DOCUMENTATION
    # A class for handling the conection of the physical DGT chess board, and it's streams.
    #
    # Fields:
    # - loop: asyncronus loop that runns the dgtSocket handlers.
    # - dgtConnection: the asyncronus conection to the dgt board.
    # 
    # Constructor:
    # __init__():
    # 
    # Methods:
    # getCurentBoard(): returns a string representation of the curent board in a 15 x 8 size, (15 because of spaces between each squares).

    def __init__(self) -> None:
        self.loop = asyncio.get_event_loop()
        try:
            port = "/dev/ttyACM*"
            self.dgtConnection = asyncdgt.auto_connect(self.loop, [port])
            print(f"Connected to board at port: {port}")
        except:
            print(f"Could not connect to board at port: {port}")
    
    def getCurentBoard(self) -> str:
        return str(self.loop.run_until_complete(self.dgtConnection.get_board()))
    
    