from window import *
from frame import *
from arena import *

def main():
    window_width = 700
    window_height = 800
    generic_distance = 18
    win = Window(window_width, window_height)
    #cell1 = Cell(100, 100, 200, 200, win)
    #cell1.draw()
    add_frame = Frame(generic_distance, generic_distance, win, generic_distance)
    add_arena = Arena(win, add_frame)
    win.wait_for_close()
main()
