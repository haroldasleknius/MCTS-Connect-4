import pygame

#Button class that creates visible button objects
class Button():
    def __init__(self, pos_x, pos_y, image, text): 
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = image
        self.font = pygame.font.SysFont("Calibri", 50)
        self.image_box = self.image.get_rect(center=(self.pos_x, self.pos_y))
        self.text_input = text
        self.colour = ((255,255,255))
        self.text = self.font.render(self.text_input, True, (self.colour))
        self.text_box = self.text.get_rect(center=(self.pos_x, self.pos_y))

    #Takes parameter position
    #Checks if position (x,y) is in the button area
    #Returns True if it is
    def positioncheck(self, position):
        if position[0] in range(self.image_box.left, self.image_box.right) and position[1] in range(self.image_box.top, self.image_box.bottom):
            return True

    #Take parameter screen
    #Draws the button and text onto the screen
    def draw(self, screen):
        screen.blit(self.image, self.image_box)
        screen.blit(self.text, self.text_box)

    #Takes parameter position
    #Updates the colour of the text if the position (x,y)
    #is inside the button
    def hover(self, position):
        if self.positioncheck(position):
            self.colour = ((0,0,0))
        else:
            self.colour = ((255,255,255))
        self.text = self.font.render(self.text_input, True, (self.colour))