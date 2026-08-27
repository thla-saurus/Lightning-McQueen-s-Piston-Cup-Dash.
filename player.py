import pygame
from pygame.sprite import Sprite 

class Car:

  def __init__(self,game):
    super().__init__()
    self.window = game.window
    self.settings = game.settings
    self.image = game.assets.car_image
    self.img_rect = self.image.get_rect()
    self.img_rect.centerx = self.window.get_rect().centerx
    self.x = self.img_rect.x
    self.img_rect.bottom = self.window.get_rect().bottom-50

  def check_new_position(self,lane_index):
    # Update the vertical position of the item to move it downwards
    shift_right = 53
    if lane_index == 0:
       self.x = shift_right
    else:
       self.x = ((lane_index * self.settings.LANE_WIDTH) + (self.settings.LANE_WIDTH // 2) - (55 // 2))+(shift_right*lane_index) +shift_right

  def draw_player(self):
    # Render the game object on the screen
      self.img_rect.x = self.x
      self.window.blit(self.image,self.img_rect)

  
