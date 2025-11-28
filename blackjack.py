from Game import Game

decks = int(input("How many decks? "))
cash = int(input("How much starting cash? "))

game = Game(decks, cash)
game.start()