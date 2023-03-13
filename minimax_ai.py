# import numpy as np
# import random
# from interface import *
# from variables import *
# from scores import *
from AI_test import *
import math


class Node:
    def __init__(self, value):
        self.value = value
        self.child = []
        
class Tree:

    def __init__(self,root_value):
        self.root_value = Node(root_value)

    def add_child(self,value,node):
        node.child.append(Node(value))

    def is_terminal(self,node):
        return not node.child
    
    def depth(self):
        """Returns depth of the tree"""
        return self._get_depth(self.root)
    
    def depth_node(self,node):
        """Returns depth of given node"""
        return self._get_depth(node)
    
    def _get_depth(self,node):
        if node is None:
            return 0
        else:
            d = 0
            for x in node.child :
                d = max(d,self._get_depth(x))
            return d + 1
    
    def min_or_max(self,node):
        """Returns True if it is the maximizing player turn, False otherwise
        (given that max plays at root)"""
        return not (self.depth_node(node) % 2 == 0)
    
    def generate_children(self,available_columns,node):
        """Generates childrens to the parent node based on the number of playable columns."""
        for x in range (len(available_columns)):
            self.add_child(0,node)
        
    def delete_terminal_nodes(self):
        """Deletes all terminal nodes"""

        # depth first search to get all the nodes
        def depth_first_search(self,node):
            discovered=[self.root]
            for x in self.child:
                if x not in discovered:
                    discovered.append(x)
                    self.delete_depth(x)
            # return discovered
        
        for x in depth_first_search(self.root):
            if self.is_terminal(x):
                del x


def minimax(board,tree,alpha,beta,symbol_player):
    playable_columns = list_valid_col(board)
    current_node=[tree.root]
    i=0
    end = tree.is_terminal(current_node[i])
    if tree.depth == tree.depth_node(current_node) or end:
        if end:
            print('jsp')
        else:
            return (None,score_column_prediction(board,symbol_player))
    
    if tree.min_or_max(current_node): #maximazing player
        value = -math.inf
        column = random.choice(playable_columns)
        for col in playable_columns:
            row = find_free_row(board,col)
            b_cp = board.copy()
            drop_disk(b_cp,col,opponent(symbol_player))
            tree.delete_terminal_nodes()
            new_score = minimax(b_cp,tree,alpha,beta,symbol_player)
            if new_score > value :
                value = new_score
                column = col
            alpha = max(alpha,value)
            if alpha>=beta:
                break
        return column,value
    
    else: #minimizing player
        value = math.inf
        column = random.choice(playable_columns)
        for col in playable_columns:
            row = find_free_row(board,col)
            b_cp = board.copy()
            drop_disk(b_cp,col,symbol_player)
            tree.delete_terminal_nodes()
            new_score = minimax(b_cp,tree,alpha,beta,symbol_player)
            if new_score < value :
                value = new_score
                column = col
            beta = min(beta,value)
            if alpha >= beta :
                break
        return column,value
        

