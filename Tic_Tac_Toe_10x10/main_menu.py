import pygame
import sys
import main
import main_play_pvp
import os
import ctypes

# Фикс для иконки в панели задач (чтобы Windows видел игру как отдельное приложение)
try:
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("mygame.tictactoe.v1")
except:
    pass

def resource_path(relative_path):
    """ Функция для поиска ресурсов внутри EXE """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def start_launcher():
    pygame.init()
    WIDTH, HEIGHT = 600, 500
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    
    # Установка иконки
    try:
        icon_img = pygame.image.load(resource_path('tictac.ico'))
        pygame.display.set_icon(icon_img)
    except:
        pass

    # Изначальный заголовок
    pygame.display.set_caption("Крестики-Нолики — Главное меню")

    font = pygame.font.SysFont("stxingkai", 36)
    small_font = pygame.font.SysFont("stxingkai", 24)

    def draw_menu():
        screen.fill((30, 30, 30))
        title = font.render("Выберите режим игры", True, (255, 255, 255))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

        # Кнопка 1
        btn1_rect = pygame.Rect(150, 150, 300, 60)
        pygame.draw.rect(screen, (0, 100, 0), btn1_rect)
        text1 = small_font.render("Против компьютера", True, (255, 255, 255))
        screen.blit(text1, (btn1_rect.centerx - text1.get_width() // 2, btn1_rect.centery - text1.get_height() // 2))

        # Кнопка 2
        btn2_rect = pygame.Rect(150, 250, 300, 60)
        pygame.draw.rect(screen, (0, 0, 100), btn2_rect)
        text2 = small_font.render("Против человека", True, (255, 255, 255))
        screen.blit(text2, (btn2_rect.centerx - text2.get_width() // 2, btn2_rect.centery - text2.get_height() // 2))

        # Кнопка Выход
        btn_exit_rect = pygame.Rect(150, 350, 300, 60)
        pygame.draw.rect(screen, (100, 0, 0), btn_exit_rect)
        text_exit = small_font.render("Выход", True, (255, 255, 255))
        screen.blit(text_exit, (btn_exit_rect.centerx - text_exit.get_width() // 2, btn_exit_rect.centery - text_exit.get_height() // 2))

        pygame.display.flip()
        return btn1_rect, btn2_rect, btn_exit_rect

    clock = pygame.time.Clock()
    running = True
    while running:
        btn1, btn2, btn_exit = draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn1.collidepoint(event.pos):
                    main.main()
                    # Возвращаем настройки меню после закрытия игры
                    screen = pygame.display.set_mode((WIDTH, HEIGHT))
                    pygame.display.set_caption("Крестики-Нолики — Главное меню")
                elif btn2.collidepoint(event.pos):
                    main_play_pvp.main()
                    # Возвращаем настройки меню после закрытия игры
                    screen = pygame.display.set_mode((WIDTH, HEIGHT))
                    pygame.display.set_caption("Крестики-Нолики — Главное меню")
                elif btn_exit.collidepoint(event.pos):
                    running = False

        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    start_launcher()
