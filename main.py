from notty_game import NottyGame
from GUI import GUI

def main():
    # # initial App
    # nottygame = NottyGame()
    # # initial NottyGUI
    # gui = NottyGUI(nottygame)
    # # run the app
    # gui.run()

    nottygame = NottyGame()
    gui = GUI(nottygame)
    gui.run_game()

if __name__ == "__main__":
    main()
