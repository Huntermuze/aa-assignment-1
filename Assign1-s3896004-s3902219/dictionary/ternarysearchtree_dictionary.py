from typing import List
from base_dictionary import BaseDictionary
from word_frequency import WordFrequency
from node import Node


# ------------------------------------------------------------------------
# This class is required to be implemented. Ternary Search Tree implementation.
#
# __author__ = 'Son Hoang Dau'
# __copyright__ = 'Copyright 2022, RMIT University'
# ------------------------------------------------------------------------


class TernarySearchTreeDictionary(BaseDictionary):

    def __init__(self):
        # Keep track of the root node of the tree (important)
        self.root_node = None

    def build_dictionary(self, words_frequencies: List[WordFrequency]):
        """
        construct the data structure to store nodes
        @param words_frequencies: list of (word, frequency) to be stored
        """
        # Here we will build the building by utilising the add operation over and over until
        # all word_freqs have been added, since recursion is used we can simply assign the root_node
        # to the final word_freq 
        for word_freq in words_frequencies:
            self.root_node = self.add_to_tst(self.root_node, word_freq.word, word_freq.frequency, 0)

    def add_to_tst(self, cur_node: Node, cur_word: str, cur_freq: int, cur_index: int):
        cur_char = cur_word[cur_index]

        # If the tree is empty, then create it
        if cur_node is None:
            cur_node = Node(cur_char)

        # Recursively create the tree by going through each letter, if the letter is less than
        # the current letter in the alphabet, it goes left, if its more, it goes right, if its the same,
        # then we move down as we have found the prefix for a word
        if cur_char < cur_node.letter:
            cur_node.left = self.add_to_tst(cur_node.left, cur_word, cur_freq, cur_index)
        elif cur_char > cur_node.letter:
            cur_node.right = self.add_to_tst(cur_node.right, cur_word, cur_freq, cur_index)
        elif cur_index < len(cur_word) - 1:
            cur_node.middle = self.add_to_tst(cur_node.middle, cur_word, cur_freq, cur_index + 1)
        else:
            # If none of the above hold true, we have reached the final letter and can assign
            # the frequency of the word to it (as required)
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
        if find_node is None or not find_node.end_word:
            return 0

        return find_node.frequency

    def search_tst(self, cur_node: Node, cur_word: str, cur_index: int):
        # Return none if such node does not exist (i.e., the word does not exist).
        if cur_node is None:
            return None

        cur_char = cur_word[cur_index]
        # Recursively search through the tree utilising a similar approach to the adding
        if cur_char < cur_node.letter:
            return self.search_tst(cur_node.left, cur_word, cur_index)
        elif cur_char > cur_node.letter:
            return self.search_tst(cur_node.right, cur_word, cur_index)
        elif cur_index < len(cur_word) - 1:
            return self.search_tst(cur_node.middle, cur_word, cur_index + 1)
        else:
            # If none of the above hold true, then that means our search is successful
            # and we have found the word, so we must return it
            return cur_node

    def add_word_frequency(self, word_frequency: WordFrequency) -> bool:
        """
        add a word and its frequency to the dictionary
        @param word_frequency: (word, frequency) to be added
        :return: True whether succeeded, False when word is already in the dictionary
        """
        # Confirm that the word_freq doesn't exist, if it doesn't then we can safely add it
        find_node = self.search_tst(self.root_node, word_frequency.word, 0)
        node_does_not_exist = find_node is None or find_node.end_word is False

        if node_does_not_exist:
            self.add_to_tst(self.root_node, word_frequency.word, word_frequency.frequency, 0)

        return node_does_not_exist

    def delete_word(self, word: str) -> bool:
        """
        delete a word from the dictionary
        @param word: word to be deleted
        @return: whether succeeded, e.g. return False when point not found
        """
        # Similar to above, we will check that the word exists, if it does
        # then we can safely delete it
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

        # This method utilises the following equation:
        # word = prefix + suffix, where suffix is variable and prefix is predefined.
        most_frequent = []
        words_to_ignore = []
        children_suffixes = []

        # CASE 1: If the prefix is the root node's letter (length = 1), just scan the entire middle subtree.
        if word == self.root_node.letter:
            root_of_suffixes = self.root_node.middle
        # CASE 2: If the prefix is not the root node,
        else:
            root_of_suffixes = self.search_tst(self.root_node, word, 0)
            # If the word is actually inside the tst, then we can process it (e.g., word = farm will return null).
            if root_of_suffixes is not None:
                # SUB-CASE2: If the prefix is itself a word, then we should prepend the prefix to the list, as it will
                # not be processed in the get_all_children_words() method, since we only use its middle node.
                if root_of_suffixes.end_word:
                    # Leave the word string empty, as it will be added in CASE 5 (prefix + suffix = word).
                    children_suffixes.append(["", root_of_suffixes.frequency])

                # Use the middle node of the root_of_suffixes node, because we only want sub-strings of the prefix,
                # but do not want different words that share prefix - 1 letters.
                root_of_suffixes = root_of_suffixes.middle

        # Get all the children of the root_of_suffixes.
        self.get_all_children_words(root_of_suffixes, "", children_suffixes)

        # CASE 3: If no words start with the prefix, return an empty list.
        if len(children_suffixes) <= 0 or root_of_suffixes is None:
            return most_frequent
        # CASE 4: If the prefix is itself the entire and only word (aka. the last letter of the prefix is an end_word).
        elif root_of_suffixes.end_word and len(children_suffixes) == 1:
            return [WordFrequency(word, root_of_suffixes.frequency)]
        # CASE 5: If the prefix has n usages, then find all the usages and add them to a list, selecting the three
        # with the highest frequency.
        else:
            for i in range(0, 3):
                highest_frequency = 0
                word_to_add = None

                for suffix_node in children_suffixes:
                    if suffix_node[1] > highest_frequency and suffix_node[0] not in words_to_ignore:
                        highest_frequency = suffix_node[1]
                        word_to_add = suffix_node[0]

                if highest_frequency != 0:
                    words_to_ignore.append(word_to_add)

                    # Check if the prefix length is greater than 0. We want to include the prefix, as it will get
                    # chopped off in the get_all_children_words, as the base_node [i.e., the one we start with]
                    # is not included, so as to prevent partial sub-strings from being added to the list).
                    if len(word) > 0:
                        # Recall the earlier equation: word = prefix + suffix => word_to_add = word + word_to_add.
                        word_to_add = word + word_to_add

                    most_frequent.append(WordFrequency(word_to_add, highest_frequency))

        return most_frequent

    def get_all_children_words(self, cur_node: Node, output: str, children_suffixes: list):
        # Get the children nodes required for autocomplete
        if cur_node is not None:
            self.get_all_children_words(cur_node.left, output, children_suffixes)
            self.get_all_children_words(cur_node.middle, output + str(cur_node.letter), children_suffixes)
            self.get_all_children_words(cur_node.right, output, children_suffixes)

            if cur_node.end_word:
                children_suffixes.append([output + cur_node.letter, cur_node.frequency])
