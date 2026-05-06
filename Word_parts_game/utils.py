# тут лежат функции
import requests
import webbrowser
from random import choice
from basic_word import BasicWord

link_test = "https://www.jsonkeeper.com/b/RW4W"  # ссылка на небольшой тестовый вариант списка словарей
link_example = 'https://www.jsonkeeper.com/b/VOGS'  # ссылка на итоговый вариант списка словарей, пилил вручную(
link_site = 'https://makeword.ru/dictionary/'  # ссылка на сайт для вывода слов


def load_random_word(link):
    """Функция переходит по ссылке, выбирает оттуда рандомно один словарь из списка словарей,
        с помощью которого создает экземпляр класса BasicWord и возвращает его """
    value = requests.get(link).json()
    random_choice_dict = choice(value)
    word = random_choice_dict.get('word')
    word_array = random_choice_dict.get('subwords')
    exemplar = BasicWord(word, word_array)
    return exemplar


def get_detalies(word):
    """Открывает ссылку в браузере для подробного описания слова, которое было ВЕРНО угадано."""
    new_link = link_site + word
    webbrowser.open(new_link)
