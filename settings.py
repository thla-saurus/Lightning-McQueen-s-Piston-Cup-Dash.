class Settings:
    def __init__(self):
        self.SCREEN_WIDTH = 480
        self.SCREEN_HEIGHT = 800
        self.NUM_LANES = 6
        self.LANE_WIDTH = (int(self.SCREEN_WIDTH / self.NUM_LANES))
        
        # Item (Obstacle / Nitro) Properties
        self.ITEM_WIDTH = 40
        self.ITEM_HEIGHT = 40
        self.ITEM_SPEED = 5
        self.SPAWN_INTERVAL = 60  # Frames between each new spawn (FPS)

        # Colors (RGB)
        self.COLOR_NITRO = (0, 200, 255)  # Light Blue
