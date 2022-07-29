import random
import pygame
import sprite_sheet_loader as sp_load
import settings

pygame.init()

#class apple
class Apple(pygame.sprite.Sprite):
    def __init__(self, surface, id):
        super().__init__()
        self.apple_type = "standard"
        #random number between 0 and 100
        self.random_int = random.randint(0,settings.MAX_Y)
        if(self.random_int < 10):
            self.apple_type = "golden"
        
        #apple image
        self.image = None
        #sprite sheet for smashed apple
        self.smashed_image_sheet = None
        if(self.apple_type == "golden"):
            self.image = pygame.image.load("2DArt/Apple_golden.png")
            self.smashed_image_sheet = pygame.image.load("2DArt/Smashed_apple_golden_sprite_sheet.png").convert_alpha()
        else:
            self.image = pygame.image.load("2DArt/Apple.png")
            self.smashed_image_sheet = pygame.image.load("2DArt/Smashed_apple_sprite_sheet.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(settings.MIN_X,settings.MAX_X),
                            random.randint(settings.MIN_Y,settings.MAX_Y))
        self.dropping = False
        self.number = id
        self.text = settings.FONT.render(str(self.number),True,settings.WHITE)
        self.rect_new = None
        self.image_new = None
        
        

        self.smashed_sheet = sp_load.Sprite_Sheet_loader(self.smashed_image_sheet)

        self.smash_1 = self.smashed_sheet.get_image(0,32,32,1,settings.BLACK)
        self.smash_2 = self.smashed_sheet.get_image(1,32,32,1,settings.BLACK)
        self.smash_3 = self.smashed_sheet.get_image(2,32,32,1,settings.BLACK)
        self.smash_4 = self.smashed_sheet.get_image(3,32,32,1,settings.BLACK)

        self.smashed_list = [self.smash_1, self.smash_2, self.smash_3, self.smash_4]

        self.smashed = False

        self.radius = settings.RADIUS

    def draw(self,surface):
        surface.blit(self.image,self.rect)        

    def move(self,x,y):
        self.rect.move_ip(x,y)

    def shake(self,surface, margin):
        self.move(margin,margin)
        surface.blit(self.image,self.rect)

    def grow_and_shrink(self,surface,margin):
        x = self.rect.width
        y = self.rect.height
        self.image_new = pygame.transform.scale(self.image,(x + margin, y + margin))
        self.rect_new = self.image_new.get_rect()
        self.rect_new.center = self.rect.center
        surface.blit(self.image_new,self.rect_new)
    
    def get_rect(self):
        return self.rect

    def get_rect_yval(self):
        return self.rect.centery

    def get_rect_xval(self):
        return self.rect.centerx

    def get_smashed_list(self):
        return self.smashed_list

    def get_type(self):
        return self.apple_type

    def set_smashed(self, state):
        self.smashed = state

    def get_smashed_state(self):
        return self.smashed


        