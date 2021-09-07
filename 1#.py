import pygame
import random

# creating the data structure for pieces
# setting up global vars
# functions
# - create_grid
# - draw_grid
# - draw_window
# - rotating shape in main
# - setting up the main

"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""

pygame.font.init()

# GLOBALS VARS
s_width = 800  # Screen width
s_height = 700  # Screen height

# Actual play area of the game within the window
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 20 height per block

block_size = 30

# Sets the coordinates of the play area
top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height

# SHAPE FORMATS - used to represent the shapes including each rotation

S = [['.....',
      '......',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]  # List to hold all the shapes to make it easy to reference the shapes
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]


# index 0 - 6 represent shape

# Essentially the constructor for the piece
class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]  # Sets the colour to the equal index in the shape_colors list
        # E.G shapes[0] == shape_colors[0]
        self.rotation = 0


def create_grid(locked_positions={}):
    grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]  # Creates one list for every row in the grid
    # - each row has 10 colours

    # i = rows, j = columns
    # Checks if there is already blocks in the grid and changes the colour
    for i in range(len(grid)):  # Loops through the row list
        for j in range(len(grid[i])):  # Loops through the column list
            if (j, i) in locked_positions:
                c = locked_positions[(j, i)]
                grid[i][j] = c  # Checks the x and y coordinates of locked positions (if there is any) against the grid
                # positions and changes the colour depending on whether there is a block there or not
    return grid


def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):  # loops through each line
        row = list(line)
        for j, column in enumerate(row):  # loops through the line looking for full stops or zeros
            if column == '0':
                positions.append((shape.x + j, shape.y + i))  # Adds the column and rows to the shapes current position,
                # to move the shape down the screen, instead of being stuck in the position it's in, in the list

    # Offsets the shape two columns left and four rows up to ignore the full stops in the list
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)


def valid_space(shape, grid):
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub]  # Converts two dimensional list into a one dimensional list

    formatted = convert_shape_format(shape)

    # The shapes begin falling before they're seen on screen, this loop checks once the shape is visible on screen,
    # whether or not it's in an accepted position. If the loop wasn't made, it would return false when the shape is
    # falling whilst hidden
    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
    return True  # if it makes it through the loop the position is accepted and it returns True


def check_lost(positions):
    # Checks whether the block is above the screen and if it is the game is lost
    for pos in positions:
        x, y = pos
        if y < 1:
            return True

    return False


def get_shape():
    return Piece(5, 0, random.choice(shapes))  # Picks a random shape from the shape list and creates an object


def draw_text_middle(text, size, color, surface):
    pass


# Draws the grid
def draw_grid(surface, grid):
    sx = top_left_x
    sy = top_left_y

    for i in range(len(grid)):
        pygame.draw.line(surface, (128, 128, 128), (sx, sy + i * block_size), (sx + play_width, sy + i * block_size))
        # Draws 20 vertical lines
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128, 128, 128), (sx + j * block_size, sy),
                             (sx + j * block_size, sy + play_height))
            # Draws 10 horizontal lines


def clear_rows(grid, locked):
    pass


def draw_next_shape(shape, surface):
    pass


def draw_window(surface, grid):
    surface.fill((0, 0, 0))  # Changes the surface of the window to black

    pygame.font.init()  # Initializes font object
    font = pygame.font.SysFont('comicsans', 60)  # Sets the font and size
    label = font.render('Tetris', 1, (255, 255, 255))  # Creates the label, sets the text and the colour

    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))  # Draws the label on the screen
    # and automatically places the label in the centre of the screen no matter whether the window has been resized

    for i in range(len(grid)):  # Loops through the grid to get the colours of the blocks in the grid
        for j in range(len(grid[i])):
            # Draws the grid
            pygame.draw.rect(surface, grid[i][j],
                             (top_left_x + j * block_size, top_left_y + i * block_size, block_size, block_size), 0)

    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 4)  # Draws the red box
    # around the tetris grid

    draw_grid(surface, grid)
    pygame.display.update()  # Updates the screen


def main(win):
    locked_positions = {}  # Dictionary for the locked positions on the grid
    grid = create_grid(locked_positions)  # Creates the grid with locked positions passed so they are added

    change_piece = False  # For when the piece needs to be changed
    run = True  # For the while loop of the game
    current_piece = get_shape()  # Sets the current piece
    next_piece = get_shape()  # Sets the next piece
    clock = pygame.time.Clock()  # Initializes the gameclock
    fall_time = 0  # Variable for the fall time
    fall_speed = 0.27  # Variable for fall speed

    while run:
        grid = create_grid(locked_positions)  # Creates a grid because every time a piece is moved, there is an
        # opportunity to create new locked positions
        fall_time += clock.get_rawtime()  # Initializes the clock to count the fall time of the piece
        clock.tick()  # Starts the clock

        # After one second has passed this will move the piece down one, check whether it has hit an invalid space
        # (either the bottom or another piece), if it has it will move the piece into the last valid position and load
        # in a new piece
        # Only checks vertical valid spaces
        if fall_time / 1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Kicks the game out of the while loop to end the game
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:  # Moves the piece left
                    current_piece.x -= 1
                    if not (valid_space(current_piece, grid)):  # Checks if the movement is valid and moves it back to
                        # where it was if it's not
                        current_piece += 1
                if event.key == pygame.K_RIGHT:  # Moves the piece right
                    current_piece.x += 1
                    if not (valid_space(current_piece, grid)):
                        current_piece -= 1
                if event.key == pygame.K_DOWN:  # Moves the piece down
                    current_piece.y += 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.y += 1
                if event.key == pygame.K_UP:  # Rotates the piece
                    current_piece.rotation += 1
                    if not (valid_space(current_piece, grid)):
                        current_piece -= 1

        shape_pos = convert_shape_format(current_piece)

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                # Locked positions is a dictionary containing the position of the piece as well as the colour of the
                # piece
                locked_positions[p] = current_piece.color
            current_piece = next_piece  # Replaces the old piece with the new piece
            next_piece = get_shape()  # Creates the new next piece with a random one
            change_piece = False  # Stops creating a new piece by setting change piece to false because the current
            # piece and next piece have been updated

        draw_window(win, grid)

        # Checks if the game is lost, quits if it is
        if check_lost(locked_positions):
            run = False
    pygame.display.quit()


def main_menu(win):
    main(win)


win = pygame.display.set_mode((s_width, s_height))  # Creates a pygame surface
pygame.display.set_caption('Tetris')  # Sets the caption
main_menu(win)  # start game
