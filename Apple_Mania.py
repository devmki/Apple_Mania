#import librarys
from copyreg import dispatch_table
from distutils.errors import DistutilsOptionError
from doctest import ELLIPSIS_MARKER
import pygame
import pygame.locals
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
LEAVES_SOUND.set_volume(2.0)

DROPPING_SOUND = pygame.mixer.Sound("Music_and_Sounds/synth_beep_02.ogg")
DROPPING_SOUND.set_volume(0.0)

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
        self.image = pygame.image.load("2DArt/Player.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (settings.PLAYER_START_X, settings.PLAYER_START_Y)

        self.player_sheet = sp_load.Sprite_Sheet_loader(self.image)

        self.idle_image_1 = self.player_sheet.get_image(0,32,32,4,settings.BLACK)
        self.idle_image_2 = self.player_sheet.get_image(1,32,32,4,settings.BLACK)
        self.idle_full_image_1 = self.player_sheet.get_image(2,32,32,4,settings.BLACK)
        self.idle_full_image_2 = self.player_sheet.get_image(3,32,32,4,settings.BLACK)
        self.catch_empty_image = self.player_sheet.get_image(4,32,32,4,settings.BLACK)
        self.catch_full_image = self.player_sheet.get_image(5,32,32,4,settings.BLACK)

        self.player_sprite_list = [self.idle_image_1, self.idle_image_2, 
                                   self.idle_full_image_1, self.idle_full_image_2,
                                   self.catch_empty_image, self.catch_full_image]

        self.bucket_full = False

    def get_sprite_list(self):
        return self.player_sprite_list

    def move(self,x,y):
        self.rect.move_ip(x,y)
    
    def get_position(self):
        return self.rect.center

    def set_bucket_full(self):
        self.bucket_full = True
    
    def set_bucket_empty(self):
        self.bucket_full = False

    def get_bucket_state(self):
        return self.bucket_full
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

        self.smash_1 = self.smashed_sheet.get_image(0,32,32,1,settings.BLACK)
        self.smash_2 = self.smashed_sheet.get_image(1,32,32,1,settings.BLACK)
        self.smash_3 = self.smashed_sheet.get_image(2,32,32,1,settings.BLACK)
        self.smash_4 = self.smashed_sheet.get_image(3,32,32,1,settings.BLACK)

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

player_1 = Player()  

def main():
    #when was the last update of the grow and shrink animation
    last_update_blink = pygame.time.get_ticks()
    #when was the last update of the drop animation
    last_update_drop = pygame.time.get_ticks()
    #when was the last update of the smash animation
    last_update_smash = pygame.time.get_ticks()
    #when was the last update of the player animation
    last_update_player = pygame.time.get_ticks()
    #channel of the dropping sound
    #used to determine when to play the sound gain
    channel = DROPPING_SOUND.play()
    #keep time and set to fps
    clock = pygame.time.Clock()
    #continue running the game?
    run = True
    #number of spawned apple
    i = 0
    #list of the spawned apples
    apples_list = []
    #apple selected to be dropped
    chosen_apple = None
    #index of the chosen apple in apples_lsit
    index_of_apple = -1
    #group of apples for easier drawing
    apple_group = None
    #number of blinks (grow and shrink) to indicate will be dropped
    blink_count = 0
    #used for smash animation when apples hits the ground
    time_smash = 0
    #used to determine when to play sound of rustling leaves
    sound_shake_or_grow = 0
    #used to set play backround music infinitly
    infinite = -1
    #when to start music
    start = 0.0
    #index to toggle which grow and shrink animation is used
    grow_index = 0
    #index to toggle which smash animation is used
    smash_index = 0
    #index to toggle which idle animation is used for the player
    idle_index = 0
    pygame.mixer.music.play(infinite, start)
    #game loop
    while run:
        #limit to 60 FPS
        clock.tick(settings.FPS)

        current_time = pygame.time.get_ticks()

        #background
        DISPLAYSURFACE.blit(BACKGROUND,(0,0))

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
        if(not any([apple_dropping for apple_dropping in apples_list if apple_dropping.dropping == True]) and
            len(apple_group) == 5):
            chosen_apple = random.choice(apples_list)
            #maximum y value to which the apple will fall
            max_y_dropping_apple = settings.MAX_Y_DROP + random.randint(-20,20)
            #mark that apple as will be dropping
            index_of_apple = apples_list.index(chosen_apple)
            #remove chosen apple from apple_group
            apple_group.remove(apples_list[index_of_apple])

        #display the apples
        apple_group.draw(DISPLAYSURFACE)

        #currently no aplle is dropping, so indicate which one will
        if(not apples_list[index_of_apple].dropping):
            if(current_time - last_update_blink > settings.ANIMATION_BLINK_COOLDOWN):
                blink_count += 1
                #shake or grow and shrink direction
                if(grow_index == len(settings.margin_list) -1):
                    grow_index = 0
                else:
                    grow_index += 1
                if(SHAKE):
                    #shake apple
                    apples_list[index_of_apple].shake(DISPLAYSURFACE,settings.margin_list[grow_index])
                    if(sound_shake_or_grow == 0):
                        LEAVES_SOUND.play()
                    sound_shake_or_grow += 1
                else:
                    #grow and shrink apple
                    apples_list[index_of_apple].grow_and_shrink(DISPLAYSURFACE,settings.margin_list[grow_index])
                    if(sound_shake_or_grow == 0):
                        LEAVES_SOUND.play()
                    sound_shake_or_grow += 1
            elif(blink_count > settings.BLINKS):
                blink_count = 0
                sound_shake_or_grow = 0
                #chosen apple will is marked to start dropping
                apples_list[index_of_apple].dropping = True
                LEAVES_SOUND.stop()
            else:
                apples_list[index_of_apple].draw(DISPLAYSURFACE)

        #if the chosen apple is dropping
        if(apples_list[index_of_apple].dropping):
            #get current y and x value of the apple
            elevation = apples_list[index_of_apple].get_rect_yval()
            xvalue = apples_list[index_of_apple].get_rect_xval()
            if elevation < max_y_dropping_apple:
                smash_index = 0    
                if(current_time - last_update_drop > settings.ANIMATION_DROP_COOLDOWN):
                    #is the dropping sound not playing? -> then play it
                    if(not channel.get_busy()):
                        DROPPING_SOUND.set_volume(0.1)
                        DROPPING_SOUND.play()
                    #drop the apple by specified amount
                    apples_list[index_of_apple].move(0,settings.DIFF_MARGIN)
                    #update the elevation of the apple
                    elevation = apples_list[index_of_apple].get_rect_yval()
                apples_list[index_of_apple].draw(DISPLAYSURFACE)
            else:
                #apple is hitting the ground, time for the smash animation
                DISPLAYSURFACE.blit(apples_list[index_of_apple].get_smashed_list()[smash_index],
                    (xvalue-16, elevation-16))   
                if(current_time - last_update_smash > settings.ANIMATION_SMASH_COOLDOWN):
                    time_smash += 1
                    if(time_smash == 1):
                        BURST_SOUND.play()
                    if(smash_index < len(apples_list[index_of_apple].get_smashed_list())-1):
                        if(time_smash % 3 == 0):
                            smash_index += 1
                    else:    
                        apples_list.pop(index_of_apple)
                        time_smash = 0


        #blit the player
        position = player_1.get_position()
        if(current_time - last_update_player > settings.ANIMATION_PLAYER_COOLDOWN):
            if(not player_1.get_bucket_state()):          
                if(idle_index == 0):
                    idle_index = 1
                elif(idle_index == 1):
                    idle_index = 0
            else:
                if(idle_index == 3):
                    idle_index = 2
                elif(idle_index == 2):
                    idle_index = 3
        DISPLAYSURFACE.blit(player_1.get_sprite_list()[idle_index],(position[0],position[1]))

        #get all events that are happening
        for event in pygame.event.get():
            #exit the game
            if (event.type == pygame.locals.QUIT):
                pygame.quit()
                sys.exit()
            #a key is pressed
            elif (pygame.key.get_pressed()):
                keys = pygame.key.get_pressed()
                position = player_1.get_position()
                #move player right
                if(keys[pygame.K_d]):
                    #right x limit
                    if(position[0] < settings.X_LIMIT_RIGHT):
                        player_1.move(settings.SPEED, 0)   
                        if(player_1.get_bucket_state()):
                            idle_index = 2 
                        else:
                            idle_index = 0             
                        DISPLAYSURFACE.blit(player_1.get_sprite_list()[idle_index],(position[0],position[1]))
                #move player left
                elif(keys[pygame.K_a]):
                    #left x limit
                    if(position[0] > settings.X_LIMIT_LEFT):
                        player_1.move(-1*settings.SPEED,0)
                        if(player_1.get_bucket_state()):
                            idle_index = 2 
                        else:
                            idle_index = 0
                        DISPLAYSURFACE.blit(player_1.get_sprite_list()[idle_index],(position[0],position[1]))
                #try to catch the apple
                elif(keys[pygame.K_w]):
                    if(not player_1.get_bucket_state()):
                        colliding = pygame.sprite.collide_circle_ratio(settings.COLLISION_RATIO)(chosen_apple, player_1)
                        if(colliding):
                            player_1.set_bucket_full()
                            apples_list.pop(index_of_apple)
                            idle_index = 5
                            DISPLAYSURFACE.blit(player_1.get_sprite_list()[idle_index],(position[0],position[1]))
                        else:
                            idle_index = 4
                            DISPLAYSURFACE.blit(player_1.get_sprite_list()[idle_index],(position[0],position[1]))
                #empty bucket
                elif(keys[pygame.K_s]):
                    if(player_1.get_bucket_state()):
                        player_1.set_bucket_empty()
                        idle_index = 0


        #update the varying timers if necessary
        if(current_time - last_update_blink > settings.ANIMATION_BLINK_COOLDOWN):
            last_update_blink =  current_time
        
        if(current_time - last_update_drop > settings.ANIMATION_DROP_COOLDOWN):
            last_update_drop =  current_time

        if(current_time - last_update_smash > settings.ANIMATION_SMASH_COOLDOWN):
            last_update_smash =  current_time

        if(current_time - last_update_player > settings.ANIMATION_PLAYER_COOLDOWN):
            last_update_player =  current_time

        #update the display
        pygame.display.update()        

if __name__ == "__main__":
    main()