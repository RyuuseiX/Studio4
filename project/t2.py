import Object
import pygame as pg

pg.init()

win_x, win_y = 1280, 720
screen = pg.display.set_mode((win_x, win_y))

black = (0, 0, 0)
white = (255, 255, 255)
gray = (200, 200, 200)
light_gray = (230, 230, 230)
green = (0, 200, 0)
red = (200, 0, 0)

run = True
tag_l = ['งู', 'ชื่อ', 'ระหว่างประเทศ', 'หน่วยงาน']
font_path = './font/FC Minimal Regular.ttf'

while run:
    screen.fill(white)
    button_l = []
    for i in range(len(tag_l)):
        if i > 0:
            button = Object.Button(button_l[i-1].x + button_l[i-1].w + 2, 200, 15*(len(tag_l[i])), 37, font_path)
        else:
            button = Object.Button(100, 200, 10 * (len(tag_l[i])), 37, font_path)
        button.color = green
        button_l.append(button)

    for i in range(len(button_l)):
        button_l[i].draw(screen, text=tag_l[i])

    pg.time.delay(1)
    pg.display.update()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            run = False
