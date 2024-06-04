import unittest
import numpy
from Node import Node
from MCTS_Search import MCTS_Search
from Connect4 import *

class TestCase(unittest.TestCase):
    def setUp(self):
        self.game_state = Connect4Model()
        self.MCTS_Search = MCTS_Search(self.game_state, 1)

    #test that leaf node is successfully selected, then expanded due to expansion being in the selection code
    def test_selection_expansion_from_root(self):
        node = self.MCTS_Search.selection()
        self.assertEqual(self.MCTS_Search.root, node.parentNode)

    #test that when each node is fully expanded, selection will return best UCB value and expand it
    def test_selection_expansion_UCB(self):
        moves = self.MCTS_Search.game_state.get_valid_moves()
        for move in moves:
            self.MCTS_Search.expansion(self.MCTS_Search.root)
        best_ucb_node = self.MCTS_Search.Best_UCB_Value(self.MCTS_Search.root)
        ucb_node_returned = self.MCTS_Search.selection().parentNode
        self.assertEqual(best_ucb_node, ucb_node_returned)

    def test_simulation_win(self):
        self.game_state.place_piece(5, 0, 2)
        self.game_state.place_piece(5, 1, 1)
        self.game_state.place_piece(5, 2, 2)
        self.game_state.place_piece(5, 3, 1)
        self.game_state.place_piece(5, 4, 2)
        self.game_state.place_piece(5, 5, 1)
        self.game_state.place_piece(2, 6, 1)
        self.game_state.place_piece(3, 6, 1)
        self.game_state.place_piece(4, 6, 1)
        self.game_state.current_player = 1
        node = Node(self.game_state, None, None, 1, self.game_state.current_player)
        result = self.MCTS_Search.simulation(node)
        self.assertEqual(result, 1)

    def test_simulation_loss(self):
        self.game_state.place_piece(5, 0, 2)
        self.game_state.place_piece(5, 1, 1)
        self.game_state.place_piece(5, 2, 2)
        self.game_state.place_piece(5, 3, 1)
        self.game_state.place_piece(5, 4, 2)
        self.game_state.place_piece(5, 5, 1)
        self.game_state.place_piece(2, 6, 2)
        self.game_state.place_piece(3, 6, 2)
        self.game_state.place_piece(4, 6, 2)
        self.game_state.current_player = 2
        node = Node(self.game_state, None, None, 1, self.game_state.current_player)
        result = self.MCTS_Search.simulation(node)
        self.assertEqual(result, -2)

    def test_simulation_draw(self):
        for row in range(6):
            for column in range(7):
                self.game_state.place_piece(row, column, 3)
        node = Node(self.game_state, None, None, 1, self.game_state.current_player)
        result = self.MCTS_Search.simulation(node)
        self.assertEqual(result, 0.5)

    #test to check that backpropagation properly updates up to the root
    def test_backpropagation(self):
        node = self.MCTS_Search.selection()
        result = self.MCTS_Search.simulation(node)
        visits = self.MCTS_Search.root.visits
        score = self.MCTS_Search.root.score
        self.MCTS_Search.backpropagation(node, result)
        self.assertGreater(self.MCTS_Search.root.visits, visits)
        self.assertNotEqual(self.MCTS_Search.root.score, score)


if __name__ == '__main__':
    unittest.main()