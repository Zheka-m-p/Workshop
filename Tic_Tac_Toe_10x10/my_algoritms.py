matrix = [['-' for j in range(10)] for i in range(10)]  # создаем заполненную матрицу (чтоб было не пусто)


def visual_matrix(m):
    for i in range(len(m)):
        for j in range(len(m[0])):
            print(str(m[i][j].rjust(3)), end='')
        print()


def proverka(matr, symbol):  # Возвращает True, если есть 5 в ряд, иначе (если нет 5 в ряд) False
    for i in matr:  # проверка по горизонтали есть ли 5 в ряд
        if symbol * 5 in ''.join(i):
            return f'Проиграл игрок с элементом "{symbol}"'

    matr = tuple(zip(*matr[::-1]))  # повернули матрицу на 90 вправо

    for i in matr:  # проверка по вертикали есть ли 5 в ряд
        if symbol * 5 in ''.join(i):
            return f'Проиграл игрок с элементом "{symbol}"'

    k = 0
    for kolvo in range(10, 4, -1):  # проверка есть ли 5 по диагоналям вида главных
        diags = []
        for i in range(0, kolvo):
            diags.append(matr[i][i + k])
        if symbol * 5 in ''.join(diags):
            return f'Проиграл игрок с элементом "{symbol}"'
        k += 1

    k = 1
    for kolvo in range(9, 4, -1):
        i = k
        diags = []
        for j in range(0, kolvo):
            diags.append(matr[i][i - k])
            i += 1
        if symbol * 5 in ''.join(diags):
            return f'Проиграл игрок с элементом "{symbol}"'
        k += 1

    matr = tuple(zip(*matr[::-1]))  # повернули матрицу на 90 вправо

    k = 0
    for kolvo in range(10, 4, -1):  # проверка есть ли 5 по диагоналям вида побочных
        diags = []
        for i in range(0, kolvo):
            diags.append(matr[i][i + k])
        if symbol * 5 in ''.join(diags):
            return f'Проиграл игрок с элементом "{symbol}"'
        k += 1

    k = 1
    for kolvo in range(9, 4, -1):
        i = k
        diags = []
        for j in range(0, kolvo):
            diags.append(matr[i][i - k])
            i += 1
        if symbol * 5 in ''.join(diags):
            return f'Проиграл игрок с элементом "{symbol}"'
        k += 1

    return False
