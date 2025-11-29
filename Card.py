class Card:
    """
    Represents a single playing card with a suit, rank, and Blackjack value.

    Attributes:
        suit (str): The suit of the card.
        rank (str): The rank of the card .
        value (int): The Blackjack value of the card (2-10 for number cards,
                         10 for face cards, 11 for Ace).
    """
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

        if rank in ["J", "Q", "K"]:
            self.value = 10
        elif rank == "A":
            self.value = 11
        else: self.value = int(rank)

    def __str__(self):
        return f"{self.suit}{self.rank}"