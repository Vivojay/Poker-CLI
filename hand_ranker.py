class PokerHand(object):
    CARD = "23456789TJQKA"
    RESULT = [False, None, True] #[loss (against oppponent), tie, win (against oppponent)]

    def __init__(self, hand):
        values = ''.join(sorted(hand[::3], key=self.CARD.index))
        # Judge whether a flush
        suits = set(hand[1::3])
        is_flush = len(suits) == 1
        #Whether straight
        is_straight = values in self.CARD
        self.score = (2 * sum(values.count(card) for card in values) # Different card counting
                      + 13 * is_straight + 14 * is_flush, #* 13  straight, flush * 15
                      [self.CARD.index(card) for card in values[::-1]])

    def compare_with(self, other):
        return self.RESULT[(self.score > other.score) - (self.score < other.score) + 1]

##test
if __name__ == '__main__':
    hand,other = "2H 3H 4H 5H 6H" , "KS AS TS QS JS"
    player, opponent = PokerHand(hand), PokerHand(other)
    print(player.compare_with(opponent),  "'{}' against '{}'".format(hand, other))
