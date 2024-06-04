import pygame
import sys
from button import Button
from menu import Menu
from Connect4 import *

pygame.init()

screen = pygame.display.set_mode((875, 875))
pygame.display.set_caption("State")

#State class that handles various class object states essentially the glue
class State():
    def __init__(self,screen):
        self.screen = screen
        self.logic = Connect4Model()
        self.game = Connect4View(screen, self.logic)
        self.menu = Menu(self.screen)
        self.play_menu = Menu(self.screen)
        self.difficulty_menu = Menu(self.screen)
        self.state = "Menu"
        self.button_image = pygame.image.load("button.png")

    #Displays the menu_screen that the user first sees
    def menu_screen(self):
        image_resize = pygame.transform.scale(self.button_image, (400, 150))
        self.menu.add_text("Connect 4", (140,50), 'Calibri', 150, (255,255,255))
        self.menu.add_button(Button(437, 337, image_resize, "Play"))
        self.menu.add_button(Button(437, 537, image_resize, "Quit"))
        self.state = self.menu.menu_loop()

    #Displays the play_menu_screen that the user sees when they press play
    def play_screen(self):
        image_resize = pygame.transform.scale(self.button_image, (300, 150))
        self.play_menu.add_text("Select A Mode", (150, 100), 'Calibri', 100, (255,255,255))
        self.play_menu.add_button(Button(237, 437, image_resize, "Singleplayer"))
        self.play_menu.add_button(Button(637, 437, image_resize, "Multiplayer"))
        self.play_menu.add_text("OR", (400, 415), 'Calibri', 60, (255,255,255))
        self.state = self.play_menu.menu_loop()

    #State loop that controls the state of the program, switching between menus and initialising the game
    def state_loop(self):
        while True:
            if self.state == "Menu":
                self.menu_screen()
            elif self.state == "Play":
                pygame.time.wait(200)
                self.play_screen()
            elif self.state == "Singleplayer":
                self.game.game_loop_singleplayer(5000)
            elif self.state == "Multiplayer":
                pygame.time.wait(200)
                self.game.game_loop_multiplayer()
            elif self.state == "Quit":
                pygame.quit()
                sys.exit()


state = State(screen)
state.state_loop()