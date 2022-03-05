import pygame

class Player(pygame.sprite.Sprite):

    

    def shot(self):
        
        pygame.mouse.set_visible()
        
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                initial_pos = pygame.mouse.get_rel()
            if event.type == MOUSEBUTTONUP:
                new_pos = pygame.mouse.get_rel()
        
    
        initial_speed = Vector2(new_pos)
    