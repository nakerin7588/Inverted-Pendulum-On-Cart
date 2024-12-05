import pygame

class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.x = x
        self.y = y
        self.original_img = image
        self.image = pygame.transform.scale(self.original_img, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def update_offset(self, x_offset, y_offset, new_scale):
        """Update button offset while maintaining aspect ratio"""
        self.x = x_offset
        self.y = y_offset
        new_width = int(self.original_img.get_width() * new_scale)
        new_height = int(self.original_img.get_height() * new_scale)
        self.image = pygame.transform.scale(self.original_img, (new_width, new_height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        self.scale = new_scale
        
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