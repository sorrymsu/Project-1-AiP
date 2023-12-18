import pytest
from your_module_name import get_new_board, board_is_full, add_random_number, move_left, move_right, move_up, move_down

# Замените 'your_module_name' на имя вашего модуля

def test_get_new_board():
    board = get_new_board()
    assert len(board) == 16
    assert sum(board) == 0  # Проверяем, что все ячейки заполнены нулями

def test_board_is_full_positive():
    full_board = [2] * 16
    assert board_is_full(full_board)  # Все ячейки заполнены, должно вернуть True

def test_board_is_full_negative():
    empty_board = [0] * 16
    assert not board_is_full(empty_board)  # Есть пустые ячейки, должно вернуть False

def test_add_random_number():
    board = [2, 0, 4, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    add_random_number(board)
    assert any(cell != 0 for cell in board)  # После добавления случайного числа, должна быть хотя бы одна ненулевая ячейка

# Тесты для функций move_left, move_right, move_up, move_down аналогичны.
# Напишите положительные и отрицательные тесты для этих функций.

# Например:
def test_move_left_positive():
    board = [2, 2, 0, 0,
             4, 0, 0, 0,
             0, 0, 0, 0,
             0, 0, 0, 0]
    score = move_left(board)
    assert score == 4  # Проверяем, что счет увеличился после слияния

def test_move_left_negative():
    board = [2, 0, 2, 0,
             4, 0, 0, 0,
             0, 0, 0, 0,
             0, 0, 0, 0]
    score = move_left(board)
    assert score == 0  # Проверяем, что счет не изменился (нет слияний)

# Продолжение файла test_2048.py

def test_move_right_positive():
    board = [0, 0, 2, 2,
             0, 0, 0, 4,
             0, 0, 0, 0,
             0, 0, 0, 0]
    score = move_right(board)
    assert score == 4  # Проверяем, что счет увеличился после слияния

def test_move_right_negative():
    board = [0, 0, 2, 0,
             0, 0, 0, 4,
             0, 0, 0, 0,
             0, 0, 0, 0]
    score = move_right(board)
    assert score == 0  # Проверяем, что счет не изменился (нет слияний)

def test_move_up_positive():
    board = [2, 0, 0, 0,
             2, 4, 0, 0,
             0, 0, 0, 0,
             0, 0, 0, 0]
    score = move_up(board)
    assert score == 4  # Проверяем, что счет увеличился после слияния

def test_move_up_negative():
    board = [2, 0, 0, 0,
             0, 4, 0, 0,
             0, 0, 0, 0,
             0, 0, 0, 0]
    score = move_up(board)
    assert score == 0  # Проверяем, что счет не изменился (нет слияний)

def test_move_down_positive():
    board = [0, 0, 0, 0,
             0, 0, 0, 0,
             2, 0, 0, 0,
             2, 4, 0, 0]
    score = move_down(board)
    assert score == 4  # Проверяем, что счет увеличился после слияния

def test_move_down_negative():
    board = [0, 0, 0, 0,
             2, 0, 0, 0,
             2, 4, 0, 0,
             0, 0, 0, 0]
    score = move_down(board)
    assert score == 0  # Проверяем, что счет не изменился (нет слияний)

# Пример теста для функции get_valid_answer
def test_get_valid_answer():
    assert get_valid_answer("да") == True
    assert get_valid_answer("нет") == False
    assert get_valid_answer("другой ответ") == False

    # Продолжение файла test_2048.py

    def test_has_won_positive():
        board = [0, 0, 0, 0,
                 0, 0, 0, 0,
                 0, 0, 0, 0,
                 0, 0, 0, 2048]
        assert has_won(board) == True  # Проверяем, что has_won возвращает True, если есть 2048

    def test_has_won_negative():
        board = [0, 0, 0, 0,
                 0, 0, 0, 0,
                 0, 0, 0, 0,
                 0, 0, 0, 1024]
        assert has_won(board) == False  # Проверяем, что has_won возвращает False, если нет 2048

    # Продолжение файла test_2048.py

    def test_get_high_score_positive():
        # Создаем временный файл для тестирования
        with open("test_high_score.txt", "w") as temp_file:
            temp_file.write("100")

        # Проверяем, что функция корректно считывает лучший результат из файла
        assert get_high_score("test_high_score.txt") == 100

    def test_get_high_score_negative():
        # Проверяем, что функция возвращает 0 при отсутствии файла
        assert get_high_score("/несуществующий/файл.txt") == 0

        # Проверяем, что функция возвращает 0 при некорректных данных в файле
        with open("test_high_score.txt", "w") as temp_file:
            temp_file.write("некорректные данные")
        assert get_high_score("test_high_score.txt") == 0

    def test_save_high_score_exception():
        # Проверяем, что функция корректно обрабатывает ошибки при записи в файл
        with open("test_high_score.txt", "r") as temp_file:
            # Устанавливаем права доступа только на чтение
            temp_file.close()
            os.chmod("test_high_score.txt", stat.S_IREAD)
            with pytest.raises(OSError):
                save_high_score("test_high_score.txt", 150)

        # Восстанавливаем права доступа
        os.chmod("test_high_score.txt", stat.S_IWRITE)

    # Завершение файла test_2048.py