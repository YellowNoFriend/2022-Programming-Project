import pygame, os, timeit
import numpy as np
import matplotlib.pyplot as plt
from useful_func import integer_input_validation, float_input_validation
def tree_anim(depth, fps = 10, angle = np.pi/6, scale_factor = 0.8, init_len = 150):
    '''
    Plays the animation of drawing a recursive tree as outlined above.
    Inputs: 
    depth - The level of the tree as explained in the report.
    fps - Numbers of lines shown per second.
    angle - the angle theta mentioned in the definition.
    scale_factor - the length ratio between two trunk that are 1 depth away.
    init_let - the length of the trunk at depth 0.
    '''
    size = width, height = 1080, 800  
    brown = (150, 75, 0)
    green = (0, 255, 0)
    white = (255, 255, 255)  
    ans_list = []
    frames_per_second = fps
    clock = pygame.time.Clock()
    def branch(length, curr_pos, direction, depth_counter=0):
        '''
        A subfunction in tree_anim which alters the ans_list when called.
        Inputs:
        length - length of the trunk
        curr_pos - The starting point of the trunk (coordinate)
        direction - current facing angle of the tree
        depth_counter - current depth of the trunk being plotted
        '''
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
    branch(init_len, (width//2, height), -np.pi/2)
    # Animation Initializations
    pygame.init()
    win = pygame.display.set_mode(size)
    pygame.display.set_caption(f"Fractal Tree of depth {depth} - Current Speed: {frames_per_second}")
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
            # Speed change if ArrowUp/ArrowDown is pressed
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                frames_per_second = (4/3)* frames_per_second
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                frames_per_second = 0.75 * frames_per_second
            pygame.display.set_caption(f"Fractal Tree of depth {depth} - Current Speed: {frames_per_second}")
        # Draw a line according to ans_list
        if move_ball and index < len(ans_list):
            col, pos, next_pos = ans_list[index]
            pygame.draw.line(win, col, pos, next_pos)
            index += 1
        # Redraw step
        pygame.display.flip()
        clock.tick(frames_per_second)
    pygame.quit()
def run_tree(): 
    """
    Draw the recursive tree using user-defined inputs. 
    """
    # Get required information from the user 
    depth = integer_input_validation('integer depth',6,1,10)
    speed = integer_input_validation('branches to generate per second',50,1, 60)
    angle = float_input_validation('Angle between Branches',np.pi/6,0, np.pi)
    scale_factor = float_input_validation('Scale Factor',0.8,0, 1)
    init_len = integer_input_validation('Length of Branch at Depth 0',150,50, 200)
    # Now run the animation with user-provided input
    tree_anim(depth, speed, angle, scale_factor, init_len)
    return None