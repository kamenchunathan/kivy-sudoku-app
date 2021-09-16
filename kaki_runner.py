from kivy.factory import Factory
from kaki.app import App
from kivymd.app import MDApp
from kivy.core.window import Window

Window.size = (395, 704)
Window.top = 64
Window.left = 971


class Live(App, MDApp):
    CLASSES = {'MyLayout': 'sudoku'}

    KV_FILES = ['sudoku.kv']

    AUTORELOADER_PATHS = [(".", {"recursive": False}), ]

    AUTORELOADER_IGNORE_PATTERNS = ["*.pyc", "*__pycache__*"]

    def build_app(self, **kwargs):
        return Factory.MyLayout()


if __name__ == '__main__':
    Live().run()
