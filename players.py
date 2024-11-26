import random

class Player:
    def __init__(self, name, is_computer=False):
        """
        初始化玩家
        :param name: 玩家名称
        :param is_computer: 是否为电脑玩家
        """
        self.name = name
        self.is_computer = is_computer
        self.hand = []  # 玩家的手牌列表

    def draw_cards(self, deck, num_cards=1):
        """
        从牌堆抽取指定数量的牌
        :param deck: 当前牌堆
        :param num_cards: 要抽取的牌数
        """
        for _ in range(min(num_cards, len(deck))):
            self.hand.append(deck.pop())

    def find_valid_groups(self):
        """
        找到手牌中所有可以丢弃的有效卡组
        :return: 有效卡组列表
        """
        sequences = []
        sets = []
        colors = {}
        numbers = {}

        for card in self.hand:
            colors.setdefault(card["color"], []).append(card["number"])
            numbers.setdefault(card["number"], []).append(card["color"])

        # 检查连续同色序列
        for color, nums in colors.items():
            nums.sort()
            temp_seq = []
            for i in nums:
                if temp_seq and i != temp_seq[-1] + 1:
                    if len(temp_seq) >= 3:
                        sequences.append([{"color": color, "number": n} for n in temp_seq])
                    temp_seq = []
                temp_seq.append(i)
            if len(temp_seq) >= 3:
                sequences.append([{"color": color, "number": n} for n in temp_seq])

        # 检查不同色相同数字
        for number, cols in numbers.items():
            if len(set(cols)) >= 3:
                sets.append([{"color": color, "number": number} for color in cols[:3]])

        return sequences + sets

    def discard_group(self):
        """
        丢弃找到的有效卡组
        :return: 丢弃的卡组列表
        """
        valid_groups = self.find_valid_groups()
        if valid_groups:
            for group in valid_groups:
                for card in group:
                    self.hand.remove(card)
            return valid_groups
        return []

    def take_random_card(self, opponent):
        """
        随机从对手手中抽取一张牌
        :param opponent: 被抽牌的对手
        :return: 抽到的牌
        """
        if opponent.hand:
            chosen_card = random.choice(opponent.hand)
            self.hand.append(chosen_card)
            opponent.hand.remove(chosen_card)
            return chosen_card
        return None
