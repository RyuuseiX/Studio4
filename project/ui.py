import pygame as pg
import Object
import Ask_Question
import Search_Question
import Auto_Tag

pg.init()

win_x, win_y = 1280, 720
screen = pg.display.set_mode((win_x, win_y))

font_path = './font/FC Minimal Regular.ttf'
# font_path = '/Users/Peace/Desktop/Studio4-main/project/font/FCMinimalRegular.otf'
font_size = 30


black = (0, 0, 0)
white = (255, 255, 255)
gray = (200, 200, 200)
light_gray = (230, 230, 230)
green = (0, 200, 0)
red = (200, 0, 0)

left_x = 150
box_height = 37
box_width = 700

ask_box = Object.InputBox(x=left_x, y=100, w=box_width, h=box_height, mode='A', input_font=font_path, font_size=font_size)
search_box = Object.InputBox(x=left_x, y=300, w=box_width, h=box_height, mode='S', input_font=font_path, font_size=font_size)
input_box = [ask_box, search_box]

clear_ask = Object.Clear_Button(x=left_x+box_width, y=100, w=100, h=box_height, input_box=ask_box, text='Clear')
clear_search = Object.Clear_Button(x=left_x+box_width, y=300, w=100, h=box_height, input_box=search_box, text='Clear')
clear_list = [clear_ask, clear_search]


ask_txt = Object.Text(screen, 'Ask', input_font=font_path, font_size=font_size)
search_txt = Object.Text(screen, 'Search', input_font=font_path, font_size=font_size)


ask_q = Ask_Question.Ask_Question()
search_q = Search_Question.Search_Question()



run = True
while run:

    screen.fill(white)

    ask_txt.write_tl(left_x, 100 - 32)
    search_txt.write_tl(left_x, 300-32)

    # input_box
    for box in input_box:
        box.update()
        box.draw(screen)
        if box.mode == 'A':
            tag_list = box.ask_q.auto_tag
            tag_y = 150
        elif box.mode == 'S':
            tag_list = box.search_q.auto_tag
            tag_y = 350

        button_list = []
        for i in range(len(tag_list)):
            space = 5
            if i > 0:
                button = Object.Auto_Tag_Button(x=button_list[i - 1].x + button_list[i - 1].w + space, y=tag_y, w=15 * (len(tag_list[i])), h=35,
                                                font=font_path, text=tag_list[i])
            else:
                button = Object.Auto_Tag_Button(x=left_x, y=tag_y, w=15*(len(tag_list[i])), h=35, font=font_path, text=tag_list[i])

            button_list.append(button)

    for button in button_list:
        button.draw(screen)

    for clear in clear_list:
        clear.draw(screen)

    pg.time.delay(1)
    pg.display.update()

    for event in pg.event.get():
        for box in input_box:
            box.handle_event(event)

        for button in button_list:
            button.handle_event(event)

        for clear in clear_list:
            clear.handle_event(event)

        if event.type == pg.QUIT:
            pg.quit()
            run = False





