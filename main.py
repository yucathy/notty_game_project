from notty_game import NottyGame
from GUI import GUI

def main():
    nottygame = NottyGame()
    gui = GUI(nottygame)
    gui.run_game()

if __name__ == "__main__":
    main()
