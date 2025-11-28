class Hand:
    def __init__(self):
        self.cards = []

    def calculate_value(self):
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

    def is_blackjack(self): # calculated at the beginning of the round ONLY
        return self.calculate_value() == 21

    def is_bust(self):
        return self.calculate_value() > 21 #calculated after each action

    def hit(self, card): #needs to call deal()
        self.cards.append(card)
        return card

    def reset_hand(self):
        self.cards = []

    def __str__(self):
        str_cards = ""
        for card in self.cards:
            str_cards += card.__str__() + ", "

        return str_cards[:-2]
