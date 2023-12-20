from random import randint, choice

FILENAME = "2048_high_score.txt"


def main():
    # Выводим приветственное сообщение
    print_intro()
    # Получаем лучший результат из файла
    high_score = get_high_score()
    # Флаг для продолжения игры
    wants_to_play = True

    while wants_to_play:
        # Создаем новое игровое поле
        board = get_new_board()
        # Счет игрока
        score = 0
        # Направление движения
        move = None

        while not (board_is_full(board) or move == "r"):
            # Добавляем новое число на поле
            add_random_number(board)
            # Выводим текущее состояние игры
            print_board(board, score, high_score)
            # Получаем от игрока направление движения
            move = get_valid_move()
            # Обновляем состояние игры в соответствии с выбранным направление
            score += update_board(board, move)

            # Если текущий счет превысил лучший результат, обновляем его
            if score > high_score:
                high_score = score

        # Выводим конечное состояние игры и результаты
        print_board(board, score, high_score)
        print_results(board, score, high_score)
        # Спрашиваем, хочет ли игрок сыграть еще раз
        wants_to_play = get_valid_answer()

    # Сохраняем лучший результат в файл
    save_high_score(high_score)
    print_outro()


# Приветственное сообщение
def print_intro():
    print("Добро пожаловать в игру \"2048\"!\n")


# Получение лучшего результата из файла
def get_high_score():
    try:
        with open(FILENAME) as file:
            data = file.read().strip()
            if data.isdecimal():
                return int(data)
        print("Файл с лучшими результатами содержит некорректные данные.\n")
        return 0
    except (FileNotFoundError, ValueError):
        return 0


# Создание нового игрового поля
def get_new_board():
    board = [0 for _ in range(16)]
    add_random_number(board)
    return board


# Проверка, полное ли игровое поле
def board_is_full(board):
    for cell in board:
        if cell == 0:
            return False
    return True


# Добавление случайного числа на поле
def add_random_number(board):
    number = 4 if randint(1, 10) == 1 else 2
    empty_cells = []
    for i in range(len(board)):
        if board[i] == 0:
            empty_cells.append(i)
    board[choice(empty_cells)] = number


# Вывод игрового поля
def print_board(board, score, high_score):
    print("-------======= 2 0 4 8 =======-------\n")
    print_scores(score, high_score)
    print("+--------+--------+--------+--------+")
    for y in range(4):
        for i in range(3):
            print("|", end="")
            for x in range(4):
                index = y * 4 + x
                if i != 1 or board[index] == 0:
                    print("        ", end="")
                else:
                    spaces = (8 - len(str(board[index]))) // 2
                    print(" " * (spaces + len(str(board[index])) % 2), end="")
                    print(board[index], end="")
                    print(" " * spaces, end="")
                print("|", end="")
            print()
        print("+--------+--------+--------+--------+")
    print()


# Вывод счета и лучшего результата
def print_scores(score, high_score):
    print(f"  SCORE:   {score}{' ' * (9 - len(str(score)))}HI:     {high_score}")


# Получение от игрока направления движения
def get_valid_move():
    move = input("Введите WASD для выбора направления или R для перезапуска игры: ").lower()
    while move not in tuple("wasdr"):
        move = input("Введите W, A, S, D или R: ").lower()
    print()
    return move


# Обновление состояния игры в соответствии с выбранным направлением
def update_board(board, move):
    global score
    if move == "w":
        score = move_up(board)
    elif move == "a":
        score = move_left(board)
    elif move == "s":
        score = move_down(board)
    elif move == "d":
        score = move_right(board)
    elif move == "r":
        return 0
    return score


# Движение вверх
def move_up(board):
    score = 0
    merged = []
    for i in range(4, 16):
        while i > 3 and board[i - 4] == 0:
            board[i - 4] = board[i]
            board[i] = 0
            i -= 4
        if i > 3 and board[i - 4] == board[i] and i - 4 not in merged:
            board[i - 4] *= 2
            merged.append(i - 4)
            score += board[i - 4]
            board[i] = 0
    return score


# Движение влево
def move_left(board):
    score = 0
    merged = []
    for i in range(1, 16):
        while i % 4 != 0 and board[i - 1] == 0:
            board[i - 1], board[i] = board[i], 0
            i -= 1
        if i % 4 != 0 and board[i - 1] == board[i] and i - 1 not in merged:
            board[i - 1] *= 2
            merged.append(i - 1)
            score += board[i - 1]
            board[i] = 0
    return score


# Движение вниз
def move_down(board):
    score = 0
    merged = []
    for i in range(11, -1, -1):
        while i < 12 and board[i + 4] == 0:
            board[i + 4] = board[i]
            board[i] = 0
            i += 4
        if i < 12 and board[i + 4] == board[i] and i + 4 not in merged:
            board[i + 4] *= 2
            merged.append(i + 4)
            score += board[i + 4]
            board[i] = 0
    return score


# Движение вправо
def move_right(board):
    score = 0
    merged = []
    for i in range(14, -1, -1):  # начинаем с последнего элемента и двигаемся влево
        while i % 4 != 3 and board[i + 1] == 0:
            board[i + 1], board[i] = board[i], 0
            i += 1
        if i % 4 != 3 and board[i + 1] == board[i] and i + 1 not in merged:
            board[i + 1] *= 2
            merged.append(i + 1)
            score += board[i + 1]
            board[i] = 0
    return score


# Вывод результатов
def print_results(board, score, high_score):
    if has_won(board):
        print("Поздравляю! вы выиграли")
    else:
        print("К сожалению вы проиграли...")
    print(f"Ваш финальный результат: {score}")
    if score == high_score:
        print("Вы установили рекорд")
    print()


# Проверка, выиграл ли игрок
def has_won(board):
    for cell in board:
        if cell >= 2048:
            return True
    return False


# Получение ответа от игрока на вопрос о продолжении игры
def get_valid_answer():
    answer = input("Хотите сыграть снова? (да/нет): ").lower()
    while answer not in ("да", "нет"):
        answer = input("Просто ответьте \"да\" или \"нет\": ").lower()
    print()
    return False if answer == "нет" else True


# Сохранение лучшего результата в файл
def save_high_score(high_score):
    try:
        with open(FILENAME, "w") as file:
            file.write(str(high_score))
    except OSError:
        print("Невозможно записать лучший результат в файл.\n")


# Вывод прощального сообщения
def print_outro():
    print("Спасибо")
    input("Нажмите ENTER для окончания игры. ")


if __name__ == "__main__":
    main
