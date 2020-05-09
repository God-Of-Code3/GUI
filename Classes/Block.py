import pygame
from pygame.locals import *
from Classes.Window import Window


operators = {"+": lambda a, b: a + b, "-": lambda a, b: a - b, "*": lambda a, b: a * b, "/": lambda a, b: a / b}


class Block:
    def __init__(self, parent, id, code='', x=0, y=0, width=100, height=100, background_color="#909090", color=(0, 0, 0), text=""):
        self.parent = parent
        self.window = parent.window if not isinstance(parent, Window) else parent
        self.window.elements.append(self)
        self.code = code
        # Style
        # ---------------
        self.x = x
        self.y = y
        self.real_x = self.x + self.parent.x
        self.real_y = self.y + self.parent.y
        self.width = width
        self.height = height
        self.id = id
        if background_color[0] != "#":
            self.background_color = background_color
        else:
            self.background_color = pygame.Color(background_color)
        self.border = [0, 0, 0, 0]
        self.border_color = pygame.Color("#000000")
        self.margin = [0, 0, 0, 0]
        self.padding = [0, 0, 0, 0]
        self.align = "row"
        # ---------------
        self.children = []
        self.style = self.decode_style(code)
        self.state = "default"
        parent.children.append(self)
        self.positing()

    def decode_style(self, code):
        style = dict()
        code = code.replace("\n", "")
        for block in code.split("}"):
            if block == "":
                continue
            style[block.split("{")[0]] = dict()
            for line in block.split("{")[1].split(";"):
                if line != "":
                    style[block.split("{")[0]][line.split(":")[0]] = line.split(":")[1]

        if "hover" not in style:
            style["hover"] = style["default"].copy()

        for param in style["default"]:
            if param not in style["hover"]:
                style["hover"][param] = style["default"][param]

        if "focus" not in style:
            style["focus"] = style["default"].copy()

        for param in style["default"]:
            if param not in style["focus"]:
                style["focus"][param] = style["default"][param]

        if "active" not in style:
            style["active"] = style["default"].copy()

        for param in style["default"]:
            if param not in style["active"]:
                style["active"][param] = style["default"][param]

        return style

    def to_standart_format(self, unit, parent_param):
        if unit[len(unit) - 2:len(unit)] == "px":
            return float(unit.replace("px", ""))
        if unit[-1] == "%":
            return (parent_param / 100) * float(unit.replace("%", ""))
        if unit.startswith("calc("):
            unit = unit.replace("calc(", "").replace(")", "")
            unit0, operator, unit1 = unit.split(" ")
            if unit0[len(unit0) - 2:len(unit0)] == "px":
                unit0 = float(unit0.replace("px", ""))
            elif unit0[-1] == "%":
                unit0 = (parent_param / 100) * float(unit0.replace("%", ""))

            if unit1[len(unit1) - 2:len(unit1)] == "px":
                unit1 = float(unit1.replace("px", ""))
            elif unit1[-1] == "%":
                unit1 = (parent_param / 100) * float(unit1.replace("%", ""))
            return operators[operator](unit0, unit1)

    def handler(self, events):
        pass

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

    def positing(self):
        if "margin" in self.style[self.state]:
            margin = self.style[self.state]["margin"]
            if " " in margin:
                i = 0
                for side in margin.split(" "):
                    if i in [0, 2]:
                        parent_param = self.width - (self.parent.padding[0] + self.parent.padding[2])
                    else:
                        parent_param = self.height - (self.parent.padding[1] + self.parent.padding[3])
                    self.margin[i] = self.to_standart_format(side, parent_param)
                    i += 1
            else:
                parent_param = self.width - (self.parent.padding[0] + self.parent.padding[2])
                self.margin = [self.to_standart_format(margin, parent_param) for _ in range(4)]

        if "width" in self.style[self.state]:
            width = self.style[self.state]["width"]
            parent_param = self.parent.width - self.parent.padding[0] - self.parent.padding[2]
            self.width = self.to_standart_format(width, parent_param)

        if "height" in self.style[self.state]:
            height = self.style[self.state]["height"]
            parent_param = self.parent.height - self.parent.padding[1] - self.parent.padding[3]
            self.height = self.to_standart_format(height, parent_param)

        if "border" in self.style[self.state]:
            border = self.style[self.state]["border"]
            if " " in border:
                i = 0
                for side in border.split(" "):
                    self.border[i] = self.to_standart_format(side, 0)
                    i += 1
            else:
                self.border = [self.to_standart_format(border, 0) for _ in range(4)]

        if "padding" in self.style[self.state]:
            padding = self.style[self.state]["padding"]
            if " " in padding:
                i = 0
                for side in padding.split(" "):
                    if i in [0, 2]:
                        parent_param = self.width
                    else:
                        parent_param = self.height
                    self.padding[i] = self.to_standart_format(side, parent_param)
                    i += 1
            else:
                parent_param = self.width
                self.padding = [self.to_standart_format(padding, parent_param) for _ in range(4)]

        if "left" in self.style[self.state]:
            left = self.style[self.state]["left"]
            parent_param = self.parent.width - self.parent.padding[0] - self.parent.padding[2]
            self.x = self.to_standart_format(left, parent_param) + self.margin[0]
        else:
            if self.parent.align == "row":
                x = self.margin[0]
                for i in range(self.parent.children.index(self)):
                    el = self.parent.children[i]
                    x += el.margin[0] + el.margin[2] + el.width + el.x
                self.x = x
            else:
                self.x = self.margin[0]
        if "position_x" in self.style[self.state]:
            if self.style[self.state]["position_x"] == "right":
                if "right" in self.style[self.state]:
                    right = self.style[self.state]["right"]
                    parent_param = self.parent.width - self.parent.padding[0] - self.parent.padding[2]
                    self.x = self.parent.width - (self.to_standart_format(right, parent_param)) - self.margin[2] - self.width
                else:
                    if self.parent.align == "row":
                        x = self.parent.width - self.width - self.margin[2]
                        for i in range(self.parent.children.index(self)):
                            el = self.parent.children[i]
                            x = el.x - el.margin[0] - self.width - self.margin[2]
                        self.x = x
                    else:
                        self.x = self.parent.width - self.width - self.margin[2]

        if "top" in self.style[self.state]:
            top = self.style[self.state]["top"]
            parent_param = self.parent.height - self.parent.padding[1] - self.parent.padding[3]
            self.y = self.to_standart_format(top, parent_param) + self.margin[1]
        else:
            if self.parent.align == "col":
                y = self.margin[1]
                for i in range(self.parent.children.index(self)):
                    el = self.parent.children[i]
                    y += el.margin[1] + el.margin[3] + el.height + el.y
                self.y = y
            else:
                self.y = self.margin[1]

        if "position_y" in self.style[self.state]:
            if self.style[self.state]["position_y"] == "bottom":
                if "bottom" in self.style[self.state]:
                    bottom = self.style[self.state]["bottom"]
                    parent_param = self.parent.height - self.parent.padding[1] - self.parent.padding[3]
                    self.y = self.parent.height - (self.to_standart_format(bottom, parent_param)) - self.margin[3] - self.height
                else:
                    if self.parent.align == "col":
                        y = self.parent.height - self.height - self.margin[3]
                        for i in range(self.parent.children.index(self)):
                            el = self.parent.children[i]
                            y = el.y - el.margin[1] - self.height - self.margin[3]
                        self.y = y
                    else:
                        self.y = self.parent.height - self.height - self.margin[3]

        if "background-color" in self.style[self.state]:
            background_color = self.style[self.state]["background-color"]
            if background_color[0] != "#":
                self.background_color = background_color
            else:
                self.background_color = pygame.Color(background_color)

        if "border-color" in self.style[self.state]:
            border_color = self.style[self.state]["border-color"]
            if border_color[0] != "#":
                self.border_color = border_color
            else:
                self.border_color = pygame.Color(border_color)

        if "align" in self.style[self.state]:
            self.align = self.style[self.state]["align"]
