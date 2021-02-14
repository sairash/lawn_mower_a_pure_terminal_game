import os
import time
import  keyboard
import sys
import random

up_just_pressed = False
height = 15
width = 120
os.system('CLS')

frames_per_second=3
score = 0
high_score=2000

player_jump_mode=3
player_jumping = False
player_jumping_up = False
player_jumping_down = False
player_location=12
grass_location = 30
types_of_grass = [';','▲',',','█', '▐', '▌', '◄']



valid_hex = '0123456789ABCDEF'.__contains__
def cleanhex(data):
    return ''.join(filter(valid_hex, data.upper()))

def print_color(text, hexcode, end='\n'):
    """print in a hex defined color"""
    hexint = int(cleanhex(hexcode), 16)
    print("\x1B[38;2;{};{};{}m{}\x1B[0m".format(hexint>>16, hexint>>8&0xFF, hexint&0xFF, text),end=end)


def player_jump():
    global player_location, player_jump_mode, player_jumping_up, player_jumping_down, player_jumping
    if player_jump_mode > 0 and player_jumping_up:
        player_jump_mode = player_jump_mode - 1
        player_location = player_location-1
    else:
        player_jumping_up = False
        player_jumping_down = True

    if player_jump_mode < 3 and player_jumping_down:
        player_jump_mode = player_jump_mode + 1
        player_location = player_location + 1
    else:
        player_jumping_up = False
        player_jumping_down = False

    if player_location == 12 and player_jumping_up == False and player_jumping_down == False:
        player_jumping = False



def print_player():
    print_color('`.','#ffffff',end='')
    print_color('=','#dd2b33',end='')
    print_color('.','#ffffff',end='')



def print_grass(number_ofSpaces):
    global player_location, grass_location
    if player_location == 12:
        print_color(' '*int(number_ofSpaces-4)+types_of_grass[random.randint(0,len(types_of_grass)-1)]+str(number_ofSpaces), '#66ff00', end='')
    else:
        if number_ofSpaces >= 4:
            print_color(' '*int(number_ofSpaces)+types_of_grass[random.randint(0,len(types_of_grass)-1)]+str(number_ofSpaces), '#66ff00', end='')
        else:
            grass_location = 0


def up():
    global up_just_pressed, player_jump_mode, player_jumping, player_location, player_jumping_up, player_jumping_down

    if up_just_pressed == False and player_jumping == False:
        player_jump_mode = player_jump_mode - 1
        player_jumping = True
        player_jumping_up = True
        player_jumping_down = False
        player_location = player_location - 1

        up_just_pressed = True


while True:
    grass_location =grass_location-1
    up_just_pressed = False
    os.system('CLS')
    print_color('Score: '+str(score)+'   HighScore:'+str(high_score), '#ffffff', end='')
    score = score+1
    if player_jumping:
        player_jump()

    keyboard.add_hotkey('up', up)
    for line in range(height):
        if line == player_location:
            print_player()
        for block in range(width):
            if line == 12 and block == grass_location:
                print_grass(grass_location)

            if grass_location == 5 and player_location == 12:
                print()
                print_color('Game Over','#ff0000',end='')
                sys.exit()
            if line == 13:
                print_color('▄', '#66ff00',end='')
            if line == 14:
                print_color('█', '#b5651d',end='')
        print()
    #
    # print_player()
    grass_location = grass_location - 1
    time.sleep(1/frames_per_second)