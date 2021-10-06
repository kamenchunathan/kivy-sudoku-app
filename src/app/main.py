"""
Main App
"""
from kivymd.app import MDApp

from ui.sudoku_ui import AppScreenManager


class SudokuApp(MDApp):
    def build(self):
        return AppScreenManager()
