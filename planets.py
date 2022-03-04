import pygame
import math




class Planet:
    def __init__(self, image, game, x_size, y_size, x_pos, y_pos) -> None:
        self.image = pygame.transform.scale(image, (x_size, y_size))
        self.game = game
        self.x_pos = x_pos 
        self.y_pos = y_pos
        self.area = math.pi * math.pow((x_size/2), 2)


    def force_applied(self, pos:tuple, mass:int) -> tuple:
        """Returns the amount of force applied to a given position

        Args:
            pos (tuple): position of the ball 
            mass (int): mass of the ball

        Returns:
            tuple: x and y components of the force 
        """
        center = self.find_center()
        x_distance = center[0] - pos[0]
        y_distance = center[1] - pos[1]
        angle = math.atan(y_distance/x_distance)

        total_distance = self.pythag(center, pos) 
        total_force = self.area/(total_distance * mass)

        return pygame.math.Vector2(total_force*math.cos(angle), total_force*math.sin(angle))


    def find_center(self) -> tuple:
        """Returns the center of the circle

        Returns:
            tuple: center of the circle in tuple format (x,y)
        """
        return (self.x_pos/2, self.y_pos/2)

    
    def pythag(pos1: tuple, pos2:tuple) -> float:
        """returns the distance between two points

        Args:
            pos1 (tuple): position of the 1st object in x,y format
            pos2 (tuple): position of the 2nd object in x,y format

        Returns:
            float: distance between the points
        """
        return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[0])**2)

        
