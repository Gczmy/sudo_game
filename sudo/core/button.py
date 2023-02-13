# -*- coding: utf-8 -*-
# @File    : button.py
# @Author  : Zichi Zhang
# @Date    : 2023/2/12
# @Software: PyCharm

import pygame


class Button:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.__image_ = image
        self.image = pygame.transform.scale(self.__image_, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.clicked = False
        self.__background = None

    @property
    def image_(self):
        return self.__image_

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 255), (self.rect.x, self.rect.y, self.image.get_width(), self.image.get_height()))
        self.__background = pygame.draw.rect(surface, (255, 255, 255), (self.rect.x, self.rect.y, self.image.get_width(), self.image.get_height()), 3)

    def collidepoint(self, surface):
        action = False
        # get the mouse's position
        pos = pygame.mouse.get_pos()

        if self.__background.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True
                action = True

            if not pygame.mouse.get_pressed()[0]:
                self.clicked = False

        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action





