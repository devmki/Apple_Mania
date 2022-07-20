#Variables for game settings

#of screen
WIDTH = 300
HEIGHT = 300

#frames per second
FPS = 60

#colors
WHITE = (255, 255, 255)

#max apples in trees
MAX_APPLES = 5

#margin by which a shook apple moves or grows and shrinks
DIFF_MARGIN = 5
margin_list = [DIFF_MARGIN, -1*DIFF_MARGIN]

#min and max for random spawn of apples in tree
MAX_X = 280
MIN_X = 30
MAX_Y = 100
MIN_Y = 10

#time is divided by this number
#modulo must be 0 for dropping apple
TIME_MODULO = 3

#number of times apple shakes or grows and shrinks
BLINKS = 8

#maximum y value of dropping apple
MAX_Y_DROP = 250
