import pygame
from random import choice, randint
import os


class LeaderboardManager:

  def __init__(self, filename="scores.txt"):
    self.filename = filename
    self.high_score = self.load_high_score()

  def load_high_score(self):
    # Read the high score from the text file if it exists
    if os.path.exists(self.filename):
      try:
        with open(self.filename, "r") as score:
          content = score.read().strip()
          if content.isdigit(): # score is + int always 
            return int(content)
          else:
            return 0
      except Exception:
        return 0
    return 0

  def check_and_update(self, current_score):
    # Check if the current score beats the high score
    if current_score > self.high_score:
      self.high_score = current_score
      self.save_high_score()
      return True  # Returns True if a new high score was achieved!
    return False

  def save_high_score(self):
    # Save the new high score into the text file
    try:
      with open(self.filename, "w") as score:
        score.write(str(self.high_score))
    except Exception as e:
      print(f"Error saving high score: {e}")

  def get_high_score(self):
    # Returns the current high score
    return self.high_score
















pygame.init()


width = 1200
height = 900
screen = pygame.display.set_mode((width, height))

time=0
watch=pygame.font.SysFont("Arial", 30)


img = pygame.image.load("lightning.png").convert()
img.set_colorkey((255, 255, 255))
img = pygame.transform.scale(img, (80, 80))
player = img.get_rect(center=(600, 750))



nitro_img = pygame.image.load("Nitro.png").convert()
nitro_img.set_colorkey((255, 255, 255))
nitro_img = pygame.transform.scale(nitro_img, (50, 30))


obstacle_img = pygame.image.load("obstacle3.png").convert()
obstacle_img.set_colorkey((255, 255, 255))
obstacle_img = pygame.transform.scale(obstacle_img, (50, 30))

life_img=pygame.image.load("life.png").convert()
life_img.set_colorkey((255, 255, 255))
life_img = pygame.transform.scale(life_img, (30, 30))

lives=[]
j=10
for life in range(3):
    life=life_img.get_rect(topright=(width-j,10))
    lives.append(life)
    j+=20

lanes = [200, 600, 1000]



nitro_lane = choice(lanes)
nitro = nitro_img.get_rect(center=(nitro_lane, 0))



obstacle_lane = choice(lanes)
obstacle = obstacle_img.get_rect(center=(obstacle_lane, -200))



player_speed = 500
nitro_speed = 150
obstacle_speed = 180

nitro_collected =0
obstacle_hit=0


clock = pygame.time.Clock()
game_over = False
run = True
while run:
    
    if not game_over:
        timer = pygame.time.get_ticks()/1000
        delta = clock.tick(60)/1000
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


        key = pygame.key.get_pressed()
        
        if key[pygame.K_a]:
            player.x -= player_speed * delta

        if key[pygame.K_d]:
            player.x += player_speed * delta

        if key[pygame.K_w]:
            player.y -= player_speed * delta

        if key[pygame.K_s]:
            player.y += player_speed * delta


    
        nitro.y+=nitro_speed*delta
        obstacle.y+=obstacle_speed*delta


        if nitro.top > height:
            nitro_lane = choice(lanes)
            nitro = nitro_img.get_rect(
                center=(nitro_lane, 0)
            )
        if player.colliderect(nitro):
            nitro_lane = choice(lanes)
            nitro = nitro_img.get_rect(
                center=(nitro_lane, 0)
            )    
            nitro_collected += 1


        if obstacle.top > height:
            obstacle_lane = choice(lanes)
            obstacle = obstacle_img.get_rect(center=(obstacle_lane, 0))
        
        if player.colliderect(obstacle):
            obstacle_lane=choice(lanes)
            obstacle=obstacle_img.get_rect(center=(obstacle_lane,0))
            lives.remove(lives[-1])
            obstacle_hit+=1

        if timer-time>=5:
            nitro_speed+=30
            obstacle_speed+=30
            player_speed+=30
            time=timer    
            
        score=int(timer)*5+nitro_collected*5-obstacle_hit*20
        screen.fill((0, 0, 0))
        screen.blit(img, player)
        screen.blit(nitro_img, nitro)
        screen.blit(obstacle_img, obstacle)
        for life in lives:
            screen.blit(life_img, life)
        screen.blit(watch.render(f"Time: {int(timer)}", True, (255, 255, 255)), (10, 10))
        screen.blit(watch.render(f"Score: {score}", True, (255, 255, 255)), (10, 50))
        pygame.display.update()
        if len(lives)==0:
            if len(lives) == 0:
                game_over = True
                screen.fill((0, 0, 0))

            if game_over:
                font = pygame.font.SysFont("Arial", 100)
                text = font.render("GAME OVER", True, (255, 0, 0))
                text_rect = text.get_rect(center=(width // 2, height // 2))
                screen.blit(text, text_rect)

            else:
                screen.blit(img, player)
                screen.blit(nitro_img, nitro)
                screen.blit(obstacle_img, obstacle)

                for life in lives:
                    screen.blit(life_img, life)

            pygame.display.update()


leaderboard = LeaderboardManager("highscore.txt")
leaderboard.check_and_update(score)
leaderboard.save_high_score()
pygame.quit()        
        
        

  