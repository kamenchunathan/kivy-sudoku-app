from kivy import platform
from kivy.factory import Factory

if platform == "linux" and __name__ == '__main__':
    from kaki.app import App
    from kivymd.app import MDApp
    from kivy.core.window import Window

    Window.size = (395, 704)
    Window.top = 64
    Window.left = 971


    class Live(App, MDApp):
        CLASSES = {'AppScreenManager': 'sudoku_ui'}

        KV_FILES = ['sudoku.kv']

        AUTORELOADER_PATHS = [(".", {"recursive": True}), ]

        AUTORELOADER_IGNORE_PATTERNS = ["*.pyc", "*__pycache__*"]

        def build_app(self, **kwargs):
            return Factory.AppScreenManager()


    Live().run()

elif platform == "android":
    from kivymd.app import MDApp


    class SudokuApp(MDApp):
        pass


    SudokuApp().run()
