import unittest
import pygame
from Connect4 import *

class TestCase(unittest.TestCase):
    #Before each test, a fresh Connect4 game is setup
    def setUp(self):
        pygame.init()
        self.game = Connect4Model()
    
    def tearDown(self):
        pygame.quit()
    
    #Tests place_piece method
    #Checking if the board gets updated with a piece
    #Checking if the piece is placed at the correct position
    def test_place_piece(self):
        self.game.place_piece(3, 6, 1)
        self.assertEqual(self.game.board[3][6], 1)

    #Tests valid_column_check method
    #Checking if it returns True for the case that the column is not full
    def test_valid_column_check_true(self):
        self.game.place_piece(0, 3, 1)
        self.assertTrue(self.game.valid_column_check(3))

    #Tests valid_column_check method
    #Checking if it returns False for the case that the column is full
    def test_valid_column_check_false(self):
        for row in range(self.game.board_row): 
            self.game.place_piece(row, 3, 1)
        self.assertFalse(self.game.valid_column_check(3))

    #Tests next_available_row method
    #Checking if it returns the correct next available row on the column
    def test_next_available_row(self):
        self.game.place_piece(0, 3, 1)
        row = self.game.next_available_row(3)
        self.assertEqual(row, 1)

    #Tests four_connected method
    #Checking if it works correctly horizontally
    def test_four_connected_horizontally(self):
        for column in range(4):
            self.game.place_piece(0, column, 1)
        self.assertTrue(self.game.four_connected(1))

    #Tests four_connected method
    #Checking if it works correctly vertically
    def test_four_connected_vertically(self):
        for row in range(4):
            self.game.place_piece(row, 0, 1)
        self.assertTrue(self.game.four_connected(1))

    #Tests four_connected method
    #Checking if it works correctly diagonally
    def test_four_connected_diagonally(self):
        for x in range(4):
            self.game.place_piece(x, x, 1)
        self.assertTrue(self.game.four_connected(1))

    #Tests game_drawn method
    #When all the pieces are filled on the board
    def test_game_drawn_full(self):
        for row in range(6):
            for column in range(7):
                self.game.place_piece(row, column, 1)
        self.assertTrue(self.game.game_drawn())

    #Tests game_drawn method
    #When only some pieces are empty
    def test_game_drawn_not_full(self):
        for row in range(5):
            for column in range(4):
                self.game.place_piece(row, column, 1)
        self.assertFalse(self.game.game_drawn())

    #Tests game_drawn method
    #When the board is fully empty
    def test_game_drawn_empty(self):
        self.assertFalse(self.game.game_drawn())

if __name__ == '__main__':
    unittest.main()