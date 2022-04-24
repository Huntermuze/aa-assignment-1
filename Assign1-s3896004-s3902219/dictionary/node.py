
# -------------------------------------------------
# __author__ = 'Son Hoang Dau'
# __copyright__ = 'Copyright 2022, RMIT University'
# -------------------------------------------------

# DON'T CHANGE THIS FILE
# Class representing a node in the Ternary Search Tree
class Node:

    def __init__(self, letter=None, frequency=None, end_word=False):
        self.letter = letter            # letter stored at this node
        self.frequency = frequency      # frequency of the word if this letter is the end of a word
        self.end_word = end_word        # True if this letter is the end of a word
        self.left = None    # pointing to the left child Node, which holds a letter < self.letter
        self.middle = None  # pointing to the middle child Node
        self.right = None   # pointing to the right child Node, which holds a letter > self.letter
