import random
import Card

class Deck:
    def __init__(self, deck_num=1):
        self.deck_num = deck_num
        self.cards = []

        self.create_deck()
        self.shuffle()

    def create_deck(self):
        self.ranks = [str(i) for i in range(2, 11)] + ["J", "Q", "K", "A"]
        self.suits = ["♠", "♥", "♦", "♣"]

        for i in range(self.deck_num):
            for suit in self.suits:
                for rank in self.ranks:
                    self.cards.append(Card.Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop()

    def reshuffle(self):
        self.cards = []
        self.create_deck()
        self.shuffle()
