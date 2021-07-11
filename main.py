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


time_for_jump = 4
time_for_jump_temp = time_for_jump
player_jumping = False
player_up = False
player_down = False
player_location=12 
player_dies_when_the_grass_reaches_here = 5

grass_despawn_when_less_than=4
grass_location = []
grass_last_position = width

game_over=False

text_file = open("data.dat", "r")
high_score = text_file.readlines()[0]
text_file.close()


os.system('mode con: cols='+str(width)+' lines='+str(height+5)+'') #change size of terminal

valid_hex = '0123456789ABCDEF'.__contains__
def cleanhex(data):
    return ''.join(filter(valid_hex, data.upper()))

def print_color(text, hexcode, end='\n'):
    """print in a hex defined color"""
    hexint = int(cleanhex(hexcode), 16)
    print("\x1B[38;2;{};{};{}m{}\x1B[0m".format(hexint>>16, hexint>>8&0xFF, hexint&0xFF, text),end=end)

def terminal_prop():
    os.system('CLS')


def print_player():
    print_color('`.','#ffffff',end='')
    print_color('=','#dd2b33',end='')
    print_color('.','#ffffff',end='')



def spawn_sky():
    print()
    print_color(' '*20+'*'+' '*19+'*'+' '*10+'*'+' '*50+'*'+'  '+'▄','#ffffff')
    print_color(' '*(width-16)+'███','#ffffff')
    print_color('*'+' '*20+'*'+' '*10+'*'+' '*49+'*'+' '*19+'   '+'▀','#ffffff')

def high_score_save(score):
    f = open("data.dat", "w")
    f.write(score)
    f.close()


def should_spwan_grass(number_of_grass):
    global grass_last_position
    if(number_of_grass == 0):
        return True
    elif(grass_location[len(grass_location)-1] <= 100):
        return True
    else:
        return False

def spawn_grass():
    global grass_last_position
    grass_location.append(width)


def grass_postion_manager():
    for key in range(len(grass_location)):
        grass_location[key] -= 1;


def print_first_grass(grass_location_postion_not_global):
    global grass_last_position
    grass_last_position = grass_location_postion_not_global
    if player_location != 12 & line == 12:
        print_color(' '*(grass_last_position)+';','#66ff00',end='')
    else:
        print_color(' '*(grass_last_position-4)+';','#66ff00',end='')

def print_other_grass(grass_location_postion_not_global):
    global grass_last_position
    print_color(' '*((grass_location_postion_not_global - 1) -grass_last_position)+';','#66ff00',end='')
    grass_last_position += (grass_location_postion_not_global - grass_last_position)


def print_grass(block):
    global game_over, grass_location
    delete_first_item = False
    for key in range(len(grass_location)):
        grass_location_postion = grass_location[key]
        if player_location == 12 and grass_location_postion+1 == player_dies_when_the_grass_reaches_here:
            game_over = True
        if key == 0:
            if block == grass_location_postion:
                print_first_grass(grass_location_postion)
        else:
            if block == grass_location[key]:
                print_other_grass(grass_location_postion)
        if grass_location_postion <= grass_despawn_when_less_than:
            delete_first_item = True
    if delete_first_item:
        grass_location.pop(0)


def grass_manager(block):
    number_of_grass = len(grass_location)
    if should_spwan_grass(number_of_grass):
        spawn_grass()
    print_grass(block)



def player_jump():
    global player_jumping, player_up, player_down, time_for_jump_temp, player_location
    if player_up:
        for x in range(time_for_jump_temp):
            player_location -= 1
            time_for_jump_temp -=1
            break
        if time_for_jump_temp == 0:
            player_up = False
            player_down = True
    elif player_down:
        for x in range(time_for_jump):
            player_location += 1
            time_for_jump_temp +=1
            break
        if time_for_jump_temp == time_for_jump:
            player_up = False
            player_down = False
    else:
        player_up = False
        player_down = False
        player_jumping = False


def up():
    global player_jumping, player_up, player_down
    if player_jumping:
        pass
    else:
        player_jumping = True
        player_up = True

def exitRequest():
    global game_over
    game_over = True

while True:
    terminal_prop()
    up_just_pressed = False
    print_color('Score: '+str(score), '#ffffff', end='')
    print_color(' HighScore: '+str(high_score),'#00ff00', end='')
    score = score+1
    if player_jumping:
        player_jump()
    keyboard.add_hotkey('up', up)
    keyboard.add_hotkey('esc', exitRequest)
    for line in range(height):
        if line == player_location:
            print_player()
        if line == 12:
            grass_postion_manager()
        for block in range(width):
            if line == 12:
                grass_manager(block)
            if game_over:
                score = score - 2
                os.system('CLS')
                print_color(' '*int(width/3)+'Game Over','#ff0000')
                sys.exit()
            if line == 13:
                print_color('#', '#00ff00',end='')
            if line == 14:
                print_color('"', '#b5651d',end='')
        print()
    print_color(' Use', '#ffffff', end='')
    print_color(' [^] ', '#0000ff',end='')
    print_color('Up Arrow Key to jump and Use ','#ffffff', end='')
    print_color('[esc] ', '#ff0000',end='')
    print_color('to Exit','#ffffff',end='')
    print()
    time.sleep(1/frames_per_second)
