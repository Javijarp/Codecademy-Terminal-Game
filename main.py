import curses
from curses import wrapper
import random
import time


main_screen = curses.initscr()
main_screen.border(0)

box = curses.newwin(20, 30)
box.border(0)
box.nodelay(True)
curses.halfdelay(60)

player_x = 10
player_y = 10
player_sprite = "▲" 

all_positions = []

""" top-left: [1,1] top-right: [28, 1] """

border_position_y = [1]
border_position_x = [i for i in range(0, 28)]

class Asteroid:
    spawn_chance = 10 # Stablishing the chance of an asteroid having the ability to spawn

    def __init__(self, collided = False):

        # Assign a random coordinate inside the box
        self.x = random.choice(border_position_x)
        self.y = random.choice(border_position_y)

        self.collided = collided

        Asteroids.append(self)
        
        if self.collided == False:
            Athread = Thread(target = self.Asteroid_Move)
            Athread.start()

    # Draw and return the asteroid sprite
    def Asteroid_Spawn(self):
        
        i = box.addch(self.y, self.x, "*", curses.A_BOLD)

        return i
    
    # Function to handle the asteroid when it is alive
    def Asteroid_Move(self):
        self.Asteroid_Spawn()
while True:
    curses.curs_set(False)
    player = box.addstr(player_y, player_x, player_sprite, curses.A_NORMAL)
    box.border(0)

    Asteroids_Destroyed = 0

    coordinate_values = str(player_x) + " , " + str(player_y)

    coordinates = "[ " + coordinate_values + " ] "

    main_screen.addstr(9, 49, "Coordinates:", curses.A_UNDERLINE) # Print the coordinates of the player in the hud screen
    main_screen.addstr(10, 50, coordinates, curses.A_BOLD) # Print the coordinate vector of the player in the hud screen
    main_screen.addstr(13, 50, "Asteroids Destroyed: " + str(Asteroids_Destroyed), curses.A_UNDERLINE) # Print the number of Asteroids destroyed in the hud screen
    main_screen.refresh()


    key = box.getch()

    if key == ord("w"):
        if player_y == 1:
            player_y = 1
        else:            
            player_y -= 1
    elif key == ord("s"):
        if player_y == 18:
            player_y = 18
        else:            
            player_y += 1
    elif key == ord("d"):
        if player_x == 28:
            player_x = 28
        else:
            player_x += 1
    elif key == ord("a"):
        if player_x == 1:
            player_x = 1
        else:
            player_x -= 1

    
    # Possible Animation Algorithm
    # if key == ord("w"):
    #     player_sprite = "▲"
    # elif key == ord("s"):
    #     player_sprite = "▼"
    # elif key == ord("d"):
    #     player_sprite = "▶"
    # elif key == ord("a"):
    #     player_sprite = "◀"
        

    time.sleep(1/60) # Set the frame rate to 60 refreshes per second
    box.erase()
    main_screen.refresh()
    box.refresh()
