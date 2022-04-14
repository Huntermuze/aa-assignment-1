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
        self.object_list = None
        self.word_frequencies = dict()

    def build_dictionary(self, words_frequencies: List[WordFrequency]):
        """
        construct the data structure to store nodes
        @param words_frequencies: list of (word, frequency) to be stored
        """
        self.object_list = words_frequencies
        for x in self.object_list:
            self.word_frequencies[x.word] = x.frequency

    def search(self, word: str) -> int:
        """
        search for a word
        @param word: the word to be searched
        @return: frequency > 0 if found and 0 if NOT found
        """
        if word in self.word_frequencies:
            return self.word_frequencies[word]
        else:
            return 0

    def add_word_frequency(self, word_frequency: WordFrequency) -> bool:
        """
        add a word and its frequency to the dictionary
        @param word_frequency: (word, frequency) to be added
        :return: True whether succeeded, False when word is already in the dictionary
        """
        if self.search(word_frequency.word) == 0:
            self.word_frequencies[word_frequency.word] = word_frequency.frequency
            return True
        else:
            return False

    def delete_word(self, word: str) -> bool:
        """
        delete a word from the dictionary
        @param word: word to be deleted
        @return: whether succeeded, e.g. return False when point not found
        """
        if self.search(word) == 0:
            return False
        else:
            del self.word_frequencies[word]
            return True

    def autocomplete(self, word: str) -> List[WordFrequency]:
        """
        return a list of 3 most-frequent words in the dictionary that have 'word' as a prefix
        @param word: word to be autocompleted
        @return: a list (could be empty) of (at most) 3 most-frequent words with prefix 'word'
        """
        top_most_frequent = []
        word_count = 0
        sorted_by_frequency = {k: v for k, v in sorted(self.word_frequencies.items(), key = lambda v: v[1], reverse=True) if k.startswith(word)}
        for x in sorted_by_frequency:
            for z in self.object_list:
                if x == z.word:
                    word_count += 1
                    top_most_frequent.append(z)
                if word_count == 3:
                    break
            
        return top_most_frequent
