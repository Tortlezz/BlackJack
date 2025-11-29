from Deck import Deck
from Hand import Hand
import pygame

class Game:
    def __init__(self, num_decks=1, starting_cash=1000):
        self.num_decks = num_decks
        self.deck = Deck(num_decks)
        self.money = starting_cash
        self.bet = 0

        self.player_hand = Hand()
        self.dealer_hand = Hand()

        #event states
        self.player_turn = True
        self.dealer_turn = False
        self.round_over = False
        self.dealer_shows = False

    def start(self, bet):
        self.bet = bet
        #setting events
        self.round_over = False
        self.player_turn = True
        self.dealer_turn = False
        self.dealer_shows = False
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
            self.dealer_turn = True

    def check_deck(self):
        deck_penetration = 0.8
        if len(self.deck.cards) < int((1 - deck_penetration) * 52 * self.num_decks):
            self.deck.reshuffle()
            print("Deck reshuffled!")

    def player_hit(self):
        self.player_hand.hit(self.deck.deal())

        # End player turn if bust or 21
        if self.player_hand.is_bust() or self.player_hand.calculate_value() == 21:
            self.player_turn = False
            self.dealer_shows = True
            self.dealer_turn = True

    def player_stand(self):
        self.player_turn = False
        self.dealer_shows = True
        self.dealer_turn = True

    def dealer_play(self):
        while self.dealer_hand.calculate_value() < 17:
            self.dealer_hand.hit(self.deck.deal())
            pygame.time.wait(500)

        self.dealer_turn = False
        self.round_over = True

    def check_winner(self):
        player_value = self.player_hand.calculate_value()
        dealer_value = self.dealer_hand.calculate_value()

        if player_value > 21:
            return "lose"
        elif dealer_value > 21:
            return "win"
        elif player_value > dealer_value:
            return "win"
        elif dealer_value > player_value:
            return "lose"
        else:
            return "push"

    def resolve_round(self):
        outcome = self.check_winner()

        if outcome == "win":
            self.money += self.bet
        elif outcome == "lose":
            self.money -= self.bet
        # Push does not change money
        return outcome





