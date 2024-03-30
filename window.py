from tkinter import Tk, BOTH, Canvas
import time

class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Biscuit")
        self.__canvas = Canvas(self.__root, width=width, height=height)
        self.__canvas.pack(fill=BOTH, expand=True)
        self.__window_running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self._ww = width
        self._wh = height

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__window_running = True
        while self.__window_running:
            self.redraw()

    def draw_line(self, line, fill_color="black", dash=None):
        line.draw(self.__canvas, fill_color, dash)

    def close(self):
        self.__window_running = False

    def _animate(self):
        self.redraw()
        time.sleep(0.00035)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    def draw(self, canvas, fill_color="black", dash=None):
        canvas.create_line(self.point1.x, self.point1.y, self.point2.x, self.point2.y, fill=fill_color, width=2, dash=dash)
        canvas.pack(fill=BOTH, expand=True)

class Cell:
    def __init__(self, x1, y1, x2, y2, win=None):
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2
        self._win = win
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.left_wall = Line(Point(self._x1, self._y1), Point(self._x1, self._y2))
        self.right_wall = Line(Point(self._x2, self._y1), Point(self._x2, self._y2))
        self.top_wall = Line(Point(self._x1, self._y1), Point(self._x2, self._y1))
        self.bottom_wall = Line(Point(self._x1, self._y2), Point(self._x2, self._y2))

    def draw(self):
        if self._win is None:
            return
        dash = 3
        if self.has_left_wall:
            self._win.draw_line(self.left_wall)
        else:
            self._win.draw_line(self.left_wall, "#b3b3cb", dash)
        if self.has_right_wall:
            self._win.draw_line(self.right_wall)
        else:
            self._win.draw_line(self.right_wall, "#b3b3cb", dash)
        if self.has_top_wall:
            self._win.draw_line(self.top_wall)
        else:
            self._win.draw_line(self.top_wall, "#b3b3cb", dash)
        if self.has_bottom_wall:
            self._win.draw_line(self.bottom_wall)
        else:
            self._win.draw_line(self.bottom_wall, "#b3b3cb", dash)

    def __repr__(self):
        return f"Cell({self._x1},{self._y1},{self._x2},{self._y2},{self.has_left_wall},{self.has_right_wall},{self.has_top_wall},{self.has_bottom_wall})"

