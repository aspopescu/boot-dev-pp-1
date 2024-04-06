from window import *

class Arena:
    def __init__(self, win, frame):
        self._win = win
        self._frame = frame
        #self._wall_length = self._frame.game_wall_length
        self._wall_length = 45
        self._arena = self._frame.arena
        self._create_cells()
        self._draw_cells(self._cells)

    def _create_cells(self):
        # determine the count of colums using the arena width and self.wall_length
        count_cols = int((self._arena._x2 - self._arena._x1) / self._wall_length )
        if count_cols % 2 == 0:
            count_cols -= 1
        start_x1 = self._arena._x1 + (self._arena._x2 - self._arena._x1 - count_cols * self._wall_length) / 2
        start_y1 = self._arena._y1 + (self._arena._x2 - self._arena._x1 - count_cols * self._wall_length) / 2
        half_length = round((count_cols - 1) / 2)
        # the max cells near the margin, the original pen and paper game has 1 cell as the margin end
        # but I like the margin end to be 3
        # logic following it is built for the margin_max being 3
        margin_max = 3
        self._cells = []
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

    def redraw_cells(self):
        for cell in self._cells:
            for line in cell.walls_ids:
                self._win.delete_element(line)
        self._create_cells()
        self._draw_cells(self._cells)
 
