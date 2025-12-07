import pygame

class SoundManager():

    def __init__(self):
        pygame.mixer.init()
        self.sounds = {
            'hit': 'sounds/Card_Hit_Effect.mp3',
            'shuffle': 'sounds/shuffling-cards-74757.mp3',
            'chips': 'sounds/pokerchipsdropping-27240.mp3',
            'turn': 'sounds/Turn_Card_Noise.mp3',
            'intro': 'sounds/jazzy-cut-to-commercial-tv-theme-albert-marlowe-production-music-all-rights-reserved.mp3'
        }

        # Load all sounds
        self.loaded_sounds = {}
        for name, filename in self.sounds.items():
            try:
                self.loaded_sounds[name] = pygame.mixer.Sound(filename)
            except Exception as e:
                print(f"Warning: Could not load sound '{filename}': {e}")
                self.loaded_sounds[name] = None

    def play_sound(self, sound_name):
        """Play a specific sound effect"""
        if sound_name in self.loaded_sounds and self.loaded_sounds[sound_name]:
            try:
                self.loaded_sounds[sound_name].play()
            except Exception as e:
                print(f"Error playing sound '{sound_name}': {e}")

    def play_hit_sound(self):
        """Play sound when player hits (draws a card)"""
        self.play_sound('hit')

    def play_shuffle_sound(self):
        """Play sound when deck is shuffled"""
        self.play_sound('shuffle')

    def play_chips_sound(self):
        """Play sound when placing a bet"""
        self.play_sound('chips')

    def play_turn_sound(self):
        """Play sound when revealing dealer's card"""
        self.play_sound('turn')

    def play_intro_sound(self):
        """Play intro sound when game starts"""
        self.play_sound('intro')