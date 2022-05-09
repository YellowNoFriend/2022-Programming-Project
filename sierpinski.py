import pygame, os, timeit
import numpy as np
import matplotlib.pyplot as plt
from useful_func import integer_input_validation, float_input_validation
def make_sierpinski(depth, triangle, triangle_list):
    '''
    Function inputs: 
    - depth (of recursion), 
    - triangle (vertex coordinates)
    - triangle_list (list of triange coordinates)
    Modifies triangle_list: all the depth 1 (bottom) triangles are added 
    to this list (using recursion relative to the input triangle)
    '''
    (x0,y0) = triangle[0]
    (x1,y1) = triangle[1]
    (x2,y2) = triangle[2]
    # Maximum depth reached (going down) so add this triangle to the list
    if depth == 1:
        triangle_list.append(triangle)
        return None 
    # Otherwise split triangle into three sub triangles
    midpoint_A = (x0 + (x1-x0)/2.0, y0)
    midpoint_B = (x0 + (x2-x0)/2.0, y2 + (y0-y2)/2.0)
    midpoint_C = (x2 + (x1-x2)/2.0, y2 + (y1-y2)/2.0)
    # Recursive call on triangles
    new_triangle = ((x0,y0), midpoint_A, midpoint_B)
    make_sierpinski(depth-1, new_triangle, triangle_list)
    new_triangle = (midpoint_A, (x1,y1), midpoint_C)
    make_sierpinski(depth-1,new_triangle,triangle_list)
    new_triangle = (midpoint_B, midpoint_C, (x2,y2))
    make_sierpinski(depth-1, new_triangle, triangle_list)    
    return None
def draw_sierpinski_ext(depth=6, speed = 50,colour=(0, 0, 255),backgroundColour = (255,255,255)):
    '''
    Function that draws the Sierpinski triangle as an animation. 
    Inputs: 
    depth - Depth of the Triangle as specified in make_sierpinski
    speed - frame per second in the animation, can be adjusted using up and down arrows
    colour - Color of the triangle: An 3-integer tuple storing the RGB Values
    backgroundColour - Color of the background: An 3-integer tuple storing the RGB Values
    Outputs: None
    '''
    dimensions = (screen_width,screen_height) = (900, 862)
    master_triangle = ((50,800),(850,800),(450,62))
    clock = pygame.time.Clock()
    frames_per_second = speed
    # Make a list of all the triangle vertex coordinates of the given 
    # depth (in make_sierpinski we process  depth to work down to 1)
    triangle_list = []
    make_sierpinski(depth,master_triangle,triangle_list)
    # Initialise pygame, the screen display and title
    pygame.init()
    screen = pygame.display.set_mode(dimensions)
    caption = 'Sierpinski Triangle            '
    caption += '(1)  \'Space\' to start or pause    '
    caption += '(2)  \'Up/Down\' to change the speed'
    pygame.display.set_caption(f'{caption} (3) speed = {speed}')
    screen.fill(backgroundColour)
    pygame.display.flip()
    # Total number of triangles to be drawn 
    number_of_triangles = len(triangle_list)
    index = 0
    draw_triangle = False
    keep_running = True
    # Animation loop 
    while keep_running:
        for event in pygame.event.get():
            # Exit (at end of this iteration) using quit (e.g Ctrl-q or red button)
            if event.type == pygame.QUIT:
                keep_running = False
            if speed < 1:
                speed = 1
            # Start and pause the animation with the space key 
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                draw_triangle  = not draw_triangle
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                speed = (4/3)* speed
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                speed = 0.75 * speed
            pygame.display.set_caption(f'{caption} (3) speed = {speed}')
            frames_per_second = speed 
        # Keep draw next triangle with index 'index' if not told to pause and not complete
        if draw_triangle and index  < number_of_triangles:
            pygame.draw.polygon(screen,colour,triangle_list[index],0)
            pygame.display.update()
            clock.tick(frames_per_second)
            # Index uptate: index walks through triangle_list indices
            index += 1
    pygame.quit()
    return None
def run_sierpinski_ext(): 
    """
    Draw the sierpinski triangle using user-defined inputs. 
    """
    # Get required information from the user 
    depth = integer_input_validation('integer depth',6,1,10)
    speed = integer_input_validation('triangles to generate per second',50,1, 60)
    trig_R = integer_input_validation('R value for triangle Color',0,0,255)
    trig_G = integer_input_validation('G value for triangle Color',255,0,255)
    trig_B = integer_input_validation('B value for triangle Color',0,0,255)
    bg_R = integer_input_validation('R value for triangle Color',255,0,255)
    bg_G = integer_input_validation('G value for triangle Color',255,0,255)
    bg_B = integer_input_validation('B value for triangle Color',255,0,255)
    trig_color = (trig_R, trig_G, trig_B)
    bg_color = (bg_R, bg_G, bg_B)
    # Now run the animation with user-provided input
    draw_sierpinski_ext(depth, speed, trig_color, bg_color) 
    return None
