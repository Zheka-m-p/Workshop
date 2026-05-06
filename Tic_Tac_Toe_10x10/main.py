import sys
import pygame
import os
from random import choice
from my_algoritms import proverka, visual_matrix   # <-- теперь правильный импорт

def resource_path(relative_path):
    """ Функция для поиска ресурсов внутри EXE """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def main():
    pygame.init()
    size_block = 50
    margin = 1

    width = size_block * 10 + margin * 11
    height_game = size_block * 10 + margin * 11
    # Добавляем место снизу
    height_window = height_game + 100

    size_window = (width, height_window)
    screen = pygame.display.set_mode(size_window)
    
    # Установка иконки
    try:
        icon_img = pygame.image.load(resource_path('tictac.ico'))
        pygame.display.set_icon(icon_img)
    except:
        pass

    pygame.display.set_caption('Обратные Крестики-Нолики. Против компьютера.')

    black = (0, 0, 0)
    blue = (0, 0, 255)
    red = (255, 0, 0)
    green = (0, 255, 0)
    white = (190, 190, 190)

    matrix = [['-'] * 10 for i in range(10)]
    query = 0
    game_over = False
    symbol = 'O'
    count_attempts = 15

    dictionary = {}
    for i in range(10):
        for j in range(10):
            dictionary[(i, j)] = (i, j)
    flag = False

    while True:
        # Очистка всего экрана (важно для нижней панели)
        screen.fill(black)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                x_mouse, y_mouse = pygame.mouse.get_pos()
                # Проверка, что клик именно по игровому полю
                if y_mouse < height_game:
                    col = x_mouse // (size_block + margin)
                    row = y_mouse // (size_block + margin)
                    if matrix[row][col] == '-':
                        if query % 2 == 0:
                            matrix[row][col] = 'X'
                            dictionary.pop(dictionary.get((row, col)), None)
                            print(f'{len(dictionary)} - количество свободных клеток после хода игрока')
                            visual_matrix(matrix)
                            query += 1
                            flag = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_over = False
                    matrix = [['-'] * 10 for i in range(10)]
                    query = 0
                    dictionary = {}
                    for i in range(10):
                        for j in range(10):
                            dictionary[(i, j)] = (i, j)

                elif event.key == pygame.K_ESCAPE:
                    return

            elif flag and not game_over:
                good_choice = choice(list(dictionary.keys()))
                row, col = good_choice[0], good_choice[1]
                matrix[row][col] = 'O'
                mb_ans = dictionary.pop(dictionary.get((row, col)), None)
                print()
                print(len(dictionary))
                query += 1
                visual_matrix(matrix)
                if proverka(matrix, 'O') == f'Проиграл игрок с элементом "{symbol}"':
                    print('погоди, я ещё подумаю')
                    bad_choice = []
                    count = 0
                    bad_choice.append((row, col))
                    matrix[row][col] = '-'
                    for i in range(count_attempts - 1):
                        if len(dictionary) > 0:
                            good_choice = choice(list(dictionary.keys()))
                            row, col = good_choice[0], good_choice[1]
                            matrix[row][col] = 'O'
                            mb_ans = dictionary.pop(dictionary.get((row, col)), None)
                            if proverka(matrix, 'O') != f'Проиграл игрок с элементом "{symbol}"':
                                bad_choice.append(mb_ans)
                                print('А куда ведёт этот брейк?')
                                break
                            else:
                                count += 1
                                print(f'{count + 1} попытка')
                                matrix[row][col] = '-'
                                bad_choice.append(mb_ans)
                                if (count + 1) == count_attempts:
                                    matrix[row][col] = 'O'
                                    print('Компьютер проиграл')
                        else:
                            matrix[row][col] = 'O'
                            print('Ну я пытался')
                    for cord in bad_choice[:-1]:
                        dictionary[cord] = cord
                flag = False

        # Отрисовка поля (всегда видна)
        for row in range(10):
            for col in range(10):
                if matrix[row][col] == 'X':
                    color = red
                elif matrix[row][col] == 'O':
                    color = blue
                else:
                    color = white
                x = col * size_block + (col + 1) * margin
                y = row * size_block + (row + 1) * margin
                pygame.draw.rect(screen, color, (x, y, size_block, size_block))
                if color == red:
                    pygame.draw.line(screen, black, (x+10, y + 10), (x + size_block-10, y + size_block-10), 3)
                    pygame.draw.line(screen, black, (x + size_block-10, y + 10), (x + 10, y + size_block-10), 3)
                elif color == blue:
                    pygame.draw.circle(screen, black, (x + size_block // 2, y + size_block // 2), size_block // 2 - 10, 3)

        # Логика проверки финала
        if not game_over:
            if len(dictionary) == 0:
                game_over = 'Ничья'
                alert = 'Ничья'
            else:
                if query > 0:
                    if (query - 1) % 2 == 0:
                        game_over = proverka(matrix, 'X')
                        alert = 'Человечество проиграло'
                    elif (query - 1) % 2 == 1:
                        game_over = proverka(matrix, 'O')
                        alert = 'Восстание машин подавлено'

        # Разделительные линии
        pygame.draw.line(screen, black, (0, height_game), (width, height_game), 2)
        pygame.draw.line(screen, (100, 100, 100), (0, height_game + 5), (width, height_game + 5), 2)

        if game_over:
            font = pygame.font.SysFont('stxingkai', 36)
            text_color = red if "проиграло" in alert else green
            text_1 = font.render(alert, True, text_color)
            text_rect = text_1.get_rect(center=(width//2, height_game + 35))
            screen.blit(text_1, text_rect)

            font_small = pygame.font.SysFont('stxingkai', 20)
            hint1 = font_small.render('SPACE - заново', True, green)
            hint2 = font_small.render('ESC - меню', True, green)
            screen.blit(hint1, (width//2 - 130, height_game + 70))
            screen.blit(hint2, (width//2 + 30, height_game + 70))

        pygame.display.update()
