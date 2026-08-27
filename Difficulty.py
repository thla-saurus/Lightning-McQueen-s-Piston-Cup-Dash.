from settings import Settings
settings = Settings()

class DifficultyManager:

    def __init__(self):
        self.game_speed = settings.ITEM_SPEED         
        self.obstacle_interval = 1000  # Initial interval for obstacles (in milliseconds)
        self.nitro_interval = 3000     # Initial interval for nitro (3 times the obstacles)
        self.difficulty_timer = 0      # Counter to track elapsed frames

    def update_difficulty(self):
        # Increment the frame counter every frame (assuming 60 FPS)
        self.difficulty_timer += 1

        # Increase difficulty every 5 seconds (approx. 300 frames at 60 FPS)
        if self.difficulty_timer >= (60 * 5):
            self.game_speed += 1  # Gradually increase obstacle and nitro speed

            # Decrease obstacle spawn interval to spawn faster (with a safe minimum limit like 400 ms)
            if self.obstacle_interval > 400:
                self.obstacle_interval -= 100
                
            # Always keep the nitro interval 3 times the obstacle interval as requested
            self.nitro_interval = self.obstacle_interval * 3

            self.difficulty_timer = 0  # Reset the difficulty timer for the next interval

    def get_current_speed(self):
        # Returns the dynamic speed to be passed into newly spawned GameObjects
        return self.game_speed

    def get_obstacle_interval(self):
        # Returns the updated obstacle spawn interval for the spawner loop
        return self.obstacle_interval

    def get_nitro_interval(self):
        # Returns the updated nitro spawn interval for the spawner loop
        return self.nitro_interval
