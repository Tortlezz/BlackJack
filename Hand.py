class Hand:
    """
    Represents a hand of cards for a player or dealer in Blackjack.

    Attributes:
        cards (list of Card): The cards currently in the hand.
    """
    def __init__(self):
        self.cards = []

    def calculate_value(self):
        """
        Calculates the total Blackjack value of the hand.
        Aces are counted as 11 unless that would cause a bust, in which
        case they are counted as 1.
        Returns: int: The total value of the hand.
        """
        sum = 0
        aces = 0
        for card in self.cards:
            sum += card.value
            if card.rank == "A":
                aces += 1
        
        while sum > 21 and aces > 0:
            sum -= 10
            aces -= 1

        return sum

    def is_blackjack(self):
        """
        Checks if the hand is a Blackjack (exactly 21).
        Returns: bool: True if hand value is 21, False otherwise.
        """
        return self.calculate_value() == 21

    def is_bust(self):
        """
        Checks if the hand is a bust (over 21).
        Returns: bool: True if hand value is greater than 21, False otherwise.
        """
        return self.calculate_value() > 21

    def hit(self, card):
        """
        Adds a card to the hand.
        Args: card (Card): The card to add to the hand.
        Returns: Card: The card that was added.
        """
        #needs to call deal()
        self.cards.append(card)
        return card

    def reset_hand(self):
        """
        Clear all cards from the hand.
        """
        self.cards = []

    def __str__(self):
        str_cards = ""
        for card in self.cards:
            str_cards += card.__str__() + ", "

        return str_cards[:-2]