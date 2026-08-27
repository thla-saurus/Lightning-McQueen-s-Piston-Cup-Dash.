import math
import pygame

NO_SIGNAL = 255 # No hand detected
COLOR_INVULNERABLE_GLOW = (0, 230, 230) 

# This is were we make our car look like it's moving smoothly between lanes,
# not teleporting
SPRING_STIFFNESS = 150 # How hard the car is pulled towards the target lane position. Higher values = faster movement.
SPRING_DAMPING = 2 * math.sqrt(SPRING_STIFFNESS) * 0.7 # How much the car's movement is dampened. Higher values = less overshoot and oscillation (will stop dead like a robot). 
                                                       # (Makes the car wobble into place so that it looks natural)
DT = 1 / 60 # Assumes the car runs at 60 FPS, so the physics don't break if the computer lags. (Keeps McQueen's speed consistent on every laptop)
MAX_TILT_DEGREES = 30 # Maximum tilt angle for the car (drifting)


# The window we draw on
class Car:
    def __init__(self, game):
        self.window = game.window
        self.settings = game.settings
        self.base_image = game.assets.car_image

        self.width = self.base_image.get_width()
        self.height = self.base_image.get_height()


        start_lane = self.settings.NUM_LANES // 2
        self.lane_index = start_lane
        self.x = self._lane_target_x(start_lane)
        self.y = self.window.get_rect().bottom - self.height - 50
        self.rect = self.get_rect()
        self.velocity_x = 0.0
        
    # Alignment logic (from Obstacles)
    def _lane_target_x(self, lane_index):
        shift_right = 53
        if lane_index == 0:
            return shift_right
        return ((lane_index * self.settings.LANE_WIDTH) + (self.settings.LANE_WIDTH // 2)
                 - (self.width // 2)) + (shift_right * lane_index) + shift_right


    # Movement logic
    def check_new_position(self, lane_index, no_signal_value=NO_SIGNAL):
        if lane_index == no_signal_value:
            return # No hand detected, don't change position (lane_index is 255)
        self.lane_index = lane_index
        target_x = self._lane_target_x(lane_index) # Get the real lane index (0, 1, 2)
        force = (target_x - self.x) * SPRING_STIFFNESS # Calc distance to target lane and apply spring stiffness to get the force
        self.velocity_x += (force - self.velocity_x * SPRING_DAMPING) * DT # update the velocity
        self.x += self.velocity_x * DT # Move X coorrdinate

    # COLLISION HITBOX FIX:
    # We generate a fresh, invisible box here instead of updating a saved self.rect.
    # Y? The game loop order is: 1) Math/Move -> 2) Crash Check -> 3) Draw.
    # If we wait to update the box in the Draw step, the Crash Check uses last frame's 
    # old position (a lagging ghost box). 
    # This function creates a perfect, up-to-the-millisecond hitbox right when the 
    # crash check asks for it, so we don't die to obstacles we already dodged.
    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    # Called by game_framework.py when the player dies or the game is reset. Resets the car to the middle lane and stops it from moving.
    def reset(self):
        start_lane = self.settings.NUM_LANES // 2
        self.lane_index = start_lane
        self.x = self._lane_target_x(start_lane)
        self.velocity_x = 0.0

    # Visuals
    def draw_player(self, is_invulnerable: bool = False): # When the peace sign logic is finished and triggers the boost, make sure to call draw_player(is_invulnerable=True) so the neon shield thingy turns on
        rect = self.get_rect() # Grab the flat hitbox so that we know where exactly the car is
        if is_invulnerable: # Sheild vis
            glow_rect = rect.inflate(10, 10) # Create a temp box that's 10 pixels bigger than the car
            pygame.draw.rect(self.window, COLOR_INVULNERABLE_GLOW, glow_rect, width=3, border_radius=6) # Trace a neon blue, rounded border around that bigger box
        tilt = max(-MAX_TILT_DEGREES, min(MAX_TILT_DEGREES, -self.velocity_x * 0.05)) # Tilt vis: Take the car's sliding speed and calc tilt angle... The max/min ensure the car never tilts past MAX_TILT_DEGREES
        rotated = pygame.transform.rotate(self.base_image, tilt) # Create a new, tilted copy of the McQueen pic
        # Pin the center of this new tilted pic dir to the center of our 
        # flat crash box so the drawing doesn't float away from the actual physics
        rotated_rect = rotated.get_rect(center=rect.center)
        # Stamp the tilted pic onto the screen
        self.window.blit(rotated, rotated_rect)