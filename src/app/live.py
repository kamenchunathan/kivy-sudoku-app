"""
Hot reload version for development
"""
from kaki.app import App
from kivy.factory import Factory
from kivymd.app import MDApp
from kivy.core.window import Window

# Local values for placing app on proper location on screen
Window.size = (395, 704)
Window.top = 64
Window.left = 971


class Live(App, MDApp):
    CLASSES = {'AppScreenManager': 'app.ui'}

    AUTORELOADER_PATHS = [("app/", {"recursive": True}), ]

    KV_FILES = ['app/sudoku.kv']

    AUTORELOADER_IGNORE_PATTERNS = ["*.pyc", "*__pycache__*"]

    def build_app(self, **kwargs):
        return Factory.AppScreenManager()
