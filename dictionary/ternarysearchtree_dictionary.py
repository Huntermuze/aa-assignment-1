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

    def add_to_tst(self, cur_node: Node, cur_word: str, cur_freq: int, cur_index: int):
        cur_char = cur_word[cur_index]

        if cur_node is None:
            cur_node = Node(cur_char)

        if cur_char < cur_node.letter:
            cur_node.left = self.add_to_tst(cur_node.left, cur_word, cur_freq, cur_index)
        elif cur_char > cur_node.letter:
            cur_node.right = self.add_to_tst(cur_node.right, cur_word, cur_freq, cur_index)
        elif cur_index < len(cur_word) - 1:
            cur_node.middle = self.add_to_tst(cur_node.middle, cur_word, cur_freq, cur_index + 1)
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

    def search_tst(self, cur_node: Node, cur_word: str, cur_index: int):
        if cur_node is None:
            return None

        cur_char = cur_word[cur_index]

        if cur_char < cur_node.letter:
            return self.search_tst(cur_node.left, cur_word, cur_index)
        elif cur_char > cur_node.letter:
            return self.search_tst(cur_node.right, cur_word, cur_index)
        elif cur_index < len(cur_word) - 1:
            return self.search_tst(cur_node.middle, cur_word, cur_index + 1)
        else:
            return cur_node

    def add_word_frequency(self, word_frequency: WordFrequency) -> bool:
        """
        add a word and its frequency to the dictionary
        @param word_frequency: (word, frequency) to be added
        :return: True whether succeeded, False when word is already in the dictionary
        """
        # self.printWords(self.root_node, "", 0)
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
        word_exists = self.search(word) != 0

        if word_exists:
            self.delete_from_tst(self.root_node, word, 0)

        return word_exists

    def delete_from_tst(self, cur_node: Node, cur_word: str, cur_index: int):
        # Do not need to check if the word exists, since that is ensured prior to this method's invocation.
        cur_char = cur_word[cur_index]

        if cur_char < cur_node.letter:
            cur_node.left = self.delete_from_tst(cur_node.left, cur_word, cur_index)
        elif cur_char > cur_node.letter:
            cur_node.right = self.delete_from_tst(cur_node.right, cur_word, cur_index)
        elif cur_index < len(cur_word) - 1:
            cur_node.middle = self.delete_from_tst(cur_node.middle, cur_word, cur_index + 1)
        else:
            # If it is a leaf, then we can simply just remove it.
            if cur_node.left is None and cur_node.right is None and cur_node.middle is None:
                return None
            # In this case, it has at least one child, and is considered an end word.
            else:
                cur_node.frequency = 0
                cur_node.end_word = False

        return cur_node

    def autocomplete(self, word: str) -> List[WordFrequency]:
        """
        return a list of 3 most-frequent words in the dictionary that have 'word' as a prefix
        @param word: word to be autocompleted
        @return: a list (could be empty) of (at most) 3 most-frequent words with prefix 'word'
        """
        return []

    #  Print the all words using recursion (debugging purposes)
    def print_words(self, cur_node: Node, output: str, cur_index: int):
        if cur_node is not None:
            self.print_words(cur_node.middle, output + str(cur_node.letter), cur_index + 1)
            self.print_words(cur_node.right, output, cur_index)
            self.print_words(cur_node.left, output, cur_index)

            if cur_node.end_word:
                print(" ", (output + cur_node.letter))


if __name__ == '__main__':
    tst = TernarySearchTreeDictionary()
    tst.build_dictionary([WordFrequency("one", 10), WordFrequency("abc", 2),
                          WordFrequency("pop", 4), WordFrequency("ono", 53)])
    tst.print_words(tst.root_node, "", 0)
    tst.delete_word("abc")
    tst.delete_word("ono")
    print()
    tst.print_words(tst.root_node, "", 0)

