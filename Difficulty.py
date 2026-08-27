from settings import Settings
settings = Settings()

class DifficultyManager:

  def __init__(self):
    self.score = 0
    self.game_speed = settings.ITEM_SPEED          
    self.spawn_interval = settings.SPAWN_INTERVAL  
    self.difficulty_timer = 0  # Counter to track elapsed frames

  def update_difficulty(self):
    # Increment the frame counter every frame (assuming 60 FPS)
    self.difficulty_timer += 1

    # Increase score by 1 every 1 second (60 frames)
    if self.difficulty_timer % settings.SPAWN_INTERVAL == 0:
      self.score += 1

    # Increase difficulty every 5 seconds
    if self.difficulty_timer >= (settings.SPAWN_INTERVAL * 5):
      self.game_speed += 1  # Increase obstacle and nitro speed gradually

      # Limit spawn interval so items don't spawn impossibly fast
      if self.spawn_interval > 25:
        self.spawn_interval -= 5

      self.difficulty_timer = 0  # Reset the difficulty timer for the next interval

  def get_current_speed(self):
    # Returns the dynamic speed to be passed into newly spawned GameObjects
    return self.game_speed

  def get_spawn_interval(self):
    # Returns the updated spawn interval for the spawner loop
    return self.spawn_interval

  def get_score(self):
    #Returns the score from still being alive 
    return self.score
