import random
import itertools
from itertools import combinations
class Players:

    maximum_hand_size = 20

    def __init__(self, name):
        self.name = name
        self.hand = []
        self.add = []
        self.delete = []

    def initialize_state(self):
        '''reset the status'''
        self.hand.clear()
        self.add.clear()
        self.delete.clear()

    def clear_temp_list(self):
        self.add.clear()
        self.delete.clear()

    def draw_cards(self, deck, num_cards, appoint_card=None) -> bool:
        """
        Draw cards from the deck. If appoint_card is provided, draw specific cards instead.

        :param deck: The deck to draw cards from.
        :param num_cards: The number of cards to draw.
        :param appoint_card: A list of specific cards to draw (optional).
        :return: True if cards were successfully drawn, False otherwise.
        """
        # Draw the appropriate cards
        if appoint_card:
            cards = deck.draw_specific(appoint_card)
            if len(cards) < len(appoint_card):
                print("Warning: Not all specified cards were available in the deck.")
        else:
            cards = deck.draw(num_cards)

        # Validate hand size
        if len(self.hand) + len(cards) <= self.maximum_hand_size:
            self.hand.extend(cards)
            self.add.extend(cards)
            return True

        # If hand size exceeded, return cards to the deck
        deck.add_to_deck(cards)
        return False

    def take_random_card(self, other_player, appoint_card=None) -> bool:
        """
        Take a random card from another player, or use a specified card if appoint_card is provided.

        :param other_player: The player from whom to take a card.
        :param appoint_card: A list containing a single specific card to take, or an empty list for random.
        :return: True if the card was successfully taken, False otherwise.
        """
        # Check if the action is possible
        if not other_player.hand:
            return False
        if len(self.hand) >= self.maximum_hand_size:
            return False

        # Determine the card to take, If appoint_card is provided and not empty
        if appoint_card:
            card = appoint_card[0]
            if card not in other_player.hand:
                return False
        else:
            card = random.choice(other_player.hand)

        # Transfer the card
        other_player.delete.append(card)
        other_player.hand.remove(card)
        self.add.append(card)
        self.hand.append(card)
        return True

    # 验证卡组是否符合丢弃条件，并更新玩家手牌和牌堆
    def discard_group(self, group, deck) -> bool:
        if self.is_valid_group(group):
            for card in group:
                print(self.hand)
                print(card)
                self.delete.append(card)
                print(self.delete)
                self.hand.remove(card)
            deck.add_to_deck(group)
            return True
        else:
            return False

    # 是否是有效组
    def is_valid_group(self, group):
        if len(group) < 3:
            return False

        group = sorted(group, key=lambda group: group.number)

        # 同样颜色连续数字
        if all(card.color == group[0].color for card in group) and \
           all(group[i].number == group[i - 1].number + 1 for i in range(1, len(group))):
            return True
        # 同样数字不同颜色
        if all(card.number == group[0].number for card in group) and \
           len(set(card.color for card in group)) == len(group):
            return True
        return False

    def find_valid_group_to_draw(self, deck, num_cards):
        """
        Find cards from the deck that can complement the current hand to form a valid group.
        :param deck: The deck to draw cards from.
        :param num_cards: Number of cards to draw.
        :return: A list of cards to draw.
        """
        needed_cards = set()

        # 如果手牌只有一张牌需要特殊处理
        if len(self.hand) == 1:
            # 仅抽一张卡
            if num_cards == 1:
                return self.find_potential_cards(deck, num_cards)

            single_card = self.hand[0]
            if num_cards == 2:
                # 从deck中找到两张卡，与single_card组成有效组
                for i, card1 in enumerate(deck.cards):
                    for j, card2 in enumerate(deck.cards):
                        if i != j and card1 != single_card and card2 != single_card:
                            potential_group = [single_card, card1, card2]
                            if self.is_valid_group(potential_group):
                                return [card1, card2]

            elif num_cards == 3:
                # 从deck中找到三张卡，与single_card组成有效组
                for i, card1 in enumerate(deck.cards):
                    for j, card2 in enumerate(deck.cards):
                        for k, card3 in enumerate(deck.cards):
                            if len({i, j, k}) == 3 and all(card not in [single_card] for card in [card1, card2, card3]):
                                potential_group = [single_card, card1, card2, card3]
                                if self.is_valid_group(potential_group):
                                    return [card1, card2, card3]

        else:
            # 遍历用户手牌的所有组合，找到补充有效组所需的卡牌
            for i in range(1, len(self.hand) + 1):
                for subset in combinations(self.hand, i):
                    potential_group = list(subset)
                    for card in deck.cards:
                        if card not in self.hand and card not in potential_group:
                            potential_group.append(card)
                            if self.is_valid_group(potential_group):
                                needed_cards.add(card)
                            potential_group.pop()

        # 从所需的卡牌中选取指定数量的卡牌
        needed_cards = list(needed_cards)
        if len(needed_cards) >= num_cards:
            return needed_cards[:num_cards]
        else:
            # 补充不足的部分从随机卡牌中选取
            # additional_cards = random.sample(deck.cards, num_cards - len(needed_cards))
            # 补充不足的部分: 从卡牌中选取与已有手牌中随机一张，相同颜色数字相近 或者 颜色不同数字相同的牌
            additional_cards = self.find_potential_cards(deck, num_cards - len(needed_cards))
            return needed_cards + additional_cards

    # 在deck中找出num_cards张和自己手牌中某一张颜色相同数字相邻，或者颜色不同数字相同的卡牌
    def find_potential_cards(self, deck, num_cards):
        hand_card = self.hand[0]
        color = hand_card.color
        number = hand_card.number
        needed_cards = []

        for card in deck.cards:
            if ((card.color == color and abs(card.number - number) == 1)
                    or (card.number == number and card.color != color)):
                needed_cards.append(card)
                num_cards -= 1
                if num_cards == 0:
                    break
        return needed_cards


    def find_valid_group_to_steal(self, ai_hand):
        """
        Find a card from the AI player's hand that can form a valid group with the current hand.
        If no valid group is found, return a random card from the AI's hand.

        :param ai_hand: The AI player's hand to check for valid groups.
        :return: A list containing a valid card to steal, or a random card if no valid group is found.
        """
        for ai_card in ai_hand:
            print(f'测试！！！！！！！！！！！！！！！！！！1」「」{ai_card}')
            for combo in combinations(self.hand, 2):  # 获取list1中所有可能的两个元素组合
                group = list(combo) + [ai_card]  # 组合成一个三元素列表
                if self.is_valid_group(group):  # 调用is_valid_group方法判断是否有效
                    print(f'通过了！！！！！！！！！！！！！！！！！！1」「」{ai_card}')
                    return [ai_card]

        # 如果没有符合条件的卡牌，随机返回AI手牌中一张
        card= random.choice(ai_hand)
        print(f'~~~~~`没有找到随机返回」{card}')
        return [card]

    # 是否存在有效组
    def has_valid_group(self, hand=None):
        if hand is None:
            hand = self.hand
        else:
            if isinstance(hand, list):
                hand = self.hand + hand
            else:
                hand = self.hand + [hand]
        print(f'待测试手-----牌--------{hand}')
        n = len(hand)
        for i in range(n):
            for j in range(i + 3, n + 1):
                group = hand[i:j]
                if self.is_valid_group(group):
                    return group
        return None

    def find_valid_element(self, other_player, is_valid_group):
        """
        在list2中寻找一个元素，与list1中的任意两个元素组合后，满足is_valid_group。

        :param list1: 第一个列表，包含多个元素。
        :param list2: 第二个列表，包含多个元素。
        :param is_valid_group: 方法，接收一个三元素列表，返回布尔值。
        :return: 如果找到符合条件的list2元素，返回该元素；否则返回None。
        """
        for element in other_player.hand:
            for combo in combinations(self.hand, 2):  # 获取list1中所有可能的两个元素组合
                group = list(combo) + [element]  # 组合成一个三元素列表
                if is_valid_group(group):  # 调用is_valid_group方法判断是否有效
                    return element  # 返回当前list2的元素
        return None  # 如果没有找到符合条件的元素，则返回None

    # 检查玩家手牌是否为空
    def has_empty_hand(self):
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

        return []

    def find_largest_valid_group(self) -> list:
        '''
        return a max valid combination in collection.
        '''

        return self.find_valid_group()
