import pygame
import sprite_sheet_loader as sp_load
import settings
from hearts import Hearts

pygame.init()

#player class
class Player(pygame.sprite.Sprite):
    def __init__(self,surface):
        super().__init__()
        self.lives_start = 3
        self.lives = self.lives_start
        self.image = pygame.image.load("2DArt/Player.png").convert_alpha()
        self.player_sheet = sp_load.Sprite_Sheet_loader(self.image)
        self.idle_image_1 = self.player_sheet.get_image(0,32,32,4,settings.BLACK)
        self.idle_image_2 = self.player_sheet.get_image(1,32,32,4,settings.BLACK)
        self.idle_full_image_1 = self.player_sheet.get_image(2,32,32,4,settings.BLACK)
        self.idle_full_image_2 = self.player_sheet.get_image(3,32,32,4,settings.BLACK)
        self.catch_empty_image = self.player_sheet.get_image(6,32,32,4,settings.BLACK)
        self.catch_full_image = self.player_sheet.get_image(7,32,32,4,settings.BLACK)

        self.rect = self.idle_image_1.get_rect()
        self.rect.move_ip(settings.PLAYER_START_X, settings.PLAYER_START_Y)


        self.player_sprite_list = [self.idle_image_1, self.idle_image_2, 
                                   self.idle_full_image_1, self.idle_full_image_2,
                                   self.catch_empty_image, self.catch_full_image]

        self.bucket_full = False
        self.radius = settings.RADIUS

        self.hearts_list = []
        for i in range(self.lives):
            self.hearts_list.append(Hearts(i))

    def get_sprite_list(self):
        return self.player_sprite_list

    def move(self,x,y):
        self.rect.move_ip(x,y)
    
    def get_rect(self):
        return self.rect

    def get_position(self):
        return self.rect.center

    def set_bucket_full(self, apple_type):
        self.bucket_full = True
        if(apple_type == "golden"):
            self.idle_full_image_1 = self.player_sheet.get_image(4,32,32,4,settings.BLACK)
            self.player_sprite_list[2] = self.idle_full_image_1
            self.idle_full_image_2 = self.player_sheet.get_image(5,32,32,4,settings.BLACK)
            self.player_sprite_list[3] = self.idle_full_image_2
            self.catch_full_image = self.player_sheet.get_image(8,32,32,4,settings.BLACK)
            self.player_sprite_list[5] = self.catch_full_image
        else:
            self.idle_full_image_1 = self.player_sheet.get_image(2,32,32,4,settings.BLACK)
            self.player_sprite_list[2] = self.idle_full_image_1
            self.idle_full_image_2 = self.player_sheet.get_image(3,32,32,4,settings.BLACK)
            self.player_sprite_list[3] = self.idle_full_image_2
            self.catch_full_image = self.player_sheet.get_image(7,32,32,4,settings.BLACK)
            self.player_sprite_list[5] = self.catch_full_image
    
    def set_bucket_empty(self):
        self.bucket_full = False

    def get_bucket_state(self):
        return self.bucket_full

    def set_lives(self,modifier):
        self.lives += modifier
        self.hearts_list[self.lives].update_heart(1)

    def reset_lives(self):
        for i in range(len(self.hearts_list)):
            self.hearts_list[i].update_heart(2)
        self.lives = 3
        
    def get_lives(self):
        return self.lives

    def draw_hearts(self,surface):
        for i in range(self.lives_start):
            surface.blit(self.hearts_list[i].get_image(),self.hearts_list[i].get_rect())