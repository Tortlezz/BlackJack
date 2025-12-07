import pygame
from Game import Game
from GameUI import GameUI

decks = int(input("How many decks? "))
cash = float(input("How much starting cash? "))

pygame.init()
game = Game(decks, cash)
ui = GameUI(game)
clock = pygame.time.Clock()

#local event states
running = True
results_mode = False
bet_input_text = ""
results_delay_start = None

while True:
    try:
        bet = float(input(f"\nYou have ${game.money:.2f}. Enter your bet: "))
        if bet > game.money:
            print("You are too poor, try again")
        else: break
    except:
        print("Invalid Input, try again")
game.start(bet)

while running:
    #player turn
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if results_mode:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Simple exit button check using rect stored by GameUI
                if hasattr(ui, "results_exit_rect") and ui.results_exit_rect.collidepoint(mouse_pos):
                    running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Try to convert input to a valid bet and start a new round
                    try:
                        new_bet = float(bet_input_text)
                        if new_bet > 0 and new_bet <= game.money:
                            bet_input_text = ""
                            results_mode = False
                            game.start(new_bet)
                        else:
                            # Invalid bet (<=0 or more than bankroll) – keep text; you could add error text if desired
                            pass
                    except ValueError:
                        # Non-numeric entry; ignore or clear
                        bet_input_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    bet_input_text = bet_input_text[:-1]
                else:
                    # Add character if it's a printable ASCII digit or dot
                    if event.unicode.isdigit() or event.unicode == ".":
                        bet_input_text += event.unicode

                # When in results mode, skip normal game interaction
            continue

        elif event.type == pygame.MOUSEBUTTONDOWN:
            action = ui.get_button_click(pygame.mouse.get_pos())
            if action == "EXIT":
                running = False

            if game.player_turn:
                if action == "Hit":
                    game.player_hit()
                elif action == "Stand":
                    game.player_stand()
                elif action == "Double Down":
                    game.player_double_down()
                elif action == "Insurance":
                    game.player_insurance()


    #dealer turn
    if game.dealer_turn:
        game.dealer_play()

    if not results_mode:
        ui.draw()
    else: ui.draw_results_screen(outcome, bet_input_text)
    clock.tick(30)

    if game.round_over and not results_mode:
        now = pygame.time.get_ticks()
        if results_delay_start is None:
            results_delay_start = now
        elif now - results_delay_start >= 2000: #ms
            outcome = game.resolve_round()
            print(f"\nRound over! Outcome: {outcome} \nMoney: ${game.money:.2f}")
            if game.money <= 0:
                print("\nYou went bankrupt! Game over.")
                running = False
            else:
                results_mode = True
            results_delay_start = None

pygame.quit()