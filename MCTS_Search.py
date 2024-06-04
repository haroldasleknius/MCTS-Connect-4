import numpy
from copy import deepcopy
import math
import random
import time
from Node import Node


#MCTS_Search class that uses Node objects for the Monte Carlo Tree Search
class MCTS_Search:
    def __init__(self,game_state, player):
        self.game_state = game_state
        self.player = player
        self.root = Node(self.game_state, None, None, self.player, self.game_state.current_player)
     
     #Using node parameter
     #It chooses the highest UCB value child node
     #Returns that child node
    def Best_UCB_Value(self, node):
        best_ucb_value = float("-inf")
        best_child_node = None
        for child in node.childNodes.values():
            ucb_value = child.Node_UCB()
            if ucb_value > best_ucb_value:
                best_ucb_value = ucb_value
                best_child_node = child

        return best_child_node

    #Selection phase of MCTS
    #Goes from the root node to the next available leaf node
    #returns the highest UCB leaf node
    def selection(self):
        node = self.root
        while node.terminal != True:
            if node.is_fully_expanded():
                node = self.Best_UCB_Value(node)
            else:
                return self.expansion(node)
        return node

    #Using the parameter node
    #It expands the tree by adding a child node
    #Returns the newly expanded node
    def expansion(self,node):
        new_node = node.add_child()
        return new_node
    
    #Taking in the newly expanded node
    #It selects random moves until a terminal state has been reached
    #Returning a score depending on the W/D/L
    def simulation(self, node):
        state = deepcopy(node.game_state)
        current_player = node.current_player
        while True:
            if state.game_drawn() or state.four_connected(1) or state.four_connected(2):
                break
            valid_moves = state.get_valid_moves()
            chosen_column = random.choice(valid_moves)
            row = state.next_available_row(chosen_column)
            state.place_piece(row, chosen_column, current_player)
            current_player = 3 - current_player  # Alternate turns

        if state.four_connected(node.mcts_player):
            return 1  
        elif state.four_connected(3 - node.mcts_player):
            return -2 
        else:
            return 0.5 

    #using the node and result parameter
    #it propagates back up the tree updating the statistics at each node
    def backpropagation(self, node, result):
        current_node = node
        while current_node is not None:
            current_node.update_statistics(result)
            current_node = current_node.parentNode

    #Takes in iteration parameter
    #Which is used in the for loop to build the tree over each iteration
    def search(self, iteration):
        for x in range(iteration):
            node = self.selection()
            result = self.simulation(node)
            self.backpropagation(node, result)
            
    #returns the move with the highest win ratio
    def next_move(self):
        action, node = max(self.root.childNodes.items(), key = lambda item: (item[1].score / item[1].visits))
        return action