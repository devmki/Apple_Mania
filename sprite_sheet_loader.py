import pygame

class Sprite_Sheet_loader():
    def __init__(self,image):
        self.sheet = image

    def get_image(self, frame, width, height, color):
        image = pygame.Surface((width,height)).convert_alpha()
        image.blit(self.sheet,(0,0),(frame * width,0,width,height))
        image.set_colorkey(color)
        return image
