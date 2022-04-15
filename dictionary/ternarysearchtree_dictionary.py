from typing import List
from dictionary.base_dictionary import BaseDictionary
from dictionary.word_frequency import WordFrequency
from dictionary.node import Node


# ------------------------------------------------------------------------
# This class is required to be implemented. Ternary Search Tree implementation.
#
# __author__ = 'Son Hoang Dau'
# __copyright__ = 'Copyright 2022, RMIT University'
# ------------------------------------------------------------------------


class TernarySearchTreeDictionary(BaseDictionary):

    def __init__(self):
        self.object_list = None
        self.root_node = None   

    def build_dictionary(self, words_frequencies: List[WordFrequency]):
        """
        construct the data structure to store nodes
        @param words_frequencies: list of (word, frequency) to be stored
        """
        self.object_list = words_frequencies
        for obj in self.object_list:
            self.create_tst(self.root_node, obj.word, obj.frequency, 0)
        print("TST Creation Complete!!")
            
    def create_tst(self, cur_node, cur_word, cur_freq, index):
        cur_char = cur_word[index]
        if cur_node is None:
            cur_node = Node(cur_char)
        
        if cur_char < cur_node.letter:
            cur_node.left = self.create_tst(cur_node.left, cur_word, cur_freq, index)
        elif cur_char > cur_node.letter:
            cur_node.right = self.create_tst(cur_node.right, cur_word, cur_freq, index)
        elif index < len(cur_word) - 1:
            cur_node.middle = self.create_tst(cur_node.middle, cur_word, cur_freq, index+1)
        else:
            cur_node.frequency = cur_freq
            cur_node.end_word = True
        
        return cur_node

    def search(self, word: str) -> int:
        """
        search for a word
        @param word: the word to be searched
        @return: frequency > 0 if found and 0 if NOT found
        """
        # TO BE IMPLEMENTED
        # place holder for return
        return 0

    def add_word_frequency(self, word_frequency: WordFrequency) -> bool:
        """
        add a word and its frequency to the dictionary
        @param word_frequency: (word, frequency) to be added
        :return: True whether succeeded, False when word is already in the dictionary
        """
        # TO BE IMPLEMENTED
        # place holder for return
        return False

    def delete_word(self, word: str) -> bool:
        """
        delete a word from the dictionary
        @param word: word to be deleted
        @return: whether succeeded, e.g. return False when point not found
        """
        # TO BE IMPLEMENTED
        # place holder for return
        return False

    def autocomplete(self, word: str) -> List[WordFrequency]:
        """
        return a list of 3 most-frequent words in the dictionary that have 'word' as a prefix
        @param word: word to be autocompleted
        @return: a list (could be empty) of (at most) 3 most-frequent words with prefix 'word'
        """
        # TO BE IMPLEMENTED
        # place holder for return
        return []
