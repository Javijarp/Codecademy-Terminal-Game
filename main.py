import curses
import random
import time
from threading import Thread
import os

main_screen = curses.initscr()

# os.system("""start cmd cd Desktop/"Curses Asteroids Game python main.py""")

# Resize the window to the specific size to work with the coordinates
curses.resize_term(20, 50)
main_screen.border(0)
main_screen.nodelay(True)

box = curses.newwin(20, 30)
box.border(0)
box.nodelay(True)
curses.noecho()
curses.halfdelay(60)

border = curses.newwin(20, 31)
border.border(0)

Asteroids = []

player_x = 10
player_y = 10
player_position = [player_x, player_y]
player_sprite = "▲"

all_positions = []

""" top-left: [1,1] top-right: [28, 1] """

top_border_position_y = 1
top_border_position_x = [i for i in range(0, 28)]

bottom_border_position_y = 18

class Asteroid:
    spawn_chance = 10 # Stablishing the chance of an asteroid having the ability to spawn

    def __init__(self):

        # Assign a randwom coordinate inside the box
        self.x = random.choice(top_border_position_x)
        self.y = top_border_position_y

        # Append the asteroid to the Asteroids list
        Asteroids.append(self)

        # Start a new thread for the asteroid to move
        self.Athread = Thread(target = self.Asteroid_Move)
        self.Athread.start()
    
    def __del__(self):
        box.add(self.y, self.x, " ")
        return False

    # Draw and return the asteroid sprite
    def Asteroid_Spawn(self):
        
        i = box.addch(self.y, self.x, "*", curses.A_BOLD)

        return i
    
    # Function to handle the asteroid when it is alive
    def Asteroid_Move(self):

        # Spawn the asteroid
        self.Asteroid_Spawn()

        # Start the movement algorithm
        while True:
            self.Check_Collision()
            box.addch(self.y, self.x, " ")
            self.x += random.randint(-1, 1)
            self.y += random.randint(0, 1)
            if self.y == bottom_border_position_y + 1:
                return False
                del self
            i = box.addch(self.y, self.x, "*", curses.A_BOLD)
            time.sleep(1/60)
    
    # Check if the asteroid collided with something
    def Check_Collision(self):
        # If the position of the Asteroid is not the bottom of the border then continue normally
        if self.y is not bottom_border_position_y:
            return
        
        # If the position in the x-axis is bigger than the largest position in of the x-axis of the border than delete the Asteroid
        elif self.x >= top_border_position_x[-1]:
            # Remove the Asteroid from the Asteroid list to update the amount of playable Asteroids
            Asteroids.pop(Asteroids.index(self))

            # Move the Asteroid without colliders to the bottom right corner of the map
            self.y = bottom_border_position_y
            self.x = top_border_position_x[-1]

            # Delete the Asteroid before it has a chance to cause any bugs to the other playable entities
            del self

            # Return false to stop the movement of the Asteroid
            return False
        
        # If the position in the x-axis is bigger than the smallest position in the x-axis of the border than delete the Asteroid
        elif self.x <= top_border_position_x[0]:
            # Remove the Asteroid from the Asteroid list to update the amount of playable Asteroids
            Asteroids.pop(Asteroids.index(self))

            # Move the Asteroid without colliders to the bottom right corner of the map
            self.y = bottom_border_position_y
            self.x = top_border_position_x[-1]

            # Delete the Asteroid before it has a chance to cause any bugs to the other playable entities
            del self

            # Return false to stop the movement of the Asteroid
            return False
        
        # If the position of the Asteroid is the same as the position of any other entity then kill the Asteroid
        else:
            for i in all_positions:
                if self.x is i.x and self.y is i.y and i != self:

                    # Remove the Asteroid from the Asteroid list to update the amount of playable Asteroids
                    Asteroids.pop(Asteroids.index(self))

                    # Move the Asteroid without colliders to the bottom right corner of the map
                    self.y = bottom_border_position_y
                    self.x = top_border_position_x[-1]

                    # Delete the Asteroid before it has a chance to cause any bugs to the other playable entities
                    del self

                    # Return false to stop the movement of the Asteroid
                    return False
                
            # If the Asteroid reached the bottom of the border then delete the Asteroid
            if self.y is bottom_border_position_y:

                # Remove the Asteroid from the Asteroid list to update the amount of playable Asteroids
                Asteroids.pop(Asteroids.index(self))

                # Move the Asteroid without colliders to the bottom right corner of the map
                self.y = bottom_border_position_y
                self.x = top_border_position_x[-1]

                # Delete the Asteroid before it has a chance to cause any bugs to the other playable entities
                del self

                # Return false to stop the movement of the Asteroid
                return False
    
    # Future Posible Animation Algorithm For The Sprite
    def Animate(self):
        pass

class Player:
    def __init__(self, player_y = player_y, player_x = player_x, collided = False):
        self.position = [player_x, player_y]
        self.x = player_x
        self.y = player_y
        self.collided = collided
        self.bullet_spawned = False

        all_positions.append(self)

    def Player_Movement(self):
        # Handle Player Movement

        while True:
            key = box.getch()

            if key == ord("w"):
                box.addch(self.y, self.x, " ")
                if self.y == 1:
                    self.y = 1
                else:            
                    self.y -= 1
                self.Draw()
            elif key == ord("s"):
                box.addch(self.y, self.x, " ")
                if self.y == 18:
                    self.y = 18
                else:            
                    self.y += 1
                self.Draw()
            elif key == ord("d"):
                box.addch(self.y, self.x, " ")
                if self.x == 28:
                    self.x = 28
                else:
                    self.x += 1
                self.Draw()
            elif key == ord("a"):
                box.addch(self.y, self.x, " ")
                if self.x == 1:
                    self.x = 1
                else:
                    self.x -= 1
                self.Draw()
            elif key == ord(" "):
                self.Shoot()
                self.Draw()
    
    def Shoot(self):
        new_bullet = Bullet()
        self.bullet_spawned = True
        return new_bullet
    
    def Draw(self):
        box.addch(self.y - 1, self.x + 1, " ")
        player_ch = box.addch(self.y, self.x, player_sprite, curses.A_NORMAL)
        for i in Asteroids:
            if self.x == i.x and self.y == i.x and i != self:
                self.Dead()
        return player_ch
    
    def Dead(self):
        del self
    
    def Animate(self):
        # Possible Animation Algorithm
        # if key == ord("w"):
        #     player_sprite = "▲"
        # elif key == ord("s"):
        #     player_sprite = "▼"
        # elif key == ord("d"):
        #     player_sprite = "▶"
        # elif key == ord("a"):
        #     player_sprite = "◀"
        pass
    
class Bullet:
    def __init__(self, collided = False):
        self.x = player.x
        self.y = player.y - 1
        self.collided = collided
        self.bullet_sprite = "|"

        bullet_thread = Thread(target = self.Move)
        bullet_thread.start()

        all_positions.append(self)
    
    def __del__(self):
        box.addch(self.y, self.x, " ")
        self.collided == True
        return self.collided

    def Move(self):
        while True:
            if self.y is not top_border_position_y:
                self.y -= 1
                self.Draw()
            else:
                # all_positions.pop(Asteroids.index(self))
                box.addch(self.y, self.x, " ")
                self.y = bottom_border_position_y
                self.x = top_border_position_x[-1]
                del self
                return False
            time.sleep(1/60)
    
    def Draw(self):
        box.addch(self.y + 1, self.x, " ")
        bullet_char = box.addch(self.y, self.x, self.bullet_sprite, curses.A_BOLD)
        return bullet_char


# Instantiating the player
player = Player()

# Starting the thread that takes control of player movement
Pthread = Thread(target = player.Player_Movement)
Pthread.start()

Refreshes = 0
Asteroids_Destroyed = 0

while True:
    curses.curs_set(False)
    box.nodelay(True)
    box.border(0)
    main_screen.border(0)
    main_screen.refresh()

    spawn_chance = 100 # Stablishing the chance of an asteroid having the ability to spawn

    # Create the the chance of creating a new Asteroid
    chance = random.randint(0, spawn_chance)

    Acounter = 0

    if chance < 2:
        Aname = random.randint(0, 100)
        Aname = Asteroid()


    Asteroids_Count = len(Asteroids)

    coordinate_values = str(player.x) + " , " + str(player.y)

    coordinates = "[ " + coordinate_values + " ] "

    Refreshes += 1

    if Refreshes == 1:
        box.refresh()
        Refreshes = 0

    main_screen.addstr(6, 30, "Coordinates:", curses.A_UNDERLINE) # Print the coordinates of the player in the hud screen
    main_screen.addstr(7, 30, coordinates, curses.A_BOLD) # Print the coordinate vector of the player in the hud screen
    main_screen.addstr(10, 30, "Asteroids Destroyed:", curses.A_UNDERLINE) # Print the number of Asteroids destroyed in the hud screen
    main_screen.addstr(11, 30, str(Asteroids_Destroyed), curses.A_BOLD)
    main_screen.addstr(13, 30, "Asteroids:", curses.A_UNDERLINE) # Print the number of Asteroids in game
    main_screen.addstr(14, 30, str(Asteroids_Count), curses.A_BOLD)
    main_screen.addstr(16, 30, "Refreshes: " + str(Refreshes), curses.A_UNDERLINE)

    time.sleep(1/60) # Adjust the frame rate to wait a sixteith of a second
