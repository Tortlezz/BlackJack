import pygame

class GameUI:
    """
    Handles all Pygame-based rendering and UI interaction for the Blackjack game.

    Attributes:
        game (Game): The main Game object containing game state and logic.
        screen (pygame): The main display surface.
        button_font (pygame): Font used for rendering button text.
        card_images (dict): Maps (rank, suit) tuples to their corresponding Pygame images.
        card_back (pygame): Image of the back of a card.
    """

    def __init__(self, game):
        self.game = game
        self.screen = pygame.display.set_mode((1280, 720))
        self.button_font = pygame.font.SysFont("arial", 30)

        self.load_pics()
        self.create_buttons()

    def load_pics(self):
        """
        Loads and scales all card images into memory.
        Creates a dict, mapping (rank, suit) tuples to images.
        """
        self.card_images = {}
        symbol_to_words = {"♠": "spades", "♥": "hearts", "♦": "diamonds", "♣": "clubs"}
        rank_to_words = {"J": "jack", "Q": "queen", "K": "king", "A": "ace"}
        suits = self.game.deck.suits
        ranks = self.game.deck.ranks

        for suit in suits:
            for rank in ranks:
                if rank in ["J", "Q", "K", "A"]:
                    filename = f"images/PNG-cards-1.3/{rank_to_words[rank]}_of_{symbol_to_words[suit]}2.png"
                else: filename = f"images/PNG-cards-1.3/{rank}_of_{symbol_to_words[suit]}.png"

                img = pygame.image.load(filename)
                img = pygame.transform.scale(img, (80, 120))
                self.card_images[(rank, suit)] = img

        self.card_back = pygame.image.load("images/PNG-cards-1.3/_back_card.png")
        self.card_back = pygame.transform.scale(self.card_back, (80, 120))

    def draw(self):
        """
        Redraws the entire game screen, including player and dealer cards and buttons.
        Should be called each action to update visuals.
        """
        color = (0, 120, 0)
        self.screen.fill(color)
        self.draw_player_cards()
        self.draw_dealer_cards()
        self.draw_buttons()
        pygame.display.flip()

    def draw_player_cards(self):
        """
        Draws all cards in the player's hand at the bottom of the screen.
        Cards are spaced horizontally with a fixed offset.
        """
        for i, card in enumerate(self.game.player_hand.cards):
            img = self.card_images[(card.rank, card.suit)]
            self.screen.blit(img, (100 + i * 90, 500))

    def draw_dealer_cards(self):
        """
        Draws all cards in the dealer's hand at the top of the screen.
        Cards are spaced horizontally with a fixed offset.
        If dealer_shows is False (start of round), the first card is displayed face down.
        """
        for i, card in enumerate(self.game.dealer_hand.cards):
            if i == 0 and self.game.dealer_shows == False:
                img = self.card_back
            else: img = self.card_images[(card.rank, card.suit)]
            self.screen.blit(img, (100 + i * 90, 100))

    def create_buttons(self):
        """
        Creates clickable button rectangles for player actions.
        Stores buttons in a dictionary mapping button names to pygame.Rect objects.
        """
        self.buttons = {}

        button_width = 120
        button_height = 50
        spacing = 20
        start_x = 100
        y = 650

        self.buttons["Hit"] = pygame.Rect(start_x, y, button_width, button_height)
        self.buttons['Stand'] = pygame.Rect(start_x + button_width + spacing, y, button_width, button_height)

    def draw_buttons(self):
        """
        Draws all buttons on the screen with text and an outline.
        """
        button_color = (200, 200, 200)
        for name, button in self.buttons.items():
            pygame.draw.rect(self.screen, (200, 200, 200), button)
            pygame.draw.rect(self.screen, (0, 0, 0), button, 3) #button outline

            text_surf = self.button_font.render(name.capitalize(), True, (0, 0, 0))
            text_rect = text_surf.get_rect(center=button.center)
            self.screen.blit(text_surf, text_rect)

    def get_button_click(self, mouse_pos):
        """
        Determine if the mouse position is over a button and return its name.
        Args: mouse_pos (tuple): (x, y) coordinates of the mouse click.
        Returns: str or None: The name of the button clicked ("Hit", "Stand"), or None if no button was clicked.
        """
        for name, rect in self.buttons.items():
            if rect.collidepoint(mouse_pos):
                return name
        return None