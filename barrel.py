import pygame
import sprite_sheet_loader as sp_load
import settings

pygame.init()

class Barrel(pygame.sprite.Sprite):
    def __init__(self,surface):
        self.max_capacity = settings.BARREL_CAPACITY
        self.current_amount = 0
        self.apples_in_barrel = False
        #sprite sheet for barrel
        self.barrel_image_sheet = pygame.image.load("2DArt/Barrel.png").convert_alpha()
        self.images = sp_load.Sprite_Sheet_loader(self.barrel_image_sheet)
        self.rect = None
        self.barrel_empty = self.images.get_image(0,32,32,3,settings.BLACK)
        self.barrel_filled = self.images.get_image(1,32,32,3,settings.BLACK)
        self.rect_empty = self.barrel_empty.get_rect()
        self.rect_filled= self.barrel_filled.get_rect()
        self.text = settings.FONT.render('/'.join([str(self.current_amount),str(self.max_capacity)]),True,settings.WHITE)
        self.text_rect = self.text.get_rect()
        self.text_rect.topleft = (settings.BARREL_X + 40, settings.BARREL_Y + 40)
        self.radius = settings.RADIUS/2
        self.sprite_list = [self.barrel_empty, self.barrel_filled]

        self.move()

    def get_status(self):
        return self.apples_in_barrel

    def get_capacity(self):
        return self.max_capacity

    def move(self):
        self.rect_empty.move_ip(settings.BARREL_X, settings.BARREL_Y)  
        self.rect_filled.move_ip(settings.BARREL_X, settings.BARREL_Y)    

    def get_current_amount(self):
        return self.current_amount

    def increment_amount(self,modifier):
            self.current_amount += modifier
            self.text = settings.FONT.render('/'.join([str(self.current_amount),str(self.max_capacity)]),True,settings.WHITE)

    def set_amount(self,amount):
        self.current_amount = amount
        self.text = settings.FONT.render('/'.join([str(self.current_amount),str(self.max_capacity)]),True,settings.WHITE)
    
    def get_sprite_list(self):
        return self.sprite_list

    def get_rect(self,index):
        if(index == 0):
            self.rect = self.rect_empty
        else:
            self.rect = self.rect_filled
        return self.rect

    def get_text(self):
        return self.text

    def get_text_rect(self):
        return self.text_rect