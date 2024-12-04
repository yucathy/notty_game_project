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

    # Validate if the deck meets the discard conditions, and update the player's hand and deck."
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

    def is_valid_group(self, group):
        if len(group) < 3:
            return False

        group = sorted(group, key=lambda group: group.number)

        # Consecutive numbers of the same color
        if all(card.color == group[0].color for card in group) and \
           all(group[i].number == group[i - 1].number + 1 for i in range(1, len(group))):
            return True
        # Same numbers in different colors
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

        # If the hand contains only one card, special handling is required.
        if len(self.hand) == 1:
            # only draw one card
            if num_cards == 1:
                return self.find_potential_cards(deck, num_cards)

            single_card = self.hand[0]
            if num_cards == 2:
                # Find two cards from the deck to form a valid set with the single_card
                for i, card1 in enumerate(deck.cards):
                    for j, card2 in enumerate(deck.cards):
                        if i != j and card1 != single_card and card2 != single_card:
                            potential_group = [single_card, card1, card2]
                            if self.is_valid_group(potential_group):
                                return [card1, card2]

            elif num_cards == 3:
                # Find three cards from the deck to form a valid set with the single_card.
                for i, card1 in enumerate(deck.cards):
                    for j, card2 in enumerate(deck.cards):
                        for k, card3 in enumerate(deck.cards):
                            if len({i, j, k}) == 3 and all(card not in [single_card] for card in [card1, card2, card3]):
                                potential_group = [single_card, card1, card2, card3]
                                if self.is_valid_group(potential_group):
                                    return [card1, card2, card3]

        else:
            # Traverse all combinations of the user's hand to find the cards needed to complete a valid set
            for i in range(1, len(self.hand) + 1):
                for subset in combinations(self.hand, i):
                    potential_group = list(subset)
                    for card in deck.cards:
                        if card not in self.hand and card not in potential_group:
                            potential_group.append(card)
                            if self.is_valid_group(potential_group):
                                needed_cards.add(card)
                            potential_group.pop()

        # Select a specified number of cards from the required cards.
        needed_cards = list(needed_cards)
        if len(needed_cards) >= num_cards:
            return needed_cards[:num_cards]
        else:
            # Select the remaining cards from random cards.
            # additional_cards = random.sample(deck.cards, num_cards - len(needed_cards))
            additional_cards = self.find_potential_cards(deck, num_cards - len(needed_cards))
            return needed_cards + additional_cards

    # Find num_cards cards in the deck that either have the same color and adjacent numbers \
    # or have different colors but the same number as one of the cards in the player's hand.
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
            for combo in combinations(self.hand, 2):  
                group = list(combo) + [ai_card]  
                if self.is_valid_group(group): 
                    return [ai_card]

        # If no cards meet the conditions, randomly return one card from the AI's hand
        card= random.choice(ai_hand)
        return [card]

    # Does a valid set exist?
    def has_valid_group(self, hand=None):
        if hand is None:
            hand = self.hand
        else:
            if isinstance(hand, list):
                hand = self.hand + hand
            else:
                hand = self.hand + [hand]
        n = len(hand)
        for i in range(n):
            for j in range(i + 3, n + 1):
                group = hand[i:j]
                if self.is_valid_group(group):
                    return group
        return None

    def find_valid_element(self, other_player, is_valid_group):
        """
        Find an element in list2 that, when combined with any two elements from list1, satisfies is_valid_group.

        :param list1: The first list containing multiple elements.
        :param list2: The second list containing multiple elements.
        :param is_valid_group: A function that takes a list of three elements and returns a boolean.
        :return: If an element from list2 meets the condition, return that element; otherwise, return None.
        """
        for element in other_player.hand:
            for combo in combinations(self.hand, 2):  
                group = list(combo) + [element]  
                if is_valid_group(group):  
                    return element  
        return None  

    def has_empty_hand(self):
        '''check whether handset is empty'''
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
