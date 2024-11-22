import random
import itertools
class Players:

    maxinum_hand_size = 20
    
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.add = []
        self.delete = []

    def __eq__(self, name: str) -> bool:
        if type(name) == str:
            return self.name == name
        else:
            return False
        
    def clear_temp_list(self):
        self.add.clear()
        self.delete.clear()

    def draw_cards(self, deck, num_cards) -> bool:
        if (len(self.hand) + num_cards) <= self.maxinum_hand_size:
            self.clear_temp_list()
            cards = deck.draw(num_cards)
            for card in cards:
                self.add.append(card)
            self.hand.extend(cards)
            return True
        
        return False

    # 从其他玩家手牌中随机取一张卡
    def take_random_card(self, other_player) -> bool:
        self.clear_temp_list()
        other_player.clear_temp_list()
        if other_player.hand and (len(self.hand) + 1) <= self.maxinum_hand_size:
            card = random.choice(other_player.hand)
            other_player.delete.append(card)
            other_player.hand.remove(card)
            self.add.append(card)
            self.hand.append(card)
            return True
        return False

    # 验证卡组是否符合丢弃条件，并更新玩家手牌和牌堆
    def discard_group(self, group, deck) -> bool:
        self.clear_temp_list()
        if self.is_valid_group(group):
            self.delete.clear()
            for card in group:
                self.hand.remove(card)
            deck.add_to_deck(group)
            return True
        else:
            return False

    # 是否是有效组
    # TODO：需要再看一下
    def is_valid_group(self, group):
        if len(group) < 3:
            return False
        # 同样颜色连续数字
        if all(card.color == group[0].color for card in group) and \
           all(group[i].number == group[i - 1].number + 1 for i in range(1, len(group))):
            return True
        # 同样数字不同颜色
        if all(card.number == group[0].number for card in group) and \
           len(set(card.color for card in group)) == len(group):
            return True
        return False

    # 显示当前玩家手牌
    def display_hand(self):
        print(f"{self.name}'s hand: {self.hand}")

    # 检查玩家手牌是否为空
    def has_empty_hand(self):
        self.clear_temp_list()
        return len(self.hand) == 0
    

class AIPlayer(Players):
    
    def __init__(self, name):
        super().__init__(name)

    def find_valid_group(self) -> list:
        '''
        return a valid combination in collection.
        '''

        length = len(self.hand)
        for number in range(length, 2, -1):
            combinations = itertools.combinations(self.hand, number)
            for combo in combinations:
                if self.is_valid_group(combo):
                    return combo
        
        return None
    
    def find_largest_valid_group(self) -> list:
        '''
        return a max valid combination in collection.
        '''

        return self.find_valid_group()
