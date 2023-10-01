import argparse

from yauza.gui.app import App


def find_args():
    parser = argparse.ArgumentParser(
        prog='yauza',
        description='Разгоняемся тормозим стоим')
    parser.add_argument('HEIGHT', type=int)
    parser.add_argument('WIDTH', type=int)
    return parser.parse_args()


def go():
    args = find_args()
    w, h = args.WIDTH, args.HEIGHT
    if (w < 200 or h < 200):
        print("not reasonable window size. 200 min")
        quit()
    app = App(w, h, [])
    quit(app.exec())
