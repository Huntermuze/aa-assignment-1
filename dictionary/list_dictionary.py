from typing import List
from dictionary.word_frequency import WordFrequency
from dictionary.base_dictionary import BaseDictionary


# ------------------------------------------------------------------------
# This class is required TO BE IMPLEMENTED. List-based dictionary implementation.
#
# __author__ = 'Son Hoang Dau'
# __copyright__ = 'Copyright 2022, RMIT University'
# ------------------------------------------------------------------------

class ListDictionary(BaseDictionary):

    def __init__(self):
        self.word_frequencies = None

    def build_dictionary(self, words_frequencies: List[WordFrequency]):
        """
        construct the data structure to store nodes
        @param words_frequencies: list of (word, frequency) to be stored
        """
        self.word_frequencies = words_frequencies
        # We will use TimSort (inbuilt) here instead because when the # of elements is > 64, it will utilise its
        # improved MergeSort instead of using BinSort (this will be horribly inefficient for larger input sizes).
        self.word_frequencies.sort(key=lambda word_freq: word_freq.word)

    def search(self, word: str) -> int:
        """
        search for a word
        @param word: the word to be searched
        @return: frequency > 0 if found and 0 if NOT found
        """
        index = self._binary_search(0, len(self.word_frequencies) - 1, word, False)

        if index != -1:
            return self.word_frequencies[index].frequency

        return 0

    def add_word_frequency(self, word_frequency: WordFrequency) -> bool:
        """
        add a word and its frequency to the dictionary
        @param word_frequency: (word, frequency) to be added
        :return: True whether succeeded, False when word is already in the dictionary
        """
        word_not_present = self.search(word_frequency.word) == 0

        if word_not_present:
            self.word_frequencies.append(word_frequency)
            self._binary_insertion_sort_elements()

        return word_not_present

    def delete_word(self, word: str) -> bool:
        """
        delete a word from the dictionary
        @param word: word to be deleted
        @return: whether succeeded, e.g. return False when point not found
        """
        index_of_word = self._binary_search(0, len(self.word_frequencies) - 1, word, False)
        word_already_present = index_of_word != -1

        if word_already_present:
            self.word_frequencies.remove(self.word_frequencies[index_of_word])

        return word_already_present

    def autocomplete(self, prefix_word: str) -> List[WordFrequency]:
        """
        return a list of 3 most-frequent words in the dictionary that have 'prefix_word' as a prefix
        @param prefix_word: word to be autocompleted
        @return: a list (could be empty) of (at most) 3 most-frequent words with prefix 'prefix_word'
        """
        most_frequent = []
        # Prune all the words that do not contain the prefix, as it is inefficient check this numerous times.
        words_with_prefix = [x for x in self.word_frequencies if prefix_word == x.word[0:len(prefix_word)]]

        for i in range(0, 3):
            highest_frequency = 0
            highest_frequency_index = 0

            for j in range(len(words_with_prefix)):
                curr_word_freq = words_with_prefix[j]

                if curr_word_freq.frequency > highest_frequency and curr_word_freq not in most_frequent:
                    highest_frequency = curr_word_freq.frequency
                    highest_frequency_index = j

            if highest_frequency != 0:
                most_frequent.append(words_with_prefix[highest_frequency_index])

        return most_frequent

    # Binary Insertion Sort (BinSort) - takes advantage of best case O(nlog(n)).
    # Only to be used when adding new items.
    def _binary_insertion_sort_elements(self):
        for i in range(1, len(self.word_frequencies)):
            current = self.word_frequencies[i]
            where_current_belongs = self._binary_search(0, i - 1, current.word, True)
            j = i

            while j > where_current_belongs:
                self.word_frequencies[j] = self.word_frequencies[j - 1]
                j -= 1

            self.word_frequencies[where_current_belongs] = current

    # Slightly modified version, so that it returns the closest index if not found or -1 if not found (up to caller).
    def _binary_search(self, left: int, right: int, word: str, return_closest: bool) -> int:
        if return_closest:
            if left == right:
                if self.word_frequencies[left].word > word:
                    return left
                else:
                    return left + 1

            if left > right:
                return left
        else:
            if left > right:
                return -1

        midpoint = (left + right) // 2

        if self.word_frequencies[midpoint].word < word:
            return self._binary_search(midpoint + 1, right, word, return_closest)
        elif self.word_frequencies[midpoint].word > word:
            return self._binary_search(left, midpoint - 1, word, return_closest)
        else:
            return midpoint
