# Import the pygame module

import pygame


# Import pygame.locals for easier access to key coordinates

# Updated to conform to flake8 and black standards

from pygame.locals import (
    MOUSEBUTTONUP,
    MOUSEBUTTONDOWN,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,

)

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Define a player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):

    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((75, 25))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)   
                 
        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
    
    
    def update_mouse(self, pressed_mouse):
        if pressed_mouse[MOUSEBUTTONUP]:
            self.rect.move_ip(5,0) 
        if pressed_mouse[MOUSEBUTTONDOWN]:
            self.rect.move_ip(0,5)         
        
        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT    

# Initialize pygame
pygame.init()

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Instantiate player. Right now, this is just a rectangle.
player = Player()

# Variable to keep the main loop running
running = True

# Position tuples
i_m_pos = (0,0)
n_m_pos = (0,0)

# Main loop
while running:

    # for loop through the event queue
    for event in pygame.event.get():
        # Check for KEYDOWN event
        if event.type == KEYDOWN:
            # If the Esc key is pressed, then exit the main loop
            if event.key == K_ESCAPE:
                running = False
                       
        # Check for QUIT event. If QUIT, then set running to false.
        elif event.type == QUIT:
            running = False
            pygame.quit()
            
        if event.type == MOUSEBUTTONDOWN:
            i_m_pos = pygame.mouse.get_rel()         
            
        if event.type == MOUSEBUTTONUP:
            new_m_pos = pygame.mouse.get_rel()
    
        i_vec = pygame.Vector2(i_m_pos)
        n_vec = pygame.Vector2(n_m_pos)
        speed = n_vec - i_m_pos 
        
        print(speed)        

    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()
    pressed_mouse = pygame.event.get()
    
    # Update the player sprite based on user keypresses
    player.update(pressed_keys)
    player.update_mouse(pressed_mouse)
    
    
    # Fill the screen with black
    screen.fill((0, 0, 0))

    # Draw the player on the screen
    screen.blit(player.surf, player.rect)

    # Update the display
    pygame.display.flip()
