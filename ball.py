"""Ball class for space basketball"""

__date__ = '3/4/22'
__version__ = 'V0.4'
__author__ = 'Nucleus team'

import pygame

class Ball:
    def __init__(self, game: 'Game', planets: ['Planet'], ini_x: int, 
                 ini_y: int, size: int = 20) -> None: 
        """ Iniitiates a ball object with a size (also indicates mass). 
        No initial speed or acceleration, initial pos based on params.
        """
        #Color constant
        self._ORANGE = (250,131,32)
        #set size (Deafult 20)
        self._radius = size
        #set initial pos
        self._pos = pygame.Vector2(ini_x,ini_y)
        #set initial spd/accel to 0
        self._spd = pygame.Vector2(0,0)
        self._accel = pygame.Vector2(0,0)
        
        #Store planets
        self._planets = planets
        #Store game screen
        self._game = game
        
        
        self.update()
        
    ##TODO: Add str, repr 
        
    ##Ideally, this is in a higher level class, like game/main
    def _sum_acceleration(ball: 'Ball', planets: ['Planet']) -> 'pygame.Vector2':
        """ Returns the sum of the accelerations exerted on the ball by
        each planet in the level.
        """
        total_accel = pygame.Vector2() #0,0
    
        for planet in planets:
            total_accel += planet.force_applied(ball.get_pos_tup(),
                                              ball.get_mass())
        
        return total_accel
    
        
    ##Might need to set bounds on acceleration/speed/position. Sometimes crashes
    def _update_pos(self, accel:'pygame.Vector2') -> None:
        """ Updates position based on speed of the ball (affected by planets). 
        Should be called on each game tick. 
        """   
        #Update accel (sum of forces) -> update spd -> update position
        self._accel += accel
        self._spd += self._accel
        self._pos += self._pos 
    
    def _draw(self) -> None:
        """Draws the ball on the screen. Should be called on each game tick.
        """
        ##With a few modifications, can use this to have the ball be an img
        #self.game.screen.blit(self.image, (self.x_pos, self.y_pos))        
        pygame.draw.circle(self._game.screen, self._ORANGE, self._pos, self._radius)
        
    def update(self) -> None:
        """ Updates the ball's state and displays it. 
        Should be called each game tick.
        """
        self._update_pos(self._sum_acceleration(self._planets))
        self._draw()
        
    def get_mass(self) -> int:
        """ Returns the mass of the ball.
        """
        return self._radius
    
    def get_pos(self) -> 'pygame.Vector2':
        """ Returns the current position of the ball as a 2D vector.
        """
        return self._pos    
    
    def get_pos_tup(self) -> tuple[int, int]:
        """ Returns the current position of the ball as a tuple 
        in the form (x, y).
        """
        return (self._pos.x, self._pos.y)
    
    