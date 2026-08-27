import pygame
from settings import Settings
from game_objects import GameObject
from game_assets import Assets
from player import Car
import random
from multiprocessing.shared_memory import SharedMemory
import numpy as np
from system import Gamesystem
from boost import Boost
from Difficulty import DifficultyManager
from Score import LeaderboardManager

# include your class file
# from file name import class name
MEMORY_SIZE = 4

class Game:
    # Initialize Pygame
    def __init__(self):
        pygame.init()
        # initiate settings object and some attributes from it
        self.settings = Settings()
        WIDTH, HEIGHT = self.settings.SCREEN_WIDTH, self.settings.SCREEN_HEIGHT

        # initiate assets object
        self.assets = Assets()

        self.stats = Gamesystem(self)
        self.boost = Boost(duration=3, boost_multiplier=2)



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

        # [DIFFICULTY + LEADERBOARD]
        self.difficulty_manager = DifficultyManager()
        self.leaderboard_manager = LeaderboardManager() 
        #font
        pygame.font.init()
        self.font = pygame.font.SysFont("Arial", 26, bold=True)

        obstacle_time = self.difficulty_manager.get_obstacle_interval()
        nitro_time = self.difficulty_manager.get_nitro_interval()


        
        # [HAND + YOLO]
        # Initialize the camera/detection system here.

        self.player = Car(self)

        self.obstacles = pygame.sprite.Group()
        self.spawn_obstacle_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.spawn_obstacle_event,obstacle_time)


        self.nitros = pygame.sprite.Group()
        self.spawn_power_up_event = pygame.USEREVENT + 2
        pygame.time.set_timer(self.spawn_power_up_event,nitro_time)

        # [COLLISION]
        # Collision is handled dynamically in update() using GameObject.check_collision()

        # [SCORE + LIVES]
        # Initialize the Score/Lives/Nitro-counter system here.

        # [BOOST]
        # Initialize the Peace Sign/Boost system here.

        # [MOTION EFFECT]
        # Initialize the motion trail/blur system here.

        # [GAME OVER + RESTART]
        # Initialize the Game Over/Restart system here.

        # setup shared memory with hand detection process
        self.shm = SharedMemory(name = "lane_number_shm")
        self.buffer = np.ndarray((MEMORY_SIZE),dtype=np.uint8,buffer=self.shm.buf)

    def handle_events(self):
        # first event: quitting game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == self.spawn_obstacle_event:
                self.obstacles.add(GameObject(random.randint(0,self.settings.NUM_LANES-1),"obstacle",self))
            if event.type == self.spawn_power_up_event:
                self.nitros.add(GameObject(random.randint(0,self.settings.NUM_LANES-1),"power_up",self))

    # continously update game (car speed, number of lanes, which lane it's in, obstacles, nitro, lifes)
    def update(self, dt):

        # =========================================================
        # HAND / YOLO
        # =========================================================
        # [HAND DETECTION TEAM]
        # Get the latest gesture and hand-position result.
        # Pass the relevant result to the McQueen/Lane system.
        
        self.player.check_new_position(lane_index=int(self.buffer[0]))

        for ob in self.obstacles:
            if ob.check_reach_edge():
                self.obstacles.remove(ob)
            else:
                ob.update()

        for ni in self.nitros:
            if ni.check_reach_edge():
                self.nitros.remove(ni)
            else:
                ni.update()

        if pygame.sprite.spritecollide(self.player,self.obstacles, True):
            print(" i am hit obstacle")
            if not self.boost.is_active():
                self.stats.lose_life()
                self.stats.score_up(-10)
                if self.stats.score < 0:
                    self.stats.score = 0
            else:
                print("boost active, no life lost")
                self.stats.score_up(30)       
            # implement obstacle car collision logic

        if pygame.sprite.spritecollide(self.player,self.nitros, True):
            print(" i got nitro")
            self.stats.nitro_boost_up()
            self.stats.score_up(20)
            # implement nitro car collision logic

        # =========================================================
        # SCORE + LIVES + NITRO COUNTER
        # =========================================================
        # [SCORE/LIVES TEAM]
        # Update score/lives/Nitro counter based on game events.

        self.stats.score_up(int(dt * 10))  #increase score over time
        final_score = self.stats.score
        self.leaderboard_manager.check_and_update(final_score)

        # =========================================================
        # KACHOW BOOST
        # =========================================================
        # [BOOST TEAM]
        # Process Peace Sign detection and Boost behavior.
        peace_sign_detected = bool(self.buffer[1])
        if peace_sign_detected and not self.boost.is_active():
            if self.stats.use_nitro():  # بتفحص إذا فيه نيترو وتخصم 1 فوراً وتجيب True
                self.boost.activate()

        self.boost.update()  

        # =========================================================
        # MOTION EFFECT
        # =========================================================
        # [MOTION EFFECT TEAM]
        # Update the visual trail/blur while Boost is active.

        # =========================================================
        # DIFFICULTY
        # =========================================================
        self.difficulty_manager.update_difficulty()
        current_speed = self.difficulty_manager.get_current_speed()

        for ob in self.obstacles:
            ob.speed = current_speed
        for ni in self.nitros:
            ni.speed = current_speed
        

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

            self.player.draw_player()

            for ob in self.obstacles.sprites():
                ob.draw_object()

            for ni in self.nitros.sprites():
                ni.draw_object()

            # [BOOST / MOTION EFFECT TEAM]
            # Draw boost and motion effects.

            # [SCORE + LIVES TEAM]
            # Draw score, lives and Nitro counter.
            self.stats.draw()

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
