import numpy
from copy import deepcopy
import math
import random

#Node class used to store the game_state and other variables
#for the Monte Carlo Tree Search algorithm
class Node:
    def __init__(self, game_state, parentNode, action, mcts_player, current_player):
        self.game_state = game_state
        self.parentNode = parentNode #Equates to None unless has parent
        self.action = action #the move from the parent node that led to this node
        self.mcts_player = mcts_player #whether the mcts is acting as player 1 or 2
        self.current_player = current_player #whos turn it is as a player
        self.childNodes = {} #dictionary to hold the children nodes
        self.visits = 0 #how many times this node has been visited
        self.score = 0 #store wins as +1 and draws as +0.5 loss = 0 
        self.terminal = self.determine_outcome()


    #Takes in result parameter
    #Which is used to update the score
    def update_statistics(self,result):
        self.score += result
        self.visits  += 1
        
    #Returns True if the node is in a terminal state
    def determine_outcome(self):
        #mcts won
        if self.game_state.four_connected(self.mcts_player):
            self.update_statistics(1)
            return True
        #mcts lost
        if self.game_state.four_connected(3 - self.mcts_player):
            self.update_statistics(-2)
            return True
        #if not won or lost and board is full its a draw
        if self.game_state.game_drawn():
            self.update_statistics(0.5)
            return True
        
        return False
    
    #Returns the UCB value of the node
    def Node_UCB(self):
        #if node hasn't been visited before
        if self.visits == 0:
            return float('inf')
        
        if self.parentNode != None: #incase its a root node
            parentNodeVisits = self.parentNode.visits
        else:
            parentNodeVisits = 1

        return (self.score / self.visits) + (2 * math.sqrt(math.log(parentNodeVisits) / self.visits))
     
     #Using the column parameter, it creates the next game_state
     #returns it as a copy
    def next_state(self,column):
        copy = deepcopy(self.game_state)
        row = copy.next_available_row(column)
        copy.place_piece(row, column, self.current_player)
        return copy

    def next_state_critical(self,column,player):
        copy = deepcopy(self.game_state)
        row = copy.next_available_row(column)
        copy.place_piece(row, column, player)
        return copy


    #Adds a child node to the current node, depending if its a critical move
    #i.e 1 move away from win/loss
    #if not it prioritises creating a child node on the centre of the board
    #returning the newly created child_node
    def add_child(self):
        center_column = self.game_state.board_column // 2
        possible_moves = sorted(self.game_state.get_valid_moves(), key=lambda x: abs(x - center_column))
        for move in possible_moves:
            copy = self.next_state_critical(move, 3 - self.current_player)
            if copy.four_connected(3 - self.current_player):
                new_node = Node(copy, self, move, self.mcts_player, 3 - self.current_player)
                self.childNodes[move] = new_node
                return new_node
            
        for move in possible_moves:
            if move not in self.childNodes:
                copy = self.next_state(move)
                new_node = Node(copy, self, move, self.mcts_player, 3 - self.current_player)
                self.childNodes[move] = new_node
                return new_node

    #Checks if there are any childnodes to expand
    #depending on that factor it returns True or False
    def is_fully_expanded(self):
        moves = self.game_state.get_valid_moves()
        return len(moves) == len(self.childNodes)