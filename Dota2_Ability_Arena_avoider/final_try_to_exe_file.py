import sys, os
import json
import threading
import tkinter as tk
from tkinter import simpledialog, messagebox

import requests
import time
import pyautogui
import pytesseract
from PIL import Image
from transliterate import translit

# =====================
# ⚙️ АВТО-ОПРЕДЕЛЕНИЕ ПУТИ К TESSERACT
# =====================
if getattr(sys, "frozen", False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.abspath(".")

tesseract_path = os.path.join(base_path, "Tesseract-OCR", "tesseract.exe")
if os.path.exists(tesseract_path):
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
else:
    pytesseract.pytesseract.tesseract_cmd = (
        r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    )

tessdata_path = os.path.join(base_path, "tessdata")
if os.path.exists(tessdata_path):
    os.environ["TESSDATA_PREFIX"] = tessdata_path
else:
    os.environ["TESSDATA_PREFIX"] = r"C:\Program Files\Tesseract-OCR\tessdata"

# =====================
# ⚙️ НАСТРОЙКИ
# =====================
url = "https://abilityarena.com/api/leaderboard"
config = r"--oem 3 --psm 6"

dog_dict = {
    "76561197988197147": {"nickname": "Гадя Хреново", "rank": 35},
    "76561198018215097": {"nickname": "Faraon", "rank": 14},
    "76561198181017931": {"nickname": "Mujui", "rank": 95},
    "76561199603229460": {"nickname": ":)", "rank": 30},
    "76561198050673483": {"nickname": "Scary Terry", "rank": "trash"},
    "76561198050673413": {"nickname": "Daniel Avocado", "rank": "trash"},
}

stop_event = threading.Event()

# =====================
# 📁 ОДИН КОНФИГ-ФАЙЛ (ЗАМЕНА EXTRA_PLAYERS_FILE)
# =====================
CONFIG_FILE = "config.json"
config_data = {"nickname": "Парфюмер", "extra_players": []}
extra_players_list = []


def load_config():
    global config_data, extra_players_list
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            loaded = json.load(f)
            config_data["nickname"] = loaded.get("nickname", "Парфюмер")
            config_data["extra_players"] = loaded.get("extra_players", [])
    except (FileNotFoundError, json.JSONDecodeError):
        save_config()
    extra_players_list = config_data["extra_players"]
    return config_data


def save_config():
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config_data, f, ensure_ascii=False, indent=4)


# =====================
# 📐 АВТОМАТИЧЕСКАЯ АДАПТАЦИЯ ПОД РАЗРЕШЕНИЕ ЭКРАНА
# =====================
screen_width, screen_height = pyautogui.size()

ACCEPT_BUTTON_REGION = (
    int(screen_width * 0.410),
    int(screen_height * 0.441),
    int(screen_width * 0.178),
    int(screen_height * 0.070),
)

LOBBY_LIST_REGION = (
    int(screen_width * 0.590),
    int(screen_height * 0.735),
    int(screen_width * 0.095),
    int(screen_height * 0.217),
)

CHAT_CLICK_X = int(screen_width * 0.469)
CHAT_CLICK_Y = int(screen_height * 0.971)
LOBBY_MOVE_X = int(screen_width * 0.469)
LOBBY_MOVE_Y = int(screen_height * 0.971)


# =====================
# 🛠️ ОСНОВНЫЕ ФУНКЦИИ
# =====================
def return_dict_top_100_tryhard_ability_arena(url=url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            dict_data = {}
            for player in data:
                dict_data[player["steam_id"]] = {
                    "nickname": player["username"],
                    "rank": player["rank"],
                }
            print("✅ Успешно получены топ 100 задротов с сайта")
            return dict_data
        else:
            print(f"❌ Ошибка {response.status_code}: Не удалось получить данные")
            return {}
    except Exception as e:
        print(f"❌ Ошибка запроса: {e}")
        return {}


def check_start_game(root=None):
    print("⏳ Ищем игру...")
    if root:
        root.after(0, lambda: status_label.config(text="🔍 Ищем игру...", fg="blue"))

    spinner = ["🔄", "🔍", "🕵️", "👁️"]
    start_time = time.time()
    attempts = 0
    last_elapsed = -1

    while not stop_event.is_set():
        attempts += 1
        elapsed = int(time.time() - start_time)

        if elapsed != last_elapsed:
            last_elapsed = elapsed
            spin_icon = spinner[elapsed % len(spinner)]
            status_text = f"{spin_icon} Поиск... ({elapsed}с | попыток: {attempts})"
            print(status_text)
            if root:
                root.after(
                    0, lambda t=status_text: status_label.config(text=t, fg="blue")
                )

        try:
            image = pyautogui.screenshot(region=ACCEPT_BUTTON_REGION)
            string_ = (
                pytesseract.image_to_string(image, config=config, lang="rus")
                .lower()
                .strip()
            )
            if "принять" in string_:
                print(f"🎉 Нашли игру за {elapsed}с ({attempts} попыток)!")
                if root:
                    root.after(
                        0,
                        lambda: status_label.config(
                            text="🎉 Игра найдена!", fg="green"
                        ),
                    )
                return True
        except Exception as e:
            print(f"⚠️ Ошибка при поиске кнопки: {e}")

        for _ in range(5):
            if stop_event.is_set():
                print(f"🛑 Остановлено после {elapsed}с")
                if root:
                    root.after(
                        0,
                        lambda: status_label.config(text="🛑 Остановлено", fg="orange"),
                    )
                return False
            time.sleep(1)

    print("🛑 Поиск завершен")
    if root:
        root.after(
            0, lambda: status_label.config(text="🛑 Поиск завершен", fg="orange")
        )
    return False


def scrinshot_lobby_players_and_get_their_list():
    print()
    print("📸 Делаем скриншот лобби...")
    pyautogui.moveTo(LOBBY_MOVE_X, LOBBY_MOVE_Y, 0.3)
    pyautogui.click()
    time.sleep(1)

    image_lobby_players = pyautogui.screenshot(region=LOBBY_LIST_REGION)

    width, height = image_lobby_players.size
    big_image_lobby_players = image_lobby_players.resize((width * 3, height * 3))

    text = pytesseract.image_to_string(
        big_image_lobby_players, config="--oem 3 --psm 6 -l rus+eng+chi_tra"
    )
    result = [line.strip() for line in text.split("\n") if line.strip()]
    print("📝 Список игроков в лобби:", result)
    return result


def play_game_or_not(three_variant_list_players, me_nickname, local_dog_dict, root):
    dict_tryhard_this_lobby = {}

    for player in three_variant_list_players:
        for key, value in local_dog_dict.items():
            if value["nickname"] == player and value["nickname"] != me_nickname:
                dict_tryhard_this_lobby[key] = value

    if dict_tryhard_this_lobby:
        # Собираем заголовок и весь список в один текст
        lines = [
            f"🚨 НАЙДЕНЫ ЗАДРОТЫ ({len(dict_tryhard_this_lobby)}): "
            + ", ".join(v["nickname"] for v in dict_tryhard_this_lobby.values())
            + "\n"
        ]
        for idx, v in enumerate(dict_tryhard_this_lobby.values(), 1):
            lines.append(f"   {idx}. {v['nickname']} - rank {v['rank']}\n")

        # Вставляем ВЕСЬ блок с тегом подсветки (безопасно из фонового потока)
        root.after(
            0, lambda txt="".join(lines): log_area.insert(tk.END, txt, "tryhard_warn")
        )
    else:
        print("😮‍💨 Задротов в лобби не найдено. Можно играть спокойно.")

    time.sleep(1)
    pyautogui.moveTo(CHAT_CLICK_X, CHAT_CLICK_Y, 0.3)

    if dict_tryhard_this_lobby:
        pyautogui.click()
        pyautogui.typewrite(
            "There are a few total nerds of this game here - namely:", interval=0.05
        )
        pyautogui.hotkey("enter")

        text = "тут ЕСТЬ задроты, а именно\n"
        count_tryhard = 0
        for value in dict_tryhard_this_lobby.values():
            count_tryhard += 1
            time.sleep(0.5)
            try:
                nicname_translit = translit(
                    value["nickname"], language_code="ru", reversed=True
                )
            except:
                nicname_translit = value["nickname"]
            pyautogui.typewrite(f"{nicname_translit} - rank {value['rank']}")
            pyautogui.hotkey("enter")
            text += f"{count_tryhard}) {value['nickname']} - rank {value['rank']}\n"

        messagebox.showinfo(
            title="Играть или нет - решать тебе", message=text, parent=root
        )
    else:
        pyautogui.click()
        pyautogui.hotkey("enter")
        time.sleep(0.5)
        pyautogui.typewrite("There are no game nerds here", interval=0.05)
        pyautogui.hotkey("enter")
        time.sleep(0.5)
        pyautogui.typewrite("Lets get started", interval=0.05)
        pyautogui.hotkey("enter")
        messagebox.showinfo(
            title="Играть или нет - решать тебе",
            message="Тут НЕТ задротов, кроме тебя))",
            parent=root,
        )


# =====================
# 🧩 GUI-ОБОЛОЧКА
# =====================
class RedirectText:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, string):
        # Запоминаем, находится ли пользователь в самом низу лога
        at_bottom = self.text_widget.yview()[1] == 1.0

        self.text_widget.insert(tk.END, string)

        # Автопрокрутка вниз ТОЛЬКО если пользователь и так смотрел в конец
        if at_bottom:
            self.text_widget.see(tk.END)

    def flush(self):
        pass


def show_context_menu(event):
    menu = tk.Menu(root, tearoff=0)
    menu.add_command(
        label="Копировать", command=lambda: event.widget.event_generate("<<Copy>>")
    )
    menu.add_command(
        label="Вставить", command=lambda: event.widget.event_generate("<<Paste>>")
    )
    menu.add_separator()
    menu.add_command(
        label="Выделить всё",
        command=lambda: event.widget.event_generate("<<SelectAll>>"),
    )
    try:
        menu.tk_popup(event.x_root, event.y_root)
    finally:
        menu.grab_release()


search_matches = []
current_match_index = -1


def perform_search():
    global search_matches, current_match_index
    log_area.tag_remove("search", "1.0", tk.END)
    log_area.tag_remove("current_match", "1.0", tk.END)
    search_matches.clear()
    current_match_index = -1

    term = entry_search.get().strip()
    if not term:
        return

    start_pos = "1.0"
    while True:
        start_pos = log_area.search(term, start_pos, stopindex=tk.END, nocase=True)
        if not start_pos:
            break
        end_pos = f"{start_pos}+{len(term)}c"
        search_matches.append((start_pos, end_pos))
        log_area.tag_add("search", start_pos, end_pos)
        start_pos = end_pos

    log_area.tag_config("search", background="yellow", foreground="black")
    log_area.tag_config("current_match", background="orange", foreground="black")

    if search_matches:
        go_to_match(0)
    else:
        messagebox.showinfo("Поиск", "Совпадений не найдено.")


def go_to_match(index):
    global current_match_index, search_matches
    if not search_matches:
        return

    log_area.tag_remove("current_match", "1.0", tk.END)
    current_match_index = index % len(search_matches)
    start, end = search_matches[current_match_index]
    log_area.tag_add("current_match", start, end)
    log_area.see(start)


def next_match():
    global current_match_index
    if search_matches:
        go_to_match(current_match_index + 1)


def prev_match():
    global current_match_index
    if search_matches:
        go_to_match(current_match_index - 1)


def clear_search():
    global search_matches, current_match_index
    log_area.tag_remove("search", "1.0", tk.END)
    log_area.tag_remove("current_match", "1.0", tk.END)
    search_matches.clear()
    current_match_index = -1
    entry_search.delete(0, tk.END)


def start_alpha_wolf(nickname, extra_dogs):
    log_area.delete("1.0", tk.END)
    print(f"🖥️ Обнаружено разрешение: {screen_width}x{screen_height}")
    print("📍 Координаты автоматически адаптированы.")
    global dog_dict
    local_dog_dict = dog_dict.copy()

    for name in extra_dogs:
        if name.strip():
            local_dog_dict[f"custom_{name}"] = {
                "nickname": name.strip(),
                "rank": "trash",
            }

    stop_event.clear()
    button_stop.config(state=tk.NORMAL)

    try:
        top_100_players_dict = return_dict_top_100_tryhard_ability_arena()
        local_dog_dict.update(top_100_players_dict)

        if top_100_players_dict:
            print("\n===== ТОП-100 ЗАДРОТОВ С САЙТА =====")
            sorted_top = sorted(
                top_100_players_dict.items(),
                key=lambda x: x[1]["rank"] if isinstance(x[1]["rank"], int) else 999,
            )
            for idx, (_, data) in enumerate(sorted_top, 1):
                print(f"{idx:3}. {data['nickname']} (rank {data['rank']})")
            print("=" * 40)

        if not check_start_game(root=root):
            print("⏹️ Процесс остановлен.")
            return

        three_variant_list_players = scrinshot_lobby_players_and_get_their_list()
        play_game_or_not(three_variant_list_players, nickname, local_dog_dict, root)

    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
    finally:
        button_stop.config(state=tk.DISABLED)


def start_button_clicked():
    nick = entry_nick.get().strip()
    if not nick:
        messagebox.showwarning("Внимание", "Введите ваш никнейм!")
        return

    extra = [item for item in extra_players_list]
    t = threading.Thread(target=start_alpha_wolf, args=(nick, extra))
    t.daemon = True
    t.start()


def stop_button_clicked():
    stop_event.set()
    print("🛑 Отправлен сигнал остановки...")


def add_player_dialog():
    name = simpledialog.askstring(
        "Добавить игрока", "Введите никнейм нежелательного игрока:"
    )
    if name and name.strip():
        name = name.strip()
        if name not in extra_players_list:
            extra_players_list.append(name)
            listbox_players.insert(tk.END, name)
            config_data["extra_players"] = extra_players_list
            save_config()
        else:
            messagebox.showinfo("Инфо", "Такой игрок уже в списке.")


def remove_selected_player():
    selection = listbox_players.curselection()
    if selection:
        index = selection[0]
        name = listbox_players.get(index)
        listbox_players.delete(index)
        extra_players_list.remove(name)
        config_data["extra_players"] = extra_players_list
        save_config()


def reset_players_list():
    global extra_players_list
    extra_players_list.clear()
    listbox_players.delete(0, tk.END)
    config_data["extra_players"] = extra_players_list
    save_config()


# -------------------------------------------------------------------
# СТАРТ ИНТЕРФЕЙСА
# -------------------------------------------------------------------
root = tk.Tk()
root.title("AlphaWolf v1.15 (авто-адаптация)")

# 📍 Центрируем окно по центру экрана
win_w, win_h = 700, 700
x_pos = (screen_width // 2) - (win_w // 2)
y_pos = (screen_height // 2) - (win_h // 2)
root.geometry(f"{win_w}x{win_h}+{x_pos}+{y_pos}")

root.resizable(True, True)

load_config()
extra_players_list = config_data["extra_players"]

frame_top = tk.Frame(root)
frame_top.pack(pady=10, fill=tk.X, padx=10)

tk.Label(frame_top, text="Твой никнейм:").grid(
    row=0, column=0, sticky="w", padx=5, pady=5
)
entry_nick = tk.Entry(frame_top, width=30)
entry_nick.grid(row=0, column=1, padx=5, pady=5)
entry_nick.insert(0, config_data["nickname"])


def on_nick_focus_out(event=None):
    config_data["nickname"] = entry_nick.get().strip()
    save_config()


entry_nick.bind("<FocusOut>", on_nick_focus_out)

frame_players = tk.Frame(root)
frame_players.pack(pady=5, fill=tk.X, padx=10)

tk.Label(frame_players, text="Дополнительные нежелательные игроки:").pack(anchor="w")

listbox_frame = tk.Frame(frame_players)
listbox_frame.pack(fill=tk.BOTH, expand=True, pady=5)

scrollbar = tk.Scrollbar(listbox_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox_players = tk.Listbox(listbox_frame, height=6, yscrollcommand=scrollbar.set)
listbox_players.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.config(command=listbox_players.yview)

for player in extra_players_list:
    listbox_players.insert(tk.END, player)

btn_frame = tk.Frame(frame_players)
btn_frame.pack(pady=5)

tk.Button(
    btn_frame, text="➕ Добавить игрока", command=add_player_dialog, bg="lightblue"
).pack(side=tk.LEFT, padx=5)
tk.Button(
    btn_frame,
    text="❌ Удалить выбранного",
    command=remove_selected_player,
    bg="lightcoral",
).pack(side=tk.LEFT, padx=5)
tk.Button(
    btn_frame, text="🔄 Сбросить список", command=reset_players_list, bg="lightyellow"
).pack(side=tk.LEFT, padx=5)

frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

tk.Button(
    frame_buttons,
    text="▶️ Старт",
    command=start_button_clicked,
    bg="lightgreen",
    width=15,
).pack(side=tk.LEFT, padx=5)
button_stop = tk.Button(
    frame_buttons,
    text="⏹️ Стоп",
    command=stop_button_clicked,
    bg="orange",
    width=15,
    state=tk.DISABLED,
)
button_stop.pack(side=tk.LEFT, padx=5)
tk.Button(
    frame_buttons, text="❎ Выход", command=root.quit, bg="lightcoral", width=15
).pack(side=tk.LEFT, padx=5)

# --- Панель поиска ---
frame_search = tk.Frame(root)
frame_search.pack(fill=tk.X, padx=10, pady=(10, 0))

tk.Label(frame_search, text="🔍 Поиск:").pack(side=tk.LEFT)
entry_search = tk.Entry(frame_search, width=30)
entry_search.pack(side=tk.LEFT, padx=5)
tk.Button(frame_search, text="Найти", command=perform_search, bg="lightgray").pack(
    side=tk.LEFT, padx=2
)
tk.Button(frame_search, text="⬆️ Пред.", command=prev_match, bg="lightgray").pack(
    side=tk.LEFT, padx=2
)
tk.Button(frame_search, text="⬇️ След.", command=next_match, bg="lightgray").pack(
    side=tk.LEFT, padx=2
)
tk.Button(frame_search, text="Сброс", command=clear_search, bg="lightgray").pack(
    side=tk.LEFT, padx=5
)

# --- Метка статуса поиска (НОВАЯ) ---
# --- Статус-бар + кнопка скролла ---
frame_status = tk.Frame(root)
frame_status.pack(fill=tk.X, padx=10, pady=5)

status_label = tk.Label(
    frame_status, text="🟢 Готов к поиску", fg="gray", anchor="w", font=("Segoe UI", 10)
)
status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

tk.Button(
    frame_status,
    text="⬇️ В конец",
    command=lambda: log_area.see(tk.END),
    width=10,
    font=("Segoe UI", 9),
    bg="#e8e8e8",
    activebackground="#d0d0d0",
).pack(side=tk.RIGHT, padx=(5, 0))

# --- Лог событий ---
log_area = tk.Text(root, height=15, state="normal", wrap="word")
# Перенаправляем весь вывод в лог-окно
sys.stdout = RedirectText(log_area)
log_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
# Подсветка для найденных трайхардов
log_area.tag_config("tryhard_warn", background="yellow", foreground="black")

log_area.bind("<Button-3>", show_context_menu)


def copy_with_insert(event=None):
    log_area.event_generate("<<Copy>>")


root.bind("<Control-Insert>", copy_with_insert)

scrollbar_log = tk.Scrollbar(log_area, command=log_area.yview)
scrollbar_log.pack(side=tk.RIGHT, fill=tk.Y)
log_area.config(yscrollcommand=scrollbar_log.set)

tk.Label(
    root, text="Лог интерактивен: правый клик для меню, поиск с навигацией.", fg="gray"
).pack(pady=5)

root.mainloop()
