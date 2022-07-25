import pygame
import sprite_sheet_loader as sp_load
import settings

pygame.init()

#player class
class Player(pygame.sprite.Sprite):
    def __init__(self,surface):
        super().__init__()
        self.lives = 3
        self.image = pygame.image.load("2DArt/Player.png").convert_alpha()
        self.player_sheet = sp_load.Sprite_Sheet_loader(self.image)

        self.idle_image_1 = self.player_sheet.get_image(0,32,32,4,settings.BLACK)
        self.idle_image_2 = self.player_sheet.get_image(1,32,32,4,settings.BLACK)
        self.idle_full_image_1 = self.player_sheet.get_image(2,32,32,4,settings.BLACK)
        self.idle_full_image_2 = self.player_sheet.get_image(3,32,32,4,settings.BLACK)
        self.catch_empty_image = self.player_sheet.get_image(4,32,32,4,settings.BLACK)
        self.catch_full_image = self.player_sheet.get_image(5,32,32,4,settings.BLACK)

        self.rect = self.idle_image_1.get_rect()
        self.rect.move_ip(settings.PLAYER_START_X, settings.PLAYER_START_Y)


        self.player_sprite_list = [self.idle_image_1, self.idle_image_2, 
                                   self.idle_full_image_1, self.idle_full_image_2,
                                   self.catch_empty_image, self.catch_full_image]

        self.bucket_full = False
        self.radius = settings.RADIUS


    def get_sprite_list(self):
        return self.player_sprite_list

    def move(self,x,y):
        self.rect.move_ip(x,y)
    
    def get_rect(self):
        return self.rect

    def get_position(self):
        return self.rect.center

    def set_bucket_full(self):
        self.bucket_full = True
    
    def set_bucket_empty(self):
        self.bucket_full = False

    def get_bucket_state(self):
        return self.bucket_full