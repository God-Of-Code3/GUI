import pygame
import pyperclip as pclp
from pygame.locals import *
from Classes.Window import Window
from Classes.Block import Block
from Classes.Button import *
standart_behaviour = {"pushedon": {"hover": "active", "default": "active", "focus": "active", "active": "active"},
                            "pushedoff": {"hover": "hover", "default": "default", "focus": "default", "active": "default"},
                            "unpushedon": {"hover": "hover", "default": "default", "focus": "focus", "active": "focus"},
                            "unpushedoff": {"hover": "hover", "default": "default", "focus": "default", "active": "default"}}
cursor_time = 210
letter_time1 = 250
letter_time2 = 10


class TextInput(Block):
    def __init__(self, parent, id, code='', x=0, y=0, width=100, height=100, background_color="#909090", color=(0, 0, 0), text="fgh",
                 behaviour=standart_behaviour.copy()):
        self.text = text
        self.color = color
        self.font_size = 16
        self.font_name = "l'SegoeUI.ttf"
        self.font = pygame.font.SysFont(self.font_name, self.font_size)
        self.lines = []
        self.text_align = "center"
        self.text_height = 0
        self.shift_x = 0
        self.cursor_symbol = 0
        self.selected_text = [0, 0]
        self.behaviour = behaviour.copy()
        self.state = "default"
        self.cursor_timer = cursor_time
        self.cursor = True
        self.start = True
        self.letters = {}
        super().__init__(parent, id, code, x, y, width, height, background_color, color, text)
        self.positing()

    def draw(self, surface):
        super().draw(surface)
        padding_x = self.parent.padding[0] if "position_x" not in self.style[self.state] else (
            -self.parent.padding[2] if self.style[self.state]["position_x"] == "right" else self.parent.padding[0])
        padding_y = self.parent.padding[1] if "position_y" not in self.style[self.state] else (
            -self.parent.padding[3] if self.style[self.state]["position_y"] == "bottom" else self.parent.padding[1])
        text_surface = pygame.Surface((int(self.width - self.padding[0] - self.padding[2]), int(self.height - self.padding[1] - self.padding[3])))
        text_surface.fill(self.background_color)
        text = self.font.render(self.text, 1, self.color)
        text_surface.blit(text, (-self.shift_x, 0))
        if self.selected_text != [0, 0]:
            x1 = self.font.render(self.text[0: self.selected_text[0]], 1, self.color).get_width() - self.shift_x
            text = self.font.render(self.text[self.selected_text[0]: self.selected_text[1]], 1, (255, 255, 255))
            width = text.get_width()
            selected_rect = Rect((x1, 2), (width, self.height - self.padding[1] - self.padding[3] - 4))
            pygame.draw.rect(text_surface, (0, 0, 255), selected_rect)
            text_surface.blit(text, (x1, 2))
        if self.state in ["focus", "active"]:
            if self.cursor and -1 < self.cursor_symbol < len(self.text) + 1:
                text_width_to_cursor = self.font.render(self.text[0:self.cursor_symbol], 1, self.color).get_width() - self.shift_x
                height = text.get_height()
                pygame.draw.line(text_surface, self.color, (int(text_width_to_cursor), int(2)), (int(text_width_to_cursor), int(height - 2)), 1)
        surface.blit(text_surface, (self.x + self.parent.real_x + padding_x, self.y + self.parent.real_y + padding_y))

    def positing(self):
        super().positing()
        if "text" in self.style[self.state]:
            self.text = self.style[self.state]["text"] if self.start else self.text
            self.start = False
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

    def get_status(self):
        return self.state

    def valid_key(self, key):
        if key not in [pygame.K_RIGHT, pygame.K_LEFT, pygame.K_BACKSPACE, pygame.K_DELETE, pygame.K_LCTRL, pygame.K_LSHIFT, pygame.K_RCTRL, pygame.K_RSHIFT]:
            return True
        return False

    def backspace(self):
        if self.cursor_symbol > 0:
            self.text = self.text[0:self.cursor_symbol - 1] + self.text[self.cursor_symbol:len(self.text)]
            self.cursor_symbol -= 1
            text = self.font.render(self.text[0:self.cursor_symbol], 1, self.color).get_width() - self.shift_x
            if text < 0:
                if text + self.shift_x > self.width - self.padding[0] - self.padding[2]:
                    self.shift_x = text + self.shift_x - (self.width - self.padding[0] - self.padding[2])
                else:
                    self.shift_x = 0

    def left(self):
        self.cursor_symbol = max(0, self.cursor_symbol - 1)
        text = self.font.render(self.text[0:self.cursor_symbol], 1, self.color).get_width() - self.shift_x
        if text < 0:
            self.shift_x += text - 2

    def get_mouse_pos_symbol(self, pos):
        acc_pos = 0
        pixel_pos = pos[0] + self.shift_x - self.real_x
        index = 0
        for char in self.text:
            width = self.font.size(char)[0]
            if acc_pos + (width / 2) > pixel_pos:
                break
            index += 1
            acc_pos += width
        return index

    def right(self):
        self.cursor_symbol = min(len(self.text), self.cursor_symbol + 1)
        text = self.font.render(self.text[0:self.cursor_symbol], 1, self.color).get_width() - self.shift_x
        if text > self.width - self.padding[0] - self.padding[2]:
            self.shift_x += text - (self.width - self.padding[0] - self.padding[2]) + 2

    def delete(self):
        if self.cursor_symbol < len(self.text):
            self.text = self.text[0:self.cursor_symbol] + self.text[self.cursor_symbol + 1:len(self.text)]

    def reset_cursor_timer(self):
        self.cursor = True
        self.cursor_timer = -60

    def handler(self, events):
        if self.state == "default":
            self.selected_text = [0, 0]
        else:
            if self.selected_text[0] > self.selected_text[1]:
                self.selected_text.sort()
        if self.state in ["focus", "active"]:
            if len(self.letters) > 0:
                self.reset_cursor_timer()
            for letter in self.letters:
                self.letters[letter] = max(0, self.letters[letter] - 1)
                if self.letters[letter] == 0:
                    self.letters[letter] = letter_time2
                    if letter == "BACKSPACE":
                        self.backspace()
                    elif letter == "LEFT":
                        self.left()
                    elif letter == "DELETE":
                        self.delete()
                    elif letter == "RIGHT":
                        self.right()
                    else:
                        self.text = self.text[0:self.cursor_symbol] + letter + self.text[self.cursor_symbol:len(self.text)]
                        self.cursor_symbol += 1
            self.cursor_timer += 1
            if self.cursor_timer >= cursor_time:
                self.cursor_timer = 0
                self.cursor = not self.cursor
        padding_x = self.parent.padding[0] if "position_x" not in self.style[self.state] else (
            -self.parent.padding[2] if self.style[self.state]["position_x"] == "right" else self.parent.padding[0])
        padding_y = self.parent.padding[1] if "position_y" not in self.style[self.state] else (
            -self.parent.padding[3] if self.style[self.state]["position_y"] == "bottom" else self.parent.padding[1])
        rect = Rect((self.x + self.parent.real_x + padding_x + self.padding[0], self.y + self.parent.real_y + padding_y + self.padding[1]), (self.width - self.padding[0] - self.padding[2], self.height - self.padding[1] - self.padding[3]))
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.selected_text = [0, 0]
                if rect.collidepoint(pygame.mouse.get_pos()):
                    self.state = self.state if self.behaviour["pushedon"][self.state] == "" else self.behaviour["pushedon"][self.state]
                    self.positing()
                    index = self.get_mouse_pos_symbol(event.pos)
                    self.cursor_symbol = index + 1
                    if self.cursor_symbol >= len(self.text) + 1:
                        self.cursor_symbol = len(self.text)
                    self.reset_cursor_timer()
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
            if self.state in ["focus", "active"]:
                if event.type == pygame.KEYDOWN:
                    self.reset_cursor_timer()
                    if event.key == pygame.K_RIGHT:
                        self.right()
                        self.letters["RIGHT"] = letter_time1
                    elif event.key == pygame.K_LEFT:
                        self.left()
                        self.letters["LEFT"] = letter_time1
                    elif event.key == pygame.K_BACKSPACE:
                        self.backspace()
                        self.letters["BACKSPACE"] = letter_time1
                    elif event.key == pygame.K_DELETE:
                        self.delete()
                        self.letters["DELETE"] = letter_time1
                    elif event.key == pygame.K_v and event.mod & pygame.KMOD_CTRL:
                        paste_text = pclp.paste()
                        if isinstance(paste_text, str):
                            self.text = self.text[0:self.cursor_symbol] + paste_text + self.text[self.cursor_symbol:len(self.text)]
                            for _ in range(len(paste_text)):
                                self.right()
                    elif self.valid_key(event.key):
                        self.letters[event.unicode] = letter_time1
                        self.text = self.text[0:self.cursor_symbol] + event.unicode + self.text[self.cursor_symbol:len(self.text)]
                        self.cursor_symbol += 1
                if event.type == pygame.KEYUP:
                    if self.valid_key(event.key):
                        if chr(event.key) not in self.letters:
                            if chr(event.key).upper() in self.letters:
                                del self.letters[chr(event.key).upper()]
                        else:
                            del self.letters[chr(event.key)]
                    elif event.key == pygame.K_BACKSPACE:
                        del self.letters["BACKSPACE"]
                    elif event.key == pygame.K_LEFT:
                        del self.letters["LEFT"]
                    elif event.key == pygame.K_RIGHT:
                        del self.letters["RIGHT"]
                    elif event.key == pygame.K_DELETE:
                        del self.letters["DELETE"]

            if rect.collidepoint(pygame.mouse.get_pos()):
                self.state = "hover" if self.state == "default" else self.state
                self.positing()
                pos = pygame.mouse.get_pos()
                if self.state == "active":
                    if self.real_x < pos[0] < self.real_x + self.width:
                        if self.selected_text == [0, 0]:
                            self.selected_text[0] = self.cursor_symbol
                        index = self.get_mouse_pos_symbol(pos)
                        self.cursor_symbol = index + 1
                        if self.cursor_symbol >= len(self.text) + 1:
                            self.cursor_symbol = len(self.text)
                        self.selected_text[1] = self.cursor_symbol
            else:
                self.state = "default" if self.state == "hover" else self.state
                self.positing()

