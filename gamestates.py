from enum import Enum

class GameState(Enum):
    INTRO = 1
    MENU = 2
    PLAYING = 3
    HIGH_SCORES = 4
    README = 5
    CREDITS = 6
    QUIT = 7