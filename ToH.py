import pygame, os, timeit
import numpy as np
import matplotlib.pyplot as plt
from useful_func import integer_input_validation, float_input_validation
class Move(object):
    """
    The class Move as introduced in the document. 
    We interpret this as a move in the towers of Hanoi.
    The key attribute of this class is Move.disk and Move.Direction, as introduced.
    """
    def __init__(self, dn=0, dir_n='Left'):
        self.disk = dn
        self.direction = dir_n
    # The Disk Number - Validation 
    def get_disk(self):
        return self._disk
    def set_disk(self, dn):
        error_message_disk = "The Disk is a Positive Integer"
        if not isinstance(dn, int):
            raise TypeError(error_message_disk)
        elif dn < 0:
            raise TypeError(error_message_disk)
        else:
            self._disk= dn
    disk = property(get_disk, set_disk)
    # The Move Direction -  Validation 
    def get_direction(self):
        return self._direction
    def set_direction(self, dir_n):
        error_messagge_direction = "The Direction is either the string 'Left' or 'Right'"
        if not isinstance(dir_n, str):
            raise TypeError(error_messagge_direction)
        elif dir_n != 'Left' and dir_n != 'Right':
            raise TypeError(error_messagge_direction)
        else:
            self._direction = dir_n
    direction = property(get_direction, set_direction)
    # Print out the move using __str__ method
    def __str__ (self):
        return f"Move disk {self.disk} to the {self.direction}"
    # Define the Equality of a Move
    def __eq__(self, other):
        if not isinstance(other, Move):
            return NotImplemented
        return self.disk == other.disk and self.direction == other.direction
ToH_Basic_Dict = {(1, 'Left'): [Move(1, 'Left')], (1, 'Right'): [Move(1, 'Right')]}
def ToH_Move_Left(n):
    """
    Given input n, produce the solution for the Classical Tower of Hanoi Problem
    """
    global ToH_Basic_Dict
    if (n, 'Left') not in ToH_Basic_Dict:
        MiddleMove = Move(n, 'Left')
        ToH_Basic_Dict[(n, 'Left')] = ToH_Move_Right(n-1) + [MiddleMove] + ToH_Move_Right(n-1)
    return ToH_Basic_Dict[(n, 'Left')]
def ToH_Move_Right(n):
    """
    A Supplmentary function to aid recursive call in ToH_Move_Left(n).
    """
    global ToH_Basic_Dict
    if (n, 'Right') not in ToH_Basic_Dict:
        MiddleMove = Move(n, 'Right')
        ToH_Basic_Dict[(n, 'Right')] = ToH_Move_Left(n-1) + [MiddleMove] + ToH_Move_Left(n-1)
    return ToH_Basic_Dict[(n, 'Right')]
ToH_NoWrap_Dict = {
    (1, 'Left'): [Move(1, 'Right'), Move(1, 'Right')],
    (1, 'Right'): [Move(1, 'Left'), Move(1, 'Left')]
    }
# Left: A -> C, Right C -> A
def ToH_NoWrap_Move_Left(n):
    """
    Given input n, produce the solution for the No Wrap Variant.
    """
    global ToH_NoWrap_Dict
    if (n, 'Left') not in ToH_NoWrap_Dict:
        MiddleMove = Move(n, 'Right')
        ToH_NoWrap_Dict[(n, 'Left')] = ToH_NoWrap_Move_Left(n-1) + [MiddleMove] +\
             ToH_NoWrap_Move_Right(n-1) + [MiddleMove] +\
                  ToH_NoWrap_Move_Left(n-1)
    return ToH_NoWrap_Dict [(n, 'Left')]
        
def ToH_NoWrap_Move_Right(n):
    """
    A Supplmentary function to aid recursive call in ToH_NoWrap_Move_Left(n).
    """
    global ToH_NoWrap_Dict
    if (n, 'Right') not in ToH_NoWrap_Dict:
        MiddleMove = Move(n, 'Left')
        ToH_NoWrap_Dict[(n, 'Right')] = ToH_NoWrap_Move_Right(n-1) + [MiddleMove]  +\
    ToH_NoWrap_Move_Left(n-1) + [MiddleMove] +  ToH_NoWrap_Move_Right(n-1)
    return ToH_NoWrap_Dict [(n, 'Right')]
def rev_list(l):
    """
    Given a List l, return the reverse list of l.
    """
    ans = []
    for ele in reversed(l):
        ans += [ele]
    return ans

ToH_Center_Dict = {
    1: [Move(1, 'Right')],
    2: [Move(2, 'Left'), Move(1, 'Right')]
}
def ToH_To_Center(n):
    """
    A Supplmentary function to aid recursive call in ToH_BiColor_Solve(n).
    """
    global ToH_Center_Dict
    # For inducitve case, we know about To Center n-2 and n-1
    if n not in ToH_Center_Dict:
        if n % 2 == 0: # Even number, deal with the last two:
            MiddleMove = Move(n, 'Left')
            ToH_Center_Dict[n]  = ToH_To_Center(n-2) + ToH_Move_Left(n-2) + [MiddleMove] +ToH_Move_Right(n-1)
        else: #Odd number 
            MiddleMove = Move(n, 'Right')
            ToH_Center_Dict[n] = ToH_To_Center(n-1) + ToH_Move_Right(n-1) + [MiddleMove] +ToH_Move_Left(n-1)
    return ToH_Center_Dict[n]
ToH_BiColor_Dict = {
    2: [Move(2, 'Left'), Move(1, 'Left'), Move(2, 'Left')]
}
def ToH_Bicolor_Solve(n):
    """
    Given input n, produce the solution for the Bicolor Variant.
    """
    global ToH_BiColor_Dict
    even_error = 'n must be an even number!'
    if n % 2 != 0:
        print(even_error)
    elif n not in ToH_BiColor_Dict:
        MiddleMove = Move(n, 'Right')
        FirstMove = ToH_To_Center(n-1)
        ToH_BiColor_Dict[n] = FirstMove + [MiddleMove] + rev_list(FirstMove)
    return ToH_BiColor_Dict[n]
def ToH_Valid_Move(m, config, WrapAround = True, Verbose = False):
    """
    Input: 
        - m (Move), 
        - config (A configuration)
    Optional Arguments: 
        - WrapAround (bool) - Whether Wrap Around is allowed
        - Verbose (bool) - Whether error messages are printed out
    Return:
        - If m is a valid move of config, return The configuration attained by m on config
        - Otherwise, return config.
    """
    # Initialize the variable count and tar
    count = 2
    tar = 2
    ValidMove = False
    # Extract information of the move
    dn = m.disk
    dir_n = m.direction
    # Assign direction number to the move
    if dir_n == 'Right':
        dir_num = 1
    else:
        dir_num = -1
    # Detect the target disk, and determine which peg to move from (count) and which peg to move to (tar)
    for count, peg in enumerate(config):
        if len(peg) != 0 and peg[0] == dn:
            if Verbose: print(f'Disk {dn} detected at peg {count +1}! Moving to the {dir_n}')
            trial = count + dir_num
            if WrapAround:
                ValidMove = True
                tar = trial % 3
                break
            elif trial in [0, 1, 2]:
                ValidMove = True
                tar = trial
                break
        else:
            if Verbose: print(f"Can't detect disk {dn} at the top!")
    # Try to move the disk 
    try:
        if ValidMove:
            if config[tar] and dn >= config[tar][0]:
                raise TypeError
            else:
                config[count].pop(0)
                config[tar].insert(0,dn)
        else:  
            print('Invalid move! Returning Original configuration.')
    except: 
        if Verbose: print('Invalid move! Returning Original configuration.')
    return [config[0], config[1], config[2]]
def ToH_ConList_Display(n):
    """
    Given number of disks n,
    Print out the configuration list under a solution for the classical variant And return None
    """
    A = list(range(1, n+1))
    B = []
    C = []   
    TOW = [A, B, C]
    MoveList = ToH_Move_Left(n)
    print("Let's Start! Our Tower looks like:")
    print(str(TOW))
    for step_num, move in enumerate(MoveList):
        print(f'Step {step_num+1}: {move}')
        print(ToH_Valid_Move(move, TOW))
    return None
def ToH_NoWrap_ConList_Display(n):
    """
    Given number of disks n,
    Print out the configuration list under a solution for the No Wrap variant.
    """
    A = list(range(1, n+1))
    B = []
    C = []   
    TOW = [A, B, C]
    MoveList = ToH_NoWrap_Move_Left(n)
    print("Let's Start! Our Tower looks like:")
    print(str(TOW))
    for step_num, move in enumerate(MoveList):
        print(f'Step {step_num+1}: {move}')
        print(ToH_Valid_Move(move, TOW))
    return None
def ToH_BiColor_ConList_Display(n):
    """
    Given number of disks n,
    Print out the configuration list under a solution for the bicolor variant.
    """
    A = list(range(1, n+1, 2))
    B = []
    C = list(range(2, n+1, 2))  
    TOW = [A, B, C]
    MoveList = ToH_Bicolor_Solve(n)
    print("Let's Start! Our Tower looks like:")
    print(str(TOW))
    for step_num, move in enumerate(MoveList):
        print(f'Step {step_num+1}: {move}')
        print(ToH_Valid_Move(move, TOW))
    return None
def ToH_interactive():
    '''
    Allows an user to play the 3 different variants of the puzzle interactively.
    '''
    def ToH_Finish_Checker(Tow, Sol, Wrap = True):
        '''
        The main interactive element of the function.
        Inputs:
        Tow - Initial configuration 
        Sol - Objective Configuration
        Wrap - Whether wrap-around is allowed
        Exit the function call only if the user enters a move sequence that produces a solution.
        '''
        print('We start with the Configuration:')
        print(Tow)
        while Tow != Sol:
            dn = input('What will be the Disk you want to move? Please enter a positive integer: ')
            dir_n = input("What will be the direction? Please enter 'Left' or 'Right' without the quotes: ")
            trial_move = Move(int(dn), dir_n)
            ans = ToH_Valid_Move(trial_move, Tow, Wrap, Verbose = True)
            print(f'Now the Tower is: {ans}')
        print('You got to the solution! Well done.')
        return None
    GameEnd = False
    while not GameEnd:
        # Prompt User to choose a Mode 
        Mode = input('Which variant? c - classical, n - nowrap, b - bicolor, q- quit')
        try:
            # For each mode, initiate the correct initial and objective configuration, and run ToH_Finish_Checker.
            if Mode == 'c':
                n = input('start with how many disk? ')
                Init_config = [list(range(1, int(n)+1)), list(), list()]
                Obj_config = [list(), list(), list(range(1, int(n)+1))]
                ToH_Finish_Checker(Init_config, Obj_config)
                GameEnd = True
            elif Mode == 'n':
                n = input('start with how many disk? ')
                Init_config = [list(range(1, int(n)+1)), list(), list()]
                Obj_config = [list(), list(), list(range(1, int(n)+1))]
                ToH_Finish_Checker(Init_config, Obj_config, False)
                GameEnd = True
            elif Mode == 'b':
                n = input('start with how many disk? ')
                if int(n) % 2 != 0:
                    print('n must be an even number!')
                    GameEnd = True
                    break
                Init_config = [list(range(1, int(n)+1, 2)), list(), list(range(2, int(n)+1, 2))]
                Obj_config = [list(range(2, int(n)+1, 2)), list(), list(range(1, int(n)+1, 2))]
                ToH_Finish_Checker(Init_config, Obj_config)
                GameEnd = True
            elif Mode == 'q':
                print('Quitting! Bye.')
                GameEnd = True
            else:
                raise TypeError
        except:
            print('Invalid input!')
def ToH_Draw_Background():
    """
    Draws the background of the Tower of Hanoi and keep it in the file ToH_BG.jpg.
    """
    screen_size = (1000, 600)
    black = (0, 0, 0)
    white = (255, 255, 255)
    grey = (100, 100, 100)
    pygame.init()
    screen = pygame.Surface(screen_size)
    screen.fill(white)
    base_rect = pygame.Rect(100,450,800,100)
    Peg1Start = (250, 150)
    Peg1End = (250, 450)
    Peg2Start = (500, 150)
    Peg2End = (500, 450)
    Peg3Start = (750, 150)
    Peg3End = (750, 450)
    pygame.draw.rect(screen, grey, base_rect)
    pygame.draw.line(screen, black, Peg1Start, Peg1End, width = 5)
    pygame.draw.line(screen, black, Peg2Start, Peg2End, width = 5)
    pygame.draw.line(screen, black, Peg3Start, Peg3End, width = 5) 
    pygame.image.save(screen, 'ToH_BG.jpg')
    return None
def ToH_Get_Coordinate(config):
    '''
    Given a configuration, return a list of coordinates where the disks are to be plotted.
    (TOP LEFT coordinate of a rectangle, each assume with width 15)
    '''
    ans = list()
    get_disk_length = lambda d_n: 10 * d_n
    for peg_num, peg in enumerate(config):
        base_x_coord = 250 * (peg_num+1)
        total_num_disk = len(peg)
        for count, disk_num in enumerate(peg):
            y_coord = 450 - (15*(total_num_disk - count))
            x_coord = base_x_coord-get_disk_length(disk_num)
            ans.append((x_coord, y_coord, disk_num))
    return ans
def ToH_Basic(n, speed_factor):
    """
    Inputs: 
    - Number of Disks n 
    - The frame speed factor speed_factor
    Return: None
    Plays the animation of solving the Classic Variant of Tower of Hanoi.
    """
    # Basic initialization
    screen_size = (screen_width, screen_height)  = (1000, 600)
    white = (255,255,255)
    blue = (0, 0, 255)
    black = (0, 0, 0)
    frames_per_second = speed_factor
    clock = pygame.time.Clock()
    pygame.init()
    screen = pygame.display.set_mode(screen_size)
    # Draw the background
    bg = pygame.image.load("ToH_BG.jpg")
    bg_rect = pygame.Rect(0,0,screen_width,screen_height)
    # Draw the disks
    get_double_disk_length = lambda d_n: 20 * d_n
    Sol_Classic_Hanoi = ToH_Move_Left(n)
    len_move_list = len(Sol_Classic_Hanoi)
    Initial_Configuration = [list(range(1, n+1)), list(), list()]
    Current_Configuration = Initial_Configuration
    Start_Coord_List = ToH_Get_Coordinate(Initial_Configuration)
    for x_cor, y_cor, disk in Start_Coord_List:
        disk_rect = pygame.Rect(x_cor, y_cor, get_double_disk_length(disk), 15)
        pygame.draw.rect(bg, blue, disk_rect)
        pygame.draw.rect(bg, black, disk_rect, width = 3)
    # Initialization of animation
    # Index_move will track through the solution for the puzzle
    index_move = 0
    screen.fill(white)
    screen.blit(bg, bg_rect)
    pygame.display.flip()
    running = True
    run_anim = False
    # Main Loop
    while running:
        # Key Press Detecting
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                run_anim = not run_anim 
            # Speed change if ArrowUp/ArrowDown is pressed
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                frames_per_second = (4/3)* frames_per_second
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                frames_per_second = 0.75 * frames_per_second
            # Title bar
            caption = 'Tower of Hanoi - Classical Variant'
            caption += f' Speed = {int(frames_per_second)}             '
            caption += '(Keystroke:  \'Space\' to start or pause, Up/Down for speed adjusting))'
            pygame.display.set_caption(caption)
        if run_anim and index_move < len_move_list:
            screen.fill(white)
            # Background has changed, update it again
            bg = pygame.image.load("ToH_BG.jpg")
            # Extract Current Configuration
            current_move = Sol_Classic_Hanoi[index_move]
            Current_Configuration = ToH_Valid_Move(current_move,Current_Configuration)
            # Print Information
            my_font = pygame.font.SysFont('Comic Sans MS', 30)
            text_surface = my_font.render(f'Move {index_move+1}/{len_move_list}: {current_move}', False, (255, 0, 0))
            bg.blit(text_surface, (0, 0))
            # Update iterator
            index_move = (index_move + 1) 
            ans = ToH_Get_Coordinate(Current_Configuration)
            # Draw the new disks
            for x_cor, y_cor, disk in ans:
                disk_rect = pygame.Rect(x_cor, y_cor, get_double_disk_length(disk), 15)
                pygame.draw.rect(bg, blue, disk_rect)
                pygame.draw.rect(bg, black, disk_rect, width = 3)         
        # Re-initialise the display 
        screen.blit(bg, (15, 0))
        pygame.display.flip()
        screen.fill(white)
        clock.tick(frames_per_second) 
    pygame.quit()
    return None 
def ToH_NoWrap(n, speed_factor):
    """
    Plays the animation of solving the No Wrap Variant of Tower of Hanoi.
    Inputs: 
    - Number of Disks n 
    - The frame speed factor speed_factor
    """
    # Basic initialization
    screen_size = (screen_width, screen_height)  = (1000, 600)
    white = (255,255,255)
    blue = (0, 0, 255)
    black = (0, 0, 0)
    frames_per_second = speed_factor
    clock = pygame.time.Clock()
    pygame.init()
    screen = pygame.display.set_mode(screen_size)

    # Draw the background
    bg = pygame.image.load("ToH_BG.jpg")
    bg_rect = pygame.Rect(0,0,screen_width,screen_height)
    # Draw the disks
    get_double_disk_length = lambda d_n: 20 * d_n
    Sol_NoWrap_Hanoi = ToH_NoWrap_Move_Left(n)
    len_move_list = len(Sol_NoWrap_Hanoi)
    Initial_Configuration = [list(range(1, n+1)), list(), list()]
    Current_Configuration = Initial_Configuration
    Start_Coord_List = ToH_Get_Coordinate(Initial_Configuration)
    for x_cor, y_cor, disk in Start_Coord_List:
        disk_rect = pygame.Rect(x_cor, y_cor, get_double_disk_length(disk), 15)
        pygame.draw.rect(bg, blue, disk_rect)
        pygame.draw.rect(bg, black, disk_rect, width = 3)
    # Initialization of animation
    # Index_move will track through the solution for the puzzle
    index_move = 0
    screen.fill(white)
    screen.blit(bg, bg_rect)
    pygame.display.flip()
    running = True
    run_anim = False
    # Main Loop - Stop animating when the end of move list is reached
    while running:
        # Key Press Detecting
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                run_anim = not run_anim 
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                frames_per_second = (4/3)* frames_per_second
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                frames_per_second = 0.75 * frames_per_second
            # Title bar
            caption = 'Tower of Hanoi - No Wrapping Variant'
            caption += f' Speed = {int(frames_per_second)}             '
            caption += '(Keystroke:  \'Space\' to start or pause, Up/Down for speed adjusting))'
            pygame.display.set_caption(caption)
        if run_anim and index_move < len_move_list:
            screen.fill(white)
            # Background has changed, update it again
            bg = pygame.image.load("ToH_BG.jpg")
            # Extract Current Configuration
            current_move = Sol_NoWrap_Hanoi[index_move]
            Current_Configuration = ToH_Valid_Move(current_move,Current_Configuration, False)
            # Print Information
            my_font = pygame.font.SysFont('Comic Sans MS', 30)
            text_surface = my_font.render(f'Move {index_move+1}/{len_move_list}: {current_move}', False, (255, 0, 0))
            bg.blit(text_surface, (0, 0))
            # Update iterator
            index_move = index_move + 1
            ans = ToH_Get_Coordinate(Current_Configuration)
            # Draw the new disks
            for x_cor, y_cor, disk in ans:
                disk_rect = pygame.Rect(x_cor, y_cor, get_double_disk_length(disk), 15)
                pygame.draw.rect(bg, blue, disk_rect)
                pygame.draw.rect(bg, black, disk_rect, width = 3)
        # Re-initialise the display 
        screen.blit(bg, (15, 0))
        pygame.display.flip()
        clock.tick(frames_per_second)
    pygame.quit()
    return None 
def ToH_BiColor(n, speed_factor):
    """
    Inputs: 
    - Number of Disks n 
    - The frame speed factor speed_factor
    Plays the animation of solving the Bicolor Variant of Tower of Hanoi.
    """
    # Basic initialization
    screen_size = (screen_width, screen_height)  = (1000, 600)
    white = (255,255,255)
    red = (255, 0, 0)
    green = (0, 255, 0)
    black = (0, 0, 0)
    frames_per_second = speed_factor
    clock = pygame.time.Clock()
    pygame.init()
    screen = pygame.display.set_mode(screen_size)
    # Title bar
    caption = 'Tower of Hanoi - Bicolor Variant'
    caption += '                              '
    caption += '(Keystroke:  \'Space\' to start or pause)'
    pygame.display.set_caption(caption)
    # Draw the background
    bg = pygame.image.load("ToH_BG.jpg")
    bg_rect = pygame.Rect(0,0,screen_width,screen_height)
    # Draw the disks
    get_double_disk_length = lambda d_n: 20 * d_n
    Sol_BiColor_Hanoi = ToH_Bicolor_Solve(n)
    len_move_list = len(Sol_BiColor_Hanoi)
    Initial_Configuration = [list(range(1, n+1, 2)), list(), list(range(2, n+1, 2))]
    Current_Configuration = Initial_Configuration
    Start_Coord_List = ToH_Get_Coordinate(Initial_Configuration)
    for x_cor, y_cor, disk in Start_Coord_List:
        disk_rect = pygame.Rect(x_cor, y_cor, get_double_disk_length(disk), 15)
        if disk % 2 ==0:
            pygame.draw.rect(bg, green, disk_rect)
        else:
            pygame.draw.rect(bg, red, disk_rect)
        pygame.draw.rect(bg, black, disk_rect, width = 3)
    # Initialization of animation
    # Index_move will track through the solution for the puzzle
    index_move = 0
    screen.fill(white)
    screen.blit(bg, bg_rect)
    pygame.display.flip()
    running = True
    run_anim = False
    # Main Loop 
    while running :
        # Key Press Detecting
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                run_anim = not run_anim 
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                frames_per_second = (4/3)* frames_per_second
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                frames_per_second = 0.75 * frames_per_second
            # Title bar
            caption = 'Tower of Hanoi - Classical Variant'
            caption += f' Speed = {int(frames_per_second)}             '
            caption += '(Keystroke:  \'Space\' to start or pause, Up/Down for speed adjusting))'
            pygame.display.set_caption(caption)
        # Stop animating when the end of move list is reached
        if run_anim and index_move < len_move_list:
            screen.fill(white)
            # Background has changed, update it again
            bg = pygame.image.load("ToH_BG.jpg")
            # Extract Current Configuration
            current_move = Sol_BiColor_Hanoi[index_move]
            Current_Configuration = ToH_Valid_Move(current_move,Current_Configuration)
            # Print Information
            my_font = pygame.font.SysFont('Comic Sans MS', 30)
            text_surface = my_font.render(f'Move {index_move+1}/{len_move_list}: {current_move}', False, (255, 0, 0))
            bg.blit(text_surface, (0, 0))
            # Update iterator
            index_move = (index_move + 1)
            ans = ToH_Get_Coordinate(Current_Configuration)
            # Draw the new disks
            for x_cor, y_cor, disk in ans:
                disk_rect = pygame.Rect(x_cor, y_cor, get_double_disk_length(disk), 15)
                if disk % 2 ==0:
                    pygame.draw.rect(bg, green, disk_rect)
                else:
                    pygame.draw.rect(bg, red, disk_rect)
                pygame.draw.rect(bg, black, disk_rect, width = 3)
        # Re-initialise the display 
        screen.blit(bg, (15, 0))
        pygame.display.flip()
        clock.tick(frames_per_second)
    pygame.quit()
    return None 
def ToH_Animation_Interactive(): 
    Mode = input('Which variant? c - classical, n - nowrap, b - bicolor, q- quit')
    if Mode == 'c':
        ds = integer_input_validation("Number of disks", 5, 1, 16)
        spe = integer_input_validation("Disks moved per second", 5, 1, 20)
        ToH_Basic(ds, spe)
    elif Mode == 'n':
        ds = integer_input_validation("Number of disks", 6, 2, 16)
        spe = integer_input_validation("Disks moved per second", 5, 1, 20)
        ToH_NoWrap(ds, spe)
    elif Mode == 'b':
        ds = integer_input_validation("Number of disks", 5, 1, 16)
        spe = integer_input_validation("Disks moved per second", 5, 1, 20)
        ToH_BiColor(ds, spe)
    elif Mode == 'q':
        print('Quitting! Bye!')
    else:
        print("Cannot recognize your input! So I quit! Please run the function again.")
def ToH_Basic_Smooth(n, speed_factor):
    """
    Inputs: 
    - Number of Disks n 
    - The frame speed factor speed_factor
    Return: None
    Plays the animation of solving the Classic Variant of Tower of Hanoi with animation of disks moving pole to pole.
    """
    x_step = 10
    y_step = 5
    # Basic initialization
    screen_size = (screen_width, screen_height)  = (1000, 600)
    white = (255,255,255)
    blue = (0, 0, 255)
    black = (0, 0, 0)
    frames_per_second = speed_factor
    clock = pygame.time.Clock()
    pygame.init()
    screen = pygame.display.set_mode(screen_size)
    
    # Draw the background
    bg = pygame.image.load("ToH_BG.jpg")
    bg_rect = pygame.Rect(0,0,screen_width,screen_height)
    # Draw the disks
    get_double_disk_length = lambda d_n: 20 * d_n
    Sol_Classic_Hanoi = ToH_Move_Left(n)
    len_move_list = len(Sol_Classic_Hanoi)
    Initial_Configuration = [list(range(1, n+1)), list(), list()]
    Current_Configuration = Initial_Configuration
    Start_Coord_List = ToH_Get_Coordinate(Initial_Configuration)
    ans = ToH_Get_Coordinate(Initial_Configuration)
    # Initialization of smooth disks
    current_disk = 1
    for x_cor, y_cor, disk in Start_Coord_List:
        disk_rect = pygame.Rect(x_cor, y_cor, get_double_disk_length(disk), 15)
        if disk == current_disk:
            moving_disk_rect = disk_rect
        pygame.draw.rect(bg, blue, disk_rect)
        pygame.draw.rect(bg, black, disk_rect, width = 3)
    # Initalization of the first move
    index_move = 0
    current_move = Sol_Classic_Hanoi[index_move]
    current_disk = current_move.disk
    current_direction = current_move.direction
    screen.fill(white)
    screen.blit(bg, bg_rect)
    pygame.display.flip()
    running = True
    run_anim = False
    smooth_disk = True
    number_of_times_moving_x = 0
    my_font = pygame.font.SysFont('Comic Sans MS', 30)
    text_surface = my_font.render(f'Move {index_move+1}: {current_move}', False, (255, 0, 0))
    bg.blit(text_surface, (0, 0))
    # Main Loop
    while running:
        # Key Press Detecting
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                run_anim = not run_anim 
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                frames_per_second = (4/3)* frames_per_second
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                frames_per_second = 0.75 * frames_per_second
            # Title bar
            caption = 'Tower of Hanoi - Classical Variant with Smooth Disks'
            caption += f' Speed = {int(frames_per_second)}             '
            caption += '(Keystroke:  \'Space\' to start/pause, Up/Down for speed adjusting)'
            pygame.display.set_caption(caption)
        if run_anim and index_move < len_move_list:
            # Smooth Transition Parts
            if smooth_disk:
                if number_of_times_moving_x < 25:
                    bg = pygame.image.load("ToH_BG.jpg")
                    move_hori = True
                    if current_direction == 'Left':
                        moving_disk_rect = moving_disk_rect.move((-x_step, 0))
                    else:
                        moving_disk_rect = moving_disk_rect.move((x_step, 0))
                    pygame.draw.rect(bg, blue ,moving_disk_rect)
                    pygame.draw.rect(bg, black ,moving_disk_rect, width = 3)
                    number_of_times_moving_x += 1
                else:
                    number_of_times_moving_x = 0
                    smooth_disk = not smooth_disk
                for x_cor, y_cor, disk in ans:
                    disk_rect = pygame.Rect(x_cor, y_cor, get_double_disk_length(disk), 15)
                    if disk != current_disk:
                        pygame.draw.rect(bg, blue, disk_rect)
                        pygame.draw.rect(bg, black, disk_rect, width = 3)
                my_font = pygame.font.SysFont('Comic Sans MS', 30)
                text_surface = my_font.render(f'Move {index_move+2}: {current_move}', False, (255, 0, 0))
                bg.blit(text_surface, (0, 0))
                clock.tick(frames_per_second)
                pygame.display.flip()
            elif index_move < len_move_list:
                screen.fill(white)
                # Background has changed, update it again
                bg = pygame.image.load("ToH_BG.jpg")
                # Extract Current Configuration
                try:
                    current_move = Sol_Classic_Hanoi[index_move+1]
                except:
                    pass
                current_disk = current_move.disk
                current_direction = current_move.direction
                Current_Configuration = ToH_Valid_Move(Sol_Classic_Hanoi[index_move],Current_Configuration)
                # Print Information
                my_font = pygame.font.SysFont('Comic Sans MS', 30)
                text_surface = my_font.render(f'Move {index_move+2}: {current_move}', False, (255, 0, 0))
                bg.blit(text_surface, (0, 0))
                # Update iterator
                ans = ToH_Get_Coordinate(Current_Configuration)
                # Draw the new disks
                for x_cor, y_cor, disk in ans:
                    disk_rect = pygame.Rect(x_cor, y_cor, get_double_disk_length(disk), 15)
                    if disk == current_disk:
                        moving_disk_rect = disk_rect
                    pygame.draw.rect(bg, blue, disk_rect)
                    pygame.draw.rect(bg, black, disk_rect, width = 3)
                smooth_disk = not smooth_disk
                index_move = (index_move + 1) 
        # Re-initialise the display 
        screen.blit(bg, (0, 0))
        pygame.display.flip()
        clock.tick(frames_per_second)
    pygame.quit()
    return None 
def ToH_Move_Left_Nomem(n):
    """
    The function ToH_Move_Left with no memoization.
    """
    if n == 1:
        return [Move(1, 'Left')]
    else:
        MiddleMove = Move(n, 'Left')
        return ToH_Move_Right_Nomem(n-1) + [MiddleMove] + ToH_Move_Right_Nomem(n-1)
def ToH_Move_Right_Nomem(n):
    """
    The function ToH_Move_Right with no memoization.
    """
    if n == 1:
        return [Move(1, 'Right')]
    else:
        MiddleMove = Move(n, 'Right')
        return ToH_Move_Left_Nomem(n-1) + [MiddleMove] + ToH_Move_Left_Nomem(n-1)
def ToH_NoWrap_Move_Left_Nomem(n):
    """
    The function ToH_NoWrap_Move_Left with no memoization.
    """
    if n == 1:
        return [Move(1, 'Right'), Move(1, 'Right')]
    else:
        MiddleMove = Move(n, 'Right')
        return ToH_NoWrap_Move_Left_Nomem(n-1) + [MiddleMove] + \
    ToH_NoWrap_Move_Right_Nomem(n-1) + [MiddleMove] + \
    ToH_NoWrap_Move_Left_Nomem(n-1)
def ToH_NoWrap_Move_Right_Nomem(n):
    """
    The function ToH_NoWrap_Move_Right with no memoization.
    """
    if n == 1:
        return [Move(1, 'Left'), Move(1, 'Left')]
    else:
        MiddleMove = Move(n, 'Left')
        return ToH_NoWrap_Move_Right_Nomem(n-1) + [MiddleMove]  +\
    ToH_NoWrap_Move_Left_Nomem(n-1) + [MiddleMove] +  ToH_NoWrap_Move_Right_Nomem(n-1)
def ToH_To_Center_Nomem(n):
    """
    The function ToH_To_Center with no memoization.
    """
    if n == 1:
        return [Move(1, 'Right')]
    elif n ==2:
        return [Move(2, 'Left'), Move(1, 'Right')]
    elif n % 2 == 0: 
        MiddleMove = Move(n, 'Left')
        return ToH_To_Center_Nomem(n-2) + ToH_Move_Left_Nomem(n-2) + [MiddleMove] +ToH_Move_Right_Nomem(n-1)
    else: 
        MiddleMove = Move(n, 'Right')
        return ToH_To_Center_Nomem(n-1) + ToH_Move_Right_Nomem(n-1) + [MiddleMove] +ToH_Move_Left_Nomem(n-1)
def ToH_Bicolor_Solve_Nomem(n):
    """
    The function ToH_BiColor_Solve with no memoization.
    """
    even_error = 'n must be an even number!'
    if n % 2 != 0:
        print(even_error)
    elif n == 2:
        return [Move(2, 'Left'), Move(1, 'Left'), Move(2, 'Left')]
    else:
        MiddleMove = Move(n, 'Right')
        CenterMove = ToH_To_Center_Nomem(n-1)
        return CenterMove + [MiddleMove] + rev_list(CenterMove)