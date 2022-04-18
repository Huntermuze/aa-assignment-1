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
        self.root_node = None

    def build_dictionary(self, words_frequencies: List[WordFrequency]):
        """
        construct the data structure to store nodes
        @param words_frequencies: list of (word, frequency) to be stored
        """
        for word_freq in words_frequencies:
            self.root_node = self.add_to_tst(self.root_node, word_freq.word, word_freq.frequency, 0)
        print("TST Creation Complete!!")

    def add_to_tst(self, cur_node: Node, cur_word: str, cur_freq: int, index: int):
        cur_char = cur_word[index]

        if cur_node is None:
            cur_node = Node(cur_char)

        if cur_char < cur_node.letter:
            cur_node.left = self.add_to_tst(cur_node.left, cur_word, cur_freq, index)
        elif cur_char > cur_node.letter:
            cur_node.right = self.add_to_tst(cur_node.right, cur_word, cur_freq, index)
        elif index < len(cur_word) - 1:
            cur_node.middle = self.add_to_tst(cur_node.middle, cur_word, cur_freq, index + 1)
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
        find_node = self.search_tst(self.root_node, word, 0)
        # The two conditions for a node not found are: 
        # - node reaches end of tree before completion
        # - node finishes but end_word is false
        if find_node is None:
            return 0
        elif find_node.end_word is False:
            return 0
        else:
            return find_node.frequency

    def search_tst(self, cur_node: Node, cur_word: str, index: int):
        if cur_node is None:
            return None

        cur_char = cur_word[index]

        if cur_char < cur_node.letter:
            return self.search_tst(cur_node.left, cur_word, index)
        elif cur_char > cur_node.letter:
            return self.search_tst(cur_node.right, cur_word, index)
        elif index < len(cur_word) - 1:
            return self.search_tst(cur_node.middle, cur_word, index + 1)
        else:
            return cur_node
    
    def add_word_frequency(self, word_frequency: WordFrequency) -> bool:
        """
        add a word and its frequency to the dictionary
        @param word_frequency: (word, frequency) to be added
        :return: True whether succeeded, False when word is already in the dictionary
        """
        #self.printWords(self.root_node, "", 0)
        find_node = self.search_tst(self.root_node, word_frequency.word, 0)
        if find_node is None:
            self.add_to_tst(self.root_node, word_frequency.word, word_frequency.frequency, 0)
            return True
        elif find_node.end_word is False:
            self.add_to_tst(self.root_node, word_frequency.word, word_frequency.frequency, 0)
            return True
        else:
            return True

    def delete_word(self, word: str) -> bool:
        """
        delete a word from the dictionary
        @param word: word to be deleted
        @return: whether succeeded, e.g. return False when point not found
        """
        # TO BE IMPLEMENTED
        # place holder for return
        return False
    
    #def delete_from_tst(self, cur_node: Node, cur_word: str, index: int):
        if cur_node is None:
            return None
        
        cur_char = cur_word[index]
        
        if cur_char < cur_node.letter:
            cur_node.left = self.delete_from_tst(cur_node.left, cur_word, index)
        elif cur_char > cur_node.letter:
            cur_node.right = self.delete_from_tst(cur_node.right, cur_word, index)
        elif index < len(cur_word) - 1:
            cur_node.middle = self.delete_from_tst(cur_node.middle, cur_word, index + 1)

    def autocomplete(self, word: str) -> List[WordFrequency]:
        """
        return a list of 3 most-frequent words in the dictionary that have 'word' as a prefix
        @param word: word to be autocompleted
        @return: a list (could be empty) of (at most) 3 most-frequent words with prefix 'word'
        """
        # TO BE IMPLEMENTED
        # place holder for return
        return []
    
    #  Print the all words using recursion (debugging purposes)
    def printWords(self, node, output, index) :
        if (node != None) :
            self.printWords(node.left, output, index)    
            self.printWords(node.middle, 
                            output + str(node.letter), 
                            index + 1)
            self.printWords(node.right, output, index)
            if (node.end_word == True) :
                print(" ", (output + node.letter) )
