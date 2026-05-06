import sys
import pygame
import os # Добавлено для работы с путями
from my_algoritms import proverka   # <-- правильный импорт

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
    height_window = height_game + 100

    size_window = (width, height_window)
    screen = pygame.display.set_mode(size_window)
    
    # Установка иконки
    try:
        icon_img = pygame.image.load(resource_path('tictac.ico'))
        pygame.display.set_icon(icon_img)
    except:
        pass

    pygame.display.set_caption('Обратные Крестики-Нолики. Человек против человека.')

    black = (0, 0, 0)
    blue = (0, 0, 255)
    red = (255, 0, 0)
    green = (0, 255, 0)
    white = (190, 190, 190)

    mas = [['-'] * 10 for i in range(10)]
    query = 0
    game_over = False

    while True:
        screen.fill(black)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                x_mouse, y_mouse = pygame.mouse.get_pos()
                if y_mouse < height_game:
                    col = x_mouse // (size_block + margin)
                    row = y_mouse // (size_block + margin)
                    if 0 <= row < 10 and 0 <= col < 10:
                        if mas[row][col] == '-':
                            if query % 2 == 0:
                                mas[row][col] = 'X'
                            else:
                                mas[row][col] = 'O'
                            query += 1

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_over = False
                    mas = [['-'] * 10 for i in range(10)]
                    query = 0

                elif event.key == pygame.K_ESCAPE:
                    return

        for row in range(10):
            for col in range(10):
                if mas[row][col] == 'X':
                    color = red
                elif mas[row][col] == 'O':
                    color = blue
                else:
                    color = white
                x = col * size_block + (col + 1) * margin
                y = row * size_block + (row + 1) * margin
                pygame.draw.rect(screen, color, (x, y, size_block, size_block))
                if mas[row][col] == 'X':
                    pygame.draw.line(screen, black, (x+10, y + 10), (x + size_block-10, y + size_block-10), 3)
                    pygame.draw.line(screen, black, (x + size_block-10, y + 10), (x + 10, y + size_block-10), 3)
                elif mas[row][col] == 'O':
                    pygame.draw.circle(screen, black, (x + size_block // 2, y + size_block // 2), size_block // 2 - 10, 3)

        if not game_over:
            zeros = sum(row.count('-') for row in mas)
            if zeros == 0:
                game_over = 'Ничья'
            else:
                if query > 0:
                    game_over = proverka(mas, 'X' if (query - 1) % 2 == 0 else 'O')

        # Разделительные линии
        pygame.draw.line(screen, black, (0, height_game), (width, height_game), 2)
        pygame.draw.line(screen, (100, 100, 100), (0, height_game + 5), (width, height_game + 5), 2)

        if game_over:
            font = pygame.font.SysFont('stxingkai', 36)
            text_1 = font.render(str(game_over), True, green)
            text_rect = text_1.get_rect(center=(width//2, height_game + 35))
            screen.blit(text_1, text_rect)

            font_small = pygame.font.SysFont('stxingkai', 20)
            h1 = font_small.render('SPACE - заново', True, white)
            h2 = font_small.render('ESC - меню', True, white)
            screen.blit(h1, (width//2 - 130, height_game + 70))
            screen.blit(h2, (width//2 + 30, height_game + 70))

        pygame.display.update()
