class Card:
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
