import enum

class Shape(enum.Enum):
    FREE, RECT, ELLIPSE, CERCLE, LINE = range(5)
    
class Mode(enum.Enum):
    DRAW, MOVE, SELECT = range(3)