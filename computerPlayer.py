from players import Player
import random

class ComputerPlayer(Player):
    def take_turn(self, opponents, deck):
        """
        电脑玩家的回合逻辑
        :param opponents: 所有其他玩家
        :param deck: 当前牌堆
        """
        # 如果电脑玩家难度是简单模式，随机选择操作
        if random.choice([True, False]) and len(deck) > 0:
            # 随机抽取 1 到 3 张牌
            self.draw_cards(deck, random.randint(1, 3))
        elif opponents:
            # 从随机对手手中抽取一张牌
            opponent = random.choice(opponents)
            self.take_random_card(opponent)
        else:
            # 尝试丢弃一个有效的卡组
            self.discard_group()

    def take_turn_advanced(self, opponents, deck):
        """
        电脑玩家的高级逻辑：优先丢弃卡组，其次抽卡，再考虑抽取对手的卡
        :param opponents: 所有其他玩家
        :param deck: 当前牌堆
        """
        if self.discard_group():
            return  # 如果可以丢弃卡组，直接结束回合

        # 如果无法丢弃，尝试从牌堆抽取最多 3 张牌
        if len(self.hand) < 15 and len(deck) > 0:
            self.draw_cards(deck, 3)
            return

        # 如果手牌接近满且无法抽牌，随机抽取对手的一张牌
        if opponents:
            opponent = random.choice(opponents)
            self.take_random_card(opponent)
