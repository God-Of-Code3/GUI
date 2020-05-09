import pygame
from pygame.locals import *
from Classes.Window import Window
from Classes.Block import Block
from Classes.Text import Text
standart_behaviour = {"pushedon": {"hover": "active", "default": "active", "focus": "default", "active": "active"},
                            "pushedoff": {"hover": "hover", "default": "default", "focus": "default", "active": "default"},
                            "unpushedon": {"hover": "hover", "default": "default", "focus": "focus", "active": "focus"},
                            "unpushedoff": {"hover": "hover", "default": "default", "focus": "default", "active": "default"}}
BUTTON_HOVER = 0
BUTTON_PUSHED_ON = 1
BUTTON_UNPUSHED_ON = 2


class Button(Block):
    def __init__(self, parent, id, code='', x=0, y=0, width=100, height=100, background_color="#909090", color=(0, 0, 0), text="fgh",
                 behaviour=standart_behaviour.copy()):
        super().__init__(parent, id, code, x, y, width, height, background_color, color, text)
        self.text = text
        self.color = color
        self.font_size = 16
        self.font_name = 'Tahoma'
        self.font = pygame.font.SysFont(self.font_name, self.font_size)
        self.lines = []
        self.text_align = "center"
        self.text_height = 0
        self.behaviour = behaviour.copy()
        self.positing()

    def positing(self):
        super().positing()
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

    def get_status(self):
        return self.state

    def wrap_lines(self):
        self.lines = []
        self.text_height = 0
        for line in self.text.split(" "):
            if len(self.lines) > 0:
                width = self.font.render(self.lines[-1] + line, -1, self.color).get_width()
                if width > self.width - self.margin[0] - self.margin[2]:

                    self.lines.append(line)
                else:
                    self.lines[-1] += " " + line
            else:
                self.lines.append(line)

    def handler(self, events):
        padding_x = self.parent.padding[0] if "position_x" not in self.style[self.state] else (-self.parent.padding[2] if self.style[self.state]["position_x"] == "right" else self.parent.padding[0])
        padding_y = self.parent.padding[1] if "position_y" not in self.style[self.state] else (-self.parent.padding[3] if self.style[self.state]["position_y"] == "bottom" else self.parent.padding[1])
        rect = Rect((self.x + self.parent.real_x + padding_x, self.y + self.parent.real_y + padding_y), (self.width, self.height))
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if rect.collidepoint(pygame.mouse.get_pos()):
                    self.state = self.state if self.behaviour["pushedon"][self.state] == "" else self.behaviour["pushedon"][self.state]
                    self.positing()
                    return BUTTON_PUSHED_ON
                else:
                    self.state = self.state if self.behaviour["pushedoff"][self.state] == "" else self.behaviour["pushedoff"][self.state]
                    self.positing()

            if event.type == pygame.MOUSEBUTTONUP:
                if rect.collidepoint(pygame.mouse.get_pos()):
                    self.state = self.state if self.behaviour["unpushedon"][self.state] == "" else self.behaviour["unpushedon"][self.state]
                    self.positing()
                    return BUTTON_UNPUSHED_ON
                else:
                    self.state = self.state if self.behaviour["unpushedoff"][self.state] == "" else self.behaviour["unpushedoff"][self.state]
                    self.positing()

            if rect.collidepoint(pygame.mouse.get_pos()):
                self.state = "hover" if self.state == "default" else self.state
                self.positing()

            else:
                self.state = "default" if self.state == "hover" else self.state
                self.positing()

    def draw(self, surface):
        padding_x = self.parent.padding[0] if "position_x" not in self.style[self.state] else (-self.parent.padding[2] if self.style[self.state]["position_x"] == "right" else self.parent.padding[0])
        padding_y = self.parent.padding[1] if "position_y" not in self.style[self.state] else (-self.parent.padding[3] if self.style[self.state]["position_y"] == "bottom" else self.parent.padding[1])
        self.real_x, self.real_y = self.x + self.parent.real_x + padding_x, self.y + self.parent.real_y + padding_y
        rect = Rect((self.x + self.parent.real_x + padding_x, self.y + self.parent.real_y + padding_y), (self.width, self.height))
        dot1 = (self.x - self.border[0], self.y - self.border[1])
        dot2 = (self.x + self.width + self.border[2], self.y + self.height + self.border[3])
        width = dot2[0] - dot1[0]
        height = dot2[1] - dot1[1]
        border_rect = Rect((dot1[0] + self.parent.real_x + padding_x, dot1[1] + self.parent.real_y + padding_y), (width, height))
        pygame.draw.rect(surface, self.border_color, border_rect, 0)
        pygame.draw.rect(surface, self.background_color, rect, 0)
        i = 0
        for line in self.lines:
            text = self.font.render(line, 1, self.color)
            height = text.get_height() * len(self.lines) + (len(self.lines) - 1) * (self.padding[1] + self.padding[3])
            if self.text_align != "center":
                padding_x = self.padding[0] if "text-align" not in self.style[self.state] else (-self.padding[2] if self.style[self.state]["text-align"] == "right" else self.padding[0])
            else:
                padding_x = 0
            padding_y = self.padding[1] if "position_y" not in self.style[self.state] else (-self.padding[3] if self.style[self.state]["position_y"] == "bottom" else self.padding[1])
            align = 0
            if self.text_align == "right":
                align = self.width - text.get_width() + padding_x
            elif self.text_align == "center":
                align = self.width / 2 - text.get_width() / 2 + padding_x
            surface.blit(text, (self.x + self.parent.real_x + padding_x + align, self.y + self.parent.real_y + self.height / 2 - height / 2 + (text.get_height() + self.padding[1] + self.padding[3]) * i))
            i += 1
