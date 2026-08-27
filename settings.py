class Settings:
    def __init__(self):
        self.SCREEN_WIDTH = 480
        self.SCREEN_HEIGHT = 800
        self.NUM_LANES = 3
        self.LANE_WIDTH = (int(self.SCREEN_WIDTH / self.NUM_LANES))-71
        # Item (Obstacle / Nitro) Properties
        self.ITEM_WIDTH = 40
        self.ITEM_HEIGHT = 40
        self.ITEM_SPEED = 5
        self.SPAWN_INTERVAL = 60  # Frames between each new spawn (FPS)
