import unittest
import numpy
from Node import Node
from Connect4 import *

class TestCase(unittest.TestCase):
    def setUp(self):
        self.game_state = Connect4Model()
        self.root_node = Node(self.game_state, None, None, 1, 1)

    def test_add_child(self):
        self.root_node.add_child(None)
        self.assertEqual(len(self.root_node.childNodes), 1)

    def test_is_fully_expanded_true(self):
        moves = self.root_node.game_state.get_valid_moves()
        for move in moves:
            self.root_node.add_child(None)
        self.assertTrue(self.root_node.is_fully_expanded())

    def test_is_fully_expanded_false(self):
        for move in range(2):
            self.root_node.add_child(None)
        self.assertFalse(self.root_node.is_fully_expanded())

    def test_update_statistics(self):
        self.root_node.update_statistics(1)
        self.assertEqual(self.root_node.score, 1)
        self.assertEqual(self.root_node.visits, 1)

    def test_determine_outcome_win(self):
        for column in range(4):
            self.root_node.game_state.place_piece(0, column, 1)
        self.assertTrue(self.root_node.determine_outcome())
        self.assertEqual(self.root_node.score, 1)

    def test_determine_outcome_loss(self):
        for column in range(4):
            self.root_node.game_state.place_piece(0, column, 2)
        self.assertTrue(self.root_node.determine_outcome())
        self.assertEqual(self.root_node.score, -2)

    def test_determine_outcome_draw(self):
        for row in range(6):
            for column in range(7):
                self.root_node.game_state.place_piece(row, column, 3)
        self.assertTrue(self.root_node.determine_outcome())
        self.assertEqual(self.root_node.score, 0.5)

    def test_Node_UCB_no_visits(self):
        self.assertEqual(self.root_node.Node_UCB(), float('inf'))

    def test_Node_UCB_with_parents(self):
        child_node = self.root_node.add_child(None)
        self.root_node.visits = 10
        child_node.visits = 3
        child_node.score = 7

        ucb = (child_node.score / child_node.visits) + (2 * math.sqrt(math.log(self.root_node.visits) / child_node.visits))
        self.assertEqual(child_node.Node_UCB(), ucb)

if __name__ == '__main__':
    unittest.main()