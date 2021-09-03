import math
from kivy.clock import Clock
from kivy.properties import NumericProperty
from kivymd.app import MDApp
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Rectangle


number_file_sources = [
    '2052194.svg',
    '2052171.svg',
    '2052150.svg',
    '2052130.svg', 
    '2015076.svg',
    '2052086.svg',
    '2052071.svg',
    '2052065.svg',
    '2052062.svg',
    '2052057.svg'
]


class SudokuBoard(Widget):
    """
    Responsible for drawing the sudoku board
    """

    sudoku_size = NumericProperty(9)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # canvas properties
        self._regular_line_thickness = 1
        self._dividing_line_color = (0, 0, 0, 1)
        self._larger_cell_line_thickness = 3

        Clock.schedule_interval(self.render, 1)

    def render(self, *args, **kwargs):
        v_len = self.height / self.sudoku_size
        h_len = self.width / self.sudoku_size
        cell_no = int(math.sqrt(self.sudoku_size))

        self.canvas.clear()

        with self.canvas:
            # Bounding box
            # might need to change later to allow diff colors
            Color(*self._dividing_line_color)
            Line(
                points=(
                    self.x,     self.y,
                    self.right, self.y,
                    self.right, self.top,
                    self.x,     self.top,
                    self.x,     self.y,
                ),
                width=self._larger_cell_line_thickness
            )

           # Background lines
            Color(*self._dividing_line_color)

            for i in range(1, self.sudoku_size):
                # vertical lines
                Line(points=(self.x + h_len * i, self.top, self.x + h_len * i, self.y),
                     width=self._regular_line_thickness)

                # horizontal lines
                Line(points=(self.x, self.y + v_len * i, self.right, self.y + v_len * i),
                     width=self._regular_line_thickness)

            # Thicker Lines dividing The larger cells
            for i in range(1, cell_no):
                # vertical lines
                Line(
                    points=(self.x + h_len * i * cell_no, self.top,
                            self.x + h_len * i * cell_no, self.y),
                    width=self._larger_cell_line_thickness
                )
                # horizontal lines
                Line(
                    points=(self.x,     self.y + v_len * i * cell_no,
                            self.right, self.y + v_len * i * cell_no),
                    width=self._larger_cell_line_thickness
                )
            


class SudokuApp(MDApp):
    pass


if __name__ == '__main__':
    SudokuApp().run()
