import os
from kivy import platform


def run_live_app():
    from app.live import Live

    Live().run()


def run_main_app():
    from app.main import SudokuApp

    SudokuApp().run()


def main():
    # Add resources folder to kivy resource manager resource paths
    from kivy.resources import resource_add_path

    base_dir = os.path.dirname(os.path.abspath(__file__))
    resource_add_path(os.path.join(base_dir, 'res/'))

    if platform == 'linux':
        os.chdir(os.path.dirname(__file__))
        run_live_app()
    else:
        run_main_app()


if __name__ == '__main__':
    main()
