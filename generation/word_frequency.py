
# -------------------------------------------------
# __author__ = 'Son Hoang Dau'
# __copyright__ = 'Copyright 2022, RMIT University'
# -------------------------------------------------

# Class representing a word and its frequency
class WordFrequency:
    def __init__(self, word: str, frequency: int):
        self.word = word
        self.frequency = frequency

    def __gt__(self, other):
        if isinstance(other, WordFrequency):
            return self.word > other.word
        elif isinstance(other, str):
            return self.word > other
        else:
            raise TypeError("You cannot compare a WordFrequency with type" + str(type(other)))

    def __lt__(self, other):
        if isinstance(other, WordFrequency):
            return self.word < other.word
        elif isinstance(other, str):
            return self.word < other
        else:
            raise TypeError("You cannot compare a WordFrequency with type" + str(type(other)))


