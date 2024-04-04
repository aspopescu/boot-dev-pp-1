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
    win = Window(window_width, window_height)
    frames = Frame(generic_distance, generic_distance, win, generic_distance)
    arena = Arena(win, frames)

    win.import_players_scores(frames._player_1_score, frames._player_2_score)
    win.import_arena_cells(arena._cells)

    def new_board_commands():
        frames.initiate_score_values()
        arena.redraw_cells()
        win.import_players_scores(frames._player_1_score, frames._player_2_score)
        win.import_arena_cells(arena._cells)
    
    new_board_button = Button("New board", host_frame=frames.buttons_area, command=new_board_commands)
    win.add_button(new_board_button)

    win.wait_for_close()
main()
