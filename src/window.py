from tkinter import Tk, BOTH, Canvas, ttk, font
import time

class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Biscuit")
        self.__canvas = Canvas(self.__root, width=width, height=height)
        self.__canvas.pack(fill=BOTH, expand=True)
        self.__canvas.bind("<Button-1>", self.find_closest_element)
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
        line_id = line.draw(self.__canvas, fill_color, dash)
        return line_id

    def delete_element(self, element):
        self.__canvas.delete(element)

    def close(self):
        self.__window_running = False

    def _animate(self):
        self.redraw()
        time.sleep(0.00035)

    def add_button(self, button):
        button.create(self.__canvas)

    def find_closest_element(self, event):
        closest_element = self.__canvas.find_closest(event.x, event.y)[0]
        print(f"closest_element_id: {closest_element}, mouse x: {event.x}, mouse y: {event.y}, coordinates: {self.__canvas.coords(closest_element)}")
        
        print(f"distance between closest element and mouse cursor: {self.mouse_cursor_position(event.x, event.y, self.__canvas.coords(closest_element))}")

        print(f"clicked near element: {self.element_in_click_range(self.mouse_cursor_position(event.x, event.y, self.__canvas.coords(closest_element)))}")

    def mouse_cursor_position(self, event_x, event_y, element_coordinates):
        element_x1 = element_coordinates[0]
        element_y1 = element_coordinates[1]
        element_x2 = element_coordinates[2]
        element_y2 = element_coordinates[3]
        mouse_position = ""
        if element_x1 == element_x2:
            if event_x < element_x1:
                mouse_position = "left"
            elif event_x == element_x1:
                mouse_position = "overlap"
            else:
                mouse_position = "right"
        if element_y1 == element_y2:
            if event_y < element_y1:
                mouse_position = "top"
            elif event_y == element_y1:
                mouse_position = "overlap"
            else:
                mouse_position = "bottom"
        info_packet = [mouse_position, (event_x, event_y), (element_x1, element_y1)]
        return info_packet

    def element_in_click_range(self, data):
        if data[0] == "overlap":
            return True
        max_range = 2
        if data[0] in ("top", "bottom"):
            if abs(int(data[2][1] - data[1][1])) <= max_range:
                return True
        if data[0] in ("left", "right"):
            if abs(int(data[2][0] - data[1][0])) <= max_range:
                return True
        return False


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point(x({self.x}), y({self.y}))"

class Line:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2
        self.id = 0

    def draw(self, canvas, fill_color="black", dash=None):
        self.id = canvas.create_line(self.point1.x, self.point1.y, self.point2.x, self.point2.y, fill=fill_color, width=2, dash=dash)
        canvas.pack(fill=BOTH, expand=True)
        return self.id

    def __repr__(self):
        return f"Line(Point1({self.point1}), Point2({self.point2}), id({self.id}))"


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
        self.walls_ids = []

    def draw(self):
        if self._win is None:
            return
        dash = 3
        if self.has_left_wall:
            wall_id = self._win.draw_line(self.left_wall)
        else:
            wall_id = self._win.draw_line(self.left_wall, "#b3b3cb", dash)
        self.walls_ids.append(wall_id)

        if self.has_right_wall:
            wall_id = self._win.draw_line(self.right_wall)
        else:
            wall_id = self._win.draw_line(self.right_wall, "#b3b3cb", dash)
        self.walls_ids.append(wall_id)

        if self.has_top_wall:
            wall_id = self._win.draw_line(self.top_wall)
        else:
            wall_id = self._win.draw_line(self.top_wall, "#b3b3cb", dash)
        self.walls_ids.append(wall_id)

        if self.has_bottom_wall:
            wall_id = self._win.draw_line(self.bottom_wall)
        else:
            wall_id = self._win.draw_line(self.bottom_wall, "#b3b3cb", dash)
        self.walls_ids.append(wall_id)

    def __repr__(self):
        return f"Cell({self._x1},{self._y1},{self._x2},{self._y2},{self.has_left_wall},{self.has_right_wall},{self.has_top_wall},{self.has_bottom_wall})"

class Button:
    def __init__(self, text, host_frame=None, command=None):
        self._text = text
        self._host_frame = host_frame
        self._command = command

    def create(self, canvas):
        if self._host_frame is None:
            return
        if self._command is None:
            return
        self._width = self._host_frame._x2 - self._host_frame._x1
        self._height = self._host_frame._y2 - self._host_frame._y1
        self._font_size = int(self._height / 2)
        self._font = font.Font(family="Lucida Console", size=self._font_size, weight="bold")

        self._style = ttk.Style()
        self._style.configure("Custom.TButton", font=self._font)
        self._button = ttk.Button(canvas, text=self._text, command=self._command)
        self._button.config(style="Custom.TButton")
        canvas.create_window(
            self._host_frame._x1, 
            self._host_frame._y1, 
            width=self._width, 
            height=self._height, 
            anchor="nw", 
            window=self._button
        )

