"""
Main App
"""
from kivymd.app import MDApp

from app.ui import AppScreenManager


class SudokuApp(MDApp):
    def build(self):
        return AppScreenManager()
