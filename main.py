# -*- coding: utf-8 -*-
# @File    : main.py
# @Author  : Zichi Zhang
# @Date    : 2023/2/12
# @Software: PyCharm

import pygame
import sudo


if __name__ == '__main__':
    screen = sudo.core.screen()

    while not screen.done:
        # screen.surface.fill((255, 255, 255))
        # 设置游戏的fps
        screen.clock.tick(30)
        press_num = screen.number_button(screen.screen_size)
        cell_button = screen.cell_button
        screen.highlight_cell()
        if press_num:
            screen.press_to_add_num_to_cell(press_num, screen.current_cell_pos)
        screen.show_num_in_cell()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                screen.done = True  # 若检测到关闭窗口，则将done置为True
        # 刷新显示屏幕
        pygame.display.update()
    # 点击关闭，退出pygame程序
    pygame.quit()
