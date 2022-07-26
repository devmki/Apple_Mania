#import librarys
from copyreg import dispatch_table
from distutils.errors import DistutilsOptionError
from doctest import ELLIPSIS_MARKER
import pygame
import pygame.locals
import sys
import random
import time

#import player, barrel and apple classes
from player import Player
from barrel import Barrel
from apple import Apple

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

CATCH_SOUND = pygame.mixer.Sound("Music_and_Sounds/power_up_02.ogg")
CATCH_SOUND.set_volume(0.1)

#create a display to show the game
DISPLAYSURFACE = pygame.display.set_mode((settings.WIDTH,settings.HEIGHT))

#background image
BACKGROUND = pygame.image.load("2DArt/apple_tree.png")

#set game caption
GAME_NAME = "APPLE MANIA"
pygame.display.set_caption(GAME_NAME)

#shake or inflate?
SHAKE = False

#create instances
player_1 = Player(DISPLAYSURFACE)  
barrel = Barrel(DISPLAYSURFACE)

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
    #play music
    pygame.mixer.music.play(infinite, start)
    #index to toggle which barrel image is used
    barrel_index = 0
    #triggered when player has no more lives
    game_over = 0 #0 run game, #1 player won, #2 player lost
    #game loop
    while run:
        #limit to 60 FPS
        clock.tick(settings.FPS)

        current_time = pygame.time.get_ticks()

        #background
        DISPLAYSURFACE.blit(BACKGROUND,(0,0))

        #blit barrel
        DISPLAYSURFACE.blit(barrel.get_sprite_list()[barrel_index],barrel.get_rect(barrel_index))
        DISPLAYSURFACE.blit(barrel.get_text(),barrel.get_text_rect())

        if(game_over == 0):
            #if less than 5 apples then add more applesS
            while len(apples_list) <= settings.MAX_APPLES-1:
                #create new instance of apple
                new_apple = Apple(DISPLAYSURFACE,i)
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
                    if(settings.DRAW_RECTS):
                        pygame.draw.rect(DISPLAYSURFACE,settings.WHITE,apples_list[index_of_apple].get_rect(),1)
                else:
                    #apple is hitting the ground, time for the smash animation
                    DISPLAYSURFACE.blit(apples_list[index_of_apple].get_smashed_list()[smash_index],
                        (xvalue-16, elevation-16))   
                    if(settings.DRAW_RECTS):    
                        pygame.draw.rect(DISPLAYSURFACE,settings.WHITE,apples_list[index_of_apple].get_rect(),1)    
                    if(current_time - last_update_smash > settings.ANIMATION_SMASH_COOLDOWN):
                        time_smash += 1
                        if(time_smash == 1):
                            BURST_SOUND.play()
                        if(smash_index < len(apples_list[index_of_apple].get_smashed_list())-1):
                            if(time_smash % 3 == 0):
                                smash_index += 1
                        else:    
                            apples_list.pop(index_of_apple)
                            player_1.set_lives(-1)
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
            player_1.draw_hearts(DISPLAYSURFACE)
            DISPLAYSURFACE.blit(player_1.get_sprite_list()[idle_index],player_1.get_rect())
            

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
                                if(idle_index != 3):
                                    idle_index = 2 
                            else:
                                if(idle_index != 1):
                                    idle_index = 0             
                            DISPLAYSURFACE.blit(player_1.get_sprite_list()[idle_index],player_1.get_rect())
                    #move player left
                    elif(keys[pygame.K_a]):
                        #left x limit
                        if(position[0] > settings.X_LIMIT_LEFT):
                            player_1.move(-1*settings.SPEED,0)
                            if(player_1.get_bucket_state()):
                                if(idle_index !=3):
                                    idle_index = 2 
                            else:
                                if(idle_index != 1):
                                    idle_index = 0
                            DISPLAYSURFACE.blit(player_1.get_sprite_list()[idle_index],player_1.get_rect())
                    #try to catch the apple
                    elif(keys[pygame.K_w]):
                        if(not player_1.get_bucket_state()):
                            player_1.move(0,0)
                            colliding = pygame.sprite.collide_circle_ratio(settings.COLLISION_RATIO)(chosen_apple, player_1)
                            if(colliding):
                                player_1.set_bucket_full()
                                apples_list.pop(index_of_apple)
                                idle_index = 5
                                DISPLAYSURFACE.blit(player_1.get_sprite_list()[idle_index],player_1.get_rect())
                                CATCH_SOUND.play()
                            else:
                                idle_index = 4
                                DISPLAYSURFACE.blit(player_1.get_sprite_list()[idle_index],player_1.get_rect())
                    #empty bucket
                    elif(keys[pygame.K_s]):
                        if(player_1.get_bucket_state()):
                            player_1.move(0,0)
                            DISPLAYSURFACE.blit(player_1.get_sprite_list()[idle_index],player_1.get_rect())
                            #check if emptied into barrel
                            colliding = pygame.sprite.collide_rect_ratio(settings.COLLISION_BARREL_RATIO)(player_1,barrel)
                            idle_index = 0
                            player_1.set_bucket_empty()
                            if(colliding):            
                                barrel.increment_amount(1)
                                barrel_index = 1


            #update the varying timers if necessary
            if(current_time - last_update_blink > settings.ANIMATION_BLINK_COOLDOWN):
                last_update_blink =  current_time
            
            if(current_time - last_update_drop > settings.ANIMATION_DROP_COOLDOWN):
                last_update_drop =  current_time

            if(current_time - last_update_smash > settings.ANIMATION_SMASH_COOLDOWN):
                last_update_smash =  current_time

            if(current_time - last_update_player > settings.ANIMATION_PLAYER_COOLDOWN):
                last_update_player =  current_time


            if(settings.DRAW_RECTS):
                pygame.draw.rect(DISPLAYSURFACE,settings.WHITE,barrel.get_rect(barrel_index),1)
                pygame.draw.rect(DISPLAYSURFACE,settings.WHITE,player_1.get_rect(),1)

            #check if player won the game
            if(barrel.get_current_amount() == barrel.get_capacity()):
                game_over = 1
            #check if player lives are spent
            elif(player_1.get_lives() < 1):
                game_over = 2

        else:
            if(game_over == 1):
                DISPLAYSURFACE.blit(settings.FONT.render("YOU WIN!",True,settings.WHITE),(125,150))                
            elif(game_over == 2):
                DISPLAYSURFACE.blit(settings.FONT.render("GAME OVER!",True,settings.WHITE),(125,150))
            
            for event in pygame.event.get():
                if(event.type == pygame.locals.QUIT):
                    pygame.quit()
                    sys.exit()
                #key pressed
                elif (pygame.key.get_pressed()):
                    keys = pygame.key.get_pressed()
                    #restart the game
                    if(keys[pygame.K_1]):
                        game_over = 0
                        player_1.reset_lives()
                        barrel.set_amount(0)
       
        #update the display
        pygame.display.update()

if __name__ == "__main__":
    main()