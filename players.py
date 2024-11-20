import random
class Players:
    
    def __init__(self, name):
        self.name = name
        self.hand = []

    def draw_cards(self, deck, num_cards):
        self.hand.extend(deck.draw(num_cards))

    # 从其他玩家手牌中随机取一张卡
    def take_random_card(self, other_player):
        if other_player.hand:
            card = random.choice(other_player.hand)
            other_player.hand.remove(card)
            self.hand.append(card)

    # 验证卡组是否符合丢弃条件，并更新玩家手牌和牌堆
    def discard_group(self, group, deck):
        if self.is_valid_group(group):
            for card in group:
                self.hand.remove(card)
            deck.add_to_deck(group)

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
        return len(self.hand) == 0