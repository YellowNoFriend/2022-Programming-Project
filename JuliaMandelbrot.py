import pygame, os, timeit
import numpy as np
import matplotlib.pyplot as plt
from useful_func import integer_input_validation, float_input_validation

def julia(j_p, c, max_n):
    '''
    Calculates the largest number n_max for which each 
    term z_n of the corresponding Julia sequence
    with parameter j_p induced by c is bounded by 2. 
    
    Inputs: j_p, c - as in the definition of the julia set.
    max_n - Maximum Number of iterationns
    '''
    z = c
    n_max = 0
    # Iterate until term is not bounded by 2.
    while abs(z) <= 2:
        z = (z ** 2) + j_p
        n_max += 1
        # Break the loop early when the largest number n_max reaches 
        # the maximum number of iterations max_n.
        if n_max == max_n:
            break
    return n_max
def julia_data(j_p, max_n, c_min, c_max, c_intervals):
    '''
    Calculates the matrices required for graphing the julia function.

    Input:
    j_p, max_n - as with the function julia
    c_min, c_max, c_intervals - used to creative an array of c to consider 
    whether they belong in the Filled in Julia set
    '''
    # Calculate the vectors required for the two matrices required for input.
    x_vector = np.linspace(c_min, c_max, c_intervals)
    y_vector = np.linspace(c_min, c_max, c_intervals)
    x_matrix, y_matrix = np.meshgrid(x_vector, y_vector)
    # Create a zero output matrix with the same dimensions as the input matrices.
    z_rows, z_cols = np.shape(x_matrix)
    z_matrix = np.zeros((z_rows, z_cols), dtype = int)
    # Calculate every element of the output matrix for every 
    # element in the input matrix using the julia function.
    for i in range(c_intervals):
        for j in range(c_intervals):
            c = x_matrix[i, j] + y_matrix[i, j] * 1j
            z_matrix[i, j] = julia(j_p, c, max_n)
    return x_matrix, y_matrix, z_matrix
def julia_graphpic(j_p, max_n, c_min, c_max, c_intervals, 
plt_width, plt_height, filename):
    '''
    Exports a Julia graph as a picture with default resuloutions.
    Inputs: 
    j_p, max_n, c_min, c_max, c_intervals - as with julia_data.
    plt_width, plt_height - Default resolution of the figure (integers)
    filename - a string used to be the filename of the exported png file
    '''
    # Calculate the two input matrices and one output matrix using the julia_data function.
    x_matrix, y_matrix, z_matrix = julia_data(j_p, max_n, c_min, c_max, c_intervals)
    # Produce a Julia graph from the given matrices without the axes.
    plt.figure(figsize = (plt_width, plt_height))
    plt.pcolor(x_matrix, y_matrix, z_matrix, cmap = 'plasma', vmin = 0, vmax = max_n, shading = "auto")
    plt.axis("off")
    # Create a filepath directory string and export  
    # the aforementioned Julia graph into the filepath directory.
    currwd = os.getcwd()
    filepath = str(currwd) + "//JULIA_GRAPHS//{}.png".format(filename)
    plt.savefig(filepath, dpi = "figure", format = "png", bbox_inches = "tight", pad_inches = 0)
    # To avoid too much memory being used up, close the active pyplot window.
    plt.close()
    return None
def julia_export(r, max_n, c_min, c_max, c_intervals, 
plt_width, plt_height, n_img, verbose = False):
    '''
    Exports n_img number of images for 
    a Julia set with parameter j_p = re^{ai} where a is chosen
    at n_img equally spaced intervals between [0, 2*pi]

    Inputs: 
    r - The r in re^{ai}
    max_n, c_min, c_max, c_intervals, plt_width, plt_height- as with julia_graphpic.
    n_img - number of different a considered in re^{ai}.
    '''
    n_intervals = np.pi*2 / (n_img - 1)
    for i in range(n_img):
        # Calculate a in between the intervals and calculate j_p.
        a = (i * n_intervals)
        j_p = r * np.exp(a * 1j)
        # Export an image of each Julia set.
        filename = "JuliaPic{}".format(i + 1)
        julia_graphpic(j_p, max_n, c_min, c_max, c_intervals, plt_width, plt_height, filename)
        # If verbose is True, output the current progress line as an addendum.
        if verbose:
            print("Please wait while the images are being exported. {}% of all the images has now been exported.".format(int((i + 1) / n_img * 100)), end = "\r")
    return None
def julia_animation(folder_name, r = 0.7885, max_n = 100, c_min = -2, c_max = 2, 
c_intervals = 200, plt_width = 14, plt_height = 12, n_img = 200,
 screen_w = 800, screen_h = 600, verbose = True, runfile = True):
    '''
    Creates a PyGame animation with
    slides of images of the Julia graph with parameter j_p = re^{ai}, 
    where a is n_img - 1 equally spaced intervals between 0 and 2pi.
    The animation has a resolution width of screen_w pixels and height of
    screen_h pixels.
    '''
    if runfile:
        try:
            # If runfile is True, always export the figure to directory/JULIA_GRAPHS
            folder_name = 'JULIA_GRAPHS'
            julia_export(r, max_n, c_min, c_max, c_intervals, plt_width, plt_height, n_img, verbose)
            if verbose:
                print("\nAll the images has now been exported. Starting Program...")
        except:
            print("Error producing graphs!")
            return None
    screen_size = (screen_w, screen_h)
    white = (255, 255, 255)
    speed_factor = 1
    clock = pygame.time.Clock()
    # Initialise PyGame.
    pygame.init()
    if verbose:
        print("Program has now initialised!")
    # Set the screen size and the title of the program.
    screen = pygame.display.set_mode(screen_size)
    # Set the path of the Julia image and load the image to the correct size.
    currwd = os.getcwd()
    filename = str(currwd) + "//" + folder_name + "//JuliaPic1.png"
    julia = pygame.image.load(filename)
    julia = pygame.transform.scale(julia, screen_size)
    # Create a rectangle for the image to be loaded in.
    julia_rect = pygame.Rect(0, 0, screen_w, screen_h)
    # Fill the background white and initialise the the image into the program.
    screen.fill(white)
    screen.blit(julia, julia_rect)
    # Refresh the program display.
    pygame.display.flip()
    # Set initial values of variables for later.
    Running = True
    pause = True
    i = 0
    # Main Animation Loop
    while Running:
        # Events and User key press detection
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                pause = not pause
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                speed_factor = 0.75 * speed_factor
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                speed_factor = (4 / 3) * speed_factor
            title = f"Animation of Julia Sets of r = {r}"
            title += f" Current Speed: {int(speed_factor)}"
            title += "(Keystroke:  Space - Stop, Up/Down - Speed)"
            pygame.display.set_caption(title)
        if not pause:
            # Set the timimg between the transition of images.
            fps = 10 * speed_factor
            clock.tick(fps)
            i += 1
            if i == n_img:
                i = 0
            # Load the corresponding Julia Graphs
            currwd = os.getcwd()
            filename = str(currwd) + "//" + folder_name +"//JuliaPic{}.png".format(i + 1)
            julia = pygame.image.load(filename)
            # Resize the loaded Julia graph and update the display.
            julia = pygame.transform.scale(julia, screen_size)
            julia_rect = pygame.Rect(0, 0, screen_w, screen_h)
            screen.fill(white)
            screen.blit(julia, julia_rect)
            pygame.display.flip()
    pygame.quit()
    return None
def mandelbrot(c, max_n):
    '''
    The mandelbrot function calculates the largest term n_max
    for which each term z_n of the corresponding Mandelbrot 
    sequence induced by c is bounded by 2. 
    '''
    z =  0 + 0j
    n_max = 0
    # Iterate until term is not bounded by 2.
    while abs(z) <= 2:
        # Derive the next term of the sequence from the current term.
        z = (z ** 2) + c
        n_max += 1
        if n_max == max_n:
            break
    # Return the value of the largest number n_max.
    return n_max
def mandelbrot_data(max_n, x_min, x_max, n_xpts, y_min, y_max, n_ypts):
    '''
    The mandelbrot_data function calculates the matrices 
    required for graphing the mandelbrot function.
    '''
    # Calculate the vectors required for the two matrices required for input.
    x_vector = np.linspace(x_min, x_max, n_xpts)
    y_vector = np.linspace(y_min, y_max, n_ypts)
    x_matrix, y_matrix = np.meshgrid(x_vector, y_vector)
    # Create a zero output matrix with the same dimensions as the input matrices.
    x_matrix_rows, x_matrix_cols = np.shape(x_matrix)
    z_matrix = np.zeros((x_matrix_rows, x_matrix_cols), dtype = int)
    # Calculate every element of the output matrix for every 
    # element in the input matrix using the mandelbrot function.
    for i in range(x_matrix_rows):
        for j in range(x_matrix_cols):
            c = x_matrix[i, j] + y_matrix[i, j] * 1j
            z_matrix[i, j] = mandelbrot(c, max_n)
    return x_matrix, y_matrix, z_matrix
def mandelbrot_graphpic(max_n, x_min, x_max, n_xpts, y_min, y_max, n_ypts, fig_w, fig_h, filename):
    '''
    The mandelbrot_graphpic function creates a Mandelbrot graph and exports
    the Mandelbrot graph as a picture with default resuloutions.
    
    '''
    # Calculate the two input matrices and one output matrix using the mandelbrot_data function.
    x_matrix, y_matrix, z_matrix = mandelbrot_data(max_n, x_min, x_max, n_xpts, y_min, y_max, n_ypts)
    # Produce a Mandelbrot graph from the given matrices without the axes.
    plt.figure(figsize = (fig_w, fig_h))
    plt.pcolor(x_matrix, y_matrix, z_matrix, cmap = 'plasma', vmin = 0, vmax = max_n, shading = "auto")
    plt.axis("off")
    # Create a filepath directory string and export  
    # the aforementioned Mandelbrot graph into the filepath directory.
    currwd = os.getcwd()
    filepath = str(currwd) + "//MANDELBROT_GRAPHS//{}.png".format(filename)
    plt.savefig(filepath, dpi = "figure", format = "png", bbox_inches = "tight", pad_inches = 0)
    plt.close()
    return None
def mandelbrot_program(max_n = 100, x_min = -2, x_max = 1, n_xpts = 400, 
y_min = -1.5, y_max = 1.5, n_ypts = 400, 
fig_w = 14, fig_h = 12, screen_w = 800, screen_h = 600):
    '''
    The mandelbrot_program function creates a PyGame/SDL program that
    displays a Mandelbrot graph, allowing the user to zoom in and out
    the graph. The animation has a resolution width of screen_w pixels
    and height of screen_h pixels.
    '''
    # Set the minimum width resolution for running the program.
    appcompatresx = 680
    if screen_w < appcompatresx:
        print("The width resolution you have inputted into the function is too small. You need a width resolution of at least {} pixels.".format(appcompatresx))
        return None
    # Try exporting the required images for the program.
    try:
        mandelbrot_graphpic(max_n, x_min, x_max, n_xpts, y_min, y_max, n_ypts, fig_w, fig_h, "MandelbrotPic0")
    except:
        print("Error producing graphs!")
        return None
    # Store the input screen size and the size of the rescaled image as tuples.
    screen_size = (screen_w, screen_h)
    mandelbrot_size = (screen_w, screen_h - 50)
    # Store colours as RGB tuples.
    white = (255, 255, 255)
    black = (0, 0, 0)
    grey = (119, 119, 119)
    green_notactive = (114, 179, 101)
    green_active = (161, 251, 142)
    red = (255, 0, 0)
    orange = (240, 134, 80)
    # Set graph axes limits as lists and add initial values.
    x_min_list = []
    x_max_list = []
    y_min_list = []
    y_max_list = []
    x_min_list.append(x_min)
    x_max_list.append(x_max)
    y_min_list.append(y_min)
    y_max_list.append(y_max)
    # Initialise PyGame and its fonts.
    pygame.init()
    pygame.font.init()
    # Set the screen size and the title of the program.
    screen = pygame.display.set_mode(screen_size)
    title = "Animation of Mandelbrot Sets"
    title += " "
    title += '(Keystroke:  \'Drag and release\' to zoom in if the functionality is enabled.)'
    pygame.display.set_caption(title)
    # Set the path of the Mandelbrot image and load the image to the correct size.
    currwd = os.getcwd()
    filename = str(currwd) + "//MANDELBROT_GRAPHS//MandelbrotPic0.png"
    mandelbrot = pygame.image.load(filename)
    mandelbrot = pygame.transform.scale(mandelbrot, mandelbrot_size)
    # Create and position initial rectangles for Mandelbrot images, drag boxes, and zoom buttons.
    mandelbrot_rect = pygame.Rect(0, 0, mandelbrot_size[0], mandelbrot_size[1])
    cropbox = pygame.Rect(0, 0, 0, 0)
    zoom_in_button_left = screen_size[0] / 2 - 115
    zoom_out_button_left = screen_size[0] - 115
    zoom_button_top = screen_size[1] - 45
    zoom_button_width = 80
    zoom_button_height = 40
    zoom_in_button = pygame.Rect(zoom_in_button_left, zoom_button_top, zoom_button_width, zoom_button_height)
    zoom_out_button = pygame.Rect(zoom_out_button_left, zoom_button_top, zoom_button_width, zoom_button_height)
    # Create Text object and other text messages
    text = pygame.font.SysFont("arial", 14)
    errortext = pygame.font.SysFont("arial", 18)
    text1 = text.render("Click the first button on the right", True, black)
    textbox1 = text1.get_rect()
    textbox_centre_x = zoom_in_button_left / 2
    textbox1_centre_y = screen_size[1] - 35
    textbox1.center = (textbox_centre_x, textbox1_centre_y)
    text2 = text.render("to enable the zoom in function.", True, black)
    textbox2 = text2.get_rect()
    textbox2_centre_y = screen_size[1] - 15
    textbox2.left = textbox1.left
    textbox2.centery = textbox2_centre_y
    text3 = text.render("to disable the zoom in function.", True, black)
    textbox3 = text3.get_rect()
    textbox3.left = textbox1.left
    textbox3.centery = textbox2_centre_y
    text4 = text.render("Click the button on the right to", True, black)
    textbox4 = text4.get_rect()
    textbox4.right = zoom_out_button_left - (zoom_in_button_left - textbox1.right)
    textbox4.centery = textbox1_centre_y
    text5 = text.render("zoom out to the previous image.", True, black)
    textbox5 = text5.get_rect()
    textbox5.left = textbox4.left
    textbox5.centery = textbox2_centre_y
    text6 = text.render("Please wait while", True, black)
    textbox6 = text6.get_rect()
    textbox6.center = textbox4.center
    text7 = text.render("it is zooming out.", True, black)
    textbox7 = text7.get_rect()
    textbox7.left = textbox6.left
    textbox7.centery = textbox5.centery
    # Set initial values of variables for later.    
    running = True
    drag = False
    rect = False
    zoomin_button = False
    zoomin = False
    zoomout_button = False
    zoomout = False
    i = 0
    # If running is set to True, continue the program.
    while running:
        # Obtain the events from system logs.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # If user down clicks the left mouse button, then look for position and check status of buttons.
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if event.pos[1] <= mandelbrot_size[1] and zoomin_button:
                        drag = True
                        mouse_x1_pos = event.pos[0]
                        mouse_y1_pos = event.pos[1]
                    # If the position of the down click is within region of the
                    # buttons, then set or change the activity statuses of the buttons.
                    elif event.pos[0] >= zoom_in_button_left and event.pos[0] <= (zoom_in_button_left + zoom_button_width) and event.pos[1] >= zoom_button_top and event.pos[1] <= (zoom_button_top + zoom_button_height):
                        zoomin_button = not zoomin_button
                    elif event.pos[0] >= zoom_out_button_left and event.pos[0] <= (zoom_out_button_left + zoom_button_width) and event.pos[1] >= zoom_button_top and event.pos[1] <= (zoom_button_top + zoom_button_height):
                        zoomout_button = True
            # If user releases the left click button, then set variables where necessary.      
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drag = False
                    if zoomin_button and rect:
                        zoomin = True
                    elif zoomout_button:
                        zoomout = True
                    rect = False
            # If the zoom in funtionality is enabled and dragging is enabled,
            # and the mouse is moving, then obtain the position of the mouse 
            # and set Rect as True.
            elif event.type == pygame.MOUSEMOTION and drag and zoomin_button:
                (mouse_x2_pos, mouse_y2_pos) = pygame.mouse.get_pos()
                rect = True
        # Fill the background with white.
        screen.fill(white)
        # Depending on the activity status of the buttons, draw
        # the appropriate textboxes and buttons onto the screen.
        screen.blit(text1, textbox1)
        if zoomin_button:
            screen.blit(text3, textbox3)
            pygame.draw.rect(screen, green_active, zoom_in_button)
        else:
            screen.blit(text2, textbox2)
            pygame.draw.rect(screen, green_notactive, zoom_in_button)
        if zoomout_button:
            pygame.draw.rect(screen, green_active, zoom_out_button)
        else:
            screen.blit(text4, textbox4)
            screen.blit(text5, textbox5)
            pygame.draw.rect(screen, green_notactive, zoom_out_button)
        # If rect is True, then calculate the appropriate position and 
        # size of the rectangle and draw the rectangle onto the screen.
        if rect:
            rect_width = abs(mouse_x2_pos - mouse_x1_pos)
            if mouse_y2_pos <= mandelbrot_size[1]:
                rect_height = abs(mouse_y2_pos - mouse_y1_pos)
            rect_left = min(mouse_x1_pos, mouse_x2_pos)
            rect_top = min(mouse_y1_pos, mouse_y2_pos)
            cropbox = pygame.Rect(rect_left, rect_top, rect_width, rect_height)
            screen.blit(mandelbrot, mandelbrot_rect)
            pygame.draw.rect(screen, grey, cropbox, 2)
            pygame.display.flip()
        else:
            # If zoomin is True, then start zooming in.
            if zoomin:
                # Display the appropriate message onto the screen.
                textwait = errortext.render("Please wait while the image is zooming in...", True, white, orange)
                textboxwait = textwait.get_rect()
                textboxwait_centre_x = mandelbrot_size[0] / 2
                textboxwait_centre_y = mandelbrot_size[1] / 2
                textboxwait.center = (textboxwait_centre_x, textboxwait_centre_y)
                screen.blit(mandelbrot, mandelbrot_rect)
                # Display the current rectangle onto the screen.
                pygame.draw.rect(screen, grey, cropbox, 2)
                screen.blit(textwait, textboxwait)
                pygame.display.flip()
                # Linearly interpolate the screen resolution of the rectangle against the axes of
                # the corresponding Mandelbrot graph, and add the new axes limits to the list.
                y_diff = y_max - y_min
                x_diff = x_max - x_min
                y_max_old = y_max
                x_min_old = x_min
                y_max = y_max_old - ((rect_top / mandelbrot_size[1]) * y_diff)
                rect_bottom = rect_top + rect_height
                y_min = y_max_old - ((rect_bottom / mandelbrot_size[1]) * y_diff)
                x_min = x_min_old + ((rect_left / mandelbrot_size[0]) * x_diff)
                rect_right = rect_left + rect_width
                x_max = x_min_old + ((rect_right / mandelbrot_size[0]) * x_diff)
                x_min_list.append(x_min)
                x_max_list.append(x_max)
                y_min_list.append(y_min)
                y_max_list.append(y_max)
                # Store the Mandelbrot graph with new axes limits
                # into a new image file, and display the new image.
                i += 1
                mandelbrot_graphpic(max_n, x_min, x_max, n_xpts, y_min, y_max, n_ypts, fig_w, fig_h, "MandelbrotPic{}".format(i))
                filename = str(currwd) + "//MANDELBROT_GRAPHS//MandelbrotPic{}.png".format(i)
                mandelbrot = pygame.image.load(filename)
                mandelbrot = pygame.transform.scale(mandelbrot, mandelbrot_size)
                screen.blit(mandelbrot, mandelbrot_rect)
                pygame.display.flip()
                # Clear the system events log to avoid bugs.
                pygame.event.clear()                
                # Set zoomin to False.
                zoomin = False
            elif not zoomout:
                # If zoomin and zoomout is False, then draw 
                # the current Mandlebrot graph onto the screen.
                screen.blit(mandelbrot, mandelbrot_rect)
                pygame.display.flip()
            # If zoomout is True, then start zooming out where necessary.
            if zoomout:
                # Check image index.
                if i <= 0:
                    # Display an error message for one second when user has zoomed out to the maximum.
                    texterror1 = errortext.render("ERROR: You have zoomed out to the original image!", True, white, red)
                    textboxerror1 = texterror1.get_rect()
                    textboxerror1_centre_x = mandelbrot_size[0] / 2
                    textboxerror1_centre_y = mandelbrot_size[1] / 2
                    textboxerror1.center = (textboxerror1_centre_x, textboxerror1_centre_y)
                    screen.blit(mandelbrot, mandelbrot_rect)
                    screen.blit(texterror1, textboxerror1)
                    pygame.display.flip()
                    zoomout = False
                    zoomout_button = False
                    pygame.time.delay(1000)
                    pygame.event.clear()
                else:
                    # Display the appropriate message onto the screen.
                    i -= 1
                    screen.blit(text6, textbox6)
                    screen.blit(text7, textbox7)
                    screen.blit(mandelbrot, mandelbrot_rect)
                    pygame.display.flip()
                    # Display the previous zoomed out image, and go back to the previous axes limits.
                    filename = str(currwd) + "//MANDELBROT_GRAPHS//MandelbrotPic{}.png".format(i)
                    mandelbrot = pygame.image.load(filename)
                    mandelbrot = pygame.transform.scale(mandelbrot, mandelbrot_size)
                    x_min = x_min_list[i]
                    x_max = x_max_list[i]
                    y_min = y_min_list[i]
                    y_max = y_max_list[i]
                    x_min_list.pop()
                    x_max_list.pop()
                    y_min_list.pop()
                    y_max_list.pop()
                    # Clear the system events log to avoid bugs.
                    pygame.event.clear()
                    # Set zoomout to False, and "unclick" the zoom out button.
                    zoomout = False
                    zoomout_button = False
    # Close the PyGame window.
    pygame.quit()
    return None
