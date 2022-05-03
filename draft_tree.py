# -*- coding: utf-8 -*-
"""
Created on Mon May  2 18:29:44 2022

@author: User
"""

import pygame
import numpy as np

def tree_anim(depth, fps = 10, angle = -np.pi/6, scale_factor = 0.8):
    '''
    Inputs: 
    depth - The level of the tree as explained in the report.
    fps - Numbers of lines shown per second.
    TODO: Give them new name!
    angle - 
    Output: None
    Plays the animation of drawing a recursive tree as outlined above.
    '''
    size = width, height = 1080, 800  
    brown = (150, 75, 0)
    green = (0, 255, 0)
    white = (255, 255, 255)  
    ans_list = []
    frames_per_second = fps
    clock = pygame.time.Clock()
    def branch(length, curr_pos, direction, depth_counter=0):
        if depth_counter > depth:
            return None
        else:
            angle_x = length * np.cos(direction)
            angle_y = length * np.sin(direction)
            next_position = (curr_pos[0] + angle_x, curr_pos[1] + angle_y)
            if depth_counter == depth:
                ans_list.append((green, curr_pos, next_position))
            else:
                ans_list.append((brown, curr_pos, next_position))
            new = length * scale_factor
            branch(new, next_position, direction-angle, depth_counter+1)
            branch(new, next_position, direction, depth_counter+1)
            branch(new, next_position, direction+angle, depth_counter+1)
    branch(150, (width//2, height), -np.pi/2)
    # Animation Initializations
    pygame.init()
    win = pygame.display.set_mode(size)
    pygame.display.set_caption("Fractal Tree")
    win.fill(white)
    # Key variables to keep track of
    keep_running = True
    move_ball = False
    index = 0
    # Animation loop 
    while keep_running:
        # Keyboard events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keep_running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                move_ball = not move_ball
        # Draw a line according to ans_list
        if move_ball and index < len(ans_list):
            col, pos, next_pos = ans_list[index]
            pygame.draw.line(win, col, pos, next_pos)
            index += 1
        # Redraw step
        pygame.display.flip()
        clock.tick(frames_per_second)
    pygame.quit()

tree_anim(7, fps=30)