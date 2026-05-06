# Основной файл
# https://www.jsonkeeper.com/b/RW4W # тестовая ссылка с коротким набором слов
from players import Player
from utils import load_random_word, link_example, get_detalies  # , link_test # для тестирования на коротком примере

if __name__ == '__main__':
    name_player = input('Привет, как Вас зовут? ')  # Имя игрока
    player = Player(name_player)  # Экземпляр класса Player
    basic_word = load_random_word(link_example)  # Экземпляр класса BasicWord
    print(f"Привет, {name_player}\n"
          f"Составьте {basic_word.count_subword()} слов из слова '{basic_word.word}'\n"
          f"Слова должны быть не короче 3 букв\n"
          f"Чтобы закончить игру, угадайте все слова или напишите 'stop'\n"
          f"Чтобы узнать значение после верно угаданного слова напишите 'значение' иначе просто нажмите 'Enter'\n"
          f"Поехали, ваше первое слово?\n")

    while True:
        new_word = input()
        if len(new_word) < 3:
            print('слишком короткое слово')
        elif new_word == 'stop':  # т.к. тут только русские слова поэтому "stop" возможно писать на английском!
            print(f"Игра завершена, вы угадали {player.word_count()} из {basic_word.count_subword()} слов!")
            break
        elif new_word not in basic_word.valid_word_array:
            print('неверно')
        elif new_word in player.used_words:
            print('уже использовано')
        elif new_word in basic_word.valid_word_array:
            player.add_word(new_word)
            print('верно')
            detalies = input()
            if detalies == 'значение':
                get_detalies(new_word)
            else:
                print('попробуйте угадать ещё одно слово')
        if player.word_count() == basic_word.count_subword():
            print('\nПоздравляю, вы угадали все слова!')
            break
        print()
