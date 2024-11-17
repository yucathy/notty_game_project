from notty_game import NottyGame
from gui import NottyGUI

def main():

    # initial App
    nottygame = NottyGame()

    # initial NottyGUI
    gui = NottyGUI(nottygame)

    # run the app
    gui.run()

if __name__ == "__main__":
    main()
