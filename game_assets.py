import pygame

class Assets:
    # contains helpful assets for the game and helper methods to create them

    def __init__(self):
        self.obstacle_images = ["assets/oil1.bmp","assets/oil2.bmp","assets/tire.bmp"]
        for i,img in enumerate(self.obstacle_images):
            self.obstacle_images[i] = self._setup_img(img)
            
        self.power_up_image = self._setup_img("assets/power_up.bmp")


    def _setup_img(self,img):
        image  = pygame.image.load(img)
        image  = pygame.transform.scale(image, (50,50))
        return image