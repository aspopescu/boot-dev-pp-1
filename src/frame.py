from window import *

class Frame:
    def __init__(self, x1, y1, win, generic_distance=None):
        self._x1 = x1
        self._y1 = y1
        self._win = win
        self._win_width = self._win._ww
        self._win_height = self._win._wh
        if generic_distance is None:
            self._generic_distance = 0
        elif generic_distance > self._win_width/40:
            self._generic_distance = self._win_width/40
        else:
            self._generic_distance = generic_distance
        self.game_wall_length = 0
        self.arena = 0
        self._frames = []
        self._draw_frames()
        self.initiate_score_values()

    def _draw_frames(self):
        # calcutate main frame
        main_frame_x1 = self._x1
        main_frame_y1 = self._y1
        main_frame_x2 = self._win_width - self._x1
        main_frame_y2 = self._win_height - self._y1
        main_frame = Cell(main_frame_x1, main_frame_y1, main_frame_x2, main_frame_y2, self._win)
        #main_frame.draw()
        #self._animate()
        self._frames.append(main_frame)
        # calcutate bottom square
        bottom_square_x1 = self._x1 + self._generic_distance
        bottom_square_x2 = self._win_width - self._x1 - self._generic_distance
        bottom_square_y1 = self._win_height - self._y1 - self._generic_distance - (bottom_square_x2 - bottom_square_x1)
        bottom_square_y2 = self._win_height - self._y1 - self._generic_distance
        bottom_square = Cell(bottom_square_x1, bottom_square_y1, bottom_square_x2, bottom_square_y2, self._win)
        self._frames.append(bottom_square)
        # calculate top rectangle
        top_rectangle_x1 = self._x1 + self._generic_distance
        top_rectangle_y1 = self._y1 + self._generic_distance
        top_rectangle_x2 = self._win_width - self._x1 - self._generic_distance
        top_rectangle_y2 = bottom_square_y1 - self._generic_distance
        top_rectangle = Cell(top_rectangle_x1, top_rectangle_y1, top_rectangle_x2, top_rectangle_y2, self._win)
        self._frames.append(top_rectangle)
        # calculate scoreboard
        scoreboard_y1 = top_rectangle_y1 + self._generic_distance
        scoreboard_y2 = top_rectangle_y2 - self._generic_distance
        scoreboard_mid_line_x = (top_rectangle_x2 - top_rectangle_x1) / 2 + top_rectangle_x1
        scoreboard_x1 = scoreboard_mid_line_x - (scoreboard_y2 - scoreboard_y1)
        scoreboard_x2 = scoreboard_mid_line_x + (scoreboard_y2 - scoreboard_y1)
        scoreboard = Cell(scoreboard_x1, scoreboard_y1, scoreboard_x2, scoreboard_y2, self._win)
        self._frames.append(scoreboard)
        scoreboard_mid_line = Line(Point(scoreboard_mid_line_x, scoreboard_y1), Point(scoreboard_mid_line_x, scoreboard_y2))
        self._win.draw_line(scoreboard_mid_line)
        # calculate "current turn"
        turn_rectangle_x1 = top_rectangle_x1 + self._generic_distance
        turn_rectangle_y1 = scoreboard_y1
        turn_rectangle_x2 = scoreboard_x1 - 2 * self._generic_distance
        turn_rectangle_y2 = scoreboard_y2
        turn_rectangle = Cell(turn_rectangle_x1, turn_rectangle_y1, turn_rectangle_x2, turn_rectangle_y2, self._win)
        self._frames.append(turn_rectangle)
        # calculate "actions area"
        actions_rectangle_x1 = scoreboard_x2 + 2 * self._generic_distance
        actions_rectangle_y1 = scoreboard_y1
        actions_rectangle_x2 = top_rectangle_x2 - self._generic_distance
        actions_rectangle_y2 = scoreboard_y2
        actions_rectangle = Cell(actions_rectangle_x1, actions_rectangle_y1, actions_rectangle_x2, actions_rectangle_y2, self._win)
        self._frames.append(actions_rectangle)
        for f in range(len(self._frames)):
            self._draw_frame(f)
        self.game_wall_length = scoreboard_y2 - scoreboard_y1
        self.arena = bottom_square
        self.buttons_area = actions_rectangle
        self.scoreboard_1 = Cell(scoreboard_x1, scoreboard_y1, scoreboard_mid_line_x, scoreboard_y2, self._win)
        self.scoreboard_2 = Cell(scoreboard_mid_line_x, scoreboard_y1, scoreboard_x2, scoreboard_y2, self._win)
        self.current_turn = turn_rectangle

    def _draw_frame(self, i):
        self._frames[i].draw()
        self._win._animate()

    def initiate_score_values(self):
        self._player_1_score = 0
        self._player_2_score = 0
        self.add_labels()

    def add_labels(self):
        player_1 = ["Player 1", "#0000ff"]
        player_2 = ["Player 2", "#ff5050"]
        x = self.current_turn._x2 - (self.current_turn._x2 - self.current_turn._x1) / 2
        y = self.current_turn._y2 - (self.current_turn._y2 - self.current_turn._y1) / 2
        l1 = Label(x, y, f"Turn: {player_2[0]}", "center", player_2[1])
        self._win.add_label(l1)

        score_1_x = self.scoreboard_1._x2 - (self.scoreboard_1._x2 - self.scoreboard_1._x1) / 2
        score_1_y = self.scoreboard_1._y2 - (self.scoreboard_1._y2 - self.scoreboard_1._y1) / 2
        label_score_1 = Label(score_1_x, score_1_y, self._player_1_score, "center", player_1[1])
        self._win.add_label(label_score_1)
        score_2_x = self.scoreboard_2._x2 - (self.scoreboard_2._x2 - self.scoreboard_2._x1) / 2
        score_2_y = self.scoreboard_2._y2 - (self.scoreboard_2._y2 - self.scoreboard_2._y1) / 2
        label_score_2 = Label(score_2_x, score_2_y, self._player_2_score, "center", player_2[1])
        self._win.add_label(label_score_2)



