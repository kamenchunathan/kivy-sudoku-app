import linecache
import math
from random import randint
from typing import Tuple

from kivy.logger import Logger


##############################################################################
#                               Sudoku Data Class
##############################################################################


def load_puzzle_from_file(file: str, puzzle_no: int):
    puzzle = linecache.getline(file, puzzle_no)

    return [
        {
            'value': int(val) if int(val) != 0 else None,
            'valid': True,
            'mutable': int(val) == 0,
            'clashing_values': []
        } for val in puzzle.strip()
    ]


class SudokuData:
    """
    info contained in sudoku each index of the sudoku:
        value: int -> number stored in sudoku
        valid: bool ->  whether or not the number is valid based on the rules
        of sudoku
        mutable: bool -> whether or not the value can be changed. Should be
        false for initial values and only true for user set values
        clashing values : list[list] -> a list of all the indices that this
        value clashes with in the case that it is not valid
    """

    def __init__(self, sudoku_size: int, file: str = '', puzzle_no: int = 0):
        if file:
            Logger.info('SudokuData: Creating a sudoku puzzle from file')
            self._sudoku_data = load_puzzle_from_file(file, puzzle_no)
            self.size = int(math.sqrt(len(self._sudoku_data)))
        else:
            Logger.info('SudokuData: No file found Creating a sudoku puzzle randomly.')
            self.size: int = sudoku_size
            self._sudoku_data = self._init_random()

    def _init_random(self):
        """Method that initializes sudoku data with random information"""
        return [
            {
                'value': val,
                'valid': True,
                'mutable': val is None,
                'clashing_values': []
            } for val in (randint(1, self.size) if randint(-4, 1) > 0 else None for _ in range(self.size ** 2))
        ]

    def __getitem__(self, key: Tuple[int, int]):
        return self._sudoku_data[key[0] * self.size + key[1]]

    def __setitem__(self, key: Tuple[int, int], val: int):
        self._sudoku_data[key[0] * self.size + key[1]]['value'] = val

    def set_value(self, key: Tuple[int, int], value: int):
        Logger.info(f'SudokuData: {key}, {len(self._sudoku_data)}')
        if self[key[0], key[1]]['mutable']:
            self[key[0], key[1]]['value'] = value

        self._update_value_validity(key, value)

    def __len__(self):
        return len(self._sudoku_data)

    def _update_value_validity(self, key: Tuple[int, int], value: int):
        """
        Checks whether entering that value at the selected point in the sudoku is valid
        or would cause clashes and updates the clashing values if any
        """
        self[key[0], key[1]]['valid'] = True
        if self[key[0], key[1]]['clashing_values']:
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
