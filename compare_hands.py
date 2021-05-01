#https://codereview.stackexchange.com/questions/225119/project-euler-54-poker-hands-in-python
#Thanks to SylvainD for the below code: git profile link: https://codereview.stackexchange.com/users/9452/sylvaind

import collections
import os


class Card:
    """Card object (value and suit)."""
    CARD_VALUES = {
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7,
        '8': 8,
        '9': 9,
        'T': 10,
        'J': 11,
        'Q': 12,
        'K': 13,
        'A': 14
    }

    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    @classmethod
    def from_string(cls, card):
        value, suit = card
        return cls(value, suit)

    def __str__(self):
        return str(self.value) + self.suit

    def __repr__(self):
        return self.__class__.__name__ + "(" + self.value + ", " + self.suit + ")"

    def evaluate(self):
        return Card.CARD_VALUES[self.value]


class Hand:
    """Hand object (iterable of NB_CARDS cards)."""
    NB_CARDS = 5

    def __init__(self, cards):
        assert len(cards) == Hand.NB_CARDS
        self.cards = cards

    @classmethod
    def from_string(cls, string):
        cards = [Card.from_string(chunk) for chunk in string.split()]
        return cls(cards[:Hand.NB_CARDS]), cls(cards[Hand.NB_CARDS:])

    def __str__(self):
        return "-".join(str(c) for c in self.cards)

    def __repr__(self):
        return self.__class__.__name__ + "(" + repr(self.cards) + ")"

    def evaluate(self):
        """Return an arbitrarly formed tuple that can be used to
        sort hands using lexicographic order. First element is an
        integer describing the type of hand. Other values are added
        to be able to differentiate hands.

        Integers used:
        1 High Card: Highest value card.
        2 One Pair: Two cards of the same value.
        3 Two Pairs: Two different pairs.
        4 Three of a Kind: Three cards of the same value.
        5 Straight: All cards are consecutive values.
        6 Flush: All cards of the same suit.
        7 Full House: Three of a kind and a pair.
        8 Four of a Kind: Four cards of the same value.
        9 Straight Flush: All cards are consecutive values of same suit.
        9 Royal Flush: Ten, Jack, Queen, King, Ace, in same suit.
        """
        values = sorted((c.evaluate() for c in self.cards), reverse=True)
        count = collections.Counter(values)
        mc, mc2 = count.most_common(2)
        mc_val, mc_nb = mc
        mc2_val, mc2_nb = mc2
        if mc_nb == 4:
            return (8, mc_val, values)
        elif mc_nb == 3:
            if mc2_nb == 2:
                return (7, mc_val, mc2_val, values)
            else:
                return (4, mc_val, values)
        elif mc_nb == 2:
            if mc2_nb == 2:
                return (3, sorted((mc_val, mc2_val)), values)
            else:
                return (2, mc_val, values)
        else:
            assert mc_nb == 1
            is_flush = len(set(c.suit for c in self.cards)) == 1
            delta = values[0] - values[-1]
            is_straight = delta == Hand.NB_CARDS - 1
            if is_straight:
                return (9 if is_flush else 5, values)
            else:
                return (6 if is_flush else 1, values)

    def __gt__(self, other):  # Note: other magic methods should be defined as well
        return self.evaluate() > other.evaluate()

def euler54(f='p054_poker.txt'):
    """Solution for problem 54."""
    resource_folder = ''
    res = [] #Winning Lines
    res_ = [] #Losing Lines

    with open(os.path.join(resource_folder, f)) as file_:
        contents = file_.read().splitlines()
        file_.seek(0)
        for i in range(len(contents)):
            hand1, hand2 = Hand.from_string(contents[i])
            if hand1 > hand2:
                if contents[i][-1] == '\n':
                    res.append((contents[i][:-1], i))
                else:
                    res.append((contents[i], i))
            
            else:
                if contents[i][-1] == '\n':
                    res_.append((contents[i][:-1], i))
                else:
                    res_.append((contents[i], i))
            # print(i)
    return res, res_
