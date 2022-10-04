


import tkinter
import time
import random
import math
import numpy as np
import matplotlib.pyplot as plt

# World settings
N_ROWS = 5
N_COLS = 8
SQUARE_SIZE = 60
KAREL_SIZE = 56
BALL_SIZE = SQUARE_SIZE/10
CANVAS_WIDTH = N_COLS * SQUARE_SIZE      # Width of drawing canvas in pixels
CANVAS_HEIGHT = N_ROWS * SQUARE_SIZE      # Height of drawing canvas in pixels
SPEED = 5  # set move speed form 1 to 50, the lowe the value the higher the speed


"""
karel list includes [canvas, rect, left_eye, right_eye, walls, beepers]

basic functions:
    Base Karel commands:
    move(karel) - makes Karel make a step forward
    turn_left(karel) - makes Karel turn left
    put_beeper(karel) - put a beeper in the current corner
    pick_beeper(karel) - pick up a beeper from the current corner
    
    Names of the conditions:
    beeper_present(karel) - check whether current corner contain a beeper
    left_is_clear(karel) - Check for a wall on the Karel left
    right_is_clear(karel) - Check for a wall on the Karel right
    front_is_clear(karel) - Check for a wall in front of karel
    facing_north(karel) - check whether karel facing North
    facing_south(karel) - check whether karel facing South
    facing_east(karel) - check whether karel facing East
    facing_west(karel) - check whether karel facing West
    
"""
def main():
    canvas = make_canvas(CANVAS_WIDTH, CANVAS_HEIGHT, 'Collect Newspaper Karel')
    karel = set_settings(canvas)

    turn_right(karel)
    move(karel)
    turn_left(karel)
    while not beeper_present(karel):
        move(karel)
    pick_beeper(karel)
    turn_around(karel)
    while front_is_clear(karel):
        move(karel)
    turn_right(karel)
    move(karel)
    put_beeper(karel)

    canvas.mainloop()


def set_settings(canvas):
    """"
    The function includes all the function that set the world and Karel
    """
    walls, beepers = create_world(canvas)
    karel = create_karel(canvas, walls, beepers)
    karel[0].update()
    time.sleep(50 / 50.)
    return karel


def create_world(canvas):
    """
    the function takes canvas and the number of columns and rows in the canvas and return a grid of
    dots. Walls (gray squares) are stored in a
    list in order not to allow karel to cross it.
    """
    for row in range(N_ROWS):
        for col in range(N_COLS):
            x = col * SQUARE_SIZE
            y = row * SQUARE_SIZE
            point_size = 2
            canvas.create_oval(x + SQUARE_SIZE/2 - point_size/2, y + SQUARE_SIZE/2 - point_size/2, x + SQUARE_SIZE/2 + point_size/2, y + SQUARE_SIZE/2 + point_size/2, fill='black')
    walls = make_walls(canvas)
    beepers = make_beepers(canvas)

    return walls, beepers


def make_walls(canvas):
    """
    The function creates lines (e.g. walls).
    Important! the lines should be specified from left to right and from top to bottom. In other words,
    starting point must be either more to the left or more to the right.
    Also, lines must have vertical or horizontal orientation
    The function return a list named "wall" that include all the created lines
    """
    walls = []
    walls.append(canvas.create_line(5 * SQUARE_SIZE, SQUARE_SIZE, 5 * SQUARE_SIZE, 2 * SQUARE_SIZE))
    walls.append(canvas.create_line(5 * SQUARE_SIZE, 3 * SQUARE_SIZE, 5 * SQUARE_SIZE, 4 * SQUARE_SIZE))
    walls.append(canvas.create_line(2 * SQUARE_SIZE, SQUARE_SIZE, 5 * SQUARE_SIZE,  SQUARE_SIZE))
    walls.append(canvas.create_line(2 * SQUARE_SIZE, 1 * SQUARE_SIZE, 2 * SQUARE_SIZE, 4 * SQUARE_SIZE))
    walls.append(canvas.create_line(2 * SQUARE_SIZE, 4 * SQUARE_SIZE, 5 * SQUARE_SIZE, 4 *  SQUARE_SIZE))
    return walls

def make_beepers(canvas):
    """
     The function creates beepers (e.g. yellow squares) that are pre-placed in the world.
     The function return a list named "beeper" that include all the created lines
     """
    beepers = []
    beepers.append(canvas.create_rectangle(6 * SQUARE_SIZE + SQUARE_SIZE / 3, 2 * SQUARE_SIZE + SQUARE_SIZE / 3,
                                           7 * SQUARE_SIZE - SQUARE_SIZE / 3, 3 * SQUARE_SIZE - SQUARE_SIZE / 3,
                                           fill='yellow'))
    return beepers


def create_karel(canvas, walls, beepers):
    """
    The function define Karel - a list of all the variable lists that are needed to guide Karel in the world.
    karel[0] = canvas,
    karel[1] = rect, body of Karel
    karel[2] = circle, the left_eye of Karel
    karel[3] = circle (shifted to rect center) - right_eye of karel,
    karel[4] = lists of rect (gray rect) - walls, squares that karel can't go through
    karel[5] = list of beepers (smaller yellow rect) - thing that Karel can put and pick
    The function draw a blue square with two eyes. All these three forms + the canvas + walls are stored
     into a list maned karel. Karel stands in the bottom-left corner.
    """
    # set initial coordinates for a rectangle
    rect_start_x = 2 * SQUARE_SIZE
    rect_start_y = 1 * SQUARE_SIZE
    make_smaller = (SQUARE_SIZE - KAREL_SIZE) / 2 # makes rect smaller by 6 pix

    rect_end_x = rect_start_x + SQUARE_SIZE
    rect_end_y = rect_start_y + SQUARE_SIZE
    rect = canvas.create_rectangle(rect_start_x + make_smaller, rect_start_y + make_smaller, rect_end_x - make_smaller, rect_end_y - make_smaller, fill='blue', outline='blue')

    # set initial coordinates for the left eye
    l_eye_start_y = canvas.coords(rect)[3] - ((SQUARE_SIZE / 3) * 2 + (BALL_SIZE / 2))
    l_eye_start_x = canvas.coords(rect)[0] + ((SQUARE_SIZE / 6) * 5 - (BALL_SIZE / 2))
    l_eye_end_y = canvas.coords(rect)[3] - ((SQUARE_SIZE / 3) * 2 - (BALL_SIZE / 2))
    l_eye_end_x = canvas.coords(rect)[0] + ((SQUARE_SIZE / 6) * 5 + (BALL_SIZE / 2))
    left_eye = canvas.create_oval(l_eye_start_x, l_eye_start_y, l_eye_end_x, l_eye_end_y, fill='white', outline='white')

    # set initial coordinates for left eye
    # IMPORTANT right eye is shifted by 1 pix to the center of rectangle to control karel orientation.
    # like the difference in eyes coordinates suggest current orientation of Karel
    r_eye_start_y = canvas.coords(rect)[3] - ((SQUARE_SIZE / 3) + (BALL_SIZE / 2))
    r_eye_start_x = canvas.coords(rect)[0] + ((SQUARE_SIZE / 6) * 5 - (BALL_SIZE / 2)) - 1
    r_eye_end_y = canvas.coords(rect)[3] - ((SQUARE_SIZE / 3) - (BALL_SIZE / 2))
    r_eye_end_x = canvas.coords(rect)[0] + ((SQUARE_SIZE / 6) * 5 + (BALL_SIZE / 2)) - 1
    right_eye = canvas.create_oval(r_eye_start_x, r_eye_start_y, r_eye_end_x, r_eye_end_y, fill='white', outline='white')

    # left the beeper list empty if you do not want any beeper to be pre-placed in the world.
    karel = [canvas, rect, left_eye, right_eye, walls, beepers]
    return karel


def turn_left(karel):
    """
    Function rotate Karel eyes 90 degrees counter-clockwise.
    First the function checks current orientation of Karel, then it moves eyes relative to the Karel's
    body coordinate
    """
    time.sleep(SPEED / 50.)
    one_six = (SQUARE_SIZE/6)  # is a 1/6 of Karel body. In this function it is used as a unit of
    # movement

    # from East to North

    if facing_east(karel):
        karel[0].move(karel[2], -one_six*3, -one_six)
        karel[0].move(karel[3], -one_six+1, -one_six*3+1)

    # from North to West
    elif facing_north(karel):
        karel[0].move(karel[2], -one_six, one_six*3)
        karel[0].move(karel[3], -one_six*3+1, one_six-1)

    # from West to South
    elif facing_west(karel):
        karel[0].move(karel[2], one_six*3, one_six)
        karel[0].move(karel[3], one_six-1, one_six*3-1)

    # from South to East
    elif facing_south(karel):
        karel[0].move(karel[2], one_six, -one_six*3)
        karel[0].move(karel[3], one_six*3-1, -one_six+1)
    karel[0].update()
    return karel


def turn_right(karel):
    for i in range(3):
        turn_left(karel)


def turn_around(karel):
    for i in range(2):
        turn_left(karel)


def move(karel):
    """
    shifts Karel forward. First the function check whether the front is blocked by a wall
    If it is not, Karel (body and eyes) is shifted forward
    If front is blocked, the function returns Error message
    """
    time.sleep(SPEED / 50.)

    if front_is_clear(karel):
        if facing_east(karel):
            karel[0].move(karel[1], SQUARE_SIZE, 0)
            karel[0].move(karel[2], SQUARE_SIZE, 0)
            karel[0].move(karel[3], SQUARE_SIZE, 0)

        elif facing_north(karel):
            karel[0].move(karel[1], 0, -SQUARE_SIZE)
            karel[0].move(karel[2], 0, -SQUARE_SIZE)
            karel[0].move(karel[3], 0, -SQUARE_SIZE)

        elif facing_west(karel):
            karel[0].move(karel[1], -SQUARE_SIZE, 0)
            karel[0].move(karel[2], -SQUARE_SIZE, 0)
            karel[0].move(karel[3], -SQUARE_SIZE, 0)

        elif facing_south(karel):
            karel[0].move(karel[1], 0, SQUARE_SIZE)
            karel[0].move(karel[2], 0, SQUARE_SIZE)
            karel[0].move(karel[3], 0, SQUARE_SIZE)
    else:
        print("Error, Karel can't move further")

    karel[0].update()
    return karel


def front_is_clear(karel):
    """
    the function check Karel orientation then check whether boarder or a gray brick in front of it.
    """
    time.sleep(SPEED / 50.)
    make_smaller = (SQUARE_SIZE - KAREL_SIZE) / 2  # free space between Karel (body) boarder and the wall

    # body coordinates. Used to determine facing brick and boarders
    body_left_top_x = karel[0].coords(karel[1])[0]
    body_left_top_y = karel[0].coords(karel[1])[1]
    body_right_bottom_x = karel[0].coords(karel[1])[2]
    body_right_bottom_y = karel[0].coords(karel[1])[3]

    # check Karel orientation then check whether boarder or a gray brick in front of it
    if facing_east(karel):
        for bricks in karel[4]:
           if karel[0].coords(bricks)[0] == body_right_bottom_x + make_smaller and karel[0].coords(bricks)[1] < body_left_top_y and karel[0].coords(bricks)[3] > body_right_bottom_y:
                return False
        return body_right_bottom_x + make_smaller < CANVAS_WIDTH

    elif facing_north(karel):
        for bricks in karel[4]:
           if karel[0].coords(bricks)[0] < body_left_top_x and karel[0].coords(bricks)[1] == body_left_top_y - make_smaller and karel[0].coords(bricks)[2] > body_right_bottom_x:
                return False
        return body_left_top_y - make_smaller > 0

    elif facing_west(karel):
        for bricks in karel[4]:
           if karel[0].coords(bricks)[0] == body_left_top_x - make_smaller and karel[0].coords(bricks)[1] < body_left_top_y and karel[0].coords(bricks)[3] > body_right_bottom_y:
                return False
        return body_left_top_x - make_smaller > 0

    elif facing_south(karel):
        for bricks in karel[4]:
           if karel[0].coords(bricks)[0] < body_left_top_x and karel[0].coords(bricks)[1] == body_right_bottom_y + make_smaller and karel[0].coords(bricks)[3] > body_right_bottom_x:
                return False
        return body_right_bottom_y + make_smaller < CANVAS_HEIGHT


def left_is_clear(karel):
    """
    the function check Karel orientation then check whether a wall on Karel's left.
    """
    time.sleep(SPEED / 50.)
    make_smaller = (SQUARE_SIZE - KAREL_SIZE) / 2  # free space between Karel (body) boarder and the wall
    # eyes coordinates. Used to determine Karel orientation

    # body coordinates. Used to determine facing brick and boarders
    body_left_top_x = karel[0].coords(karel[1])[0]
    body_left_top_y = karel[0].coords(karel[1])[1]
    body_right_bottom_x = karel[0].coords(karel[1])[2]
    body_right_bottom_y = karel[0].coords(karel[1])[3]

    # check Karel orientation then check whether boarder or a gray brick in front of it
    if facing_east(karel):
        for bricks in karel[4]:
           if karel[0].coords(bricks)[0] < body_left_top_x and karel[0].coords(bricks)[1] == body_left_top_y - make_smaller and karel[0].coords(bricks)[2] > body_right_bottom_x:
                return False
        return body_left_top_y - make_smaller > 0

    elif facing_north(karel):
        for bricks in karel[4]:
            if karel[0].coords(bricks)[0] == body_left_top_x - make_smaller and karel[0].coords(bricks)[
                1] < body_left_top_y and karel[0].coords(bricks)[3] > body_right_bottom_y:
                return False
        return body_left_top_x - make_smaller > 0

    elif facing_west(karel):
        for bricks in karel[4]:
           if karel[0].coords(bricks)[0] < body_left_top_x and karel[0].coords(bricks)[1] == body_right_bottom_y + make_smaller and karel[0].coords(bricks)[3] > body_right_bottom_x:
                return False
        return body_right_bottom_y + make_smaller < CANVAS_HEIGHT

    elif facing_south(karel):
        for bricks in karel[4]:
           if karel[0].coords(bricks)[0] == body_right_bottom_x + make_smaller and karel[0].coords(bricks)[1] < body_left_top_y and karel[0].coords(bricks)[3] > body_right_bottom_y:
                return False
        return body_right_bottom_x + make_smaller < CANVAS_WIDTH

def right_is_clear(karel):
    """
    the function check Karel orientation then check whether a wall on Karel's left.
    """
    time.sleep(SPEED / 50.)
    make_smaller = (SQUARE_SIZE - KAREL_SIZE) / 2  # free space between Karel (body) boarder and the wall
    # eyes coordinates. Used to determine Karel orientation

    # body coordinates. Used to determine facing brick and boarders
    body_left_top_x = karel[0].coords(karel[1])[0]
    body_left_top_y = karel[0].coords(karel[1])[1]
    body_right_bottom_x = karel[0].coords(karel[1])[2]
    body_right_bottom_y = karel[0].coords(karel[1])[3]

    # check Karel orientation then check whether boarder or a gray brick in front of it
    if facing_east(karel):
        for bricks in karel[4]:
           if karel[0].coords(bricks)[0] < body_left_top_x and karel[0].coords(bricks)[1] == body_right_bottom_y + make_smaller and karel[0].coords(bricks)[3] > body_right_bottom_x:
                return False
        return body_right_bottom_y + make_smaller < CANVAS_HEIGHT

    elif facing_north(karel):
        for bricks in karel[4]:
           if karel[0].coords(bricks)[0] == body_right_bottom_x + make_smaller and karel[0].coords(bricks)[1] < body_left_top_y and karel[0].coords(bricks)[3] > body_right_bottom_y:
                return False
        return body_right_bottom_x + make_smaller < CANVAS_WIDTH

    elif facing_west(karel):
        for bricks in karel[4]:
           if karel[0].coords(bricks)[0] < body_left_top_x and karel[0].coords(bricks)[1] == body_left_top_y - make_smaller and karel[0].coords(bricks)[2] > body_right_bottom_x:
                return False
        return body_left_top_y - make_smaller > 0

    elif facing_south(karel):
        for bricks in karel[4]:
           if karel[0].coords(bricks)[0] == body_left_top_x - make_smaller and karel[0].coords(bricks)[1] < body_left_top_y and karel[0].coords(bricks)[3] > body_right_bottom_y:
                return False
        return body_left_top_x - make_smaller > 0


def put_beeper(karel):
    """
    create a new rectangle (a beeper) at the Karel's location. Beeper's coordinates are calculated relative to
    Karel's body location
    """
    time.sleep(SPEED / 50.)
    body_left_top_x = karel[0].coords(karel[1])[0]
    body_left_top_y = karel[0].coords(karel[1])[1]
    body_right_bottom_x = karel[0].coords(karel[1])[2]
    body_right_bottom_y = karel[0].coords(karel[1])[3]
    size_difference = SQUARE_SIZE/3
    karel[5].append(karel[0].create_rectangle(body_left_top_x + size_difference, body_left_top_y + size_difference, body_right_bottom_x - size_difference, body_right_bottom_y - size_difference, fill='yellow'))
    karel[0].update()


def beeper_present(karel):
    """
    The function checks for a beeper in Karel current location
    """
    body_left_top_x = karel[0].coords(karel[1])[0]
    body_left_top_y = karel[0].coords(karel[1])[1]
    body_right_bottom_x = karel[0].coords(karel[1])[2]
    body_right_bottom_y = karel[0].coords(karel[1])[3]
    for beepers in karel[5]:
        beeper_left_top_x = karel[0].coords(beepers)[0]
        beeper_left_top_y = karel[0].coords(beepers)[1]
        if beeper_left_top_x > body_left_top_x and beeper_left_top_x < body_right_bottom_x and beeper_left_top_y > body_left_top_y and beeper_left_top_y < body_right_bottom_y:
            return True
    return False


def pick_beeper(karel):
    """
    The function first check for a beeper in the current Karel's location.
    If beeper is present in current location, the function removes the beeper form the canvas and form the
    list of beepers
    If a beeper is not present, the function return an Error massage
    """
    time.sleep(SPEED / 50.)
    body_left_top_x = karel[0].coords(karel[1])[0]
    body_left_top_y = karel[0].coords(karel[1])[1]
    body_right_bottom_x = karel[0].coords(karel[1])[2]
    body_right_bottom_y = karel[0].coords(karel[1])[3]
    if beeper_present(karel):
        for beepers in karel[5]:
            beeper_left_top_x = karel[0].coords(beepers)[0]
            beeper_left_top_y = karel[0].coords(beepers)[1]
            if beeper_left_top_x > body_left_top_x and beeper_left_top_x < body_right_bottom_x and beeper_left_top_y > body_left_top_y and beeper_left_top_y < body_right_bottom_y:
                karel[0].delete(beepers)
                karel[5].remove(beepers)

    else:
        print("Error, no beeper to pick")
    karel[0].update()


def facing_east(karel):
    """
    The function checks if Karel facing east
    """
    left_x = karel[0].coords(karel[2])[0]  # x of the left eye
    left_y = karel[0].coords(karel[2])[1]  # y of the left eye
    right_x = karel[0].coords(karel[3])[0]  # x of the right eye
    right_y = karel[0].coords(karel[3])[1]  # x of the right eye
    return left_x > right_x and left_y < right_y


def facing_north(karel):
    """
    The function checks if Karel facing North
    """
    left_x = karel[0].coords(karel[2])[0]  # x of the left eye
    left_y = karel[0].coords(karel[2])[1]  # y of the left eye
    right_x = karel[0].coords(karel[3])[0]  # x of the right eye
    right_y = karel[0].coords(karel[3])[1]  # x of the right eye
    return left_x < right_x and left_y < right_y


def facing_west(karel):
    """
    The function checks if Karel facing West
    """
    left_x = karel[0].coords(karel[2])[0]  # x of the left eye
    left_y = karel[0].coords(karel[2])[1]  # y of the left eye
    right_x = karel[0].coords(karel[3])[0]  # x of the right eye
    right_y = karel[0].coords(karel[3])[1]  # x of the right eye
    return left_x < right_x and left_y > right_y


def facing_south(karel):
    """
    The function checks if Karel facing South
    """
    left_x = karel[0].coords(karel[2])[0]  # x of the left eye
    left_y = karel[0].coords(karel[2])[1]  # y of the left eye
    right_x = karel[0].coords(karel[3])[0]  # x of the right eye
    right_y = karel[0].coords(karel[3])[1]  # x of the right eye
    return left_x > right_x and left_y > right_y



######## DO NOT MODIFY ANY CODE BELOW THIS LINE ###########

# This function is provided to you and should not be modified.
# It creates a window that contains a drawing canvas that you
# will use to make your drawings.
def make_canvas(width, height, title):
    """
    DO NOT MODIFY
    Creates and returns a drawing canvas
    of the given int size with a blue border,
    ready for drawing.
    """
    top = tkinter.Tk()
    top.minsize(width=width, height=height)
    top.title(title)
    canvas = tkinter.Canvas(top, width=width + 1, height=height + 1)
    canvas.pack()
    return canvas




if __name__ == '__main__':
    main()
