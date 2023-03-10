# -*- coding: utf-8 -*-
# @File    : screen.py
# @Author  : Zichi Zhang
# @Date    : 2023/2/12
# @Software: PyCharm

import numpy as np
import pygame
import copy
import sudo.core.button as core_button
import sudo.core.gen_sudo as core_gen_sudo
import sudo.core.component as core_comp


class Screen:
    """
    initialization screen
    """

    def __init__(self):
        # 初始化
        pygame.init()
        # 设置主屏幕大小
        SCREEN_WIDTH = 1080
        SCREEN_HEIGHT = 960
        self.__screen_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
        self.__surface = pygame.display.set_mode(self.__screen_size)
        # 设置标题
        pygame.display.set_caption("sudo")
        # 设置一个控制主循环的变量
        self.__done = False
        # 创建时钟对象
        self.__clock = pygame.time.Clock()
        self.__surface.fill((255, 255, 255))
        # 获取字体对象
        self.__basicFont = pygame.font.SysFont("方正粗黑宋简体", 100)
        self.__cell_row_col = [[(row, col) for col in range(9)] for row in range(9)]
        self.__cell_num_dict = {}  # store which number in a cell, key: (cell row, cell col), value: num
        self.__current_cell_pos = None
        self.__current_cell_row_col = None
        self.__users_num = [[None for _ in range(9)] for _ in range(9)]
        self.__clear_flag = False  # flag for clear users num
        self.__num_mat = [[None for _ in range(9)] for _ in range(9)]  # store all the number's value on the board
        self.__num_color = [[None for _ in range(9)] for _ in range(9)]  # store all the number's color on the board
        self.__color_map = {'black': [0, 0, 0],
                            'apple green': [0.55 * 255, 0.71 * 255, 0 * 255],
                            'white': [255, 255, 255],
                            'blue': [0, 0.5 * 255, 255],
                            'red': [255, 0, 0],
                            'light gray': [0.75 * 255, 0.75 * 255, 0.75 * 255],
                            'baby blue': [0.54 * 255, 0.81 * 255, 0.94 * 255]}

    @property
    def done(self):
        return self.__done

    @property
    def surface(self):
        return self.__surface

    @property
    def screen_size(self):
        return self.__screen_size

    @property
    def current_cell_pos(self):
        return self.__current_cell_pos

    @property
    def current_cell_row_col(self):
        return self.__current_cell_row_col

    @property
    def cell_num_dict(self):
        return self.__cell_num_dict

    @cell_num_dict.setter
    def cell_num_dict(self, val):
        self.__cell_num_dict = val

    @done.setter
    def done(self, val):
        self.__done = val

    @property
    def clock(self):
        return self.__clock

    @staticmethod
    def update_screen():
        pygame.display.update()

    def draw_square(self, points_pos):
        p = points_pos
        p_num_in_row = len(p)
        p_num_in_col = len(p[0])
        black = [0, 0, 0]
        dark_gray = np.multiply([0.66, 0.66, 0.66], 255)
        # 灰框横条
        for i in range(p_num_in_row):
            if i % 3:
                pygame.draw.line(self.__surface, dark_gray, p[i][0], p[i][p_num_in_row - 1], 5)
        # 灰框竖条
        for i in range(p_num_in_col):
            if i % 3:
                pygame.draw.line(self.__surface, dark_gray, p[0][i], p[p_num_in_col - 1][i], 5)
        # 黑框横条
        for i in range(p_num_in_row):
            if not i % 3:
                pygame.draw.line(self.__surface, black, p[i][0], p[i][p_num_in_row - 1], 5)

        # 黑框竖条
        for i in range(p_num_in_col):
            if not i % 3:
                pygame.draw.line(self.__surface, black, p[0][i], p[p_num_in_col - 1][i], 5)

    def draw_cell_button(self, all_cell_button):
        for row in range(9):
            for col in range(9):
                # draw cell buttons
                all_cell_button[row][col].draw(self.__surface)

    def draw_num_button(self, all_num_button):
        # draw number buttons
        for i in range(9):
            all_num_button[i].draw(self.__surface)

    def draw_difficulty_option_button(self, all_diff_opt_button):
        for i in all_diff_opt_button:
            i.draw(self.__surface)

    def highlight_cell(self, points_pos, all_cell_pos, all_cell_button, current_cell_row_col):
        """
        When a cell is pressed, highlight other cells in the same row and column as well as other cells in the larger
        cell
        cell which is pressed: green
        other cells in the same row and column: light blue
        other cells in the larger cell: light gray
        """
        p = points_pos
        cell_center_x = 0.93 * (p[1][1][0] - p[0][0][0])
        cell_center_y = 0.93 * (p[1][1][1] - p[0][0][1])
        cell_center = (cell_center_x, cell_center_y)
        row = current_cell_row_col[0]
        col = current_cell_row_col[1]
        for row_ in range(9):
            for col_ in range(9):
                # other cells in the same row and column: light blue
                if row_ == row or col_ == col:
                    color = self.__color_map['baby blue']
                    all_cell_button[row_][col_] = core_button.CellButton(cell_center, all_cell_pos[row_][col_], color)
                # other cells in the larger cell: light gray
                elif int(row_ / 3) == int(row / 3) and int(col_ / 3) == int(col / 3):
                    color = self.__color_map['light gray']
                    all_cell_button[row_][col_] = core_button.CellButton(cell_center, all_cell_pos[row_][col_], color)
                # other cells: white
                else:
                    color = self.__color_map['white']
                    all_cell_button[row_][col_] = core_button.CellButton(cell_center, all_cell_pos[row_][col_], color)

        # cell which is pressed: green
        color = self.__color_map['apple green']
        all_cell_button[row][col] = core_button.CellButton(cell_center, all_cell_pos[row][col], color)
        return all_cell_button

    def highlight_number(self, all_cell_pos, current_cell_row_col):
        """
        highlight all the same numbers when press the cell which has a number
        """
        row = current_cell_row_col[0]
        col = current_cell_row_col[1]
        num = self.__num_mat[row][col]
        for row_ in range(9):
            for col_ in range(9):
                if self.__num_mat[row][col] != " ":
                    if self.__num_mat[row_][col_] == num:
                        self.__num_color[row_][col_] = 'apple green'
                    else:
                        if self.__num_color[row_][col_] == 'blue' or self.__num_color[row_][col_] == 'red':
                            pass
                        else:
                            self.__num_color[row_][col_] = 'black'
                else:
                    if self.__num_color[row_][col_] == 'blue' or self.__num_color[row_][col_] == 'red':
                        pass
                    else:
                        self.__num_color[row_][col_] = 'black'

        self.__num_color[row][col] = 'white'
        self.__current_cell_pos = all_cell_pos[row][col]
        self.__current_cell_row_col = (row, col)

    def __show_num_in_cell(self, pos, num, color):
        num_font = pygame.font.SysFont("方正粗黑宋简体", 100)
        num_surface = num_font.render(str(num), True, color)
        rect = num_surface.get_rect(center=pos)
        self.__surface.blit(num_surface, rect.topleft)

    def create_num_mat(self, puzzle):
        self.__num_mat = [[None for _ in range(9)] for _ in range(9)]  # store all the number's value on the board
        self.__num_color = [[None for _ in range(9)] for _ in range(9)]  # store all the number's color on the board
        for row in range(9):
            for col in range(9):
                self.__num_mat[row][col] = puzzle[row][col]
                self.__num_color[row][col] = 'black'

    def update_num_mat(self, all_users_num, all_num_is_valid):
        """
        create the number matrix in the board
        """
        for row in range(9):
            for col in range(9):
                if all_users_num[row][col] is not None:
                    self.__num_mat[row][col] = all_users_num[row][col]
                    if all_num_is_valid[row][col]:
                        self.__num_color[row][col] = 'blue'
                    else:
                        self.__num_color[row][col] = 'red'

    def show_num_in_screen(self, all_cell_pos):
        for row in range(9):
            for col in range(9):
                num = self.__num_mat[row][col]
                color = self.__num_color[row][col]
                color = self.__color_map[color]
                pos = all_cell_pos[row][col]
                self.__show_num_in_cell(pos, num, color)

    def show_remaining_num(self, all_num_pos, all_remain_num):
        screen_size = self.__screen_size
        screen_width = screen_size[0]
        screen_height = screen_size[1]
        remain_num_font = pygame.font.SysFont("方正粗黑宋简体", 30)
        yellow = np.multiply([1, 0.75, 0], 255)
        white = np.multiply([1, 1, 1], 255)
        for i in range(9):
            pos = all_num_pos[i]
            remain_num_image = remain_num_font.render(str(all_remain_num[i]), True, yellow, white)
            remain_num_pos = [pos[0] + 0.03 * screen_width, pos[1] + 0.015 * screen_height]
            rect = remain_num_image.get_rect(center=remain_num_pos)
            self.__surface.blit(remain_num_image, rect.topleft)

    def clear_all_users_num(self, all_users_num):
        # 遍历所有格子，若用户数字与字典中数字相等（即确定为用户数字），则清除该格子字典值
        for row in range(9):
            for col in range(9):
                string = "{row}, {col}".format(row=row, col=col)
                if all_users_num[row][col] == self.__cell_num_dict[string]:
                    self.__cell_num_dict[string] = None
