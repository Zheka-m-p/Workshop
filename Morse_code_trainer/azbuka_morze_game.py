from random import choice

words_list = [
    # Простые (3-4 буквы)
    'code', 'bit', 'list', 'soul', 'next', 'cat', 'dog', 'car', 'bag', 'pen',
    'sun', 'cup', 'hat', 'map', 'ice', 'key', 'egg', 'fox', 'bus', 'red',
    
    # Средние (5-6 букв)
    'doctor', 'driver', 'teacher', 'milk', 'dress', 'animal', 'flag', 'bank',
    'floor', 'snake', 'knife', 'mouse', 'banana', 'rabbit', 'castle', 'bridge',
    'python', 'binary', 'module', 'bottle',
    
    # Сложные (7+ букв)
    'volleyball', 'chocolate', 'developer', 'algorithm', 'variable', 'function',
    'keyboard', 'mountain', 'universe', 'fragile', 'penguin', 'artificial',
    'backpack'
]

morze_dict = {
    "0": "-----",
    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----.",
    "a": ".-",
    "b": "-...",
    "c": "-.-.",
    "d": "-..",
    "e": ".",
    "f": "..-.",
    "g": "--.",
    "h": "....",
    "i": "..",
    "j": ".---",
    "k": "-.-",
    "l": ".-..",
    "m": "--",
    "n": "-.",
    "o": "---",
    "p": ".--.",
    "q": "--.-",
    "r": ".-.",
    "s": "...",
    "t": "-",
    "u": "..-",
    "v": "...-",
    "w": ".--",
    "x": "-..-",
    "y": "-.--",
    "z": "--..",
    ".": ".-.-.-",
    ",": "--..--",
    "?": "..--..",
    "!": "-.-.--",
    "-": "-....-",
    "/": "-..-.",
    "@": ".--.-.",
    "(": "-.--.",
    ")": "-.--.-",
}
answers = []


def morse_encode(word):
    """Преобразует английское слово в кодировку азбуки морзе"""
    result = []
    for i in word:
        result.append(morze_dict[i])
    return " ".join(result)


def get_word():
    """Возвращает случайное слово из заданного нами списка слов"""
    return choice(words_list)


def print_statistics(answers):
    """Выводит статистику по ответам после окончания игры"""
    print(f"Всего задачек: {len(answers)}")
    print(f"Отвечено верно: {answers.count(True)}")
    print(f"Отвечено неверно: {answers.count(False)}")
    print(
        f"Ваш процент верных отгадываний: {round(answers.count(True) / len(answers) * 100, 2)}%"
    )


print("Добро пожаловать в игру!")
print("Сегодня мы потренируемся расшифровывать морзянку.")
print("Введите Ваше имя: ")
print(f"Привет, {input().upper()}! Игра начинается!")
print()
count = 0
while True:
    count += 1
    new_word = get_word()
    print(f"Слово {count}: {morse_encode(new_word)}")
    word = "".join(input("Напишите Ваше предполагаемое слово: ").lower().split())
    if word == new_word:
        print(f"Верно, {new_word}!")
        answers.append(True)
    else:
        print(f"Неверно, {new_word}!")
        answers.append(False)
    print()
    print("Хотите закончить?", "Введите 'stop'.")
    print("Хотите продолжить? Нажмите Enter.")
    if input().lower() == "stop":
        print()
        print_statistics(answers)
        break
