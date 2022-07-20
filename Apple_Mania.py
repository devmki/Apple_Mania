#import librarys
from distutils.errors import DistutilsOptionError
import pygame
from pygame.locals import *
import sys
import random
import time

#import settings
import settings
import sprite_sheet_loader as sp_load

#initialize pygame engine
pygame.init()

#initialize sound mixer
pygame.mixer.init()

#background music
pygame.mixer.music.load("Music_and_Sounds/Groovy booty.wav")
pygame.mixer.music.set_volume(0.1)

#sound effects
LEAVES_SOUND = pygame.mixer.Sound("Music_and_Sounds/leaves.wav")
LEAVES_SOUND.set_volume(1.0)

DROPPING_SOUND = pygame.mixer.Sound("Music_and_Sounds/synth_beep_02.ogg")
DROPPING_SOUND.set_volume(0.1)

BURST_SOUND = pygame.mixer.Sound("Music_and_Sounds/retro_misc_01.ogg")
BURST_SOUND.set_volume(0.1)

#create a display to show the game
DISPLAYSURFACE = pygame.display.set_mode((settings.WIDTH,settings.HEIGHT))

#background image
BACKGROUND = pygame.image.load("2DArt/apple_tree.png")

#set game caption
GAME_NAME = "APPLE MANIA"
pygame.display.set_caption(GAME_NAME)

#text font
FONT = pygame.font.Font('freesansbold.ttf', 32)

#shake or inflate?
SHAKE = False

#sprite sheet for smashed apple
smashed_image_sheet = pygame.image.load("2DArt/Smashed_apple_sprite_sheet.png").convert_alpha()

#player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.lives = 3
        self.image = pygame.image.load("2DArt/Player.png")

#class apple
class Apple(pygame.sprite.Sprite):
    def __init__(self, id):
        super().__init__()
        self.image = pygame.image.load("2DArt/Apple.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(settings.MIN_X,settings.MAX_X),
                            random.randint(settings.MIN_Y,settings.MAX_Y))
        self.dropping = False
        self.number = id
        self.text = FONT.render(str(self.number),True,settings.WHITE)
        self.rect_new = None
        self.image_new = None
        self.smashed_sheet = sp_load.Sprite_Sheet_loader(smashed_image_sheet)

        self.smash_1 = self.smashed_sheet.get_image(0,32,32,settings.BLACK)
        self.smash_2 = self.smashed_sheet.get_image(1,32,32,settings.BLACK)
        self.smash_3 = self.smashed_sheet.get_image(2,32,32,settings.BLACK)
        self.smash_4 = self.smashed_sheet.get_image(3,32,32,settings.BLACK)

        self.smashed_list = [self.smash_1, self.smash_2, self.smash_3, self.smash_4]


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

    def get_rect_yval(self):
        return self.rect.centery

    def get_rect_xval(self):
        return self.rect.centerx

    def get_smashed_list(self):
        return self.smashed_list
   

def main():
    clock = pygame.time.Clock()
    run = True
    apples_list = []
    chosen_apple = None
    i = 0
    index_of_apple = -1
    apple_group = None
    timer = 0
    infinite = -1
    start = 0.0
    smash_animation_counter = 0
    pygame.mixer.music.play(infinite, start)
    #game loop
    while run:
        #limit to 60 FPS
        clock.tick(settings.FPS)

        #if less than 5 apples then add more applesS
        while len(apples_list) <= settings.MAX_APPLES-1:
            #create new instance of apple
            new_apple = Apple(i)
            if(apples_list):
                #check if apple collides with any of already existing apples
                colliding = pygame.sprite.spritecollideany(new_apple, apple_group)
                if(type(colliding) == type(None)):
                    #if not append to apple list
                    apples_list.append(new_apple)
                    i = i+1
            else:     
                apples_list.append(new_apple)
                i = i+1

            #make a sprite group from apples list
            apple_group = pygame.sprite.Group(apples_list)

        #select an apple that will drop, if no other apple is currently dropping
        if(not any([apple_dropping for apple_dropping in apples_list if apple_dropping.dropping == True])):
            chosen_apple = random.choice(apples_list)
            max_y_dropping_apple = settings.MAX_Y_DROP + random.randint(0,10)

        #mark that apple as will be dropping
        index_of_apple = apples_list.index(chosen_apple)
        #remove chosen apple from apple_group
        apple_group.remove(apples_list[index_of_apple])

        if(not apples_list[index_of_apple].dropping):
            LEAVES_SOUND.play()
            for i in range(settings.BLINKS):
                #background
                DISPLAYSURFACE.blit(BACKGROUND,(0,0))
                #display the apples
                apple_group.draw(DISPLAYSURFACE)
                #shake or inflate direction
                index = 0
                if(i%2 == 0):
                    index = 0
                else:
                    index = 1
                if(SHAKE):
                    #shake apple
                    apples_list[index_of_apple].shake(DISPLAYSURFACE,settings.margin_list[index])
                else:
                    #grow and shrink apple
                    apples_list[index_of_apple].grow_and_shrink(DISPLAYSURFACE,settings.margin_list[index])
                #update the display
                pygame.display.update()
                time.sleep(0.1)
            LEAVES_SOUND.stop()

        #chosen apple will drop or is dropping
        apples_list[index_of_apple].dropping = True

        #if the chosen apple is dropping
        if(apples_list[index_of_apple].dropping):
            #get current y value of the apple
            elevation = apples_list[index_of_apple].get_rect_yval()
            xvalue = apples_list[index_of_apple].get_rect_xval()
            if elevation < max_y_dropping_apple:
                smash_animation_counter = 0
                if(timer % settings.TIME_MODULO == 0):
                    if(timer % (6*settings.TIME_MODULO) == 0):
                        DROPPING_SOUND.play()
                    apples_list[index_of_apple].move(0,settings.DIFF_MARGIN)
                    elevation = apples_list[index_of_apple].get_rect_yval()
                    #background
                    DISPLAYSURFACE.blit(BACKGROUND,(0,0))
                    #display the apples
                    apple_group.draw(DISPLAYSURFACE)
                    #draw dropping aplle
                    if(elevation < max_y_dropping_apple):
                        apples_list[index_of_apple].draw(DISPLAYSURFACE)
                    #update the display
                    pygame.display.update()
                    timer += 1
                else:
                    timer += 1
            else:
                if(smash_animation_counter < len(apples_list[index_of_apple].get_smashed_list())-1):
                    DISPLAYSURFACE.blit(apples_list[index_of_apple].get_smashed_list()[smash_animation_counter],
                                        (xvalue-16, elevation-16))
                    smash_animation_counter += 1
                    pygame.display.update()
                    time.sleep(0.1)
                else:    
                    apples_list.pop(index_of_apple)
                    BURST_SOUND.play()
                    time.sleep(0.5)

        #get all events that are happening
        for event in pygame.event.get():
            #exit the game
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

if __name__ == "__main__":
    main()