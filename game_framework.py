import pygame
from settings import Settings
from game_objects import GameObject
from game_assets import Assets
import random

# include your class file
# from file name import class name


class Game:
    # Initialize Pygame
    def __init__(self):
        pygame.init()
        # initiate settings object and some attributes from it
        self.settings = Settings()
        WIDTH, HEIGHT = self.settings.SCREEN_WIDTH, self.settings.SCREEN_HEIGHT

        # initiate assets object
        self.assets = Assets()



        # Set up the game window
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))  # dimensions
        self.original = pygame.image.load(
            "pistoncup track.png"
        )   # loading the background image
        self.background = pygame.transform.scale(self.original, (WIDTH, HEIGHT))

        icon = pygame.image.load("MIAicon.png")  # loading the window icon
        pygame.display.set_icon(icon)

        pygame.display.set_caption("McQueen dodging game")  # window name

        # setting game speed clock
        self.clock = pygame.time.Clock()
        self.running = True

        # game state
        self.state = "PLAYING"

        # =========================================================
        # TEAM SYSTEMS
        # =========================================================

        # [HAND + YOLO]
        # Initialize the camera/detection system here.

        # [LANES + McQUEEN]
        # Initialize the lane and McQueen systems here.

        self.obstacles = pygame.sprite.Group()
        self.spawn_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.spawn_event,500)


        # [NITRO]
        # Initialize the Nitro system here.

        # [COLLISION]
        # Initialize the collision system here.

        # [SCORE + LIVES]
        # Initialize the Score/Lives/Nitro-counter system here.

        # [BOOST]
        # Initialize the Peace Sign/Boost system here.

        # [MOTION EFFECT]
        # Initialize the motion trail/blur system here.

        # [GAME OVER + RESTART]
        # Initialize the Game Over/Restart system here.

        # [DIFFICULTY + LEADERBOARD]
        # Initialize the difficulty and leaderboard systems here.


    def handle_events(self):
        # first event: quitting game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == self.spawn_event:
                self.obstacles.add(GameObject(random.randint(0,5),"obstacle",self))

    # continously update game (car speed, number of lanes, which lane it's in, obstacles, nitro, lifes)
    def update(self, dt):

        # =========================================================
        # HAND / YOLO
        # =========================================================
        # [HAND DETECTION TEAM]
        # Get the latest gesture and hand-position result.
        # Pass the relevant result to the McQueen/Lane system.

        # =========================================================
        # McQUEEN + LANES
        # =========================================================
        # [McQUEEN/LANES TEAM]
        # Use the hand-position result to determine McQueen's lane.
        # Update McQueen's position.

        for ob in self.obstacles:
            ob.update()

        # =========================================================
        # NITRO
        # =========================================================
        # [NITRO TEAM]
        # Update Nitro objects and their movement.

        # =========================================================
        # COLLISION
        # =========================================================
        # [COLLISION TEAM]
        # Check interactions between McQueen and relevant objects.
        # Provide the collision result to the Score/Lives system.

        # =========================================================
        # SCORE + LIVES + NITRO COUNTER
        # =========================================================
        # [SCORE/LIVES TEAM]
        # Update score/lives/Nitro counter based on game events.

        # =========================================================
        # KACHOW BOOST
        # =========================================================
        # [BOOST TEAM]
        # Process Peace Sign detection and Boost behavior.

        # =========================================================
        # MOTION EFFECT
        # =========================================================
        # [MOTION EFFECT TEAM]
        # Update the visual trail/blur while Boost is active.

        # =========================================================
        # DIFFICULTY
        # =========================================================
        # [DIFFICULTY TEAM]
        # Apply customizable/progressive difficulty.

        # =========================================================
        # GAME STATE / GAME OVER
        # =========================================================
        # Use the result from the Score/Lives system to trigger
        # the Game Over state. change the game state if lives become zero
        #     self.state = "GAME_OVER"
        # Do NOT reset the game here.
        pass

    def draw(self):
        # =========================================================
        # DRAW GAME WORLD
        # =========================================================
        self.window.blit(self.background, (0, 0))

        if self.state == "PLAYING":

            # =====================================================
            # NORMAL GAME DISPLAY
            # =====================================================

            # [LANES + McQUEEN TEAM]
            # Draw lanes and McQueen.

            for ob in self.obstacles.sprites():
                ob.draw_object()

            # [NITRO TEAM]
            # Draw active Nitro.

            # [BOOST / MOTION EFFECT TEAM]
            # Draw boost and motion effects.

            # [SCORE + LIVES TEAM]
            # Draw score, lives and Nitro counter.

            # [DIFFICULTY / LEADERBOARD TEAM]
            # Draw leaderboard/high score if required.

            pass

        elif self.state == "GAME_OVER":

            # =====================================================
            # GAME OVER DISPLAY
            # =====================================================

            # [GAME OVER + RESTART TEAM]
            # Draw the Game Over screen.
            # Display final score and restart instructions.
            # The Game Over system owns the actual visual design.
            pass
        pygame.display.update()

    # Game loop
    def run(self):

        while self.running:

            # Time since previous frame
            dt = self.clock.tick(60) / 1000
            # Handle Pygame events
            self.handle_events()

            # Run the appropriate game state
            if self.state == "PLAYING":

                self.update(dt)

            elif self.state == "GAME_OVER":

                # [GAME OVER + RESTART TEAM]
                # Run the Game Over screen/logic.
                #
                # This system should:
                # - wait for the restart input
                # - reset the necessary game systems
                # - indicate when the game should return to PLAYING
                #
                # Example integration:
                # restart = self.game_over_system.update(...)
                #
                # if restart:
                #     self.state = "PLAYING"

                pass

            # Draw current state
            self.draw()

    pygame.quit()
