import pygame

class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.x = x
        self.y = self.original_img = image
        self.image = pygame.transform.scale(self.original_img, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.clicked = False

    def update_offset(self, x, y, scale):
        self.rect.x = x
        self.rect.y = y
        self.clicked = False
        # Update image size based on scale
        self.image = pygame.transform.scale(self.original_img, 
            (int(self.original_img.get_width() * scale), 
             int(self.original_img.get_height() * scale)))
        self.rect = self.image.get_rect(center=(x, y))
        
    def draw(self, surface):
        action = False
        
        # get mouse position
        pos = pygame.mouse.get_pos()
        
        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True
                
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
            
        # draw button on screen
        surface.blit(self.image, (self.rect.x, self.rect.y))
        
        return action