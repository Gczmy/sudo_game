# -*- coding: utf-8 -*-
# @File    : gen_sudo.py
# @Author  : Zichi Zhang
# @Date    : 2023/2/13
# @Software: PyCharm

import random
import copy


class GenSudo:
    def __init__(self, none_num):
        self.__nums = list(range(1, 10))
        self.__answer = self.__generate_sudoku([[0 for _ in range(9)] for _ in range(9)])
        self.__none_num = none_num
        self.__puzzle = self.__generate_sudo_puzzle()

    @property
    def answer(self):
        return self.__answer

    @property
    def puzzle(self):
        return self.__puzzle

    def __generate_sudo_puzzle(self):
        puzzle_list = [1 for _ in range(9 * 9)]
        puzzle = copy.deepcopy(self.__answer)
        for i in range(9 * 9):
            if i < self.__none_num:
                puzzle_list[i] = " "
        random.shuffle(puzzle_list)
        for i in range(9 * 9):
            if puzzle_list[i] == " ":
                row = int(i / 9)
                col = i % 9
                puzzle[row][col] = " "
        return puzzle

    @staticmethod
    def check_num(sudoku, row, col, val):
        # 检查当前位置是否合法
        for i in range(9):
            if sudoku[row][i] == val and i != col:
                return False
            if sudoku[i][col] == val and i != row:
                return False
        start_row = row // 3 * 3
        start_col = col // 3 * 3
        for i in range(3):
            for j in range(3):
                if sudoku[start_row + i][start_col + j] == val and start_row + i != row and start_col + j != col:
                    return False
        return True

    def RollUp(self, unit):
        return unit[1:]+[unit[0]]

    def RollDown(self, unit):
        return [unit[-1]]+unit[:-1]

    def RollLeft(self, unit):
        return [self.RollUp(x) for x in unit]

    def RollRight(self, unit):
        return [self.RollDown(x) for x in unit]

    def unit_copy(self, puzzle, row, col, unit):
        for r in range(3):
            for c in range(3):
                puzzle[row * 3 + r][col * 3 + c] = unit[r][c]

    def __generate_sudoku(self, puzzle):
        random.shuffle(self.__nums)
        bu = [[self.__nums[r * 3 + c] for c in range(3)] for r in range(3)]

        l_bu = self.RollUp(bu)
        r_bu = self.RollDown(bu)
        t_bu = self.RollLeft(bu)
        b_bu = self.RollRight(bu)

        self.unit_copy(puzzle, 1, 1, bu)
        self.unit_copy(puzzle, 1, 0, l_bu)
        self.unit_copy(puzzle, 1, 2, r_bu)
        self.unit_copy(puzzle, 0, 1, t_bu)
        self.unit_copy(puzzle, 2, 1, b_bu)
        self.unit_copy(puzzle, 0, 0, self.RollLeft(l_bu))
        self.unit_copy(puzzle, 2, 0, self.RollRight(l_bu))
        self.unit_copy(puzzle, 0, 2, self.RollLeft(r_bu))
        self.unit_copy(puzzle, 2, 2, self.RollRight(r_bu))

        return puzzle
