from window import *
from frame import *
from arena import *

def main():
    # At the moment, I recommend to not change the window width and height, and the distance
    # I need to think about checks for these 3, to avoid broken scenarios
    # Maybe I should enforce a 7:8 ratio for width:height, maybe
    window_width = 770
    window_height = 880
    generic_distance = 18
    first_turn_player = random.randint(0, 1)
    win = Window(window_width, window_height)
    frames = Frame(generic_distance, generic_distance, win, first_turn_player, generic_distance)
    arena = Arena(win, frames)
    win.import_labels(frames._labels_pack)
    win.import_arena_cells(arena._cells)
    def new_board_commands():
        first_turn_player = random.randint(0, 1)
        frames.initiate_labels(first_turn_player)
        arena.redraw_cells()
        win.remove_marks()
        win.import_labels(frames._labels_pack)
        win.import_arena_cells(arena._cells)
    new_board_button = Button("New board", host_frame=frames.buttons_area, command=new_board_commands)
    win.add_button(new_board_button)
    win.wait_for_close()
main()
