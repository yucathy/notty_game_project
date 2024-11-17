class NottyGUI:

    def __init__(self, nottygame):
        self.nottygame = nottygame
        self.nottygame.register_callback(self.update_gui)
        self.turn_count = -1
        pass

    def update_gui(self, status: dict):
        self.turn_count = status["turns_count"]
        pass

    def run(self):

        self.nottygame.setup(2, ['Amy'], self.nottygame.ComputerLevel.EASY)

        self.nottygame.start_game()
        self.nottygame.receive_action(self.nottygame.GameActions.DISCARD)
        
        while self.turn_count == -1:
            print(self.turn_count)
            continue
        print(self.turn_count)
        self.nottygame.end_game()

