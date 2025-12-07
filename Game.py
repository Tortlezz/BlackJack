from Deck import Deck
from Hand import Hand
from SoundManager import SoundManager
import pygame

class Game:
    """
    Represents a game of Blackjack, managing the deck, player and dealer hands,
    bets, money, and game flow (turns and round outcomes).

    Attributes:
        num_decks (int): Number of decks used in the game.
        deck (Deck): The deck object used to deal cards.
        money (float): The player’s current money balance.
        bet (float): Current bet amount.
        player_hand (Hand): The player’s current hand.
        dealer_hand (Hand): The dealer’s current hand.
        """
    def __init__(self, num_decks=1, starting_cash=1000):
        self.num_decks = num_decks
        self.deck = Deck(num_decks)
        self.money = starting_cash
        self.bet = 0

        self.player_hand = Hand()
        self.dealer_hand = Hand()

        #sound
        self.sound_manager = SoundManager()

        #event states
        self.player_turn = True
        self.dealer_turn = False
        self.round_over = False
        self.dealer_shows = False
        self.insurance = False
        self.betting_screen = True

    def start(self, bet):
        """
        Starts a new round with a given bet.
        Resets hands, checks the deck for reshuffling, and deals initial cards.
        Also checks for natural Blackjack on the player's hand.
        Args: bet (int): The amount the player wants to wager for this round.
        """
        self.bet = bet

        self.sound_manager.play_chips_sound()
        #setting events
        self.round_over = False
        self.player_turn = True
        self.dealer_turn = False
        self.dealer_shows = False
        self.insurance = False
        #reset hands
        self.player_hand.reset_hand()
        self.dealer_hand.reset_hand()
        #check deck
        self.check_deck()
        #initial deal
        self.player_hand.hit(self.deck.deal())
        self.player_hand.hit(self.deck.deal())
        self.dealer_hand.hit(self.deck.deal())
        self.dealer_hand.hit(self.deck.deal())

        if self.player_hand.is_blackjack():
            self.player_turn = False
            self.dealer_shows = True
            self.sound_manager.play_turn_sound()
            self.dealer_turn = True

    def check_deck(self):
        """
        Reshuffle the deck if penetration reaches threshold.
        Prints a message when reshuffling occurs.
        """
        deck_penetration = 0.8
        if len(self.deck.cards) < int((1 - deck_penetration) * 52 * self.num_decks):
            self.deck.reshuffle()
            self.sound_manager.play_shuffle_sound()
            print("\nDeck reshuffled!")

    def player_hit(self):
        """
        Player takes a hit: add a card to their hand.
        Automatically ends the player’s turn and starts dealer's turn if the player busts or hits 21.
        """
        self.sound_manager.play_hit_sound()
        self.player_hand.hit(self.deck.deal())

        # End player turn if bust or 21
        if self.player_hand.is_bust() or self.player_hand.calculate_value() == 21:
            self.player_turn = False
            self.dealer_shows = True
            self.sound_manager.play_turn_sound()
            self.dealer_turn = True

    def player_stand(self):
        """
        Player chooses to stand.
        Ends the player’s turn and starts the dealer’s turn.
        """
        self.player_turn = False
        self.dealer_shows = True
        self.sound_manager.play_turn_sound()
        self.dealer_turn = True

    def player_double_down(self):
        if self.bet <= 0.5 * self.money:
            self.bet = 2 *  self.bet
            self.sound_manager.play_hit_sound()
            self.player_hand.hit(self.deck.deal())

            # End player turn if bust or 21
            if self.player_hand.is_bust() or self.player_hand.calculate_value() == 21:
                self.player_turn = False
                self.dealer_shows = True
                self.sound_manager.play_turn_sound()
                self.dealer_turn = True

    def player_insurance(self):
        self.insurance = True

    def dealer_play(self):
        """
        Dealer's turn logic: hits until reaching 17 or higher.
        After finishing, ends the dealer's turn and marks the round as over.
        """
        while self.dealer_hand.calculate_value() < 17:
            self.dealer_hand.hit(self.deck.deal())
            pygame.time.wait(500)

        self.dealer_turn = False
        self.round_over = True

    def check_winner(self):
        """
        Determine the outcome of the round based on hand values.
        Returns: str: "win" if player wins, "lose" if player loses, "push" if tied.
        """
        player_value = self.player_hand.calculate_value()
        dealer_value = self.dealer_hand.calculate_value()

        self.insurance_result = False
        if self.insurance:
            if dealer_value == 21 and len(self.dealer_hand.cards) == 2:
                return "insurance"
            else: self.insurance_result = True

        if len(self.player_hand.cards) == 2 and self.player_hand.is_blackjack():
            return "blackjack", self.insurance_result

        if player_value > 21: return "lose", self.insurance_result
        elif dealer_value > 21: return "win", self.insurance_result
        elif player_value > dealer_value: return "win", self.insurance_result
        elif dealer_value > player_value: return "lose", self.insurance_result
        else: return "push", self.insurance_result

    def resolve_round(self):
        """
        Resolve the round by updating player's money according to outcome.
        Returns: str: Outcome of the round ("win", "lose", "push").
        """
        outcome = self.check_winner()

        if outcome[1] == False:
            if outcome[0] == "push": self.money += 0
            elif outcome[0] == "win": self.money += self.bet
            elif outcome[0] == "lose": self.money -= self.bet
            elif outcome[0] == "blackjack": self.money += 1.5 * self.bet

            return outcome[0]

        if outcome[0] == "push": self.money -= self.bet
        elif outcome[0] == "win": self.money += 0
        elif outcome[0] == "lose": self.money -= 2 * self.bet

        print(f"Insurance side-bet lost. Main hand: {outcome[0]}")
        return outcome[0]

