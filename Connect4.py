import numpy
import pygame
import sys
import math
import time
from Node import Node
from MCTS_Search import MCTS_Search
from copy import deepcopy

#Connect4Model class that represents the game logic
class Connect4Model:
    def __init__(self):
        self.board_row = 6
        self.board_column = 7
        self.board = numpy.zeros((self.board_row, self.board_column))
        self.current_player = 1

    #Returns a list of columns that are able to be placed inside
    def get_valid_moves(self):
        valid_moves = []
        for column in range(self.board_column):
            if self.valid_column_check(column):
                valid_moves.append(column)
        return valid_moves
    
    #Returns the total number of pieces on the board
    def get_total_pieces(self):
        return numpy.count_nonzero(self.board)
    
    #Takes in piece parameter
    #parameter used to check if any obvious wins or losses are visible
    #Returns column of obvious win/loss else None
    def one_away_from_win_or_loss(self,piece):
            columns = self.get_valid_moves()
            for column in columns:
                row = self.next_available_row(column)
                self.place_piece(row, column, piece)
                if self.four_connected(piece):
                    self.place_piece(row, column, 0)
                    return column
                self.place_piece(row, column, 3 - piece)
                if self.four_connected(3 - piece):
                    self.place_piece(row, column, 0)
                    return column
                self.place_piece(row, column, 0)
            return None
    
    #Takes column parameter
    #Returns True or False if there is space in the column
    def valid_column_check(self, column):
        return self.board[5][column] == 0
    
    #Method that changes the current player
    def switch_player(self):
        if self.current_player == 1:
            self.current_player = 2
        else:
            self.current_player = 1

    #Takes in column parameter
    #Returns the next free row within the column
    def next_available_row(self, column):
        for row in range(self.board_row):
            if self.board[row][column] == 0:
                return row

    #Takes in row, column and piece parameters
    #Places the piece in the specified row and column
    def place_piece(self, row, column, piece):
        self.board[row][column] = piece

    #Takes in piece parameters
    #Returns True if there are 4 pieces connected vertically, horizontally or diagonally
    def four_connected(self, piece):
        for column in range(self.board_column - 3):
            for row in range(self.board_row):
                if self.board[row][column] == piece and self.board[row][column + 1] == piece and self.board[row][column + 2] == piece and self.board[row][column + 3] == piece: 
                    return True
                
        for column in range(self.board_column):
            for row in range(self.board_row - 3):
                if self.board[row][column] == piece and self.board[row + 1][column] == piece and self.board[row + 2][column] == piece and self.board[row + 3][column] == piece:
                    return True

        for column in range(self.board_column - 3):
            for row in range(self.board_row - 3):
                if self.board[row][column] == piece and self.board[row + 1][column + 1] == piece and self.board[row + 2][column + 2] == piece and self.board[row + 3][column + 3] == piece:
                    return True

        for column in range(self.board_column-3):
            for row in range(3, self.board_row):
                if self.board[row][column] == piece and self.board[row - 1][column + 1] == piece and self.board[row - 2][column + 2] == piece and self.board[row - 3][column + 3] == piece:
                    return True

    #Returns True if the board is full else False
    def game_drawn(self):
        return numpy.all(self.board != 0)

#Connect4View class that handles the GUI aspect of the game
class Connect4View:
    def __init__(self,screen,model):
        self.screen = screen
        self.model = model
        self.rgb_blue = (0, 0, 255)
        self.rgb_black = (0, 0, 0)
        self.rgb_red = (255, 0, 0)
        self.rgb_yellow = (255, 255, 0)
        self.SQUARESIZE = 125
        self.width = self.model.board_column * self.SQUARESIZE 
        self.height = self.model.board_column * self.SQUARESIZE
        self.RADIUS = int(self.SQUARESIZE / 2 - 5)
        self.font = pygame.font.SysFont("calibri",50)
        self.moving_left = False
        self.moving_right = False
        self.currentx = 438

    #Method thats draws the current state of the board
    def draw_board(self):
        for column in range(self.model.board_column):
            for row in range(self.model.board_row):
                pygame.draw.rect(self.screen, self.rgb_blue, (column * self.SQUARESIZE, row * self.SQUARESIZE + self.SQUARESIZE, self.SQUARESIZE, self.SQUARESIZE))
                pygame.draw.circle(self.screen, self.rgb_black, (int(column * self.SQUARESIZE + self.SQUARESIZE / 2), int(row * self.SQUARESIZE + self.SQUARESIZE + self.SQUARESIZE / 2)), self.RADIUS)
                
        for column in range(self.model.board_column):
            for row in range(self.model.board_row):
                if self.model.board[row][column] == 1:
                    pygame.draw.circle(self.screen, self.rgb_red, (int(column * self.SQUARESIZE + self.SQUARESIZE / 2), self.height - int(row * self.SQUARESIZE + self.SQUARESIZE / 2)), self.RADIUS)
                elif self.model.board[row][column] == 2:
                    pygame.draw.circle(self.screen, self.rgb_yellow, (int(column * self.SQUARESIZE + self.SQUARESIZE / 2), self.height - int(row * self.SQUARESIZE + self.SQUARESIZE / 2)), self.RADIUS)
        pygame.display.update()

    #Takes posx parameter
    #Draws the piece on the top of the screen following mouse movement
    def mousemotion(self,posx):
        pygame.draw.rect(self.screen, self.rgb_black, (0,0, self.width, self.SQUARESIZE))
        if self.model.current_player == 1:
            pygame.draw.circle(self.screen, self.rgb_red, (posx, int(self.SQUARESIZE/2)), self.RADIUS)
            self.currentx = posx
        else:
            pygame.draw.circle(self.screen, self.rgb_yellow, (posx, int(self.SQUARESIZE/2)), self.RADIUS)
            self.currentx = posx   

    #Takes in choice, player, colour and position parameter
    #Using the parameters it generates the next available row
    #Places the piece using the parameters
    #Returns True if the game was won/drawn else False
    def gameplaying(self, choice, player, colour, position):
        row = self.model.next_available_row(choice)
        self.model.place_piece(row, choice, player)
        if self.model.four_connected(player):
            label = self.font.render("Player {} won".format(player), 1, colour)
            self.screen.blit(label, (100,10))
            return True
        if self.model.game_drawn():
            label = self.font.render("The game has been drawn", 1, colour)
            self.screen.blit(label, (100,10))
            return True
        pygame.draw.circle(self.screen, colour, (position, int(self.SQUARESIZE / 2)), self.RADIUS)

    #Takes in direction and colour parameters
    #Updates the class variable using the direction parameter
    #Draws the newly moved piece using colour parameter
    def moving(self, direction, colour):
        self.currentx = self.currentx + direction
        pygame.draw.circle(self.screen, colour, (self.currentx, int(self.SQUARESIZE / 2)), self.RADIUS)

    #Game loop that handles user interactions, updates the screen, plays the game essentially for 2 human players
    def game_loop_multiplayer(self):
        running = True
        while running:
            self.draw_board()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEMOTION:
                    self.mousemotion(event.pos[0])
                    pygame.display.update()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    choice = int(math.floor(event.pos[0] / self.SQUARESIZE))
                    if self.model.valid_column_check(choice):
                        if self.model.current_player == 1:
                            if self.gameplaying(choice, 1, self.rgb_yellow, event.pos[0]):
                                running = False
                        else:
                            if self.gameplaying(choice, 2, self.rgb_red, event.pos[0]):
                                running = False
                        self.draw_board()
                        self.model.switch_player()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.moving_left = True
                    if event.key == pygame.K_RIGHT:
                        self.moving_right = True
                    if event.key == pygame.K_SPACE:
                        choice = int(math.floor(self.currentx / self.SQUARESIZE))
                        if self.model.valid_column_check(choice):
                            if self.model.current_player == 1:
                                if self.gameplaying(choice, 1, self.rgb_yellow, self.currentx):
                                    running = False
                            else:
                                if self.gameplaying(choice, 2, self.rgb_red, self.currentx):
                                    running = False
                            self.draw_board()
                            self.model.switch_player()
                
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.moving_left = False
                    if event.key == pygame.K_RIGHT:
                        self.moving_right = False
            
            if self.moving_left and self.currentx - 10 > self.RADIUS:
                pygame.draw.rect(self.screen, self.rgb_black, (0,0, self.width, self.SQUARESIZE))
                if self.model.current_player == 1:
                    self.moving(-15, self.rgb_red)
                else:
                    self.moving(-15, self.rgb_yellow)

            if self.moving_right and self.currentx < self.width - self.RADIUS:
                pygame.draw.rect(self.screen, self.rgb_black, (0,0, self.width, self.SQUARESIZE))
                if self.model.current_player == 1:
                    self.moving(15, self.rgb_red)
                else:
                    self.moving(15, self.rgb_yellow)

            pygame.display.update()
            pygame.time.Clock().tick(60) 
            if running == False:
                pygame.time.wait(10000)


    #Game loop for handling user interactions, updating the screen, playing the game for 1 human player and 1 mcts agent
    #Takes in iterations parameter which is used to indicate how many simulations the mcts agent runs
    def game_loop_singleplayer(self,iterations):
        running = True
        while running:
            self.draw_board()
            if self.model.current_player == 1:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()

                    if event.type == pygame.MOUSEMOTION:
                        self.mousemotion(event.pos[0])
                        pygame.display.update()

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        choice = int(math.floor(event.pos[0] / self.SQUARESIZE))
                        if self.model.valid_column_check(choice):
                            if self.model.current_player == 1:
                                if self.gameplaying(choice, 1, self.rgb_yellow, event.pos[0]):
                                    running = False
                            self.draw_board()
                            self.model.switch_player()


                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            self.moving_left = True
                        if event.key == pygame.K_RIGHT:
                            self.moving_right = True
                        if event.key == pygame.K_SPACE:
                            choice = int(math.floor(self.currentx / self.SQUARESIZE))
                            if self.model.valid_column_check(choice):
                                if self.model.current_player == 1:
                                    if self.gameplaying(choice, 1, self.rgb_yellow, self.currentx):
                                        running = False
                                self.draw_board()
                                self.model.switch_player()
                    
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_LEFT:
                            self.moving_left = False
                        if event.key == pygame.K_RIGHT:
                            self.moving_right = False
                
                if self.moving_left and self.currentx - 10 > self.RADIUS:
                    pygame.draw.rect(self.screen, self.rgb_black, (0,0, self.width, self.SQUARESIZE))
                    if self.model.current_player == 1:
                        self.moving(-15, self.rgb_red)
                    else:
                        self.moving(-15, self.rgb_yellow)

                if self.moving_right and self.currentx < self.width - self.RADIUS:
                    pygame.draw.rect(self.screen, self.rgb_black, (0,0, self.width, self.SQUARESIZE))
                    if self.model.current_player == 1:
                        self.moving(15, self.rgb_red)
                    else:
                        self.moving(15, self.rgb_yellow)
            else:
                copy = deepcopy(self.model)
                mcts = MCTS_Search(copy, self.model.current_player)
                mcts.search(iterations)
                column = mcts.next_move()
                if self.gameplaying(column, self.model.current_player, self.rgb_red, self.currentx):
                    running = False
                self.draw_board()
                self.model.switch_player()

            pygame.display.update()
            pygame.time.Clock().tick(60) 
            if running == False:
                pygame.time.wait(10000)