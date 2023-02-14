# -*- coding: utf-8 -*-
# @File    : component.py
# @Author  : Zichi Zhang
# @Date    : 2023/2/14
# @Software: PyCharm

import pygame
import numpy as np
import sudo.core.button as core_button


class Component:
    def __init__(self, screen):
        self.__surface = screen.surface
        self.__screen_size = screen.screen_size
        self.__points_pos = self.__build_points()
        self.__all_cell_pos, self.__all_cell_button = self.__create_cell_button()
        self.__all_num_pos, self.__all_num_button = self.__create_number_button()
        self.__all_difficulty_option_button = self.__create_difficulty_option_button()
        self.__clear_flag = False

    @property
    def points_pos(self):
        return self.__points_pos

    @property
    def all_cell_pos(self):
        return self.__all_cell_pos

    @property
    def all_cell_button(self):
        return self.__all_cell_button

    @property
    def all_num_pos(self):
        return self.__all_num_pos

    @property
    def all_num_button(self):
        return self.__all_num_button

    @property
    def all_difficulty_option_button(self):
        return self.__all_difficulty_option_button

    @property
    def clear_flag(self):
        return self.__clear_flag

    def __build_points(self):
        screen_size = self.__screen_size
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
        return points

    def __create_cell_button(self):
        screen_size = self.__screen_size
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

        p = self.__points_pos
        p_num_in_row = len(p)
        p_num_in_col = len(p[0])
        all_cell_pos = [[(0, 0) for _ in range(p_num_in_row - 1)] for _ in range(p_num_in_col - 1)]
        all_cell_pos[0][0] = np.add(p[0][0], np.multiply(np.add(p[1][1], np.multiply(p[0][0], -1)), 0.5))
        for row in range(p_num_in_col - 1):
            if row < p_num_in_row - 2:
                zipped = zip(all_cell_pos[row][0], (p_d_length, 0))
                mapped = map(sum, zipped)
                all_cell_pos[row + 1][0] = tuple(mapped)
            for col in range(p_num_in_row - 2):
                zipped = zip(all_cell_pos[row][col], (0, p_d_width))
                mapped = map(sum, zipped)
                all_cell_pos[row][col + 1] = tuple(mapped)
        all_cell_button = [[None for j in range(p_num_in_row - 1)] for i in range(p_num_in_col - 1)]
        for row in range(p_num_in_col - 1):
            for col in range(p_num_in_row - 1):
                cell_image = pygame.Surface(np.multiply(np.add(p[1][1], np.multiply(p[0][0], -1)), 0.93))
                cell_image.fill(color='white')
                all_cell_button[row][col] = core_button.Button(all_cell_pos[row][col][0], all_cell_pos[row][col][1],
                                                               cell_image, 1)
        return all_cell_pos, all_cell_button

    def __create_number_button(self):
        """
        build the number button for filling the cell
        """
        screen_size = self.__screen_size
        num_font = pygame.font.SysFont("方正粗黑宋简体", 100)
        screen_width = screen_size[0]
        screen_height = screen_size[1]
        # define the number's color
        blue = np.multiply([0, 0.5, 1], 255)
        num_image = []
        all_num_pos = []
        all_num_button = []
        for i in range(9):
            num_image.append(num_font.render(str(i + 1), True, blue))
            pos = [0.12 * screen_width + 0.07 * screen_width * i, 0.87 * screen_height]
            all_num_pos.append(pos)
            all_num_button.append(core_button.Button(pos[0], pos[1], num_image[i], 1))
        return all_num_pos, all_num_button

    def cal_number_of_remaining_num(self, cell_num_dict):
        # calculate the number of remaining numbers(digits)
        all_remain_num = [9 for _ in range(9)]
        for num in range(9):
            for v in cell_num_dict.values():
                if v == (num+1):
                    all_remain_num[num] -= 1
                    if all_remain_num[num] < 0:
                        all_remain_num[num] = 0
        return all_remain_num

    def __create_difficulty_option_button(self):
        screen_size = self.__screen_size
        key_font = pygame.font.SysFont("SimSun", 30)
        screen_width = screen_size[0]
        screen_height = screen_size[1]
        blue = np.multiply([0, 0.5, 1], 255)
        diff_opt_name = ["入门", "简单", "中等", "困难", "地狱"]
        all_diff_opt_button = []
        for i in range(len(diff_opt_name)):
            diff_opt_image = key_font.render(diff_opt_name[i], True, blue)
            diff_opt_pos = [0.8 * screen_width, 0.27 * screen_height + 0.07 * screen_height * i]
            all_diff_opt_button.append(core_button.Button(diff_opt_pos[0], diff_opt_pos[1], diff_opt_image, 1))
        return all_diff_opt_button
