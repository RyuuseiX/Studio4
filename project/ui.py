import pygame as pg
import Object
import Ask_Question
import Search_Question
import Auto_Tag

pg.init()

win_x, win_y = 1280, 720
screen = pg.display.set_mode((win_x, win_y))

font_path = './font/FC Minimal Regular.ttf'
font_size = 30

black = (0, 0, 0)
white = (255, 255, 255)
gray = (200, 200, 200)
light_gray = (230, 230, 230)
green = (0, 200, 0)
red = (200, 0, 0)

box_height = 37
ask_box = Object.InputBox(100, 100, 300, box_height, mode='A', input_font=font_path, font_size=font_size)
search_box = Object.InputBox(100, 300, 300, box_height, mode='S', input_font=font_path, font_size=font_size)
input_box = [ask_box, search_box]

# clear_ask = Object.Clear_Button()

ask_txt = Object.Text(screen, 'Ask', input_font=font_path, font_size=font_size)
search_txt = Object.Text(screen, 'Search', input_font=font_path, font_size=font_size)

ask_q = Ask_Question.Ask_Question()
search_q = Search_Question.Search_Question()

run = True

while run:
    screen.fill(white)

    ask_txt.write_tl(100, 100 - 32)
    search_txt.write_tl(100, 300-32)

    # input_box
    for box in input_box:
        box.update()
        box.draw(screen)
        if box.mode == 'A':
            tag_list = box.ask_q.auto_tag
            y = 150
        elif box.mode == 'S':
            tag_list = box.search_q.auto_tag
            y = 350
        button_l = []
        for i in range(len(tag_list)):
            space = 5
            if i > 0:
                button = Object.Auto_Tag_Button(button_l[i - 1].x + button_l[i - 1].w + space, y, 15 * (len(tag_list[i])), 35,
                                                font_path)
            else:
                button = Object.Auto_Tag_Button(100, y, 15 * (len(tag_list[i])), 35, font_path)
            button_l.append(button)

        for i in range(len(button_l)):
            button_l[i].draw(screen, text=tag_list[i])

    pg.time.delay(1)
    pg.display.update()

    for event in pg.event.get():
        for box in input_box:
            box.handle_event(event)

        for button in button_l:
            button.handle_event(event)

        if event.type == pg.QUIT:
            pg.quit()
            run = False


