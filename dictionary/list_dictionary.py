from typing import List
import bisect
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
        self.word_frequencies = [*words_frequencies]
        # We will use TimSort (inbuilt) here instead because when the # of elements is > 64, it will utilise its
        # improved MergeSort instead of using BinSort (this will be horribly inefficient for larger input sizes).
        self.word_frequencies.sort(key=lambda word_freq: word_freq.word)

    def search(self, word: str) -> int:
        """
        search for a word
        @param word: the word to be searched
        @return: frequency > 0 if found and 0 if NOT found
        """
        index = bisect.bisect_left(self.word_frequencies, word)

        # Check if the WordFrequency object's word at the index is the same as the word passed in.
        # If it is, then it has found the word, otherwise it has not found it and found the last closest item.
        if 0 <= index < len(self.word_frequencies) and self.word_frequencies[index].word == word:
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
            index_to_place = bisect.bisect_left(self.word_frequencies, word_frequency.word)
            self.word_frequencies.insert(index_to_place, word_frequency)

        return word_not_present

    def delete_word(self, word: str) -> bool:
        """
        delete a word from the dictionary
        @param word: word to be deleted
        @return: whether succeeded, e.g. return False when point not found
        """
        index_of_word = bisect.bisect_left(self.word_frequencies, word)
        word_present = False

        if 0 <= index_of_word < len(self.word_frequencies) and self.word_frequencies[index_of_word].word == word:
            word_present = True
            self.word_frequencies.remove(self.word_frequencies[index_of_word])

        return word_present

    def autocomplete(self, prefix_word: str) -> List[WordFrequency]:
        """
        return a list of 3 most-frequent words in the dictionary that have 'prefix_word' as a prefix
        @param prefix_word: word to be autocompleted
        @return: a list (could be empty) of (at most) 3 most-frequent words with prefix 'prefix_word'
        """
        most_frequent = []
        # Prune all the words that do not contain the prefix, as it is inefficient check this numerous times.
        # The following, 0:len(prefix_word), will be inlined, so calculations are not repeated (exclude from
        # theoretical time complexity).
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
