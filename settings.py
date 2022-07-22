#Variables for game settings

#of screen
WIDTH = 300
HEIGHT = 300

#frames per second
FPS = 60

#colors
WHITE = (255, 255, 255)
BLACK = (0,0,0)

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
SPEED = 5

#x boundary
X_LIMIT_LEFT = -25
X_LIMIT_RIGHT = 215