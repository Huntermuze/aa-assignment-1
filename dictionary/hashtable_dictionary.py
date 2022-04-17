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
        top_most_frequent = []

        # Utilising TimSort.
        # Consider removing the reverse arg, as it may add additional complexity to TimSort (research).
        # It might be better to do a linear scan over the KeyValue objects and handle them the same in List_dict
        # for bias reasons and because O(n) < O(nlog(n)).
        temp = sorted(self.word_frequencies.items(), key=lambda v: v[1], reverse=True)

        for kv in temp:
            if len(top_most_frequent) == 3:
                break

            if kv[0][0:len(word)] == word:
                top_most_frequent.append(WordFrequency(kv[0], kv[1]))

        return top_most_frequent
