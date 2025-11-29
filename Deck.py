import random
import Card

class Deck:
    """
    Represents a deck (or multiple decks) of playing cards used in Blackjack.

    Attributes:
        deck_num (int): Number of standard 52-card decks in this shoe.
        cards (list of Card): The list of Card objects currently in the deck.
        ranks (list of str): List of all possible card ranks.
        suits (list of str): List of all possible card suits.
        """
    def __init__(self, deck_num=1):
        self.deck_num = deck_num
        self.cards = []

        self.create_deck()
        self.shuffle()

    def create_deck(self):
        """
        Generates the cards for the deck(s) according to the number of decks.
        """
        self.ranks = [str(i) for i in range(2, 11)] + ["J", "Q", "K", "A"]
        self.suits = ["♠", "♥", "♦", "♣"]

        for i in range(self.deck_num):
            for suit in self.suits:
                for rank in self.ranks:
                    self.cards.append(Card.Card(suit, rank))

    def shuffle(self):
        """
        Randomly shuffles the cards in the deck.
        """
        random.shuffle(self.cards)

    def deal(self):
        """
        Removes and returns the top card from the deck (shuffled).
        Returns: Card: The card dealt from the deck.
        """
        return self.cards.pop()

    def reshuffle(self):
        """
        Resets the deck to its original state and shuffles all cards.
        Clears current cards, recreates the deck(s), and shuffles them.
        """
        self.cards = []
        self.create_deck()
        self.shuffle()