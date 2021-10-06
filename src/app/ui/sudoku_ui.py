import math
from functools import partial
import os
from typing import Tuple

from kivy import Logger
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Line, Rectangle
from kivy.properties import NumericProperty
from kivy.resources import resource_find
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.textfield import MDTextField

from app.sudoku_data import SudokuData

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

SUDOKU_DATA_FILE = 'res/puzzle_files/0.txt'


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
        """Addition of widgets done in method scheduled after init to allow for loading of variables"""
        for i in range(1, self.sudoku_size + 1):
            self.add_widget(Image(
                source=f'res/images/{NUMBER_FILE_SOURCES[i]}'
            ))

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            Clock.schedule_once(
                partial(
                    self.sudoku_board.set_cell_value,
                    math.floor((touch.x - self.x) *
                               self.sudoku_size / self.size[0]) + 1
                ),
                -1
            )


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

        # solely for keeping track of the cell that is currently selected so as to set
        # it once the number selector is pressed
        self._highlighted_cell = (0, 0)

        # BUG: will fail if set to other value
        self._sudoku_data = SudokuData(self.sudoku_size)

        Clock.schedule_interval(self.render, 1 / 15)

    def load_puzzle(self, puzzle_no: int):
        for root, dirs, files in os.walk(os.curdir):
            path = root.split(os.sep)
            print((len(path) - 1) * '---', os.path.basename(root))
            for file in files:
                print(len(path) * '---', file)

        self._sudoku_data = SudokuData(
            self.sudoku_size, resource_find(SUDOKU_DATA_FILE), puzzle_no)
    # ---------------------------------------- Rendering ------------------------------------

    def render(self, *args, **kwargs):
        if len(self._sudoku_data):
            self.canvas.clear()
            self._render_numbers()
            self._render_overlays()

    def _render_overlays(self):
        v_len = self.height / self.sudoku_size
        h_len = self.width / self.sudoku_size
        cell_no = int(math.sqrt(self.sudoku_size))

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
        for i in range(self.sudoku_size):
            for j in range(self.sudoku_size):
                if self._sudoku_data[i, j]['value'] is None:
                    continue

                if not self._sudoku_data[i, j]['mutable']:
                    with self.canvas:
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

                if not self._sudoku_data[i, j]['valid']:
                    with self.canvas:
                        Color(1.0, 0.5, 0.5, 1.0)
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

    # --------------------------------------- UI actions ----------------------------------------------
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            touch_pos_hint = (touch.x - self.x) / \
                self.size[0], (touch.y - self.y) / self.size[1]
            cell_coord = tuple(math.floor(x * self.sudoku_size)
                               for x in touch_pos_hint)
            Logger.info(
                f"Sudoku widget: Coordinates of cell pressed: {cell_coord}")
            self._set_selected_cell(cell_coord)

    def _set_selected_cell(self, key: Tuple[int, ...]):
        """ Reset once a key is set """
        self._highlighted_cell = key

    def set_cell_value(self, selected_value: int, dt: float):
        Logger.info("NumberSelector: Selected value: {selected_value}, {self._highlighted_cell}")
        self._sudoku_data.set_value(self._highlighted_cell, selected_value)


class SudokuScreen(Screen):
    def on_enter(self, *args):
        super().on_enter(*args)
        self.ids.sudoku_board.load_puzzle(self.manager.level_selected)


class PuzzleNumberInput(MDTextField):
    def _keyboard_close(self):
        pass

    def setup_keyboard(self):
        keyboard = Window.request_keyboard(self._keyboard_close, self)
        if keyboard:
            keyboard.widget.layout = 'numeric.json'


class LevelSelectionScreen(Screen):
    def enter_level(self, level_no: str):
        self.manager.level_selected = int(level_no)
        self.manager.current = 'sudoku-screen'


class AppScreenManager(ScreenManager):
    level_selected = NumericProperty(0)
    """Used to pass the selected level to the Sudoku screen"""
