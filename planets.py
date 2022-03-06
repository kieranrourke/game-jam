import pygame
import math

__date__ = '3/5/22'
__version__ = 'V0.4'
__author__ = 'Nucleus team'

class Planet(pygame.sprite.Sprite):
    def __init__(self, game: 'Game', image: 'pygame.Surface', 
                 size, x_pos, y_pos) -> None:
        #Superclass constructor
        pygame.sprite.Sprite.__init__(self)
        
        #Initialise sprite image (might change to sheet later)
        self._SIZE = size
        
        #self.image = image   #Std. image storing
        #A way to scale images later:
        self.image = pygame.transform.scale(image, (size, size))
        
        self._pos = pygame.Vector2(x_pos, y_pos)
        
        #Hitbox attributes. Mask prefered
        self.rect = pygame.Rect(tuple(self._pos), (self._SIZE, self._SIZE))
        self.radius = self._SIZE/2
        self.mask = pygame.mask.from_surface(self.image)      
            
        self.game = game        

    def accel_applied(self, pos:'pygame.Vector2', other_mass: int) -> 'pygame.Vector2':
        """Returns the amount of acceleration applied to a given object
        Args:
            pos (Vector2): position of object
            mass (int): mass of object
        Returns:
            tuple: x and y components of the force 
        """
        #Higher factor means more force applied (1 is default)
        GRAV_FACTOR = 1
        
        center = self.get_center()
        
        #Normalized direction of gravity
        grav_dir = (center - pos).normalize()

        total_distance = self.pythag(center, pos) 
        #Symptomatic of another problem, should not happen
        if total_distance == 0:
            raise ArithmeticError("total_distance is 0, center == pos")
        
        grav_mag = GRAV_FACTOR * self.get_mass() / (total_distance * other_mass)
        

        return pygame.math.Vector2(grav_mag * grav_dir.x, 
                                   grav_mag * grav_dir.y)

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
                   
    ##Accessors        
    def get_mass(self) -> int:
        """ Returns the mass of the planet.
        """
        return math.pi * math.pow((self.radius), 2)   
    
    def get_size(self) -> int:
        """ Returns the mass of the planet.
        """
        return self._SIZE
    
    def get_pos(self) -> 'pygame.Vector2':
        """ Returns the position vector of the planet.
        """
        return self._pos
    
    def get_pos_tup(self) -> tuple[float, float]:
        """ Returns the position vector of the planet.
        """
        return self._pos.x, self._pos.y   
    
    def get_center(self) -> 'pygame.Vector2':
        """Returns the center of the image
        Returns:
            Vector2: center of the image in 2D vector format [x,y]
        """
        width, height = self.image.get_size()
        return pygame.Vector2(self._pos.x + width / 2, 
                              self._pos.y +  height / 2)    
