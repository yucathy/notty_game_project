import time
from enum import Enum
from collections import Counter
from itertools import combinations
from Card import Card
from deck import Deck
from players import Players, AIPlayer
import threading
import queue
import copy
import random
import string


class NottyGame:
    '''
    manage the game.
    '''

    max_draw_times_per_turn = 3
    max_steal_times_per_turn = 1
    user_id = 0


    class ComputerLevel(Enum):
        EASY = 'easy'
        MEDIUM = 'medium'
        HARD = 'hard'

    class GameActions(Enum):
        DEAL = "deal"
        DRAW = "draw"
        STEAL = "steal"
        DISCARD = "discard"
        SKIP = "skip"

    def __init__(self):
        '''initilize all the settings for the game'''
        self.action_queue = queue.Queue()
        self.render_queue = queue.Queue()
        self.game_thread = None
        self.winner = None
        self.running = False
        self.game_status = {}
        self.players = []
        self.game_ai_level = None
        self.turn_count = 0
        self.draw_times = 0
        self.steal_times = 0

        self.deck = Deck()
        self.ai_actions_pool = [action for action in self.GameActions \
                                if action != self.GameActions.DEAL]

        # self.start_time = time.time()

    def __initialize_state(self):
        '''keep players' setting when play again.'''
        self.action_queue = queue.Queue()
        self.render_queue = queue.Queue()
        self.game_thread = None
        self.winner = None
        self.running = False
        self.game_status = {}
        self.turn_count = 0
        self.draw_times = 0
        self.steal_times = 0
        self.deck = Deck()
        self.ai_actions_pool = [action for action in self.GameActions \
                                if action != self.GameActions.DEAL]

        for player in self.players:
            player.initialize_state()

    def setup(self, player_count: int, player_name: list, computer_level: ComputerLevel):
        '''
        info is a list about the setup for the card game.
        - player_count
        - player_name
        - computer_level
        '''

        assert type(player_count) != 'int', "player_count type should be int."
        assert type(player_name) != 'list', "player_name type should be a list."
        assert type(computer_level) != str, "computer_level type should be ComputerLevel."

        self.players.clear()
        for i in range(player_count):
            self.players.append(AIPlayer(player_name[i]))

        self.game_ai_level = computer_level

        print(player_count, player_name, computer_level)

    def create_card(self, colour: str, number: int) -> Card:
        return Card(colour, number)

    def send_action(self, action: GameActions, action_user_id: int = None, action_info=None):
        self.action_queue.put([action, action_user_id, action_info])

    def start_game(self):
        self.running = True
        self.game_thread = threading.Thread(target=self.__process_turns)
        self.game_thread.start()

    def end_game(self):
        self.running = False
        if self.game_thread:
            self.game_thread.join()
        self.__initialize_state()

    def __update_status(self, user_action, action_success, error_info, active_status, next_player):
        self.game_status["deck"] = self.deck.cards
        self.game_status["type"] = user_action
        self.game_status["action_success"] = action_success
        self.game_status["turns_count"] = self.turn_count
        self.game_status["winner"] = self.winner

        # end_time = time.time()
        # print("end_time - self.start_time",end_time - self.start_time)
        # if end_time - self.start_time > 10:
        #     self.game_status["winner"] = "Grace"

        player_list = []
        for player, active in zip(self.players, active_status):
            sorted_handset = sorted(player.hand, key=lambda card: (card.color, card.number))
            player_list.append({"name": player.name, "handset": sorted_handset, \
                                "add": player.add, "delete": player.delete, "active": active})

        self.game_status["players"] = player_list
        self.game_status['next_player'] = next_player
        self.game_status['error_info'] = error_info

    def __process_turns(self):
        while self.running:
            try:
                # get user action
                user_action_with_info = self.action_queue.get(timeout=1)
                # print(user_action_with_info)
                user_action = user_action_with_info[0]
                action_user_id = user_action_with_info[1]
                user_info = user_action_with_info[2]

                action_success = True
                active_status = [False for _ in range(len(self.players))]
                next_player = -1
                error_info = None

                # take action
                if user_action == self.GameActions.DEAL:
                    for player in self.players:
                        player.draw_cards(self.deck, 5)

                    self.turn_count += 1

                elif user_action == self.GameActions.DRAW:
                    if len(self.deck.cards) < user_info:
                        action_success = False
                        error_info = "the number of deck is not enough to draw"
                        print(f"the length of deck ({len(self.deck)}) is shorter than the cards({user_info}) you want.")
                    else:
                        self.draw_times += 1
                        if self.draw_times <= self.max_draw_times_per_turn:
                            current_player = self.players[action_user_id]
                            if not current_player.draw_cards(self.deck, user_info):
                                action_success = False
                                error_info = "the maximum hand size is 20"
                        else:
                            action_success = False
                            error_info = "the times of draw are over 3"
                    active_status[action_user_id] = True

                elif user_action == self.GameActions.STEAL:
                    self.steal_times += 1
                    print(self.steal_times)
                    print(type(user_info))
                    if self.steal_times <= self.max_steal_times_per_turn and \
                            type(user_info) == int:
                        current_player = self.players[action_user_id]
                        stealed_player = self.players[user_info]
                        if not current_player.take_random_card(stealed_player):
                            action_success = False
                            error_info = "the maximum hand size is 20"
                    else:
                        action_success = False
                        error_info = "only can steal one time per turn or the type is error"
                    active_status[action_user_id] = True

                elif user_action == self.GameActions.DISCARD:
                    if type(user_info) == set:
                        user_info = list(user_info)
                    if type(user_info) == list:
                        current_player = self.players[action_user_id]
                        if (current_player.discard_group(user_info, self.deck)):
                            if self.players[action_user_id].has_empty_hand():
                                self.winner = self.players[action_user_id].name
                        else:
                            action_success = False
                            error_info = "selected cards are illegal to discard"
                    else:
                        action_success = False
                        error_info = "the type is error"
                    active_status[action_user_id] = True

                elif user_action == self.GameActions.SKIP:
                    active_status[action_user_id] = True
                    self.draw_times = 0
                    self.steal_times = 0
                    for player in self.players:
                        player.clear_temp_list()
                    if action_user_id + 1 < len(self.players):
                        next_player = action_user_id + 1
                    else:
                        next_player = self.user_id

                    self.ai_actions_pool = [action for action in self.GameActions \
                                            if action != self.GameActions.DEAL]

                self.__update_status(user_action, action_success, error_info, active_status, next_player)

                # self.callback(copy.deepcopy(self.game_status))
                self.render_queue.put(copy.deepcopy(self.game_status))

                if action_user_id != None and user_action == self.GameActions.SKIP:
                    if action_user_id + 1 >= len(self.players):
                        self.turn_count += 1
                for player in self.players:
                    player.clear_temp_list()

            except queue.Empty:
                continue

    @staticmethod
    def _str_to_card(card_str):
        """
        字符串转Card对象
        :param card_str: 如 "red 3" 的卡牌字符串
        :return: Card 对象
        """
        color, number = card_str.split()
        return Card(color=color, number=int(number))

    def __probability_of_valid_group(self, current_player, target_cardset, card_amount):
        output = []
        target_cardset_str = {f"{card.color} {card.number}" for card in target_cardset}
        target_counter = Counter(target_cardset_str)

        valid_group_count = 0
        total_target_cards = sum(target_counter.values())

        valid_cards = []

        for card_str, count in target_counter.items():
            if count > 0:
                current_player.hand.append(self._str_to_card(card_str))
                if current_player.find_largest_valid_group():
                    valid_cards.append(card_str)
                    valid_group_count += count
                current_player.hand.pop()

        print(valid_group_count, total_target_cards, valid_group_count / total_target_cards)
        print(valid_cards)
        print("wwwww")
        output.append([1, valid_group_count / total_target_cards if total_target_cards > 0 else 0.0])
        if card_amount == 1:
            return output
        else:
            for i in range(2, 4):
                all_combinations = list(combinations(target_cardset_str, i))
                filtered_combinations = [comb for comb in all_combinations if any(c in valid_cards for c in comb)]
                total_filtered_count = len(filtered_combinations)
                total_comb_count = len(all_combinations)
                output.append([i, total_filtered_count / total_comb_count])
                if card_amount == 2:
                    return output

            return output

    def __evaluate_action(self, current_ai_id, action):
        if action == self.GameActions.SKIP:
            return [None, 0.2]
        elif action == self.GameActions.DRAW:
            temp = self.__probability_of_valid_group(self.players[current_ai_id],
                                                     self.deck.cards, 3)

            return temp
        else:
            idx_array = [i for i in range(len(self.players))]
            the_rest = [idx for idx in idx_array if idx != current_ai_id]
            temp = []
            print(current_ai_id)
            for other in the_rest:
                p = self.__probability_of_valid_group(self.players[current_ai_id],
                                                      self.players[other].hand, 1)[0][1]
                temp.append([other, p])

            return temp

    def __get_action_and_scrore(self, current_ai_id):
        skip_score = self.__evaluate_action(current_ai_id, self.GameActions.SKIP)[1]
        steal_scores = self.__evaluate_action(current_ai_id, self.GameActions.STEAL)  # [id, score]
        draw_scores = self.__evaluate_action(current_ai_id, self.GameActions.DRAW)  # [card_amount, score]

        draw_card_number = 0
        if len(self.players[current_ai_id].hand) == 1 or \
                len(self.players[current_ai_id].hand) == 18:
            draw_score = draw_scores[1][1]  # only want to draw 2 cards
            draw_card_number = draw_scores[1][0]
        elif len(self.players[current_ai_id].hand) == 2 or \
                len(self.players[current_ai_id].hand) == 19:
            draw_score = draw_scores[0][1]  # only want to draw 1 card
            draw_card_number = draw_scores[0][0]
        else:
            if len(self.players[current_ai_id].hand) == 20:
                draw_score = 0.0
            else:
                draw_score = draw_scores[2][1]  # draw 3 cards can get the largerst probability
                draw_card_number = draw_scores[2][0]

        print("-----")
        if draw_score < skip_score:
            draw_score = random.randint(19, 21) * 0.01
            draw_card_number = random.randint(1, 3)
            print(draw_score)
        print("----")

        for a in steal_scores:
            if len(self.players[a[0]].hand) < 5:
                a[1] = 0.0
        steal_target, steal_socre = max(steal_scores, key=lambda x: x[1])

        action_scores = {self.GameActions.SKIP: skip_score,
                         self.GameActions.STEAL: steal_socre,
                         self.GameActions.DRAW: draw_score}

        return [draw_card_number, steal_target, action_scores]

    def __ai_take_easy_action(self, current_ai_id):
        random_action = random.choice(self.ai_actions_pool)
        if random_action != self.GameActions.DISCARD:
            self.ai_actions_pool.remove(random_action)
        print(self.ai_actions_pool)
        print(f"Randomly selected action: {random_action}")

        if random_action == self.GameActions.DRAW:
            draw_card_number = random.randint(1, self.max_draw_times_per_turn)
            self.send_action(random_action, current_ai_id, draw_card_number)
        elif random_action == self.GameActions.STEAL:
            candidate_idx = [idx for idx in range(len(self.players)) if idx != current_ai_id \
                             and len(self.players[idx].hand) > 1]
            if candidate_idx:
                target_idx = random.choice(candidate_idx)
                print(target_idx)
                self.send_action(random_action, current_ai_id, target_idx)
        elif random_action == self.GameActions.DISCARD:
            discarded_cards = list(self.players[current_ai_id].find_largest_valid_group())
            print(discarded_cards)
            self.send_action(random_action, current_ai_id, discarded_cards)
            if len(discarded_cards) == 0 and len(self.ai_actions_pool) == 2:
                self.ai_actions_pool.remove(random_action)
        elif random_action == self.GameActions.SKIP:
            self.send_action(random_action, current_ai_id)

    def __ai_take_medium_action(self, current_ai_id):
        if self.GameActions.DISCARD in self.ai_actions_pool:
            self.ai_actions_pool.remove(self.GameActions.DISCARD)
        else:
            print("discard not in the pool...")
            print(self.ai_actions_pool)
        discarded_cards = list(self.players[current_ai_id].find_largest_valid_group())
        if discarded_cards:
            self.send_action(self.GameActions.DISCARD, current_ai_id, discarded_cards)
            return
        else:
            draw_card_number, steal_target, action_scores = self.__get_action_and_scrore(current_ai_id)
            print(action_scores)
            print(self.ai_actions_pool)
            try:
                best_action = max(self.ai_actions_pool, key=lambda action: action_scores[action])
                self.ai_actions_pool.remove(best_action)
            except ValueError:
                print("DISCARD not found in ai_actions_pool")
            
            if best_action == self.GameActions.DRAW:
                self.send_action(best_action, current_ai_id, draw_card_number)
            elif best_action == self.GameActions.STEAL:
                self.send_action(best_action, current_ai_id, steal_target)
            elif best_action == self.GameActions.SKIP:
                self.send_action(best_action, current_ai_id)

    def __ai_take_hard_action(self, current_ai_id):
        if self.GameActions.DISCARD in self.ai_actions_pool:
            self.ai_actions_pool.remove(self.GameActions.DISCARD)
        discarded_cards = list(self.players[current_ai_id].find_largest_valid_group())
        if discarded_cards:
            self.send_action(self.GameActions.DISCARD, current_ai_id, discarded_cards)
            return
        else:
            temp = []
            best_action = None
            draw_card_number = None
            steal_target = None
            for idx in range(len(self.players)):
                draw_card_number, steal_target, action_scores = self.__get_action_and_scrore(idx)
                if idx == current_ai_id:
                    print(action_scores)
                    best_action = max(self.ai_actions_pool, key=lambda action: action_scores[action])
                    print("hahah==>", best_action)
                else:
                    best_action = max(action_scores, key=action_scores.get)
                best_score = action_scores[best_action]
                temp.append([draw_card_number, steal_target, best_action, best_score])

            best_index, best_one = max(enumerate(temp), key=lambda x: x[1][3])
            print("the best_index:", best_index)
            print("current ai id:", current_ai_id)
            if best_index != current_ai_id and len(self.players[best_index].hand) > 1 and \
                    self.GameActions.STEAL in self.ai_actions_pool:
                best_action = self.GameActions.STEAL
                steal_target = best_index
                print(f"haha, I'm going to steal a card from the opponent{best_index}....")
            else:
                draw_card_number = temp[current_ai_id][0]
                steal_target = temp[current_ai_id][1]
                best_action = temp[current_ai_id][2]

            print("I'm going to remove-->", best_action)
            self.ai_actions_pool.remove(best_action)

            if best_action == self.GameActions.DRAW:
                self.send_action(best_action, current_ai_id, draw_card_number)
            elif best_action == self.GameActions.STEAL:
                self.send_action(best_action, current_ai_id, steal_target)
            elif best_action == self.GameActions.SKIP:
                self.send_action(best_action, current_ai_id)

    def ai_take_action(self, current_ai_id):

        if self.game_ai_level == self.ComputerLevel.EASY:
            self.__ai_take_easy_action(current_ai_id)
        elif self.game_ai_level == self.ComputerLevel.MEDIUM:
            self.__ai_take_medium_action(current_ai_id)
        else:
            self.__ai_take_hard_action(current_ai_id)





















