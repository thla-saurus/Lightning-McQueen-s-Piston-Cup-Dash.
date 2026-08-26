import pygame
from pygame.sprite import Sprite 
from random import choice

# Item (Obstacle / Nitro) Properties
ITEM_WIDTH = 40
ITEM_HEIGHT = 40
ITEM_SPEED = 5
SPAWN_INTERVAL = 60  # Frames between each new spawn (FPS)

# Colors (RGB)
COLOR_NITRO = (0, 200, 255)  # Light Blue


class GameObject(Sprite):

  def __init__(self, lane_index, item_type ,game):
    # Initialize obstacle or nitro power-up item.
    # item_type: 'obstacle' or 'nitro'
    super().__init__()
    self.window = game.window
    self.settings = game.settings
    self.lane_index = lane_index
    self.item_type = item_type

    self.image = choice(game.assets.images)
    self.x = (lane_index * self.settings.LANE_WIDTH) + (self.settings.LANE_WIDTH // 2) - (ITEM_WIDTH // 2)
    self.y = -ITEM_HEIGHT  # Start spawning from above the screen boundary

    self.width = ITEM_WIDTH
    self.height = ITEM_HEIGHT
    self.speed = ITEM_SPEED

  def update(self):
    # Update the vertical position of the item to move it downwards
    self.y += self.speed

  def draw_object(self):
    # Render the game object on the screen
    if self.item_type == "obstacle":
      
      img_rect = self.image.get_rect()
      img_rect.x = self.x
      img_rect.y = self.y
      self.window.blit(self.image,img_rect)

    else:
      # Draw nitro power-up using global color and dimensions
      pygame.draw.rect(
          self.window, COLOR_NITRO, (self.x, self.y, self.width, self.height)
      )

  def check_collision(self, player_rect):
    # Check if this item collides with the player's rectangle
    # Creates a Pygame Rect for the current item
    item_rect = pygame.Rect(self.x, self.y, self.width, self.height)

    # colliderect returns True if the two rectangles overlap (collide), False otherwise
    return item_rect.colliderect(player_rect)
  
