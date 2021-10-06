import argparse
import os


def run_live_app():
    os.chdir(os.path.dirname(__file__))
    from app.live_app import Live

    Live().run()


def run_main_app():
    from app.main import SudokuApp

    SudokuApp().run()


def main():
    # Disable kivy's argparse
    os.environ.setdefault('KIVY_NO_ARGS', '1')

    # Add resources folder to kivy resource manager resource paths
    from kivy.resources import resource_add_path

    base_dir = os.path.dirname(os.path.abspath(__file__))
    resource_add_path(os.path.join(base_dir, 'res/'))

    # parse arguments and run appropriate app
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true', help='run in debug mode')
    parser.add_argument('-l', '--live', action='store_true', help='enable hot reload, DEBUG=1 must be set')

    args = parser.parse_args()

    if args.debug:
        # TODO: perhaps add a check if app is not running in an android environment and require a key /
        #   pass if it is
        from kivy.logger import Logger, LOG_LEVELS

        Logger.setLevel(LOG_LEVELS['debug'])
        # --- do anything else supposed to run in debug mode ---

    if args.live:
        run_live_app()
    else:
        run_main_app()


if __name__ == '__main__':
    main()
