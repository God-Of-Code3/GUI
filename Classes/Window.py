import pygame
from pygame.locals import *


class Window:
    def __init__(self, width, height, background, title="window", icon="GUI_Logo128x128.png"):
        self.x = 0
        self.y = 0
        self.real_x = 0
        self.real_y = 0
        self.width = width
        self.height = height
        self.padding = [0, 0, 0, 0]
        self.align = "row"
        self.title = title
        self.background = pygame.Color(background)
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height), RESIZABLE)
        pygame.mouse.set_cursor((16, 19), (0, 0), (
            128, 0, 192, 0, 160, 0, 144, 0, 136, 0, 132, 0, 130, 0, 129, 0, 128, 128, 128, 64, 128, 32, 128, 16, 129,
            240, 137, 0, 148, 128, 164, 128, 194, 64, 2, 64, 1, 128), (
                                    128, 0, 192, 0, 224, 0, 240, 0, 248, 0, 252, 0, 254, 0, 255, 0, 255, 128, 255, 192,
                                    255, 224, 255, 240, 255, 240, 255, 0, 247, 128, 231, 128, 195, 192, 3, 192, 1, 128))
        self.icon = pygame.image.load(icon)
        self.children = []
        self.elements = []
        pygame.display.set_caption(self.title)
        pygame.display.set_icon(self.icon)

    def draw_elements(self):
        for element in self.elements:
            element.draw(self.screen)

    def handler(self, events):
        self_events = []
        for element in self.elements:
            self_events.append([element.id, element.handler(events)])
        return self_events.copy()

    def reinit(self, size):
        self.width = size[0]
        self.height = size[1]
        self.screen = pygame.display.set_mode(size, RESIZABLE)
        pygame.mouse.set_cursor((16, 19), (0, 0), (
            128, 0, 192, 0, 160, 0, 144, 0, 136, 0, 132, 0, 130, 0, 129, 0, 128, 128, 128, 64, 128, 32, 128, 16, 129,
            240, 137, 0, 148, 128, 164, 128, 194, 64, 2, 64, 1, 128), (
                                    128, 0, 192, 0, 224, 0, 240, 0, 248, 0, 252, 0, 254, 0, 255, 0, 255, 128, 255, 192,
                                    255, 224, 255, 240, 255, 240, 255, 0, 247, 128, 231, 128, 195, 192, 3, 192, 1, 128))
        pygame.display.set_caption(self.title)
        pygame.display.set_icon(self.icon)
        for element in self.elements:
            element.positing()

    def fill(self):
        self.screen.fill(self.background)

    def render(self):
        pygame.display.update()

    def __str__(self):
        return "GUI Window"
