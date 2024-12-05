import random

from card import Card


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
    def draw(self, num_cards):
        return [self.cards.pop() for _ in range(min(num_cards, len(self.cards)))]

    # 从牌堆中抽取指定卡牌
    def draw_specific(self, cards_to_draw):
        drawn_cards = []
        for card in cards_to_draw:
            for deck_card in self.cards:
                if deck_card.color == card.color and deck_card.number == card.number:
                    drawn_cards.append(deck_card)
                    self.cards.remove(deck_card)
                    break
        return drawn_cards

    # 将玩家丢弃的牌放回牌堆并重新洗牌
    def add_to_deck(self, discarded_cards):
        self.cards.extend(discarded_cards)
        self.shuffle()