import pygame
import settings
import sprite_sheet_loader as sp_load

pygame.init()

class Hearts(pygame.sprite.Sprite):
    def __init__(self, id):
        super().__init__()
        self.hearts_image= pygame.image.load("2DArt/Hearts.png").convert_alpha()
        self.hearts_sheet = sp_load.Sprite_Sheet_loader(self.hearts_image)
        self.broken_heart_image = self.hearts_sheet.get_image(0,32,32,1,settings.BLACK)
        self.healthy_heart_image = self.hearts_sheet.get_image(1,32,32,1,settings.BLACK)
        self.image = self.healthy_heart_image
        self.rect = self.image.get_rect()
        self.rect.move_ip(settings.HEARTS_X[id],settings.HEARTS_Y)

    def update_heart(self):
        self.image = self.broken_heart_image
    
    def get_rect(self):
        return self.rect

    def get_image(self):
        return self.image