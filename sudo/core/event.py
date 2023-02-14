# -*- coding: utf-8 -*-
# @File    : event.py
# @Author  : Zichi Zhang
# @Date    : 2023/2/14
# @Software: PyCharm

import sudo.core.gen_sudo as core_gen_sudo


class Event:
    def __init__(self, screen):
        self.__surface = screen.surface
        self.__all_users_num = [[None for _ in range(9)] for _ in range(9)]
        self.__cell_num_dict = {}
        self.__cell_row_col = [[(row, col) for col in range(9)] for row in range(9)]
        self.__clear_flag = False
        self.__all_num_is_valid = [[False for _ in range(9)] for _ in range(9)]

    @property
    def cell_num_dict(self):
        return self.__cell_num_dict

    @property
    def all_users_num(self):
        return self.__all_users_num

    @all_users_num.setter
    def all_users_num(self, val):
        self.__all_users_num = val

    @property
    def all_num_is_valid(self):
        return self.__all_num_is_valid

    @property
    def clear_flag(self):
        return self.__clear_flag

    @clear_flag.setter
    def clear_flag(self, val):
        self.__clear_flag = val

    def cell_is_pressed(self, all_cell_button):
        """
        events:
            highlight_cell
            highlight_number
        """
        for row in range(9):
            for col in range(9):
                # when press the cell
                if all_cell_button[row][col].collidepoint(self.__surface):
                    current_cell_row_col = (row, col)
                    return current_cell_row_col
        return False

    def num_is_pressed(self, all_num_button):
        for i in range(9):
            if all_num_button[i].collidepoint(self.__surface):
                return i + 1  # return the number which is pressed
        return None

    def diff_option_is_pressed(self, all_difficulty_option_button):
        for diff_option in range(len(all_difficulty_option_button)):
            if all_difficulty_option_button[diff_option].collidepoint(self.__surface):
                return diff_option + 1  # return the difficulty option
        return False

    def add_num_to_cell(self, num, current_cell_row_col, num_in_screen, puzzle):
        # 只有当格子已被选中时，点击number button才生效
        if current_cell_row_col is not None:
            row = current_cell_row_col[0]
            col = current_cell_row_col[1]
            # 如果谜题中值为“ ”，说明未被填入数字
            if puzzle[row][col] == " ":
                self.__all_num_is_valid[row][col] = core_gen_sudo.GenSudo.check_num(num_in_screen, row, col, num)
                num_in_screen[row][col] = num  # add user's num choice to list
                self.__all_users_num[row][col] = num
                string = "{row}, {col}".format(row=row, col=col)
                self.__cell_num_dict[string] = num
        return num_in_screen

    def regen_sudo(self, diff_option):
        blank_num = 10 * diff_option
        gen_sudo = core_gen_sudo.GenSudo(blank_num)
        self.__clear_flag = True
        return gen_sudo

    def create_cell_num_dict(self, puzzle):
        for row in range(9):
            for col in range(9):
                string = "{row}, {col}".format(row=row, col=col)
                if puzzle[row][col] != " ":
                    self.__cell_num_dict[string] = puzzle[row][col]
                else:
                    self.__cell_num_dict[string] = None
