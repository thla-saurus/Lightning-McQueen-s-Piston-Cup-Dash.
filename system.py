import pygame

class Gamesystem:
    def __init__(self, game):
        self.game = game
        self.window = game.window
        self.settings = game.settings

        self.score = 0
        self.lives = 3
        self.nitro_boost = 0

        self.font = pygame.font.Font(None, 40)
        self.heart_red = pygame.transform.scale(pygame.image.load("heart.png"), (30, 30))
        self.heart_black = pygame.transform.scale(pygame.image.load("black heart.png"), (30, 30))
        self.nitro_image = pygame.transform.scale(pygame.image.load("nitro.png"), (30, 30))

    def score_up(self, amount):
        self.score += amount

    def lose_life(self):
        if self.lives > 0:
            self.lives -= 1

    def nitro_boost_up(self):
        self.nitro_boost += 1

    def use_nitro(self):
        if self.nitro_boost > 0:
            self.nitro_boost -= 1
            return True
        return False

    def draw(self):
        score_text = self.font.render(
            f"Score: {self.score}",
            True,
            (255, 255, 255)
        )
        self.window.blit(score_text, (self.settings.SCREEN_WIDTH - 150, 50))

        for i in range(3):
            x = 20 + i * 40
            y = 50
            if i < self.lives:
                self.window.blit(self.heart_red, (x, y))
            else:
                self.window.blit(self.heart_black, (x, y))

        for i in range(self.nitro_boost):
            x = 20 + i * 50
            y = 110
            self.window.blit(self.nitro_image, (x, y))