import itertools

from Card import Card
from players import Players
import random

"""
电脑玩家的回合逻辑
根据难易策略行动
"""
class ComputerPlayer(Players):

    def __init__(self, name):
        super().__init__(name, is_computer=True)

    # version1.0 easy
    def take_turn(self, opponents, deck):
        """
        电脑玩家的回合逻辑
        :param opponents: 所有其他玩家
        :param deck: 当前牌堆
        """
        num = random.random()
        # 随机决定是否直接跳过回合（20%的概率）
        if num <= 0.2:
            return

        # 随机选择抽牌或偷牌
        if num <= 0.4 and num > 0.2 and len(deck) > 0:
            # 随机抽取 1 到 3 张牌
            self.draw_cards(deck, random.randint(1, 3))

        if num <= 0.6 and num > 0.4 and opponents:
            # 从随机对手手中抽取一张牌
            opponent = random.choice(opponents)
            self.take_random_card(opponent)

        if num <= 0.8 and num > 0.6 and len(deck) > 0:
            # 随机抽取 1 到 3 张牌
            self.draw_cards(deck, random.randint(1, 3))
            # 尝试丢弃一个有效的卡组
            valid_group = self.find_valid_group()
            if valid_group:
                self.discard_group(valid_group, deck)

        if num <= 1 and num > 0.8 and opponents:
            # 从随机对手手中抽取一张牌
            opponent = random.choice(opponents)
            self.take_random_card(opponent)
            # 尝试丢弃一个有效的卡组
            valid_group = self.find_valid_group()
            if valid_group:
                self.discard_group(valid_group, deck)

    # version1.0 hard
    def take_turn_advanced(self, opponents, deck):
        """
        电脑玩家的高级逻辑：优先丢弃卡组，其次抽卡，再考虑抽取对手的卡
        :param opponents: 所有其他玩家
        :param deck: 当前牌堆
        """
        valid_group = self.find_valid_group()
        # 如果可以丢弃卡组，直接结束回合
        if valid_group and self.discard_group(valid_group, deck):
            return

        # 如果无法丢弃，尝试从牌堆抽取最多 3 张牌
        if len(self.hand) < 15 and deck.size() > 0:
            self.draw_cards(deck, 3)
        # 如果手牌接近满且无法抽牌，随机抽取对手的一张牌
        elif opponents:
            opponent = random.choice(opponents)
            self.take_random_card(opponent)

    def find_valid_group(self) -> list:
        length = len(self.hand)
        for number in range(length, 2, -1):
            combinations = itertools.combinations(self.hand, number)
            for combo in combinations:
                if self.is_valid_group(combo):
                    return list(combo)
        return None

    # ——————————————————————————————————————————————————————————————————————————
    # version2.0 easy
    def easy_mode(self, opponents, deck):
        """
        电脑玩家简单模式：随机执行一个动作（抽卡或从对手手中随机抽取一张卡）
        :param opponents: 其他玩家的列表
        :param deck: 当前的牌堆
        """
        if random.choice([True, False]) and deck.size() > 0:
            self.draw_cards(deck, random.randint(1, 3))
        elif opponents:
            opponent = random.choice(opponents)
            self.take_random_card(opponent)

    # version2.0 medium
    def medium_mode(self, opponents, deck):
        """
        电脑玩家中等模式：优先丢弃有效组，如果没有组可丢弃，则随机抽卡或从对手手中抽卡
        :param opponents: 其他玩家的列表
        :param deck: 当前的牌堆
        """
        # 尝试找到一个有效组进行丢弃
        valid_group = self.find_valid_group()
        if valid_group and self.discard_group(valid_group, deck):
            return
        # 如果不能丢弃有效组，从牌堆随机抽取 1 到 3 张牌
        if deck.size() > 0:
            self.draw_cards(deck, random.randint(1, 3))
        # 如果无法抽牌，则从随机对手手中抽取一张牌
        elif opponents:
            opponent = random.choice(opponents)
            self.take_random_card(opponent)

    # version2.0 hard
    def hard_mode(self, opponents, deck, hands):
        """
        电脑玩家困难模式：优先计算最大的有效组和胜率，再决定策略（抽卡或从对手手中抽牌）
        :param opponents: 其他玩家的列表
        :param deck: 当前的牌堆
        :param hands: 所有玩家的手牌列表
        """
        # 尝试丢弃最大的有效组
        largest_valid_group = self.find_largest_valid_group()
        if largest_valid_group and self.discard_group(largest_valid_group, deck):
            return

        # 计算胜率
        win_probability = self.probability_of_valid_group(hands)
        if win_probability > 0.5:
            # 如果赢牌概率较高，优先抽 3 张牌
            if deck.size() > 0:
                self.draw_cards(deck, 3)
            elif opponents:
                # 否则从随机对手手中抽一张牌
                opponent = random.choice(opponents)
                self.take_random_card(opponent)
        else:
            # 如果赢牌概率较低，优先从对手手中抽牌增加手牌选择
            if opponents:
                opponent = random.choice(opponents)
                self.take_random_card(opponent)
            elif deck.size() > 0:
                # 如果无法从对手抽牌，则从牌堆随机抽 1 到 3 张牌
                self.draw_cards(deck, random.randint(1, 3))

    def find_largest_valid_group(self):
        """
        查找手牌中最大的有效组
        :return: 最大的有效组（列表形式），如果没有找到则返回空列表。
        """
        n = len(self.hand)
        # 按卡牌的数字进行排序，便于查找连续组
        groups = sorted(self.hand, key=lambda card: card.number)
        largest_group = None

        # 遍历所有可能的起始点和结束点，寻找有效组
        for i in range(n):
            # 组的长度至少为 3
            for j in range(i + 3, n + 1):
                group = groups[i:j]
                if self.is_valid_group(group):
                    # 如果找到一个更大的有效组，更新 largest_group
                    if largest_group is None or len(group) > len(largest_group):
                        largest_group = group

        return largest_group if largest_group is not None else []

    def probability_of_valid_group(self, hands):
        """
        计算当前玩家形成有效组的概率。
        :param hands: 所有玩家的手牌列表
        :return: 当前玩家的赢牌概率（0.0 到 1.0）。
        """
        first_player_hand = hands[0]

        # 当前手牌存在有效组
        if first_player_hand.find_valid_group():
            return 1.0

        deck_dict = {f"{color} {number}": 2 for color in ["red", "blue", "green", "yellow"] for number in range(1, 11)}

        for hand in hands:
            for card in hand.hand:
                card_str = f"{card.color} {card.number}"
                if deck_dict[card_str] > 0:
                    deck_dict[card_str] -= 1

        original_hand = [f"{card.color} {card.number}" for card in first_player_hand.hand]

        valid_group_count = 0
        total_deck_cards = sum(deck_dict.values())

        for card_str, count in deck_dict.items():
            if count > 0:
                temp_hand = original_hand + [card_str]
                temp_collection = [self._str_to_card(card) for card in temp_hand]

                if self.is_valid_group(temp_collection):
                    valid_group_count += count

        return valid_group_count / total_deck_cards if total_deck_cards > 0 else 0.0

    @staticmethod
    def _str_to_card(card_str):
        """
        字符串转Card对象
        :param card_str: 如 "red 3" 的卡牌字符串
        :return: Card 对象
        """
        color, number = card_str.split()
        return Card(color=color, number=int(number))

