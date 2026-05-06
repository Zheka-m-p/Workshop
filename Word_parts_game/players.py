#  тут класс игрока
class Player:
    def __init__(self, name, used_words=set()):
        self.name = name
        self.used_words = used_words

    def word_count(self):
        return len(self.used_words)

    def add_word(self, word):
        self.used_words.add(word)

    def word_repeat_yes_or_no(self, word):
        return word in self.used_words

    def __repr__(self):
        return f"Игрок с именем {self.name}"
