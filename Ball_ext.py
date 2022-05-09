import pygame, os, timeit
import numpy as np
import matplotlib.pyplot as plt
from useful_func import integer_input_validation, float_input_validation
class Ball(object):
    '''
    The class Ball encapsulate all the information needed to 
    draw a ball on the PyGame module.
    '''
    def __init__(self, x, y, x_step, y_step, size=50):
        '''
        Initialization of the class Ball. 
        (x, y) - the coordinate relative to the screen, 
        both of them are float from 0 to 1.
        (x_step, y_step) - the velocity of the ball (pixel per frame).
        size - optional argument, size of the ball.
        '''
        self.x = x
        self.y = y
        self.x_step = x_step
        self.y_step = y_step
        self.size = size

def bouncing_ball_ext(ball, speed_factor=5,gravity=9.81):
    '''
    Play a bouncing ball animation according to the inputs:
    Inputs:
    ball - an object from the class Ball
    speed_factor - the frames per second of animation
    gravity - the drag factor affecting the motion of the ball (positive is upwards)
    (N.B., gravity = 0 corresponds to no gravity, obviously)
    Output: None
    '''
    # Required variables, x0, y0 is the starting coordinate of the ball
    screen_size = (screen_width, screen_height) = (1080, 800)
    white = (255,255,255)
    x0, y0 = (screen_width - ball.size)*ball.x, (screen_height - ball.size)*ball.y
    g = -gravity
    # Used for the pause time in the animation while loop below
    frames_per_second = 10 + 10*speed_factor
    clock = pygame.time.Clock()
    # Set up the animation     
    pygame.init()
    screen = pygame.display.set_mode(screen_size)
    # Titles and Instructions
    caption = f'Bouncing Ball with Two Balls with gravity factor {-gravity},'
    caption += '                   '
    caption += '(Keystroke:  \'Space\' to start or pause, \'ArrowUp/ArrowDown\' to speed up/down)'
    caption += '                   '
    pygame.display.set_caption(f'{caption} speed = {frames_per_second}')
    # Load the image
    ball_fig = pygame.image.load("intro_ball.gif")
    ball_fig = pygame.transform.scale(ball_fig, (ball.size, ball.size))
    # Assign an pygame.Rect object to the ball
    ball_rect = pygame.Rect(x0,y0,ball.size,ball.size)
    # Initalize the Screen
    screen.fill(white)
    screen.blit(ball_fig, ball_rect)
    pygame.display.flip()
    # Variable to detect change
    keep_running = True
    move_ball = False
    # Animation loop 
    while keep_running:
        # If a keyboard event happens register it... 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keep_running = False
            # Start/Stop Animation
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                move_ball = not move_ball
            # Speed change if ArrowUp/ArrowDown is pressed
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                frames_per_second = (4/3)* frames_per_second
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                frames_per_second = 0.75 * frames_per_second
            # Re-initiate caption to display change
            pygame.display.set_caption(f'{caption} speed = {frames_per_second}')
        if move_ball:
            # Move the ball a step under gravity
            ball.y_step += g/(frames_per_second)
            ball_rect.x += ball.x_step
            ball_rect.y += ball.y_step
            if ball_rect.left < 0 or ball_rect.right > screen_width:
                ball.x_step = - ball.x_step
            if ball_rect.top < 0 or ball_rect.bottom > screen_height:
                ball.y_step = - ball.y_step
        # Redraw and update the screen
        screen.fill(white)
        screen.blit(ball_fig, ball_rect)
        pygame.display.flip()
        clock.tick(frames_per_second)
    pygame.quit()
    return None 
def bouncing_ball_two(ball1, ball2, speed_factor=5,gravity=9.81):
    '''
    Play an animation similar to bouncing_ball with two balls with elastic collision between the balls.
    The input (and code, actually) are similar with an extra parameter ball2 in the Class Ball.
    '''
    # Required variables, x0, y0 is the starting coordinate of the ball
    screen_size = (screen_width, screen_height) = (1080, 800)
    white = (255,255,255)
    x0, y0 = (screen_width - ball1.size)*ball1.x, (screen_height - ball1.size)*ball1.y
    x1, y1 = (screen_width - ball1.size)*ball2.x, (screen_height - ball2.size)*ball2.y
    g = -gravity
    # Used for the pause time in the animation while loop below
    frames_per_second = 10 + 10*speed_factor
    clock = pygame.time.Clock()
    # Set up the animation     
    pygame.init()
    screen = pygame.display.set_mode(screen_size)
    # Titles and Instructions
    caption = f'Bouncing Ball with Two Balls with gravity factor {-gravity}'
    caption += '                              '
    caption += '(Keystroke:  \'Space\' to start or pause)'
    pygame.display.set_caption(f'{caption} speed = {frames_per_second}')
    # Load the image and rescale
    ball1_fig = pygame.image.load("intro_ball1.gif")
    ball1_fig = pygame.transform.scale(ball1_fig, (ball1.size, ball1.size))
    ball1_rect = pygame.Rect(x0,y0,ball1.size,ball1.size)
    ball2_fig = pygame.image.load("intro_ball2.gif")
    ball2_fig = pygame.transform.scale(ball2_fig, (ball2.size, ball2.size))
    ball2_rect = pygame.Rect(x1,y1,ball2.size,ball2.size)
    # Initalize the Screen
    screen.fill(white)
    screen.blit(ball1_fig, ball1_rect)
    screen.blit(ball2_fig, ball2_rect)
    pygame.display.flip()
    # Variable to detect change
    keep_running = True
    move_ball = False
    # Animation loop 
    while keep_running:
        # Keyboard Event: Quit Button and Space to Start/Stop
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
            pygame.display.set_caption(f'{caption} speed = {frames_per_second}')
        if move_ball:
            ball1.y_step += g/(frames_per_second)
            ball2.y_step += g/(frames_per_second)
            # Move the ball a step and Screen Border Detection
            ball1_rect.x += ball1.x_step
            ball1_rect.y += ball1.y_step
            if ball1_rect.left < 0 or ball1_rect.right > screen_width:
                ball1.x_step = - ball1.x_step
            if ball1_rect.top < 0 or ball1_rect.bottom > screen_height:
                ball1.y_step = - ball1.y_step
            ball2_rect.x += ball2.x_step
            ball2_rect.y += ball2.y_step
            if ball2_rect.left < 0 or ball2_rect.right > screen_width:
                ball2.x_step = - ball2.x_step
            if ball2_rect.top < 0 or ball2_rect.bottom > screen_height:
                ball2.y_step = - ball2.y_step
            # Collision Detection 
            collide = ball1_rect.colliderect(ball2_rect)
            if collide:
                # If they collide, the velocity of the two balls exchange
                copy_ball1 = ball1
                ball1 = Ball(ball2.x, ball2.y, ball2.x_step, ball2.y_step)
                ball2 = Ball(copy_ball1.x, copy_ball1.y, copy_ball1.x_step , copy_ball1.y_step) 
        # Redraw and reinitiate              
        screen.fill(white)
        screen.blit(ball1_fig, ball1_rect)
        screen.blit(ball2_fig, ball2_rect)
        pygame.display.flip()
        clock.tick(frames_per_second)
    pygame.quit()
    return None 

def run_bouncing_ball():
    '''
    Interactively let the user choose which version of the animation is to be used.
    '''
    # Setting defaults and limits
    min_pos, max_pos = 0, 1
    min_vel, max_vel = -20, 20
    default_speed = 5
    default_r1 = 5
    default_theta1 = -2
    default_r2 = -8
    default_theta2 = 5
    default_position1 = 0.5
    default_position2 = 0.2
    default_gravity = 9.81
    # Get the parameters from the user. 
    x_pos = float_input_validation('initial x position', default_position1, min_pos, max_pos)
    y_pos = float_input_validation('initial y position', default_position2, min_pos, max_pos)
    x_step = float_input_validation('initial x velocity', default_r1, min_vel, max_vel)
    y_step = float_input_validation('initial y velocity', default_theta1, min_vel, max_vel)
    speed = float_input_validation('speed factor', default_speed, 0, 10)
    gravity = float_input_validation("gravity (if you do not want gravity, enter 0)", default_gravity,0, 20)
    test_ball = Ball(x_pos, y_pos,x_step, y_step)
    # Prompt the user whether an extra ball is needed
    extra_ball = input("Do you want an extra ball? Enter 'y' if you need one, 'n' otherwise. ")
    if extra_ball == 'y':
        # Parameters of the extra ball, again from the user.
        print('Please provide information about the extra ball...')
        x_pos2 = float_input_validation('initial x position', default_position2, min_pos, max_pos)
        y_pos2 = float_input_validation('initial y position', default_position1, min_pos, max_pos)
        x_step2 = float_input_validation('initial x velocity', default_r2, min_vel, max_vel)
        y_step2 = float_input_validation('initial y velocity', default_theta2, min_vel, max_vel)
        test_ball2 = Ball(x_pos2, y_pos2,x_step2, y_step2)
        bouncing_ball_two(test_ball, test_ball2, speed, gravity)
    elif extra_ball == 'n':
        print('Running with 1 ball!')
        bouncing_ball_ext(test_ball,speed, gravity)
    else:
        print('Invalid input! Running with 1 ball!')
        bouncing_ball_ext(test_ball,speed, gravity)
    return None