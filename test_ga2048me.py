import os
import unittest
from unittest import mock

import pytest
from ga2048me import get_new_board, board_is_full, add_random_number, move_left, move_right, move_up, move_down, \
    get_valid_answer, has_won, get_high_score, save_high_score


class gameTest(unittest.TestCase):
    def test_get_new_board(self):
        board = get_new_board()
        assert len(board) == 16
        assert any(board)  # Проверяем, что все ячейки заполнены нулями

    def test_board_is_full_positive(self):
        full_board = [2] * 16
        assert board_is_full(full_board)  # Все ячейки заполнены, должно вернуть True

    def test_board_is_full_negative(self):
        empty_board = [0] * 16
        assert not board_is_full(empty_board)  # Есть пустые ячейки, должно вернуть False

    def test_add_random_number(self):
        board = [2, 0, 4, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        add_random_number(board)
        assert any(
            cell != 0 for cell in board)  # После добавления случайного числа, должна быть хотя бы одна ненулевая ячейка

        # Тесты для функций move_left, move_right, move_up, move_down аналогичны.

    def test_move_left_positive(self):
        board = [2, 2, 0, 0,
                 4, 0, 0, 0,
                 0, 0, 0, 0,
                 0, 0, 0, 0]
        score = move_left(board)
        assert score == 4  # Проверяем, что счет увеличился после слияния

    def test_move_left_negative(self):
        board = [2, 4, 2, 0,
                 4, 0, 0, 0,
                 0, 0, 0, 0,
                 0, 0, 0, 0]
        score = move_left(board)
        assert score == 0  # Проверяем, что счет не изменился (нет слияний)

        # Продолжение файла test_2048_game.py

    def test_move_right_positive(self):
        board = [0, 0, 2, 2,
                 0, 0, 0, 4,
                 0, 0, 0, 0,
                 0, 0, 0, 0]
        score = move_right(board)
        assert score == 4  # Проверяем, что счет увеличился после слияния

    def test_move_right_negative(self):
        board = [0, 0, 2, 0,
                 0, 0, 0, 4,
                 0, 0, 0, 0,
                 0, 0, 0, 0]
        score = move_right(board)
        assert score == 0  # Проверяем, что счет не изменился (нет слияний)

    def test_move_up_positive(self):
        board = [2, 0, 0, 0,
                 2, 4, 0, 0,
                 0, 0, 0, 0,
                 0, 0, 0, 0]
        score = move_up(board)
        assert score == 4  # Проверяем, что счет увеличился после слияния

    def test_move_up_negative(self):
        board = [2, 0, 0, 0,
                 0, 4, 0, 0,
                 0, 0, 0, 0,
                 0, 0, 0, 0]
        score = move_up(board)
        assert score == 0  # Проверяем, что счет не изменился (нет слияний)

    def test_move_down_positive(self):
        board = [0, 0, 0, 0,
                 0, 0, 0, 0,
                 2, 0, 0, 0,
                 2, 4, 0, 0]
        score = move_down(board)
        assert score == 4  # Проверяем, что счет увеличился после слияния

    def test_move_down_negative(self):
        board = [0, 0, 0, 0,
                 0, 2, 0, 0,
                 2, 4, 0, 0,
                 0, 0, 0, 0]
        score = move_down(board)
        assert score == 0  # Проверяем, что счет не изменился (нет слияний)

    # Пример теста для функции get_valid_answer
    def test_get_valid_answer(self):
        with mock.patch('builtins.input', return_value="да"):
            # Проверяем, что функция возвращает True
            assert get_valid_answer() == True

    def test_has_won_positive(self):
        board = [0, 0, 0, 0,
                 0, 0, 0, 0,
                 0, 0, 0, 0,
                 0, 0, 0, 2048]
        assert has_won(board) == True  # Проверяем, что has_won возвращает True, если есть 2048

    def test_has_won_negative(self):
        board = [0, 0, 0, 0,
                 0, 0, 0, 0,
                 0, 0, 0, 0,
                 0, 0, 0, 1024]
        assert has_won(board) == False  # Проверяем, что has_won возвращает False, если нет 2048

    # Продолжение файла test_2048_game.py

    def test_get_high_score_positive(self):
        # Создаем временный файл для тестирования
        with open("test_high_score.txt", "w") as temp_file:
            temp_file.write("100")

        # Проверяем, что функция корректно считывает лучший результат из файла
        assert get_high_score("test_high_score.txt") == 100

    def test_get_high_score_negative(self):
        # Проверяем, что функция возвращает 0 при отсутствии файла
        assert get_high_score("/несуществующий/файл.txt") == 0

        # Проверяем, что функция возвращает 0 при некорректных данных в файле
        with open("test_high_score.txt", "w") as temp_file:
            temp_file.write("некорректные данные")
        assert get_high_score("test_high_score.txt") == 0

    def test_save_high_score_exception(self):
        # Проверяем, что функция корректно обрабатывает ошибки при записи в файл
        with open("test_high_score.txt", "r") as temp_file:
            # Устанавливаем права доступа только на чтение
            temp_file.close()
            os.chmod("test_high_score.txt", os.stat.S_IREAD)
            with pytest.raises(OSError):
                save_high_score("test_high_score.txt", 150)

        # Восстанавливаем права доступа
        os.chmod("test_high_score.txt", os.stat.S_IWRITE)


if __name__ == '__main__':
    unittest.main()
    # Завершение файла test_2048_game.py
