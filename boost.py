import pygame

class Boost:

    def __init__(self, duration=3, boost_multiplier=2):
        self.active = False
        self.duration = duration
        self.boost_multiplier = boost_multiplier
        self.start_time = 0

    def activate(self):
        self.active = True
        self.start_time = pygame.time.get_ticks()

    def update(self):
        if self.active:
            elapsed = (pygame.time.get_ticks() - self.start_time) / 1000

            if elapsed >= self.duration:
                self.active = False

    def is_active(self):
        return self.active

    def get_speed(self, normal_speed):
        if self.active:
            return normal_speed * self.boost_multiplier

        return normal_speed