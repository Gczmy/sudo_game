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


class screen:
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
        self.__points = self.__build_points(self.__screen_size)
        self.__draw_square(self.__surface, self.__points)
        self.__cell_pos, self.__cell_button = self.__create_cell_button(self.__screen_size)
        self.__current_cell_pos = None
        self.__current_cell_row_col = None
        self.__users_num = [[None for _ in range(9)] for _ in range(9)]
        self.__clear_flag = False  # flag for clear users num

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
    def cell_button(self):
        return self.__cell_button

    @property
    def current_cell_pos(self):
        return self.__current_cell_pos

    @property
    def current_cell_row_col(self):
        return self.__current_cell_row_col

    @done.setter
    def done(self, val):
        self.__done = val

    @property
    def clock(self):
        return self.__clock

    @staticmethod
    def update_screen():
        pygame.display.update()

    def __build_points(self, screen_size):
        # p_1-----p_2-----p_3-----p_4
        #  |-------|-------|-------|
        #  |-------|-------|-------|
        # p_5-----p_6-----p_7-----p_8
        #  |-------|-------|-------|
        #  |-------|-------|-------|
        # p_9-----p_10-----p_11-----p_12
        #  |-------|-------|-------|
        #  |-------|-------|-------|
        # p_13-----p_14-----p_15-----p_16

        # points number in row/column
        p_num_in_row = 10
        p_num_in_col = 10

        screen_width = screen_size[0]
        screen_height = screen_size[1]
        all_len = min(screen_width, screen_height)
        blank_width = all_len / 10
        blank_height = all_len / 10
        start_point = (blank_width, blank_height)
        p_d_length = (all_len - 2 * blank_width) / p_num_in_row - 1  # points distance length
        p_d_width = (all_len - 2 * blank_height) / p_num_in_col - 1  # points distance width

        # build points
        points = [[(0, 0) for _ in range(p_num_in_row)] for _ in range(p_num_in_col)]
        points[0][0] = start_point  # point 1
        # loop for build points
        for row in range(p_num_in_col):
            if row < p_num_in_row - 1:
                zipped = zip(points[row][0], (p_d_length, 0))
                mapped = map(sum, zipped)
                points[row + 1][0] = tuple(mapped)
            for col in range(p_num_in_row - 1):
                zipped = zip(points[row][col], (0, p_d_width))
                mapped = map(sum, zipped)
                points[row][col + 1] = tuple(mapped)
        # create cell num dict
        for row in range(9):
            for col in range(9):
                string = "{row}, {col}".format(row=row, col=col)
                self.__cell_num_dict[string] = None
        return points

    @staticmethod
    def __draw_square(surface, points):
        p = points
        p_num_in_row = len(p)
        p_num_in_col = len(p[0])
        black = [0, 0, 0]
        dark_gray = np.multiply([0.66, 0.66, 0.66], 255)
        # 灰框横条
        for i in range(p_num_in_row):
            if i % 3:
                pygame.draw.line(surface, dark_gray, p[i][0], p[i][p_num_in_row - 1], 5)
        # 灰框竖条
        for i in range(p_num_in_col):
            if i % 3:
                pygame.draw.line(surface, dark_gray, p[0][i], p[p_num_in_col - 1][i], 5)
        # 黑框横条
        for i in range(p_num_in_row):
            if not i % 3:
                pygame.draw.line(surface, black, p[i][0], p[i][p_num_in_row - 1], 5)

        # 黑框竖条
        for i in range(p_num_in_col):
            if not i % 3:
                pygame.draw.line(surface, black, p[0][i], p[p_num_in_col - 1][i], 5)

    def __create_cell_button(self, screen_size):
        # points number in row/column
        p_num_in_row = 10
        p_num_in_col = 10

        screen_width = screen_size[0]
        screen_height = screen_size[1]
        all_len = min(screen_width, screen_height)
        blank_width = all_len / 10
        blank_height = all_len / 10
        p_d_length = (all_len - 2 * blank_width) / p_num_in_row - 1  # points distance length
        p_d_width = (all_len - 2 * blank_height) / p_num_in_col - 1  # points distance width

        p = self.__points
        p_num_in_row = len(p)
        p_num_in_col = len(p[0])
        cell_pos = [[(0, 0) for _ in range(p_num_in_row - 1)] for _ in range(p_num_in_col - 1)]
        cell_pos[0][0] = np.add(p[0][0], np.multiply(np.add(p[1][1], np.multiply(p[0][0], -1)), 0.5))
        for row in range(p_num_in_col - 1):
            if row < p_num_in_row - 2:
                zipped = zip(cell_pos[row][0], (p_d_length, 0))
                mapped = map(sum, zipped)
                cell_pos[row + 1][0] = tuple(mapped)
            for col in range(p_num_in_row - 2):
                zipped = zip(cell_pos[row][col], (0, p_d_width))
                mapped = map(sum, zipped)
                cell_pos[row][col + 1] = tuple(mapped)
        cell_button = [[None for j in range(p_num_in_row - 1)] for i in range(p_num_in_col - 1)]
        for row in range(p_num_in_col - 1):
            for col in range(p_num_in_row - 1):
                cell_image = pygame.Surface(np.multiply(np.add(p[1][1], np.multiply(p[0][0], -1)), 0.93))
                cell_image.fill(color='white')
                cell_button[row][col] = core_button.Button(cell_pos[row][col][0], cell_pos[row][col][1], cell_image, 1)
        return cell_pos, cell_button

    def __highlight_cell(self, row, col):
        """
        When a cell is pressed, highlight other cells in the same row and column as well as other cells in the larger
        cell
        cell which is pressed: green
        other cells in the same row and column: light blue
        other cells in the larger cell: light gray
        """
        p = self.__points
        green = np.multiply([0.55, 0.71, 0], 255)
        baby_blue = np.multiply([0.54, 0.81, 0.94], 255)
        light_gray = np.multiply([0.75, 0.75, 0.75], 255)
        cell_image = pygame.Surface(np.multiply(np.add(p[1][1], np.multiply(p[0][0], -1)), 0.93))
        for row_ in range(9):
            for col_ in range(9):
                # other cells in the same row and column: light blue
                if row_ == row or col_ == col:
                    cell_image.fill(color=baby_blue)
                    self.__cell_button[row_][col_] = core_button.Button(self.__cell_pos[row_][col_][0],
                                                                        self.__cell_pos[row_][col_][1],
                                                                        cell_image,
                                                                        1)
                # other cells in the larger cell: light gray
                elif int(row_ / 3) == int(row / 3) and int(col_ / 3) == int(col / 3):
                    cell_image.fill(color=light_gray)
                    self.__cell_button[row_][col_] = core_button.Button(self.__cell_pos[row_][col_][0],
                                                                        self.__cell_pos[row_][col_][1],
                                                                        cell_image,
                                                                        1)
                # other cells: white
                else:
                    cell_image.fill(color="white")
                    self.__cell_button[row_][col_] = core_button.Button(self.__cell_pos[row_][col_][0],
                                                                        self.__cell_pos[row_][col_][1],
                                                                        cell_image,
                                                                        1)

        # cell which is pressed: green
        cell_image.fill(color=green)
        self.__cell_button[row][col] = core_button.Button(self.__cell_pos[row][col][0],
                                                          self.__cell_pos[row][col][1], cell_image, 1)

    def __highlight_number(self, row, col, num_in_screen):
        """
        highlight all the same numbers when press the cell which has a number
        """
        green = np.multiply([0.55, 0.71, 0], 255)
        if num_in_screen[row][col] != " ":
            for row_ in range(9):
                for col_ in range(9):
                    if num_in_screen[row_][col_] == num_in_screen[row][col]:
                        num = num_in_screen[row][col]
                        self.__show_num_in_cell(num, row_, col_, green)
        self.__current_cell_pos = self.__cell_pos[row][col]
        self.__current_cell_row_col = (row, col)

    def events_when_press_cell(self, num_in_screen):
        """
        events:
            highlight_cell
            highlight_number
        """
        for row in range(9):
            for col in range(9):
                # draw cell buttons
                self.__cell_button[row][col].draw(self.__surface)
                # when press the cell
                if self.__cell_button[row][col].collidepoint(self.__surface):
                    self.__highlight_cell(row, col)
                    # self.__highlight_number(row, col, num_in_screen)
                    self.__current_cell_pos = self.__cell_pos[row][col]
                    self.__current_cell_row_col = (row, col)

    def number_button(self, screen_size):
        """
        build the number button for filling the cell
        """
        num_font = pygame.font.SysFont("方正粗黑宋简体", 100)
        screen_width = screen_size[0]
        screen_height = screen_size[1]
        # define the number's color
        NUM_COL = np.multiply([0, 0.5, 1], 255)
        num_image = []
        num_button = []
        for i in range(9):
            num_image.append(num_font.render(str(i+1), True, NUM_COL))
            pos = [0.12 * screen_width + 0.07 * screen_width * i, 0.87 * screen_height]
            num_button.append(core_button.Button(pos[0], pos[1], num_image[i], 1))
            num_button[i].draw(self.__surface)
            if num_button[i].collidepoint(self.__surface):
                return i + 1  # return the number which is pressed
        return None

    def press_to_add_num_to_cell(self, num, current_cell_row_col):
        if current_cell_row_col is not None:
            row = current_cell_row_col[0]
            col = current_cell_row_col[1]
            self.__users_num[row][col] = num
            string = "{row}, {col}".format(row=self.__cell_row_col[row][col][0], col=self.__cell_row_col[row][col][1])
            self.__cell_num_dict[string] = num

    def __show_num_in_cell(self, num, row, col, color):
        num_font = pygame.font.SysFont("方正粗黑宋简体", 100)
        cell_pos = self.__cell_pos[row][col]
        num_surface = num_font.render(str(num), True, color)
        rect = num_surface.get_rect(center=cell_pos)
        self.__surface.blit(num_surface, rect.topleft)

    def show_num_in_screen(self, num_in_screen, puzzle):
        if self.__clear_flag:
            num_in_screen = copy.deepcopy(puzzle)
        blue = np.multiply([0, 0.5, 1], 255)
        black = np.multiply([0, 0, 0], 255)
        red = np.multiply([1, 0, 0], 255)
        # show puzzle in screen
        for row in range(9):
            for col in range(9):
                num = puzzle[row][col]
                self.__show_num_in_cell(num, row, col, black)
        # show user's choice in screen
        for (cell_row_col, num) in self.__cell_num_dict.items():
            if num:
                # 获得当前格子的行和列的值
                cell_row_col = tuple(map(int, cell_row_col.split(', ')))
                row = cell_row_col[0]
                col = cell_row_col[1]
                # 如果谜题中值为“ ”，说明未被填入数字
                if puzzle[row][col] == " ":
                    num_is_valid = core_gen_sudo.GenSudo.check_num(num_in_screen, row, col, num)
                    num_in_screen[row][col] = num  # add user's num choice to list
                    if num_is_valid:
                        self.__show_num_in_cell(num, row, col, blue)
                    else:
                        self.__show_num_in_cell(num, row, col, red)
        return num_in_screen

    def difficulty_option_button(self, screen_size, gen_sudo):
        key_font = pygame.font.SysFont("SimSun", 30)
        screen_width = screen_size[0]
        screen_height = screen_size[1]
        blue = np.multiply([0, 0.5, 1], 255)
        diff_opt_name = ["入门", "简单", "中等", "困难", "地狱"]
        for i in range(len(diff_opt_name)):
            diff_opt_image = key_font.render(diff_opt_name[i], True, blue)
            diff_opt_pos = [0.8 * screen_width, 0.27 * screen_height + 0.07 * screen_height * i]
            diff_opt_button = core_button.Button(diff_opt_pos[0], diff_opt_pos[1], diff_opt_image, 1)
            diff_opt_button.draw(self.__surface)
            if diff_opt_button.collidepoint(self.__surface):
                gen_sudo = core_gen_sudo.GenSudo(10 * (i+1))
                self.__clear_flag = True
        return gen_sudo

    def clear_all_users_num(self):
        if self.__clear_flag:
            # 遍历所有格子，若用户数字与字典中数字相等（即确定为用户数字），则清除该格子字典值
            for row in range(9):
                for col in range(9):
                    string = "{row}, {col}".format(row=self.__cell_row_col[row][col][0],
                                                   col=self.__cell_row_col[row][col][1])
                    if self.__users_num[row][col] == self.__cell_num_dict[string]:
                        self.__cell_num_dict[string] = None
            self.__clear_flag = False

    @property
    def clear_flag(self):
        return self.__clear_flag

    @clear_flag.setter
    def clear_flag(self, val):
        self.__clear_flag = val
