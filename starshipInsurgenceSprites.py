"""
    Author: Jimmy Lin
    Date: May 28, 2017
    Description: This file contains sprite classes needed for the Starship
    Insurgence game.
"""

import pygame, random

class Wallpaper(pygame.sprite.Sprite):
    '''This class defines the sprite for a infinite scrolling background.'''
    def __init__(self, screen):
        '''This initializer takes a screen surface as a parameter, initializes
                the image and rect attributes, and scroll speed of the image.'''
        pygame.sprite.Sprite.__init__(self)
        self.__screen = screen
        self.image = pygame.image.load("Sprites/wallpaper.png")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.left = 0
        self.rect.bottom = self.__screen.get_height()

    def update(self):
        '''Resets position of image when it scrolls to the last section.'''
        if self.rect.top == 0:
            self.rect.bottom = self.__screen.get_height()
        else:
            self.rect.top += 4


class HomingPlasma(pygame.sprite.Sprite):
    '''This class defines the sprite for Homing Plasma.'''

    def __init__(self, screen, x, y, delay, dx, dy):
        '''This initializer takes a screen surface, delay time, x position and y position and speed as parameters, initializes
        the image and rect attributes, and x, y direction of the plasma.'''
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("Sprites/homingPlasma.png")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y

        # Instance variables to keep track of speed/direction, screen, delay timer and frames
        self.__dx = dx
        self.__dy = dy
        self.__screen = screen
        self.__delay = delay
        self.__counter = 0  # Frames counter for changing direction and to kill itself

    def update(self):
        '''This method repositions the projectile sprite on the screen.'''
        if self.rect.top > self.__screen.get_height() or self.rect.bottom < 0:
            self.kill()

        self.rect.top += self.__dy
        self.rect.left += self.__dx
        self.__counter += 1

        if self.__counter == 80:
            self.kill()

    def tracking(self, player_center):
        """This method calculates distance between ships to determine the speed of the projectile."""
        if self.__counter == self.__delay:  # Checks that the frames counter is equal to the tracking delay specified
            missile_center = self.rect.center
            x_distance = 0
            y_distance = 0
            if missile_center[0] > player_center[0]:
                x_distance = -1 * (missile_center[0] - player_center[0])
            elif missile_center[0] < player_center[0]:
                x_distance = player_center[0] - missile_center[0]
            if missile_center[1] > player_center[1]:
                y_distance = -1 * (missile_center[1] - player_center[1])
            elif missile_center[1] < player_center[1]:
                y_distance = player_center[1] - missile_center[1]
            self.__dx = x_distance / 30
            self.__dy = y_distance / 30


class Plasma(pygame.sprite.Sprite):
    '''This class defines the sprite for Plasma.'''
    def __init__(self, screen, x, y, team):
        '''This initializer takes a screen surface, x and y position, and team (0 - player or 1 - enemy), as parameters,
        initializes the image and rect attributes, and y direction of the Plasma.'''
        pygame.sprite.Sprite.__init__(self)
        # Set the team image, rect and direction for the plasma
        self.image = pygame.image.load("Sprites/plasma" + str(team) + ".png")
        self.image = self.image.convert()     
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        if team == 0:
            self.rect.top = y
            self.__dy = -20
        elif team == 1:
            self.rect.bottom = y
            self.__dy = 10

        self.__screen = screen
        
    def update(self):
        '''This method repositions the projectile sprite on the screen.'''
        if self.rect.top > self.__screen.get_height() or self.rect.bottom < 0:
            self.kill()
        self.rect.top += self.__dy

class Laser(pygame.sprite.Sprite):
    '''This class defines the sprite for Laser.'''
    def __init__(self, screen, ship_rect, team):
        '''This initializer takes a screen surface, the rect of the ship its firing from, and team (0 - player or 1 - enemy),
        as parameters, initializes the image and rect attributes of the laser.'''
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Sprites/laser" + str(team) + ".png")
        self.image = self.image.convert()     
        self.rect = self.image.get_rect()
        if team == 0:
            self.rect.centerx = ship_rect.centerx
            self.rect.bottom = ship_rect.top + 20
        elif team == 1:
            self.rect.bottom = ship_rect.bottom - 20

        # Instance variables to keep track of team, screen and frames alive
        self.__team = team
        self.__screen = screen
        self.__life_frames = 0
        
    def move(self, ship_rect):
        '''This method will be called automatically to reposition the
        ball sprite on the screen.'''
        if self.__team == 0:
            self.rect.centerx = ship_rect.centerx
            self.rect.bottom = ship_rect.bottom - 20

    def update(self):
        # Kills self once power up time limit (3 seconds) is up
        if self.__life_frames == 90:
            self.kill()
        self.__life_frames += 1
        
class Player(pygame.sprite.Sprite):
    '''This class defines the sprite for the Player'''

    def __init__(self, screen):
        '''This initializer takes a screen surface as a parameter and initializes the image and rect attributes'''
        pygame.sprite.Sprite.__init__(self)

        # Define the image and rect attributes, load other images
        self.__image_default = pygame.image.load("Sprites/heroStarship.png")
        self.__image_left = pygame.image.load("Sprites/heroStarshipLeft.png")
        self.__image_right = pygame.image.load("Sprites/herostarshipRight.png")
        self.__image_hit = pygame.image.load("Sprites/heroStarshipHit.png")
        self.__image_left_hit = pygame.image.load("Sprites/heroStarshipLeftHit.png")
        self.__image_right_hit = pygame.image.load("Sprites/herostarshipRightHit.png")
        self.image = self.__image_default
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        
        # Center the player in the window.
        self.rect.bottom = screen.get_height() / 2
        self.rect.centerx = screen.get_width() / 2
        self.__dx = 0
        self.__dy = 0

        # Instance variables to keep track of screen, shooting, etc.
        self.__screen = screen
        self.__shooting = False
        self.__shot_counter = 0  # Frames past since last shot fired
        self.__fire_rate = 5  # Number of frames past before able to shoot again
        self.__power_up = 0  # Power up variant currently using (0 being none)
        self.__power_up_frames = 0  # Used for timing how long player has been power up
        self.__hit_frames = 0  # Used for timing graphic changes and invincibility frames
        
    def go_left(self):
        '''This function changes the x speed and sprite image.'''
        self.image = self.__image_left
        self.image = self.image.convert()
        self.__dx = -8
            
    def go_right(self):
        '''This function changes the x speed and sprite image.'''
        self.image = self.__image_right
        self.image = self.image.convert()
        self.__dx = 8

    def go_up(self):
        '''This function changes the y speed.'''
        self.__dy = -7
                    
    def go_down(self):
        '''This function changes the y speed.'''
        self.__dy = 7
      
    def stop_left(self):
        '''This function stops x movement, unless the player has already changed the x speed since calling go_left().'''
        if self.__dx < 0:
            self.image = self.__image_default
            self.image = self.image.convert()
            self.__dx = 0
            
    def stop_right(self):
        '''This function stops x movement, unless the player has already changed the x speed since calling go_right().'''
        if self.__dx > 0:
            self.image = self.__image_default
            self.image = self.image.convert()
            self.__dx = 0
                
    def stop_up(self):
        '''This function stops y movement, unless the player has already changed the y speed since calling go_up().'''
        self.__dy = 0
                    
    def stop_down(self):
        '''This function stops y movement, unless the player has already changed the y speed since calling go_down().'''
        self.__dy = 0

    def set_power_up(self, power_up):
        '''This function sets the variant of power up and resets the power up timer.'''
        self.__power_up_frames = 0
        self.__power_up = power_up

    def get_power_up(self):
        '''This function returns the active power up.'''
        return self.__power_up
            
    def start_shooting(self):
        '''This function sets the shooting variable to true and resets the shot_counter to allow always shots when the player wants to.'''
        self.__shot_counter = self.__fire_rate
        self.__shooting = True
        
    def stop_shooting(self):
        '''This function sets shooting variable to false'''
        self.__shooting = False
    
    def shoot(self):
        '''This function returns true or false depending on if enough frames have passed to allow firing to match the fire rate set.'''
        if self.__shot_counter % self.__fire_rate == 0 and self.__shooting:
            return True

    def hit(self):
        '''This function sets the amount of frames left until the player can be hit again. Variable is also used to time how long "hit" images of the ship should be displayed.'''
        self.__hit_frames = 16

    def get_hit_frames(self):
        '''This function returns the value of __hit_frames.'''
        return self.__hit_frames

    def update(self):
        '''This method repositions the player sprite on the screen.'''
        # Check if the player reached the top or bottom of the screen.
        # If not, then keep moving the player in the same y direction.
        if ((self.rect.left > 10) and (self.__dx < 0)) or \
                ((self.rect.right < self.__screen.get_width() - 10) and (self.__dx > 0)):
            self.rect.left += self.__dx
        # Check if the player have reached the left or right of the screen.
        # If not, then keep moving the player in the same x direction.
        if (self.rect.top > 10 and self.__dy < 0) or (
                self.rect.bottom < self.__screen.get_height() - 10 and self.__dy > 0):
            self.rect.bottom += self.__dy
            
        # Keep track of frames for managing fire rate
        self.__shot_counter += 1

        # "Hit" graphics
        if self.__dx == 0:
            image_default = self.__image_default
            image_hit = self.__image_hit
        if self.__dx < 0:
            image_default = self.__image_left
            image_hit = self.__image_left_hit
        if self.__dx > 0:
            image_default = self.__image_right
            image_hit = self.__image_right_hit
        if self.__hit_frames == 16:
            self.image = image_hit
            self.image = self.image.convert()
        if self.__hit_frames > 0:
            self.__hit_frames -= 1
        if self.__hit_frames == 0:
            self.image = image_default
            self.image = self.image.convert()

        # Keep track of frames for managing time left on power ups
        if self.__power_up > 0:
            self.__power_up_frames += 1
        if self.__power_up == 1:
            if self.__power_up_frames == 90:
                self.__power_up = 0
        if self.__power_up == 2:
            if self.__power_up_frames == 450:
                self.__power_up = 0

class EnemyShip(pygame.sprite.Sprite):
    '''This class defines the sprite for enemy grunt and boss ships'''

    def __init__(self, screen, hit_points, worth):
        '''This initializer takes a screen surface as a parameter and initializes the image and rect attributes'''
        pygame.sprite.Sprite.__init__(self)

        # Define images and speed attributes depending on if grunt or boss sprite
        if worth == 3:
            self.__image_default = pygame.image.load("Sprites/enemyStarship1.png")
            self.__image_hit = pygame.image.load("Sprites/enemyStarship1Hit.png")
            self.__dying_images = []
            for x in range(0, 7):
                        self.__dying_images.append(pygame.image.load("Sprites/enemyExplosion" + str(x) + ".png"))
            self.image = self.__image_default
            self.__boss = False
        elif worth == 50:
            self.__image_default = pygame.image.load("Sprites/enemyStarshipBoss1.png")
            self.__image_hit = pygame.image.load("Sprites/enemyStarshipBoss1Hit.png")
            self.__dying_images = []
            for x in range(0, 7):
                self.__dying_images.append(pygame.image.load("Sprites/enemyBossExplosion" + str(x) + ".png"))
            self.image = self.__image_default
            self.__boss = True
        
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.__screen = screen
        self.__dying_frames = -1

        # Determine spawn position and x and y speed depending on if grunt or boss.
        if self.__boss:
            self.rect.bottom = 0
            self.rect.centerx = screen.get_width() / 2
            self.__dx = 3 * [-1, 1][random.randint(0, 1)]
            self.__dy = 2
        elif not self.__boss:
            self.rect.bottom = 0
            self.rect.right = random.randint(20, self.__screen.get_width())
            self.__dx = random.randint(3, 5)
            if self.rect.right > self.__screen.get_width() / 2:
                self.__dx = self.__dx * -1
            self.__dy = random.randint(3, 4)

        self.__hit_points = hit_points
        self.__worth = worth
        self.__hit_frames = 0

    def hit(self):
        '''This function sets the amount of frames used to time how long "hit" image of the ship should be displayed and subtracts a health point.'''
        self.__hit_frames = 4
        self.__hit_points -= 1
        
        # Used for death animation
        if self.__hit_points == 0:
            self.__dying_frames = 0
            return True

    def get_worth(self):
        '''This function returns how many points this sprite is worth.'''
        return self.__worth

    def get_dying_frames(self):
        '''This sprite returns the amount of dying animation frames that have passed'''
        return self.__dying_frames

    def is_boss(self):
        '''Returns if the sprite is a boss sprite or not.'''
        return self.__boss

    def update(self):
        '''This method will be called automatically to reposition the
        player sprite on the screen.'''
        # Sets image to "hit" images for a few frames if recently hit
        if self.__hit_frames == 4:
            self.image = self.__image_hit
            self.image = self.image.convert()
        if self.__hit_frames > 0:
            self.__hit_frames -= 1
        if self.__hit_frames == 0:
            self.image = self.__image_default
            self.image = self.image.convert()
        
        # Changes position of ship
        self.rect.left += self.__dx
        self.rect.bottom += self.__dy
        
        if self.__boss:
            # Stops y movement when the boss is completely visible on the screen
            if self.rect.top > 0:
                self.__dy = 0
            # Switches x direction if hits screen boundaries
            if self.rect.left < 0 or self.rect.right > self.__screen.get_width():
                self.__dx = -self.__dx
        elif not self.__boss:
            # Kills self if out of screen boundaries
            if self.rect.top > self.__screen.get_height() or self.rect.right < 0 or self.rect.left > self.__screen.get_width():
                self.kill()

        # Starts dying animation if health is 0
        if self.__dying_frames >= 0:
            self.image = self.__dying_images[self.__dying_frames]
            self.image = self.image.convert()
            position = self.rect.center  # Variable to store original position to center new image/image.rect
            self.rect = self.image.get_rect()
            self.rect.center = position
            if self.__dying_frames == 6:
                self.kill()
            self.__dying_frames += 1


class ScoreKeeper(pygame.sprite.Sprite):
    '''This class defines a label sprite to display the score.'''
    def __init__(self):
        '''This initializer loads the system font "Quantum of Mechanic.ttf", and
        sets the starting score to 0'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
 
        # Load font, and initialize the starting score and HP.
        self.__font = pygame.font.SysFont("arial", 30)
        self.__player_score = 0
        self.__player_health_points = 5
         
    def player_scored(self, value):
        '''This method adds value to the score for player'''
        self.__player_score += value
        
    def player_hit(self):
        '''This method subtracts 1 for player's life points'''
        self.__player_health_points -= 1

    def player_heal(self):
        '''This method adds 1 life for player'''
        self.__player_health_points += 1

    def winner(self):
        '''Returns True when the player reaches 450 points.
        This method returns False otherwise.'''
        if self.__player_score > 450:
            return True

    def loser(self):
        '''Returns True when the player reaches 2000 points.
        This method returns False otherwise.'''
        if self.__player_health_points < 0:
            return True
 
    def update(self):
        '''This method will be called automatically to display 
        the current score at the bottom of the game window.'''
        if self.__player_health_points == -1:
            self.__player_health_points = 0
        message = "Score: %d                                                   HP: %d" %\
                (self.__player_score, self.__player_health_points)
        self.image = self.__font.render(message, 1, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.left = 0
        self.rect.bottom = 480

class PowerUp(pygame.sprite.Sprite):
    '''This class defines the sprite for our Ball.'''

    def __init__(self, screen, ship_rect, variant):
        '''This initializer takes a screen surface as a parameter, initializes
        the image and rect attributes, and x,y direction of the ball.'''
        pygame.sprite.Sprite.__init__(self)

        # Set the images, speed and rect attributes for the powerup
        self.__font = pygame.font.SysFont("arial", 20)
        if variant == 1:
            self.image = pygame.image.load("Sprites/powerup1.png")
            self.__picked_up_image = self.__font.render("+Laser", 1, (255, 255, 255))
        elif variant == 2:
            self.image = pygame.image.load("Sprites/powerup2.png")
            self.__picked_up_image = self.__font.render("+Double Shot", 1, (255, 255, 255))
        elif variant == 3:
            self.image = pygame.image.load("Sprites/powerup3.png")
            self.__picked_up_image = self.__font.render("+HP", 1, (255, 255, 255))
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.centerx = ship_rect.centerx
        self.rect.top = ship_rect.top
        self.__dy = 3

        # Instance variables to keep track of the screen surface and variant
        self.__screen = screen
        self.__variant = variant
        self.__picked_up = -1

    def used(self):
        '''This function returns if the power up has been picked up to be used in the main function to prevent
        multiple power ups from one sprite while it plays "picked up" animation.'''
        if self.__picked_up >= 0:
            return True
        else:
            return False
        
    def picked_up(self):
        '''This function sets the power up to play picked up animation in update()'''
        self.__picked_up = 0        

    def get_variant(self):
        '''This function returns the power up variant'''
        return self.__variant

    def update(self):
        '''This method will be called automatically to reposition the sprite on the screen.'''
        if self.rect.top > self.__screen.get_height():
            self.kill()
        self.rect.top += self.__dy

        # Kills self after few frames of displaying "picked up" image
        if self.__picked_up >= 0:
            self.image = self.__picked_up_image
            self.__picked_up += 1
            if self.__picked_up == 20:
                self.kill()

class DisplayOverlap(pygame.sprite.Sprite):
    '''This class defines a label sprite to display the score.'''

    def __init__(self):
        '''This initializer loads the system font "Quantum of Mechanic.ttf", and
        sets the starting score to 0'''
        pygame.sprite.Sprite.__init__(self)

        # Load display overlap images
        self.__images = []
        self.__images.append(pygame.image.load("Sprites/beginningScreen.png"))
        self.__images.append(pygame.image.load("Sprites/gameOverWin.png"))
        self.__images.append(pygame.image.load("Sprites/gameOverLoss.png"))

    def set_display(self, display_value):
        '''This method sets the overlap image to display over the screen or moves the display off view of the screen.'''
        if display_value == -1:
            self.rect.bottom = 0
        else:
            self.image = self.__images[display_value]
            self.image = self.image.convert()
            self.rect = self.image.get_rect()
            self.rect.left = 0
            self.rect.top = 0
