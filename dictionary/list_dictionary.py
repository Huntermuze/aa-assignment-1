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
        sorted(self.word_frequencies, key=lambda word_freq: word_freq.word)

    def search(self, word: str) -> int:
        """
        search for a word
        @param word: the word to be searched
        @return: frequency > 0 if found and 0 if NOT found
        """
        index = self._binary_search(0, len(self.word_frequencies), word, False)

        if index != -1:
            return self.word_frequencies[index].frequency

        return 0

    def add_word_frequency(self, word_frequency: WordFrequency) -> bool:
        """
        add a word and its frequency to the dictionary
        @param word_frequency: (word, frequency) to be added
        :return: True whether succeeded, False when word is already in the dictionary
        """
        word_not_present = True if self.search(word_frequency.word) == 0 else False

        if word_not_present:
            self.word_frequencies.append(word_frequency)
            self._binary_insertion_sort_elements()

        # TODO we can add a check here that checks whether it is greater than elements in the top 3 lis of frequencies,
        #  and if it is place it there and remove the smallest one
        return word_not_present

    def delete_word(self, word: str) -> bool:
        """
        delete a word from the dictionary
        @param word: word to be deleted
        @return: whether succeeded, e.g. return False when point not found
        """
        index_of_word = self._binary_search(0, len(self.word_frequencies), word, False)
        word_already_present = False if index_of_word == -1 else True

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

        for i in range(0, 3):
            highest_frequency = 0
            highest_frequency_index = 0

            for j in range(len(self.word_frequencies)):
                curr_word_freq = self.word_frequencies[j]

                if curr_word_freq.frequency > highest_frequency and curr_word_freq not in most_frequent \
                        and prefix_word == curr_word_freq.word[0:len(prefix_word)]:
                    highest_frequency = curr_word_freq.frequency
                    highest_frequency_index = j

            if highest_frequency != 0:
                most_frequent.append(self.word_frequencies[highest_frequency_index])

        return most_frequent

    # Binary Insertion Sort (BinSort) - takes advantage of best case O(nlog(n)).
    # Only to be used when adding new items.
    def _binary_insertion_sort_elements(self) -> None:
        for i in range(1, len(self.word_frequencies)):
            current = self.word_frequencies[i]
            index_of_current = self._binary_search(0, i, current, True)
            j = i

            while j > index_of_current:
                self.word_frequencies[j] = self.word_frequencies[j - 1]
                j -= 1

            self.word_frequencies[index_of_current] = current

    # Slightly modified version, so that it returns the closest index if not found or -1 if not found (up to caller).
    def _binary_search(self, left: int, right: int, word: str, return_closest: bool) -> int:
        if left > right and not return_closest:
            return -1
        elif left > right and return_closest:
            # Return the right index since it does not move from where the last element ACTUALLY is (alternatively,
            # can return left - 1).
            return right

        midpoint = (left + right) // 2

        if word == self.word_frequencies[midpoint].word:
            return midpoint
        elif word < self.word_frequencies[midpoint].word:
            return self._binary_search(left, midpoint - 1, word, return_closest)
        else:
            return self._binary_search(midpoint + 1, right, word, return_closest)
