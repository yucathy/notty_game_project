import queue

class NottyGUI:

    def __init__(self, nottygame):
        self.nottygame = nottygame
        self.game_status = {}
        pass
        
    def run(self):

        self.nottygame.setup(2, ['Amy'], self.nottygame.ComputerLevel.EASY)

        self.nottygame.start_game()
        self.nottygame.receive_action(self.nottygame.GameActions.DISCARD)

        self.game_status = self.nottygame.render_queue.get(timeout= 0.033)
        print(self.game_status)

        self.nottygame.end_game()

