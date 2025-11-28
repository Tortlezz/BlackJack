from Deck import Deck
from Hand import Hand

class Game:
    def __init__(self, num_decks=1, starting_cash=1000):
        self.deck = Deck(num_decks)
        self.money = starting_cash
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self.bet = 0

    def start(self):
        while self.money > 0:
            self.take_bet()
            self.play_round()

            again = input("Play another round? (Y/N) ").strip().lower()
            if again != "y":
                break

        print("Thanks for playing!")

    def take_bet(self):
        print(f"\nYou have ${self.money:.2f}")
        self.bet = float(input("Enter your bet: "))

    def play_round(self):
        self.reset_hands()
        self.initial_deal()
        self.inital_show()

        if self.player_hand.is_blackjack():
            print(f"\nBlackjack! +${self.bet * 1.5:.2f}")
            self.money += self.bet * 1.5
            return

        result = self.player_turn()

        if result == "bust":
            print(f"Total value: {self.player_hand.calculate_value()}")
            print("\nStinky loser!\n")
            self.money -= self.bet
            return

        self.dealer_turn()
        outcome = self.check_winner()
        self.distribute_money(outcome)

    def reset_hands(self):
        self.player_hand.reset_hand()
        self.dealer_hand.reset_hand()

        if len(self.deck.cards) < 8:
            self.deck.reshuffle()

    def initial_deal(self):
        #2 cards per player
        self.player_hand.hit(self.deck.deal())
        self.player_hand.hit(self.deck.deal())
        self.dealer_hand.hit(self.deck.deal())
        self.dealer_hand.hit(self.deck.deal())

    def inital_show(self):
        print(f"\nYour hand: {self.player_hand}")
        print(f"Dealer hand: {self.dealer_hand.cards[0]}, ??")

    def player_turn(self):
        while True:
            print(f"Your hand value: {self.player_hand.calculate_value()}")

            move = input("\nHit (H) or Stand (S)? ").strip().lower()
            if move == "h":
                print(f"\nYou drew {self.player_hand.hit(self.deck.deal())}")

                if self.player_hand.is_blackjack():
                    return ""

                if self.player_hand.is_bust():
                    return "bust"
            else:
                return ""

    def dealer_turn(self):
        print(f"\nDealer hand: {self.dealer_hand}")
        print(f"Dealer value: {self.dealer_hand.calculate_value()}")

        while self.dealer_hand.calculate_value() < 17:
            print(f"Dealer drew {self.dealer_hand.hit(self.deck.deal())}")
            print(f"Dealer value: {self.dealer_hand.calculate_value()}")

    def check_winner(self):
        player_value = self.player_hand.calculate_value()
        dealer_value = self.dealer_hand.calculate_value()

        if dealer_value > 21: #dealer busts
            return "win"

        if player_value == dealer_value:
            return "push"
        elif dealer_value > player_value:
            return "lose"
        else: return "win"

    def distribute_money(self, outcome):
        if outcome == "win":
            print(f"\nYou won! +${self.bet}")
            self.money += self.bet
        elif outcome == "lose":
            print(f"\nYou lost! -${self.bet}")
            self.money -= self.bet
        else: print("\nPush!")
