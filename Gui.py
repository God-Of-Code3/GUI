import pygame
from pygame.locals import *
from Classes.Block import Block
from Classes.Window import Window
from Classes.Text import Text
from Classes.Button import *
from Classes.TextInput import TextInput
import math
pygame.init()
COLORS = {
	"red": (255, 0, 0),
	"green": (0, 255, 0),
	"blue": (0, 0, 255),
	"orange": (255, 69, 0),
	"yellow": (255, 255, 0),
	"lightblue": (66, 170, 255),
	"violet": (128, 0, 255),
	"white": (255, 255, 255),
	"black": (0, 0, 0)
}
