import pygame
from Game import Game
from GameUI import GameUI

decks = int(input("How many decks? "))
cash = float(input("How much starting cash? "))

pygame.init()
game = Game(decks, cash)
ui = GameUI(game)
clock = pygame.time.Clock()
running = True

bet = float(input(f"\nYou have ${game.money:.2f}. Enter your bet: "))
game.start(bet)
while running:
    #player turn
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            action = ui.get_button_click(pygame.mouse.get_pos())

            if game.player_turn:
                if action == "Hit":
                    game.player_hit()
                elif action == "Stand":
                    game.player_stand()

    #dealer turn
    if game.dealer_turn:
        game.dealer_play()

    ui.draw()
    clock.tick(30)

    if game.round_over:
        outcome = game.resolve_round()
        print(f"Round over! Outcome: {outcome}, Money: ${game.money:.2f}")
        if game.money <= 0:
            print("You went bankrupt! Game over.")
            running = False
        else:
            pygame.display.quit()
            bet = float(input(f"\nYou have ${game.money:.2f}. Enter your bet: "))
            pygame.display.init()
            ui = GameUI(game)
            game.start(bet)

pygame.quit()