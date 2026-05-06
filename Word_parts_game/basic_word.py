# тут класс словA
class BasicWord:
    def __init__(self, word, valid_word_array):
        self.word = word
        self.valid_word_array = valid_word_array

    def chek_word_in_valid_array(self, word):
        return word in self.valid_word_array

    def __repr__(self):
        return f"{self.word} - слово из которого надо составить слова\n" \
               f"{self.valid_word_array} - набор допустимых подслов"

    def count_subword(self):
        return len(self.valid_word_array)
