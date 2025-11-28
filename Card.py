class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

        if rank in ["K", "Q", "J"]:
            self.value = 10
        if rank == "A":
            self.value = 11
        else: self.value = int(rank)

    def __str__(self):
        return f"{self.suit}{self.rank}"
