import Deck
import Hand

deck_num = int(input("Enter the number of decks: "))
deck = Deck.Deck(deck_num)

cash = int(input("Enter the starting cash: "))

while cash > 0:
    bet = int(input("Enter the bet: "))
    player = Hand.Hand(bet)

    player.cards.append(deck.deal())
    player.cards.append(deck.deal())

    value = player.calculate_value() #will be displayed

    #all cash is returned at the end of round
    if player.is_blackjack():
        cash += 2.5 * bet
        continue

    if player.is_bust():
        cash -= bet
        continue

    decision = input("What action would you like to take?: ")
    #More words can be added
    hitWords = ["hit", "hit me"]
    standWords = ["stand"]