from typing import List
from dictionary.base_dictionary import BaseDictionary
from dictionary.word_frequency import WordFrequency


# ------------------------------------------------------------------------
# This class is required TO BE IMPLEMENTED. Hash-table-based dictionary.
#
# __author__ = 'Son Hoang Dau'
# __copyright__ = 'Copyright 2022, RMIT University'
# ------------------------------------------------------------------------

class HashTableDictionary(BaseDictionary):

    def __init__(self):
        self.word_frequencies = dict()

    def build_dictionary(self, words_frequencies: List[WordFrequency]):
        """
        construct the data structure to store nodes
        @param words_frequencies: list of (word, frequency) to be stored
        """
        for word_freq in words_frequencies:
            self.word_frequencies[word_freq.word] = word_freq.frequency

    def search(self, word: str) -> int:
        """
        search for a word
        @param word: the word to be searched
        @return: frequency > 0 if found and 0 if NOT found
        """
        return self.word_frequencies[word] if word in self.word_frequencies else 0

    def add_word_frequency(self, word_frequency: WordFrequency) -> bool:
        """
        add a word and its frequency to the dictionary
        @param word_frequency: (word, frequency) to be added
        :return: True whether succeeded, False when word is already in the dictionary
        """
        word_not_found = self.search(word_frequency.word) == 0

        if word_not_found:
            self.word_frequencies[word_frequency.word] = word_frequency.frequency

        return word_not_found

    def delete_word(self, word: str) -> bool:
        """
        delete a word from the dictionary
        @param word: word to be deleted
        @return: whether succeeded, e.g. return False when point not found
        """
        word_found = self.search(word) != 0

        if word_found:
            del self.word_frequencies[word]

        return word_found

    def autocomplete(self, word: str) -> List[WordFrequency]:
        """
        return a list of 3 most-frequent words in the dictionary that have 'word' as a prefix
        @param word: word to be autocompleted
        @return: a list (could be empty) of (at most) 3 most-frequent words with prefix 'word'
        """
        most_frequent = []
        words_to_ignore = []
        # Prune all the words that do not contain the prefix, as it is inefficient check this numerous times.
        words_with_prefix = [kv for kv in self.word_frequencies.items() if word == kv[0][0:len(word)]]

        # It is better to do a linear scan over the KeyValue objects and handle them the same in List_dict
        # for bias reasons (minimises bias) and to achieve the lowest theoretical time complexity. In this instance,
        # it is better to perform a linear scan rather than sorting first, then performing a binary search.
        # The former wields a complexity of O(n), whilst the latter is O(nlog(n)), and no sorting algorithm can
        # have a lower order (evident via mathematical proof). Hence, to ensure the lowest theoretical time complexity
        # or order, we will use a simple linear scan, as the outer loop always runs 3 times, making it
        # indifferent/insensitive to input (performance is constant).
        for i in range(0, 3):
            highest_frequency = 0
            word_to_add = None

            for kv in words_with_prefix:
                if kv[1] > highest_frequency and kv[0] not in words_to_ignore:
                    highest_frequency = kv[1]
                    word_to_add = kv[0]

            if highest_frequency != 0:
                words_to_ignore.append(word_to_add)
                most_frequent.append(WordFrequency(word_to_add, highest_frequency))

        return most_frequent
