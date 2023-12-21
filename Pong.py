# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 10:04:21 2023

@author: Ethan
"""

import pygame
import time
import random
import numpy as np
import threading

# initialize global variables
x_screen = 720
y_screen = 460
paddle_size = 80
pong_speed = 10
pong_xspeed = 0
pong_yspeed = 0

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)

# Initialize pygame
pygame.init()

pygame.display.set_caption("PONG")

game_window = pygame.display.set_mode((x_screen, y_screen))

fps = pygame.time.Clock()

# intialize paddle positions
player_paddle = [0, y_screen / 2]
enemy_paddle = [x_screen, y_screen/2]

# intialize pong position
pong_pos = [x_screen / 2, y_screen / 2]

# pong moving boolean for some logic
pong_moving = False

# computer paddle moving boolean
comp_moving = False

# Create score variables
player_score = 0
enemy_score = 0


def display_score():
    
    # Create a font for the score
    score_font = pygame.font.SysFont("Comic Sans MS", 40)
    
    # Create the surface for the font
    score_surface = score_font.render(str(player_score) + " - " + str(enemy_score), True, white)
    
    # Create the rect object
    score_rect = score_surface.get_rect()
    score_rect.center = (x_screen / 2, 20)
    
    # Apply the text to the screen
    game_window.blit(score_surface, score_rect)

def start_pong():
    global pong_xspeed, pong_yspeed, pong_pos, pong_moving, pong_speed
    pong_moving = True
    pong_xspeed = 0
    pong_yspeed = 0
    pong_speed += random.randrange(-5, 5)
    pong_pos = [x_screen / 2, y_screen / 2]
    time.sleep(2)
    
    angle = 0
    if random.randrange(0, 2) == 0:
        angle = random.randrange(135, 226)
    else:
        angle = random.randrange(315, 406)
    pong_xspeed = np.cos(np.radians(angle)) * pong_speed
    pong_yspeed = np.sin(np.radians(angle)) * pong_speed

def end_game(winner):
    game_window.fill(black)

    # creating font object score_font
    game_over_font = pygame.font.SysFont("Comic Sans MS", 20)
     
    # create the display surface object
    # score_surface
    game_over_surface = game_over_font.render(winner + " Wins!!", True, white)
     
    # create a rectangular object for the text
    # surface object
    game_over_rect = game_over_surface.get_rect()
    
    # center the text object
    game_over_rect.midtop = (x_screen / 2, y_screen / 4)
    
    # display the text
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
        
    time.sleep(5)
    
    pygame.quit()

def computer_move():
    global comp_moving
    comp_moving = True
    time.sleep(.5)
    comp_moving = False
    # Very rudimentary AI for enemy paddle
    if enemy_paddle[1] + 40 < pong_pos[1]:
        enemy_paddle[1] += 10
    elif enemy_paddle[1] + 40 > pong_pos[1]:
        enemy_paddle[1] -= 10

# Main Code

while True:
          
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                player_paddle[1] -= 10
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                player_paddle[1] += 10
    
    keys = pygame.key.get_pressed()
    
    # After the line keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        player_paddle[1] -= 10
    elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player_paddle[1] += 10
    
    # end game if someone has enough points
    if player_score == 11:
        end_game("Player 1")
    elif enemy_score == 11:
        end_game("Computer")
    

    if not comp_moving:
        y = threading.Thread(target=computer_move)
        y.start()

    # start moving the pong if not moving
    if not pong_moving:
        
        x = threading.Thread(target=start_pong)
        x.start()
        
    
    # Change pong position based on x and y speed
    pong_pos[0] += pong_xspeed
    pong_pos[1] += pong_yspeed
    
    # checks if intersecting player paddle
    if pong_pos[0] < 5 and pong_pos[0] >= 0 and pong_pos[1] > player_paddle[1] and pong_pos[1] < player_paddle[1] + paddle_size:
        if pong_xspeed < 0:
            pong_xspeed *= -1
    elif pong_pos[0] <= 0:
        enemy_score += 1
        pong_moving = False
    
    
    # checks if intersecting enemy paddle or across border
    if pong_pos[0] > x_screen - 5 and pong_pos[0] <= x_screen and pong_pos[1] > enemy_paddle[1] and pong_pos[1] < enemy_paddle[1] + paddle_size:
        if pong_xspeed > 0:
            pong_xspeed *= -1
    elif pong_pos[0] >= x_screen:
        player_score += 1
        pong_moving = False
        
    # top and bottom edge detection
    if pong_pos[1] <= 0 or pong_pos[1] >= y_screen:
        pong_yspeed *= -1
    
    # Draw stuff
    game_window.fill(black)
    
    pygame.draw.rect(game_window, white, pygame.Rect(player_paddle[0], player_paddle[1], 5, paddle_size))
    pygame.draw.rect(game_window, white, pygame.Rect(enemy_paddle[0] - 5, enemy_paddle[1], 5, paddle_size))
    pygame.draw.circle(game_window, white, (pong_pos[0], pong_pos[1]), 5)
    display_score()
    
    # update display
    pygame.display.update()
    
    fps.tick(30)
    