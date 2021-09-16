import math
from typing import Tuple

from kivy import Logger
from kivy.clock import Clock
from kivy.graphics import Color, Line, Rectangle
from kivy.properties import NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image

# todo: Major priority next time: find way to get the index of the number that has been pressed
# based on the touch position


# images
NUMBER_FILE_SOURCES = [
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


##############################################################################
#                               Sudoku Data Class
##############################################################################


class SudokuData:
    """
    info contained in sudoku each index of the sudoku:
        value: int -> number stored in sudoku
        valid: bool ->  whether or not the number is valid based on the rules
        of sudoku 
        mutable: bool -> whether or not the value can be changed. Should be 
        false for intial values and only true for user set values
        clashing values : list[list] -> a list of all the indices that this
        value clashes with in the case that it is not valid
    """

    def __init__(self, sudoku_size: int, preset_values=None):
        self.size: int = sudoku_size
        self.__sudoku_data = self._init_random()

    def _init_random(self):
        """Method that initializes sudoku data with random information"""
        from random import randint
        return [
            {
                'value': randint(1, self.size) if randint(-4, 1) > 0 else None,
                'valid': True,
                'mutable': False,
                'clashing_values': []
            } for _ in range(self.size ** 2)
        ]

    def __getitem__(self, key: Tuple[int, int]):
        return self.__sudoku_data[key[0] * self.size + key[1]]

    def set_value(self, key: Tuple[int, int], value: int):
        # TODO: Be able to mark certain positions as immutable by being unable to set the value
        # TODO: Additionally add other checks to make sure values are valid  i.e. cannot set
        #   box to 5 in a 4x4 sudoku
        self._check_move_legality(key, value)
        self[key[0], key[1]]['value'] = value

    def _check_move_legality(self, key: Tuple[int, int], value: int):
        self[key[0], key[1]]['clashing_values'].clear()

        for i in range(self.size):
            # check numbers in same row
            if key[1] != i and self[key[0], i]['value'] == value:
                self[key[0], key[1]]['valid'] = False
                self[key[0], key[1]]['clashing_values'].append((key[0], i))

            # check numbers in same column
            if key[0] != i and self[i, key[1]]['value'] == value:
                self[key[0], key[1]]['valid'] = False
                self[key[0], key[1]]['clashing_values'].append((i, key[1]))

        # check numbers in same box
        size_root = int(math.sqrt(self.size))
        large_box_index = key[0] // size_root, key[1] // size_root
        for i in range(large_box_index[0] * size_root, (large_box_index[0] + 1) * size_root):
            for j in range(large_box_index[1] * size_root, (large_box_index[1] + 1) * size_root):
                if (i, j) != key and self[i, j]['value'] == value:
                    self[key[0], key[1]]['valid'] = False
                    self[key[0], key[1]]['clashing_values'].append((i, j))


##############################################################################
#                                   Sudoku Renderer
##############################################################################
class NumberSelector(BoxLayout):

    # to be passed during creation
    sudoku_size = NumericProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        Clock.schedule_once(self._post_init)

    def _post_init(self, *args):
        """Addtion of widgets done in method scheduled after init to allow for loading of variables"""
        for i in range(self.sudoku_size):
            self.add_widget(Image(
                source=f'res/images/{NUMBER_FILE_SOURCES[i]}',
            ))


class SudokuBoard(FloatLayout):
    """
    Responsible for rendering the board to the screen and receiving input
    """

    sudoku_size = NumericProperty(9)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # canvas properties
        self._regular_line_thickness = 1
        self._dividing_line_color = (0, 0, 0, 1)
        self._larger_cell_line_thickness = 2

        self._sudoku_data = SudokuData(self.sudoku_size)

        Clock.schedule_interval(self.render, 1)

    def render(self, *args, **kwargs):
        self._render_background()
        self._render_numbers()

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

    def _render_numbers(self, **kwargs):
        """Renders numbers as individual image widgets and the number background"""
        self.clear_widgets()
        self.canvas.before.clear()
        for i in range(self.sudoku_size):
            for j in range(self.sudoku_size):
                if self._sudoku_data[i, j]['value'] is None:
                    continue

                # Darker background indicating this value cannot be changed
                # set using canvas.before so as not to intefere with the dividing lines
                # NOTE: another option would be changing the draw order such that the lines are
                # drawn after the images
                # TODO: explore this option
                if not self._sudoku_data[i, j]['mutable']:
                    with self.canvas.before:
                        Color(0.5, 0.5, 0.5, 1.0)
                        Rectangle(
                            pos=(
                                self.pos[0] + i * self.size[0] /
                                self.sudoku_size,
                                self.pos[1] + j * self.size[1] /
                                self.sudoku_size
                            ),
                            size=(
                                self.size[0] / self.sudoku_size,
                                self.size[1] / self.sudoku_size
                            )
                        )

                # FIXME: This is a temporary solution
                if not self._sudoku_data[i, j]['valid']:
                    with self.canvas.before:
                        Color(0.5, 0.5, 0.5, 1.0)
                        Rectangle(
                            pos=(
                                self.pos[0] + i * self.size[0] /
                                self.sudoku_size,
                                self.pos[1] + j * self.size[1] /
                                self.sudoku_size
                            ),
                            size=(
                                self.size[0] / self.sudoku_size,
                                self.size[1] / self.sudoku_size
                            )
                        )

                # magic number definitions:
                # The reciprocal of the sudoku size is provided because kivy operates on a system
                # of size hints and the number of widgets to be placed is equal to the size of the sudoku
                #  0.7 is used instead for the size hint so that the image widget is slightly smaller
                # than its box effectively serving as a padding
                image = Image(
                    source=f'res/images/{NUMBER_FILE_SOURCES[self._sudoku_data[i, j]["value"]]}',
                    size_hint=(0.7 / self.sudoku_size,
                               0.7 / self.sudoku_size),
                    pos_hint={'center': (
                        1 / (self.sudoku_size * 2) + i * 1 / self.sudoku_size,
                        1 / (self.sudoku_size * 2) + j * 1 / self.sudoku_size
                    )},
                )
                self.add_widget(image)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            touch_pos_hint = (touch.x - self.x) / \
                self.size[0], (touch.y - self.y) / self.size[1]
            cell_coord = [math.floor(x * self.sudoku_size)
                          for x in touch_pos_hint]
            Logger.info(
                f"Sudoku widget: Coordinates of cell pressed: {cell_coord}")


class MyLayout(FloatLayout):
    pass
