import pygame
from Gui import *


window = Window(800, 600, "#ffffff", title="GUI-TEST", icon="NNC.ico")
block = Block(window, "block", "default{"
                   "margin:0px;"
                   "padding:20px;"
                   "width:50%;"
                   "height:500px;"
                   "left:20px;"
                   "top:20px;"
                   "}"
                   "hover{"
                   "background-color:#ff0000;"
                   "}")
block2 = Block(block, "block2", "default{"
                    "margin:0px;"
                    "position_x:right;"
                    "padding:0px;"
                    "width:40%;"
                    "height:60px;"
                    "border:4px;"
                    "background-color:#ffffff;"
                    "border-color:#4de3e8;"
                    "}"
                    "hover{"
                    "background-color:#ff0000;"
                    "}")
block3 = Block(block, "block3", "default{"
                    "margin:0px;"
                    "padding:0px 5px 0px 0px;"
                      "position_y:bottom;"
                      "position_x:right;"
                    "right:calc(50% - 15%);"
                    "bottom:-20px;"
                    "width:30%;"
                    "height:60px;"
                    "background-color:#ffffff;"
                    "}"
                    "hover{"
                    "background-color:#ff0000;"
                    "}")
block4 = TextInput(block, "textInput", "default{"
                    "margin:0px;"
                    "padding:0px;"
                    "position_y:bottom;"
                    "position_x:right;"
                    "right:calc(50% - 45%);"
                    "bottom:60px;"
                    "border:1px;"
                    "border-color:#bbbaba;"
                    "width:90%;"
                    "text:TEST_TEXT_1_2_3_4_5_6_7_8_9_10_11_12_13_14_15;"
                    "color:#000000;"
                    "font-size:14;"
                    "height:24px;"
                    "background-color:#ffffff;"
                    "}"
                    "focus{"
                    "background-color:#ffffff;"
                    "border-color:#1276ae;"
                    "border:1px;"
                    "}"
                    "active{"
                    "border-color:#1276ae;"
                    "border:1px;"
                    "}"
                    )
text1 = Button(block3, "button1", "default{"
                    "margin:0px;"
                    "position_y:top;"
                    "position_x:right;"
                    "right:calc(50% - 50px);"
                    "width:100px;"
                    "height:50px;"
                    "background-color:#e7e6e5;"
                    "border-color:#bbbaba;"
                    "border:1px;"
                    "text:ЭТО КНОПКА ЛОЛ;"
                    "text-align:center;"
                    "font-size:14;"
                    "font-name:l'SegoeUI-Light.ttf;"
                    "color:#3f3f3f;"
                    "}"
                    "hover{"
                    "background-color:#e6eff8;"
                    "border-color:#1276ae;"
                    "border:1px;"
                    "}"
                    "active{"
                    "background-color:#d2e5f3;"
                    "border-color:#1276ae;"
                    "border:1px;"
                    "}"
                    "focus{"
                    "background-color:#e6eff8;"
                    "border-color:#1276ae;"
                    "border:2px;"
                    "}"
               )

while True:
    window.fill()
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.VIDEORESIZE:
            window.reinit(event.size)
    window.draw_elements()
    evs = window.handler(events)
    for ev in evs:
        if ev[1] is not None:
            print(ev)
    window.render()
