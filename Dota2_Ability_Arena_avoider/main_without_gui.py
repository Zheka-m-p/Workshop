'''Что надо сделать: p.s. Всегда запускать с английской раскладкой, иначе могут быть проблемы при выводе в лобби текста
# 0)Импортировать все нужные нам библиотеки. +
# 1) Вводим все наши данные, которые нужны нам
# 2)Парсим данные с сайта абилити.арена и загоняем в словарь всех игроков.
# 3)Скриншот первоначальный при запуске программы
# 4)Скриншоты делать до тех пор, пока в центре не будет "принять"
5)Когда нашли скрин, переводим мышку на лобби, щёлкаем ей и делаем другой скришнот игроков лобби и получаем их словарь
6)Проверяем есть ли игроки из топ 100 в этом списке.
7)Если есть, то спустя 3 сек нажимаем отмена, перенеся мышку. Если нет, то нажимаем принять, спустя 3 секунды
8)Запускаем все нужные функции для отработки программы
'''

      
# ===================== 
# 📌 ИМПОРТ БИБЛИОТЕК
# =====================
import requests  # Для запросов к API Ability Arena
import time  # Для задержек (time.sleep)
import pyautogui  # Для скриншотов и управления мышкой/клавиатурой
import pytesseract  # Распознавание текста с картинок
from PIL import Image  # Обработка изображений
from transliterate import translit  # Транслитерация кириллицы в латиницу

# =====================
# ⚙️ НАСТРОЙКИ
# =====================
url = 'https://abilityarena.com/api/leaderboard'  # API для получения топа игроков
config = r'--oem 3 --psm 6'  # Конфиг для Tesseract (режим автоматического распознавания)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Путь к Tesseract
me_nickname = 'Парфюмер'  # Ваш ник (чтобы программа не считала вас )

# Словарь "нежелательных" игроков (добавляются вручную + топ 100 с сайта)
dog_dict = {
    '76561197988197147': {'nickname': 'Гадя Хреново', 'rank': 35},
    '76561198018215097': {'nickname': 'Faraon', 'rank': 14},
    '76561198181017931': {'nickname': 'Mujui', 'rank': 95},
    '76561199603229460': {'nickname': ':)', 'rank': 30},
    '76561198050673483': {'nickname': 'Scary Terry', 'rank': 'trash'},
    '76561198050673413': {'nickname': 'Daniel Avocado', 'rank': 'trash'},
}


# =====================
# 🛠️ ФУНКЦИИ
# =====================

def return_dict_top_100_tryhard_ability_arena(url=url):
    """
    📊 Получает топ-100 задротов с сайта Ability Arena.
    Возвращает словарь вида {steam_id: {'nickname': str, 'rank': int}}.
    """
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        dict_data = {}
        for player in data:
            dict_data[player["steam_id"]] = {'nickname': player['username'], 'rank': player['rank']}
        print('✅ Успешно получены топ 100 задротов с сайта')
        return dict_data
    else:
        print(f'❌ Ошибка {response.status_code}: Не удалось получить данные')
        return {}


def check_start_game():
    """
    🎮 Поиск кнопки "Принять" в игре.    
    Делает скриншот каждые 5 секунд, пока не найдет текст "принять".
    """
    global image  # Сохраняем скриншот в глобальную переменную (если нужно для отладки)
    while True:
        # Делаем скриншот области с кнопкой
        image = pyautogui.screenshot('кнопка принять.PNG', region=(787, 477, 340, 75))
        # Распознаем текст с картинки
        string_ = pytesseract.image_to_string(image, config=config, lang='rus').lower().strip()
        if 'принять' in string_:
            print('🎉 Поздравляю, мы нашли игру!')
            break
        time.sleep(5)  # Проверяем каждые 5 секунд


def scrinshot_lobby_players_and_get_their_list():
    """
    📸 Делает скриншот лобби, сохраняет его на диск и возвращает список ников.
    Действия:
    1. Кликает в указанную точку (чтобы открыть список игроков).
    2. Сохраняет 2 версии скриншота: оригинал и увеличенную (для лучшего распознавания).
    3. Распознает ники на 3 языках (русский, английский, китайский).
    """
    pyautogui.moveTo(900, 1048, 0.3)  # Перемещаем курсор
    pyautogui.click()  # Кликаем, чтобы открыть список игроков
    time.sleep(1)  # Ждем, пока список откроется

    # Сохраняем скриншот лобби
    pyautogui.screenshot('list_players_lobby.png', region=(1132, 793, 183, 234))
    image_lobby_players = Image.open('list_players_lobby.png')

    # Увеличиваем разрешение для лучшего распознавания
    width, height = image_lobby_players.size
    big_image_lobby_players = image_lobby_players.resize((width * 3, height * 3))
    big_image_lobby_players.save('big_list_players_lobby.png')

    # Распознаем текст (русский + английский + китайский)
    text = pytesseract.image_to_string(big_image_lobby_players, config='--oem 3 --psm 6 -l rus+eng+chi_tra')
    # Разбиваем текст по строкам и убираем пустые
    result = [line.strip() for line in text.split('\n') if line.strip()]

    print('📝 Список игроков в лобби:', result)
    return result



def play_game_or_not():
    """
    🤔 Решает, играть или нет, на основе списка игроков.
    Если в лобби есть задроты из dog_dict — пишет предупреждение.
    """
    dict_tryhard_this_lobby = {}  # Словарь для задротов в текущем лобби

    # Ищем игроков из dog_dict в текущем лобби
    for player in three_variant_list_players:
        for key, value in dog_dict.items():
            if value['nickname'] == player and value['nickname'] != me_nickname:
                dict_tryhard_this_lobby[key] = value

    print(dict_tryhard_this_lobby, ' - это список задротов этого лобби')
    time.sleep(1)
    pyautogui.moveTo(900, 1048, 0.3)  # Перемещаем курсор в чат

    if dict_tryhard_this_lobby:
        # Если есть задроты — пишем в чат и выводим предупреждение
        pyautogui.click()
        pyautogui.typewrite('There are a few total nerds of this game here - namely:', interval=0.05)
        pyautogui.hotkey('enter')

        text = 'тут ЕСТЬ задроты, а именно\n'
        count_tryhard = 0
        for value in dict_tryhard_this_lobby.values():
            count_tryhard += 1
            time.sleep(0.5)
            try:
                # Пытаемся транслитерировать ник (например, "Гадя" -> "Gadya")
                nicname_translit = translit(value['nickname'], language_code='ru', reversed=True)
            except:
                nicname_translit = value['nickname']
            # Пишем в чат ник и ранг
            pyautogui.typewrite(f"{nicname_translit} - rank {value['rank']}")
            pyautogui.hotkey('enter')
            text += f"{count_tryhard}) {value['nickname']} - rank {value['rank']}\n"

        # Выводим всплывающее окно с предупреждением
        pyautogui.alert(text=text, title='Играть или нет - решать тебе', button='Нажми меня чтобы начать или не начать')
    else:
        # Если задротов нет — пишем, что можно играть
        pyautogui.click()
        pyautogui.hotkey('enter')
        time.sleep(0.5)
        pyautogui.typewrite('There are no game nerds here', interval=0.05)
        pyautogui.hotkey('enter')
        time.sleep(0.5)
        pyautogui.typewrite('Lets get started', interval=0.05)
        pyautogui.hotkey('enter')
        # Выводим позитивное сообщение
        pyautogui.alert(text='Тут НЕТ задротов, кроме тебя))', title='Играть или нет - решать тебе',
                        button='Нажми меня чтобы начать или не начать')

    
# =====================
# 🚀 ЗАПУСК ПРОГРАММЫ
# =====================
if __name__ == "__main__":
    print('🐺 Альфа-Волк активирован!')

    # 1. Получаем топ-100 задротов и обновляем словарь
    top_100_players_dict = return_dict_top_100_tryhard_ability_arena()
    dog_dict.update(top_100_players_dict)   

    # 2. Выводим список игроков для проверки
    print('\n📊 Текущий список задротских псов:')
    print(*dog_dict.values(), sep='\n')
    print(f'\n📌 Всего задротов в списке: {len(dog_dict)}')

    # 3. Ищем игру
    check_start_game()

    # 4. Делаем скриншот лобби и получаем список игроков
    three_variant_list_players = scrinshot_lobby_players_and_get_their_list()

    # 5. Проверяем, есть ли задроты, и решаем, играть или нет
    play_game_or_not()