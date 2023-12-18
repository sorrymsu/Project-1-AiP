from random import randint, choice

FILENAME = "2048_high_score.txt"


def main():
    print_intro()
    high_score = get_high_score()
    wants_to_play = True

    while wants_to_play:
        board = get_new_board()
        score = 0
        move = None

        while not (board_is_full(board) or move == "r"):
            add_random_number(board)
            print_board(board, score, high_score)
            move = get_valid_move()
            score += update_board(board, move)

            if score > high_score:
                high_score = score

        print_board(board, score, high_score)
        print_results(board, score, high_score)
        wants_to_play = get_valid_answer()

    save_high_score(high_score)
    print_outro()


def print_intro():
    print("Добро пожаловать в игру \"2048\"!\n")


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


def get_new_board():
    board = [0 for _ in range(16)]
    add_random_number(board)
    return board


def board_is_full(board):
    return all(cell != 0 for cell in board)


def add_random_number(board):
    number = 4 if randint(1, 10) == 1 else 2
    empty_cells = [i for i, cell in enumerate(board) if cell == 0]
    board[choice(empty_cells)] = number


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


def print_scores(score, high_score):
    print(f"  SCORE:   {score}{' ' * (9 - len(str(score)))}HI:     {high_score}")


def get_valid_move():
    move = input("Введите WASD для выбора направления или R для перезапуска игры: ").lower()

    while move not in tuple("wasdr"):
        move = input("Введите W, A, S, D или R: ").lower()

    print()
    return move


def update_board(board, move):
    if move == "w":
        return move_up(board)
    elif move == "a":
        return move_left(board)
    elif move == "s":
        return move_down(board)
    elif move == "d":
        return move_right(board)
    elif move == "r":
        return 0


def move_up(board):
    score = 0
    merged = []

    for i in range(4, 16):
        while i > 3 and board[i - 4] == 0:
            board[i - 4], board[i] = board[i], 0
            i -= 4

        if i > 3 and board[i - 4] == board[i] and i - 4 not in merged:
            board[i - 4] *= 2
            merged.append(i - 4)
            score += board[i - 4]
            board[i] = 0

    return score


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


def move_right(board):
    score = 0
    merged = []

    for i in range(14, -1, -1):
        while i % 4 != 3 and board[i + 1] == 0:
            board[i + 1], board[i] = board[i], 0
            i += 1

        if i % 4 != 3 and board[i + 1] == board[i] and i + 1 not in merged:
            board[i + 1] *= 2
            merged.append(i + 1)
            score += board[i + 1]
            board[i] = 0

    return score


def print_results(board, score, high_score):
    if has_won(board):
        print("Поздравляю! Вы выиграли.")
    else:
        print("К сожалению, вы проиграли...")

    print(f"Ваш финальный результат: {score}")

    if score == high_score:
        print("Вы установили рекорд!")
    print()


def has_won(board):
    return any(cell >= 2048 for cell in board)


def get_valid_answer():
    answer = input("Хотите сыграть снова? (да/нет): ").lower()

    while answer not in ("да", "нет"):
        answer = input("Просто ответьте \"да\" или \"нет\": ").lower()

    print()
    return False if answer == "нет" else True


def save_high_score(high_score):
    try:
        with open(FILENAME, "w") as file:
            file.write(str(high_score))
    except OSError:
        print("Невозможно записать лучший результат в файл.\n")


def print_outro():
    print("Спасибо!")
    input("Нажмите ENTER для окончания игры. ")


if __name__ == "__main__":
    main()
