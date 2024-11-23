import queue
import time

class NottyGUI:

    def __init__(self, nottygame):
        self.nottygame = nottygame
        self.game_status = {}
        pass
        
    def run(self):

        self.nottygame.setup(2, ['Amy', "Cathy"], self.nottygame.ComputerLevel.EASY) # name can be None.

        self.nottygame.start_game()

        # deal cards
        self.nottygame.send_action(self.nottygame.GameActions.DEAL)

        time.sleep(0.02)
        self.game_status = self.nottygame.render_queue.get(timeout= 0.033)
        print(self.game_status)
        print("-----------------------")
        for _ in range(2):
            # draw a card
            for _ in range(3):
                self.nottygame.send_action(self.nottygame.GameActions.DRAW, self.nottygame.user_id, 1)
                time.sleep(0.02)
                start_time = time.time()
                self.game_status = self.nottygame.render_queue.get(timeout= 0.033)
                end_time = time.time()
                elapsed_time = end_time - start_time
                print(f"Elapsed time: {elapsed_time:.2f} seconds")
                print(self.game_status)
                print("-----------------------")


            # discard card
            discarded_list = [self.game_status['players'][0]['handset'][0],
                            self.game_status['players'][0]['handset'][1],
                            self.game_status['players'][0]['handset'][2]]

            self.nottygame.send_action(self.nottygame.GameActions.DISCARD, self.nottygame.user_id, discarded_list)

            # self.nottygame.send_action(self.nottygame.GameActions.DISCARD, 
            #                               self.nottygame.user_id,
            #                               [self.nottygame.create_card("Blue", 4),
            #                                self.nottygame.create_card("Yellow", 4),
            #                                self.nottygame.create_card("Green", 4)])
            time.sleep(0.02)

            self.game_status = self.nottygame.render_queue.get(timeout= 0.033)

            print(self.game_status)
            print("-----------------------")

            # steal card
            self.nottygame.send_action(self.nottygame.GameActions.STEAL, self.nottygame.user_id, 1) 

            time.sleep(0.02)

            self.game_status = self.nottygame.render_queue.get(timeout= 0.033)
            print(self.game_status)

            print("-----------------------")

            # skip card
            self.nottygame.send_action(self.nottygame.GameActions.SKIP, self.nottygame.user_id)

            time.sleep(0.02)

            self.game_status = self.nottygame.render_queue.get(timeout= 0.033)
            print(self.game_status)
            print("----ai start------")

            if self.game_status['next_player'] != -1:
                next_player = self.game_status['next_player']
                while True:
                    self.nottygame.ai_take_action(next_player)

                    time.sleep(0.033)
                    try:
                        self.game_status = self.nottygame.render_queue.get(timeout= 0.033)
                    except queue.Empty:
                        continue
                    print(self.game_status)
                    print("-----------------------")
                    if self.game_status['type'] == self.nottygame.GameActions.SKIP:
                        break

        print("ai play for me now!!!")

        while True:
            self.nottygame.ai_take_action(self.game_status['next_player'])

            try:
                self.game_status = self.nottygame.render_queue.get(timeout= 0.033)
            except queue.Empty:
                continue
            print(self.game_status)
            if self.game_status['type'] == self.nottygame.GameActions.SKIP:
                break

        self.nottygame.end_game()

