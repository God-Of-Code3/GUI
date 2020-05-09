import pygame
from pygame.locals import *
from Classes.Window import Window
from Classes.Block import Block


class Text(Block):
    def __init__(self, parent, id, code='', x=0, y=0, width=100, height=100, background_color="#909090", color=(0, 0, 0), text="fgh"):
        self.text = text
        self.color = color
        self.font_size = 16
        self.font_name = 'Tahoma'
        self.text_align = "left"
        self.font = pygame.font.SysFont(self.font_name, self.font_size)
        super().__init__(parent, id, code, x, y, width, height, background_color, color, text)
        self.lines = []
        self.bold = False
        self.positing()

    def positing(self):
        super().positing()

        self.font_size = 16
        self.font_name = 'Tahoma'
        self.text_align = "left"
        if "text" in self.style[self.state]:
            self.text = self.style[self.state]["text"]
        if "color" in self.style[self.state]:
            color = self.style[self.state]["color"]
            if color[0] != "#":
                self.color = color
            else:
                self.color = pygame.Color(color)
        if "font-size" in self.style[self.state]:
            self.font_size = int(self.style[self.state]["font-size"])
        if "font-name" in self.style[self.state]:
            self.font_name = self.style[self.state]["font-name"]
        if "text-align" in self.style[self.state]:
            self.text_align = self.style[self.state]["text-align"]
        if self.font_name.startswith("l'"):
            self.font = pygame.font.Font("Fonts/" + self.font_name[2:len(self.font_name)], self.font_size)
        else:
            self.font = pygame.font.SysFont(self.font_name, self.font_size)
        self.wrap_lines()

    def wrap_lines(self):
        self.lines = []
        for line in self.text.split(" "):
            if len(self.lines) > 0:
                width = self.font.render(self.lines[-1] + line, -1, self.color).get_width()
                if width > self.width - self.margin[0] - self.margin[2]:
                    self.lines.append(line)
                else:
                    print("1", line)
                    self.lines[-1] += " " + line
            else:
                self.lines.append(line)

    def draw(self, surface):

        i = 0
        for line in self.lines:
            text = self.font.render(line, 1, self.color)
            padding_x = self.parent.padding[0] if "text-align" not in self.style[self.state] else (-self.parent.padding[2] if self.style[self.state]["text-align"] == "right" else self.parent.padding[0])
            padding_y = self.parent.padding[1] if "position_y" not in self.style[self.state] else (-self.parent.padding[3] if self.style[self.state]["position_y"] == "bottom" else self.parent.padding[1])
            align = 0
            if self.text_align == "right":
                align = self.width - text.get_width()
            elif self.text_align == "center":
                align = self.width / 2 - text.get_width() / 2
            surface.blit(text, (self.x + self.parent.real_x + padding_x + align, self.y + self.parent.real_y + padding_y + (text.get_height() + self.padding[1] + self.padding[3]) * i))
            i += 1


