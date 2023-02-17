# -*- coding: utf-8 -*-
# @File    : main.py
# @Author  : Zichi Zhang
# @Date    : 2023/2/12
# @Software: PyCharm

import pygame
import sudo
import copy

if __name__ == '__main__':
    screen = sudo.core.Screen()
    gen_sudo = sudo.core.GenSudo(20)
    component = sudo.core.Component(screen)
    event = sudo.core.Event(screen)
    num_in_screen = copy.deepcopy(gen_sudo.puzzle)
    last_num_row_col = None
    points_pos = component.points_pos
    all_cell_pos = component.all_cell_pos
    all_cell_button = component.all_cell_button
    all_num_pos = component.all_num_pos
    all_num_button = component.all_num_button
    all_difficulty_option_button = component.all_difficulty_option_button
    event.create_cell_num_dict(gen_sudo.puzzle)
    screen.create_num_mat(gen_sudo.puzzle)
    while not screen.done:
        # 设置游戏的fps
        screen.clock.tick(30)

        screen.cell_num_dict = event.cell_num_dict
        screen.update_num_mat(event.all_users_num, event.all_num_is_valid)
        # draw components in the screen
        # -----------------------------------------
        screen.draw_square(points_pos)
        screen.draw_cell_button(all_cell_button)
        screen.draw_num_button(all_num_button)
        all_remain_num = component.cal_number_of_remaining_num(screen.cell_num_dict)
        screen.show_remaining_num(all_num_pos, all_remain_num)
        screen.draw_difficulty_option_button(all_difficulty_option_button)

        # events
        # -----------------------------------------
        current_cell_row_col = event.cell_is_pressed(all_cell_button)
        if current_cell_row_col:
            # highlight cells and numbers when cell is pressed
            all_cell_button = screen.highlight_cell(points_pos, all_cell_pos, all_cell_button, current_cell_row_col)
            # highlight the number when cell is pressed
            screen.highlight_number(all_cell_pos, current_cell_row_col)

        # add number to the cell when cell has been chosen and number button is pressed
        press_num = event.num_is_pressed(all_num_button)
        if press_num:
            num_in_screen = event.add_num_to_cell(press_num, screen.current_cell_row_col, num_in_screen,
                                                  gen_sudo.puzzle)

        # re-generate sudo puzzle and clear all user's number when difficulty option button is pressed
        blank_num = event.diff_option_is_pressed(all_difficulty_option_button)
        if blank_num:
            gen_sudo = event.regen_sudo(blank_num)

        # if clear_flag has been set, clear all the user's number in the screen and reset relate lists
        if event.clear_flag:
            screen.create_num_mat(gen_sudo.puzzle)
            screen.clear_all_users_num(event.all_users_num)
            event.all_users_num = [[None for _ in range(9)] for _ in range(9)]
            num_in_screen = copy.deepcopy(gen_sudo.puzzle)
            event.create_cell_num_dict(gen_sudo.puzzle)
            event.clear_flag = False

        # show all the necessary numbers in the screen
        screen.show_num_in_screen(all_cell_pos)

        for pygame_event in pygame.event.get():
            if pygame_event.type == pygame.QUIT:
                screen.done = True  # 若检测到关闭窗口，则将done置为True
        # 刷新显示屏幕
        pygame.display.update()
    # 点击关闭，退出pygame程序
    pygame.quit()
