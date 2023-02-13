# -*- coding: utf-8 -*-
# @File    : screen.py
# @Author  : Zichi Zhang
# @Date    : 2023/2/12
# @Software: PyCharm

import numpy as np
import pygame
import sudo.core.button as sudo_button


class screen:
    """
    initialization screen
    """

    def __init__(self):
        # 初始化
        pygame.init()
        # 设置主屏幕大小
        SCREEN_WIDTH = 1000
        SCREEN_HEIGHT = 1000
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
        self.__basicFont = pygame.font.SysFont("方正粗黑宋简体", 48)
        self.__cell_num_dict = {}  # store which number in a cell, key: cell pos, value: num
        self.__points = self.__build_points(self.__screen_size)
        self.__draw_square(self.__surface, self.__points)
        self.__cell_pos, self.__cell_button = self.__create_cell_button(self.__screen_size)
        self.__current_cell_pos = None

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
        points = [[(0, 0) for j in range(p_num_in_row)] for i in range(p_num_in_col)]
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
        for row in range(p_num_in_col):
            for col in range(p_num_in_row):
                string = "{x}, {y}".format(x=points[row][col][0], y=points[row][col][1])
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
        cell_pos = [[(0, 0) for j in range(p_num_in_row - 1)] for i in range(p_num_in_col - 1)]
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
                # cell_image = pygame.draw.rect(screen, CELL_COL, (50, 50, 150, 50), 0)
                cell_image = pygame.Surface(np.multiply(np.add(p[1][1], np.multiply(p[0][0], -1)), 0.93))
                cell_image.fill(color='white')
                cell_button[row][col] = sudo_button.Button(cell_pos[row][col][0], cell_pos[row][col][1], cell_image, 1)
        return cell_pos, cell_button

    def highlight_cell(self):
        """
        When a cell is pressed, highlight other cells in the same row and column as well as other cells in the larger
        cell
        cell which is pressed: green
        other cells in the same row and column: light blue
        other cells in the larger cell: light gray
        """
        p = self.__points
        green = np.multiply([0, 0.5, 0], 255)
        baby_blue = np.multiply([0.54, 0.81, 0.94], 255)
        light_gray = np.multiply([0.75, 0.75, 0.75], 255)
        cell_image = pygame.Surface(np.multiply(np.add(p[1][1], np.multiply(p[0][0], -1)), 0.93))
        for row in range(9):
            for col in range(9):
                self.__cell_button[row][col].draw(self.__surface)
                if self.__cell_button[row][col].collidepoint(self.__surface):
                    for row_ in range(9):
                        for col_ in range(9):
                            # other cells in the same row and column: light blue
                            if row_ == row or col_ == col:
                                cell_image.fill(color=baby_blue)
                                self.__cell_button[row_][col_] = sudo_button.Button(self.__cell_pos[row_][col_][0],
                                                                                    self.__cell_pos[row_][col_][1],
                                                                                    cell_image,
                                                                                    1)
                            # other cells in the larger cell: light gray
                            elif int(row_ / 3) == int(row / 3) and int(col_ / 3) == int(col / 3):
                                cell_image.fill(color=light_gray)
                                self.__cell_button[row_][col_] = sudo_button.Button(self.__cell_pos[row_][col_][0],
                                                                                    self.__cell_pos[row_][col_][1],
                                                                                    cell_image,
                                                                                    1)
                            # other cells: white
                            else:
                                cell_image.fill(color="white")
                                self.__cell_button[row_][col_] = sudo_button.Button(self.__cell_pos[row_][col_][0],
                                                                                    self.__cell_pos[row_][col_][1],
                                                                                    cell_image,
                                                                                    1)
                    # cell which is pressed: green
                    cell_image.fill(color=green)
                    self.__cell_button[row][col] = sudo_button.Button(self.__cell_pos[row][col][0],
                                                                      self.__cell_pos[row][col][1], cell_image, 1)
                    self.__current_cell_pos = self.__cell_pos[row][col]

    def number_button(self, screen_size):
        """
        build the number button for filling the cell
        """
        screen_width = screen_size[0]
        screen_height = screen_size[1]
        # define the number's color
        NUM_COL = np.multiply([0, 0.5, 1], 255)
        num_image = []
        num_button = []
        for i in range(10):
            num_image.append(self.__basicFont.render(str(i), True, NUM_COL))
            pos = [0.2 * screen_width + 0.05 * screen_width * i, 0.85 * screen_height]
            num_button.append(sudo_button.Button(pos[0], pos[1], num_image[i], 1))
            num_button[i].draw(self.__surface)
            if num_button[i].collidepoint(self.__surface):
                return i  # return the number which is pressed
        return None

    def press_to_add_num_to_cell(self, num, current_cell_pos):
        if current_cell_pos:
            string = "{x}, {y}".format(x=current_cell_pos[0], y=current_cell_pos[1])
            self.__cell_num_dict[string] = num

    def show_num_in_cell(self):
        num_font = self.__basicFont
        blue = np.multiply([0, 0.5, 1], 255)
        for (cell_pos, num) in self.__cell_num_dict.items():
            if num:
                cell_pos = tuple(map(float, cell_pos.split(', ')))
                num_surface = num_font.render(str(num), True, blue)
                rect = num_surface.get_rect(center=cell_pos)
                self.__surface.blit(num_surface, rect.topleft)
