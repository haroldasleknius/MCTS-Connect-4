import pygame
import sys

#Menu class that stores button objects and displays them
class Menu():
    def __init__(self,screen):
        self.screen = screen
        self.buttons = []
        self.text = []
    
    #Takes in text,position,font,size,colour parameters
    #Used to add text that gets displayed on the screen
    def add_text(self, text, position, font, size, colour):
        font = pygame.font.SysFont(font,size)
        font_rendered = font.render(text, 1, colour)
        self.text.append((font_rendered, position))

    #Takes in button parameter
    #Adds the button object to the buttons array
    def add_button(self, button):
        self.buttons.append(button)

    #Method that draws every button and piece of text in the respective arrays
    def draw(self):
        for button in self.buttons:
            button.draw(self.screen)
        for text, position in self.text:
            self.screen.blit(text, position)

    #Takes in mouse_pos parameter
    #Using mouse_pos (x,y) to check if inside of a button
    #Updates the button accordingly
    def button_hover(self,mouse_pos):
        for button in self.buttons:
            button.hover(mouse_pos)

    #Takes in mouse_pos parameter
    #Uses this parameter (x,y) position to check if a button was clcik
    #Returns the text of button clicked else None
    def button_checks(self, mouse_pos):
        for button in self.buttons:
            if button.positioncheck(mouse_pos):
                return button.text_input
        return None

    #Menu loop that handles user interactions & updates the display
    #Returns the text_input of the button clicked
    def menu_loop(self):
        state = None
        while True:
            self.screen.fill((0,0,0))
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    state = self.button_checks(mouse_pos)
                if event.type == pygame.MOUSEMOTION:
                    self.button_hover(mouse_pos)

            self.draw()
            if state != None:
                break
            pygame.display.update()
        return state




