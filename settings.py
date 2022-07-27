import pygame

pygame.init()

#Variables for game settings

#draw rects for collision
DRAW_RECTS = True

#of screen
WIDTH = 300
HEIGHT = 300

#frames per second
FPS = 60

#text font
FONT = pygame.font.Font('freesansbold.ttf', 16)

#collision ratio
COLLISION_RATIO = 0.7
COLLISION_BARREL_RATIO = 0.7

#radius for collision
RADIUS = 64

#colors
WHITE = (255, 255, 255)
BLACK = (0,0,0)
RED = (255,0,0)
LIGHTRED = (255,80,80)

#max apples in trees
MAX_APPLES = 5

#margin by which a shook apple moves or grows and shrinks
DIFF_MARGIN = 5
margin_list = [2*DIFF_MARGIN,-2*DIFF_MARGIN]

#min and max for random spawn of apples in tree
MAX_X = 280
MIN_X = 30
MAX_Y = 100
MIN_Y = 10

#ms cooldown of animations
ANIMATION_BLINK_COOLDOWN = 50
ANIMATION_DROP_COOLDOWN = 50
ANIMATION_SMASH_COOLDOWN = 50
ANIMATION_PLAYER_COOLDOWN = 200

#ms cooldown of sounds
SOUND_DROP_COOLDOWN = 100

#number of times apple shakes or grows and shrinks
BLINKS = 12

#maximum y value of dropping apple
MAX_Y_DROP = 250

#player start coordinates
PLAYER_START_X = 40
PLAYER_START_Y = 180

#player movement speed
SPEED = 7

#x boundary
X_LIMIT_LEFT = 25
X_LIMIT_RIGHT = 280

#barrel capacity
BARREL_CAPACITY = 5

#barrel position
BARREL_X = -10
BARREL_Y = 215

#hearts positions
HEARTS_X = [200,230,260]
HEARTS_Y = 270