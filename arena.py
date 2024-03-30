from window import *

class Arena:
    def __init__(self, win, frame):
        self._win = win
        self._frame = frame
        self._wall_length = self._frame.game_wall_length
        self._arena = self._frame.arena
        self._arena_center()
#        self._main_cell = self._draw_main_cell()
        self._cells = []
#        self._logic_tuples: a list of tuples, they decide the direction of new x and y coordinates
#        self._logic_tuples = [(1, 0), (0, 1), (-1, 0), (0, -1)]
# creating arena cells starting from layer 1, the center is layer 0
#        self._create_cells_r(1)
        self._create_cells()
        self._draw_cells(self._cells)

    def _arena_center(self):
        self._arena_mid = (self._arena._x2 - self._arena._x1) / 2
        self.arena_mid_x = self._arena._x1 + self._arena_mid
        self.arena_mid_y = self._arena._y1 + self._arena_mid

    def _draw_main_cell(self):
        self.main_cell_x1 = self.arena_mid_x - self._wall_length / 2
        self.main_cell_y1 = self.arena_mid_y - self._wall_length / 2
        self.main_cell_x2 = self.main_cell_x1 + self._wall_length
        self.main_cell_y2 = self.main_cell_y1 + self._wall_length
        main_cell = Cell(self.main_cell_x1, self.main_cell_y1, self.main_cell_x2, self.main_cell_y2, self._win)
        main_cell.draw()
        return main_cell

# original implementation
#    def _create_cells_r(self, layer):
#        # determine if there is space for a new cell
#        if self._arena._x2 - (self._main_cell._x2 + self._wall_length * (layer - 1)) < self._wall_length + 1:
#            return
#        for t in self._logic_tuples:
#            cell_x1 = self.main_cell_x1 + self._wall_length * t[0] * layer
#            cell_y1 = self.main_cell_y1 + self._wall_length * t[1] * layer
#            cell_x2 = cell_x1 + self._wall_length
#            cell_y2 = cell_y1 + self._wall_length
#            axis_cell = Cell(cell_x1, cell_y1, cell_x2, cell_y2, self._win)
#            self._cells.append(axis_cell)
#            if layer == 1:
#                continue
#            for l in range(1, layer):
#                diagonal_x1 = self.main_cell_x1 + self._wall_length * (t[0] + t[1]) * l
#                diagonal_y1 = self.main_cell_y1 + self._wall_length * (t[0] - t[1]) * (layer - l)
#                diagonal_x2 = diagonal_x1 + self._wall_length
#                diagonal_y2 = diagonal_y1 + self._wall_length
#                diagonal_cell = Cell(diagonal_x1, diagonal_y1, diagonal_x2, diagonal_y2, self._win)
#                self._cells.append(diagonal_cell)
#        self._create_cells_r(layer + 1)

# improved the original implementation, but I knew that it could be done differently   
#    def _create_cells_r(self, layer):
#        # determine if there is space for a new cell
#        if self._arena._x2 - (self._main_cell._x2 + self._wall_length * (layer - 1)) < self._wall_length + 1:
#            # this is adds and extra layer, so that the arena ends up with 3 cells instead of 1
#            for t in self._logic_tuples:
#                for l in range(1, layer):
#                    diagonal_x1 = self.main_cell_x1 + self._wall_length * (t[0] + t[1]) * l
#                    diagonal_y1 = self.main_cell_y1 + self._wall_length * (t[0] - t[1]) * (layer - l)
#                    diagonal_x2 = diagonal_x1 + self._wall_length
#                    diagonal_y2 = diagonal_y1 + self._wall_length
#                    diagonal_cell = Cell(diagonal_x1, diagonal_y1, diagonal_x2, diagonal_y2, self._win)
#                    self._cells.append(diagonal_cell)
#            return
#        layer = layer + 1
#        for t in self._logic_tuples:
#            for l in range(layer):
#                diagonal_x1 = self.main_cell_x1 + self._wall_length * (t[0] + t[1]) * l
#                diagonal_y1 = self.main_cell_y1 + self._wall_length * (t[0] - t[1]) * (layer - l - 1)
#                diagonal_x2 = diagonal_x1 + self._wall_length
#                diagonal_y2 = diagonal_y1 + self._wall_length
#                diagonal_cell = Cell(diagonal_x1, diagonal_y1, diagonal_x2, diagonal_y2, self._win)
#                self._cells.append(diagonal_cell)
#        self._create_cells_r(layer)

# a different approach, I like the above implementation more, but this one has fewer moving parts
    def _create_cells(self):
        # determine the count of colums using the arena width and self.wall_length
        count_cols = int((self._arena._x2 - self._arena._x1) / self._wall_length )
        start_x1 = self._arena._x1 + (self._arena._x2 - self._arena._x1 - count_cols * self._wall_length) / 2
        start_y1 = self._arena._y1 + (self._arena._x2 - self._arena._x1 - count_cols * self._wall_length) / 2
        half_length = round((count_cols - 1) / 2)
        # the max cells near the margin, the original pen and paper game has 1 cell as the margin end
        # but I like the margin end to be 3; the logic following it is built for the margin_max being 3
        margin_max = 3
        for a in range(count_cols):
            if a < half_length - 1:
                to_keep_blank = count_cols - margin_max - 2 * a
                start = round(to_keep_blank / 2)
            elif a in range(half_length - 1, half_length + 2):
                start = 0
            else:
                to_keep_blank = count_cols - margin_max - 2 * (count_cols - 1 - a)
                start = round(to_keep_blank / 2)
            end = count_cols - start
            cell_to_append_x1 = start_x1 + self._wall_length * a
            cell_to_append_x2 = start_x1 + self._wall_length * (a + 1)
            for b in range (start, end):
                cell_to_append_y1 = start_y1 + self._wall_length * b
                cell_to_append_y2 = start_y1 + self._wall_length * (b + 1)
                cell = Cell(cell_to_append_x1, cell_to_append_y1, cell_to_append_x2, cell_to_append_y2, self._win)
                cell.has_right_wall = False
                cell.has_bottom_wall = False
                cell.has_left_wall = False
                cell.has_top_wall = False
                if a == 0:
                    cell.has_left_wall = True
                if a == count_cols - 1:
                    cell.has_right_wall = True
                if b == start:
                    cell.has_top_wall = True
                    if a <= half_length - 1:
                        cell.has_left_wall = True
                    if a >= half_length + 1:
                        cell.has_right_wall = True
                if b == end - 1:
                    cell.has_bottom_wall = True
                    if a <= half_length - 1:
                        cell.has_left_wall = True
                    if a >= half_length + 1:
                        cell.has_right_wall = True
                self._cells.append(cell)

    def _draw_cells(self, cells):
        for cell in cells:
            cell.draw()
        self._win._animate()



