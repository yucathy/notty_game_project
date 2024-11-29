from notty_game import NottyGame
from gui import NottyGUI
from GUI_crystal import GUI

def main():

    nottygame = NottyGame()
    gui = GUI(nottygame)
    gui.run_game()

if __name__ == "__main__":
    main()
