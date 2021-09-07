import math
from typing import Union, Tuple

from kivy.clock import Clock
from kivy.graphics import Color, Line
from kivy.properties import NumericProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivymd.app import MDApp

number_file_sources = [
    '2052194.svg.png',
    '2052171.svg.png',
    '2052150.svg.png',
    '2052130.svg.png',
    '2015076.svg.png',
    '2052086.svg.png',
    '2052071.svg.png',
    '2052065.svg.png',
    '2052062.svg.png',
    '2052057.svg.png'
]


class SudokuData:
    def __init__(self, sudoku_size: int, preset_values=None):
        # FIXME: change this to actually load values and not use this testing default
        self.__sudoku_data: list = [3, None, 1, None,
                                    None, None, 4, None,
                                    1, None, 2, None, None,
                                    None, 3, None, 4]
        self.size: int = sudoku_size

    def __getitem__(self, key: Union[int, Tuple[int, int]]):
        if type(key) == int:
            return self.__sudoku_data[key]
        elif type(key) == tuple:
            return self.__sudoku_data[key[0] * self.size + key[1]]

    def __setitem__(self, key: Union[int, Tuple[int, int]], value: int):
        # TODO: Be able to mark certain positions as immutable by being unable to set the value
        # TODO: Additionally add other checks to make sure values are valid i.e. cannot set
        #   box to 5 in a 4x4 sudoku
        if type(key) == int:
            self.__sudoku_data[key] = value
        elif type(key) == tuple:
            self.__sudoku_data[key[0] * self.size + key[1]] = value


class SudokuBoard(FloatLayout):
    """
    Responsible for drawing the sudoku board
    """

    sudoku_size = NumericProperty(4)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # canvas properties
        self._regular_line_thickness = 1
        self._dividing_line_color = (0, 0, 0, 1)
        self._larger_cell_line_thickness = 2

        self._sudoku_data = SudokuData(4)

        Clock.schedule_interval(self.render, 1)

    def render(self, *args, **kwargs):
        self._render_background()
        self._render_images()

    def _render_background(self):
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
                    self.x, self.y,
                    self.right, self.y,
                    self.right, self.top,
                    self.x, self.top,
                    self.x, self.y,
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
                    points=(self.x, self.y + v_len * i * cell_no,
                            self.right, self.y + v_len * i * cell_no),
                    width=self._larger_cell_line_thickness
                )

    def _render_images(self, **kwargs):
        self.clear_widgets()
        for i in range(self.sudoku_size):
            for j in range(self.sudoku_size):
                if self._sudoku_data[i, j] is not None:
                    image = Image(
                        source=f'res/images/{number_file_sources[self._sudoku_data[i, j]]}',
                        size_hint=(0.7 / self.sudoku_size, 0.7 / self.sudoku_size),
                        pos_hint={'center': (
                            1 / (self.sudoku_size * 2) + i * 1 / self.sudoku_size,
                            1 / (self.sudoku_size * 2) + j * 1 / self.sudoku_size
                        )}
                    )
                    self.add_widget(image)


class SudokuApp(MDApp):
    pass


if __name__ == '__main__':
    SudokuApp().run()
