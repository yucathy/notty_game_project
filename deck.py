import random

from Card import Card


class Deck:

    def __init__(self):
        self.cards = self.create_deck()
        self.shuffle()

    # 创建一副牌-4色/80张
    def create_deck(self):
        colors = ['red', 'blue', 'green', 'yellow']
        numbers = range(1, 11)
        return [Card(color, number) for color in colors for number in numbers] * 2

    # 洗牌（打乱卡牌顺序）
    def shuffle(self):
        random.shuffle(self.cards)

    # 从牌堆中抽取指定数量的卡牌并加入玩家的手牌（包括第一轮发牌）
    # TODO：1.这里由前端限制用户仅可抽取1到3张（提醒前端交互防控）；2.如果牌堆已不足要抽取的数量的处理
    def draw(self, num_cards):
        return [self.cards.pop() for _ in range(min(num_cards, len(self.cards)))]

    # 将玩家丢弃的牌放回牌堆并重新洗牌
    def add_to_deck(self, discarded_cards):
        self.cards.extend(discarded_cards)
        self.shuffle()