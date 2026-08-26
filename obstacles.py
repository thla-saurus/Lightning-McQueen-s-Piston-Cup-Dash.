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


class Obstacle:

  def __init__(self, lane_index, item_type ,game):
    # Initialize obstacle or nitro power-up item.
    # item_type: 'obstacle' or 'nitro'
    self.settings = game.settings
    self.lane_index = lane_index
    self.item_type = item_type
    self.images = ["assets/oil1.bmp","assets/oil2.bmp","assets/tire.bmp"]
    for i,img in enumerate(self.images):
      self.images[i] = self._setup_img(img)
    self.rect = self
    self.x = (lane_index * self.settings.LANE_WIDTH) + (self.settings.LANE_WIDTH // 2) - (ITEM_WIDTH // 2)
    self.y = -ITEM_HEIGHT  # Start spawning from above the screen boundary

    self.width = ITEM_WIDTH
    self.height = ITEM_HEIGHT
    self.speed = ITEM_SPEED
  def _setup_img(self,img):
    image  = pygame.image.load(img)
    #image  = pygame.transform.scale(image, (60,25))
    return image

  def update(self):
    # Update the vertical position of the item to move it downwards
    self.y += self.speed

  def draw_object(self):
    # Render the game object on the screen
    if self.item_type == "obstacle":
      img  =  choice([self.images])
      img_rect = img.get_rect()
      self.screen.blit(img,img_rect)

    else:
      # Draw nitro power-up using global color and dimensions
      pygame.draw.rect(
          screen, COLOR_NITRO, (self.x, self.y, self.width, self.height)
      )

  def check_collision(self, player_rect):
    # Check if this item collides with the player's rectangle
    # Creates a Pygame Rect for the current item
    item_rect = pygame.Rect(self.x, self.y, self.width, self.height)

    # colliderect returns True if the two rectangles overlap (collide), False otherwise
    return item_rect.colliderect(player_rect)
  
