import pygame
import math

__date__ = '3/5/22'
__version__ = 'V0.3'
__author__ = 'Nucleus team'



class Planet(pygame.sprite.Sprite):
    def __init__(self, game: 'Game', image: 'pygame.Surface', 
                 size, x_pos, y_pos) -> None:
        self._SIZE = size
        
        #Initialise sprite image (might change to sheet later)
        self.image = image   
        ##A way to scale images later:
        #self.image = pygame.transform.scale(image, (size, size))
        
        #Hitbox attributes. Mask prefered
        self.rect = (self._SIZE, self._SIZE)
        self._radius = self._SIZE/2
        self.mask = pygame.mask.from_surface(self.image)        
        
        self.game = game
        self._pos = pygame.Vector2(x_pos, y_pos)
        #Used as mass


    def accel_applied(self, pos:'pygame.Vector2', mass: int) -> 'pygame.Vector2':
        """Returns the amount of acceleration applied to a given object
        Args:
            pos (Vector2): position of object
            mass (int): mass of object
        Returns:
            tuple: x and y components of the force 
        """
        #Higher factor means more force applied (1 is default)
        ACCEL_FACTOR = 1
        
        center = self.find_img_center()
        x_distance = center.x - pos.x
        y_distance = center.y - pos.y
        
        #if distance is +ve, planet coord > object coord. 
        #Should increase object coord
        x_sign = 1 if x_distance >= 0 else -1
        y_sign = 1 if y_distance >= 0 else -1
        
        #Technically, should never divide by 0 when collisions exist. 
        #So as a temp measure, set x_distance to 1 IFF it is eequal to 0
        x_distance += 1 if x_distance == 0 else 0
        angle = math.atan(y_distance/x_distance)

        total_distance = self.pythag(center, pos) 
        #see prev comment about zero div
        total_distance += 1 if total_distance == 0 else 0
        total_accel = ACCEL_FACTOR * self.area / (total_distance * mass)
        
        return pygame.math.Vector2(total_accel*math.cos(angle) * x_sign, 
                                   total_accel*math.sin(angle) * y_sign)


    def find_img_center(self) -> 'pygame.Vector2':
        """Returns the center of the image
        Returns:
            Vector2: center of the image in 2D vector format [x,y]
        """
        #Not quite true I think.
        width, height = self.image.get_size()
        return pygame.Vector2(self._pos.x + width / 2, 
                              self._pos.y +  height / 2)

    @staticmethod
    def pythag(pos1: 'pygame.Vector2', pos2:'pygame.Vector2') -> float:
        """returns the distance between two points
        Args:
            pos1 (tuple): position of the 1st object in x,y format
            pos2 (tuple): position of the 2nd object in x,y format
        Returns:
            float: distance between the points
        """
        return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[0])**2)

    def draw_planet(self) -> None:
        """Draws the planet on the screen
        """
        self.game.screen.blit(self.image, (self._pos.x, self._pos.y))
        
        ##draw circle draws around the center. 
        ##Blit takes position as top left corner of image
        #pygame.draw.circle(self.game.screen, (255,255,255), 
                           #(self.x_pos, self.y_pos), 10)        
                           
    def get_mass(self) -> int:
        """ Returns the mass of the planet.
        """
        return math.pi * math.pow((self._radius/2), 2)    