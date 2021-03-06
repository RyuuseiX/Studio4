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
top_y = 350
right_x = win_x
bottom_y = win_y

box_height = 37
box_width = 700
tag_height = 35
tag_width = 80
space = 5
image_space = 5
button_size = (tag_height, tag_height)


image_title = Object.Image(140, 0, '108')
image_manual = Object.Image(x=left_x, y=top_y + 250, name='manual')
image_manual.resize(button_size)
image_positive = Object.Image(x=left_x, y=top_y + 50, name='positive')
image_positive.resize(button_size)
image_negative = Object.Image(x=left_x + button_size[0] + image_space, y=top_y + 50, name='negative')
image_negative.resize(button_size)
image_list = [image_title, image_manual, image_positive, image_negative]


search_box = Object.InputBox(x=left_x, y=top_y, w=box_width, h=box_height, mode='S',
                             input_font=font_path, font_size=font_size, resizable=False)
ask_box = Object.InputBox(x=left_x, y=top_y+200, w=box_width, h=box_height, mode='A',
                          input_font=font_path, font_size=font_size, resizable=False)

manual_box = Object.InputBox(x=image_manual.x, y=image_manual.y, w=tag_width, h=tag_height, mode='M',
                             input_font=font_path, font_size=font_size, resizable=True)
positive_box = Object.InputBox(x=image_positive.x, y=image_positive.y, w=tag_width, h=tag_height, mode='P',
                               input_font=font_path, font_size=font_size, resizable=True)
negative_box = Object.InputBox(x=image_negative.x, y=image_negative.y, w=tag_width, h=tag_height, mode='N',
                               input_font=font_path, font_size=font_size, resizable=True)
input_box = [search_box, ask_box]
tag_box = [manual_box, negative_box, positive_box]
for box in tag_box:
    box.rect.w = 0

clear_search = Object.Clear_Button(x=left_x + box_width, y=top_y, w=100, h=box_height, input_box=search_box, text='Clear')
clear_ask = Object.Clear_Button(x=left_x + box_width, y=top_y+200, w=100, h=box_height, input_box=ask_box, text='Clear')
clear_list = [clear_search, clear_ask]

search_txt = Object.Text(screen, 'Find Question', input_font=font_path, font_size=font_size)
ask_txt = Object.Text(screen, 'New Question', input_font=font_path, font_size=font_size)

disable_search = []
new_disable_search = []

disable_ask = []
new_disable_ask = []

run = True
while run:

    right_x = win_x
    bottom_y = win_y

    screen.fill(white)

    search_txt.write_tl(left_x, top_y - 32)
    ask_txt.write_tl(left_x, top_y + 200 - 32)

    disable_search = new_disable_search
    new_disable_search = []

    disable_ask = new_disable_ask
    new_disable_ask = []

    # input_box
    for box in input_box:
        box.update()
        box.draw(screen)

        if box.mode == 'A':
            auto_tag_list = box.ask_q.auto_tag
            box.ask_q.disable_tag = disable_ask
            tag_y = top_y + 250
            ask_button_list = []

            for i in range(len(auto_tag_list)):
                if i > 0:
                    ask_button = Object.Tag_Button(
                        x=ask_button_list[i - 1].x + ask_button_list[i - 1].w + space, y=tag_y, w=15 * (len(auto_tag_list[i])),
                        h=tag_height, font=font_path, text=auto_tag_list[i])
                elif i == 0:
                    ask_button = Object.Tag_Button(
                        x=left_x, y=tag_y, w=15 * (len(auto_tag_list[i])),
                        h=tag_height, font=font_path, text=auto_tag_list[i])

                if ask_button.text in disable_ask:
                    ask_button.status = False
                    ask_button.color = light_gray

                ask_button_list.append(ask_button)
                ask_button.draw(screen)

                if i == len(auto_tag_list) - 1:
                    image_manual.x = ask_button_list[i].x + ask_button_list[i].w + space

            manual_tag_list = box.ask_q.manual_tag
            for i in range(len(auto_tag_list), len(auto_tag_list) + len(manual_tag_list)):
                if i > 0:
                    ask_button = Object.Tag_Button(
                        x=ask_button_list[i - 1].x + ask_button_list[i - 1].w + space, y=tag_y, w=15 * (len(manual_tag_list[i-len(auto_tag_list)])),
                        h=tag_height, font=font_path, text=manual_tag_list[i-len(auto_tag_list)])
                elif i == 0:
                    ask_button = Object.Tag_Button(
                        x=left_x, y=tag_y, w=15 * (len(manual_tag_list[i])),
                        h=tag_height, font=font_path, text=manual_tag_list[i])

                if ask_button.text in disable_ask:
                    ask_button.status = False
                    ask_button.color = light_gray

                ask_button_list.append(ask_button)
                ask_button.draw(screen)

                if i == len(manual_tag_list) + len(auto_tag_list) - 1:
                    image_manual.x = ask_button_list[i].x + ask_button_list[i].w + space

            if len(auto_tag_list) + len(manual_tag_list) == 0:
                image_manual.x = left_x

            elif len(auto_tag_list) + len(manual_tag_list) > 0:
                right_x = max(right_x, ask_button_list[-1].x + ask_button_list[-1].w + tag_height + (2*space))

        elif box.mode == 'S':
            auto_tag_list = box.search_q.auto_tag
            box.search_q.disable_tag = disable_search
            tag_y = top_y + 50
            search_button_list = []

            for i in range(len(auto_tag_list)):
                if i > 0:
                    search_button = Object.Tag_Button(
                        x=search_button_list[i - 1].x + search_button_list[i - 1].w + space, y=tag_y, w=15 * (len(auto_tag_list[i])),
                        h=35, font=font_path, text=auto_tag_list[i])
                elif i == 0:
                    search_button = Object.Tag_Button(
                        x=left_x, y=tag_y, w=15 * (len(auto_tag_list[i])),
                        h=35, font=font_path, text=auto_tag_list[i])

                if search_button.text in disable_search:
                    search_button.status = False
                    search_button.color = light_gray

                search_button_list.append(search_button)
                search_button.draw(screen)

                if i == len(auto_tag_list) - 1:
                    image_positive.x = search_button_list[i].x + search_button_list[i].w + space

            pos_tag_list = box.search_q.pos_tag
            for i in range(len(auto_tag_list), len(auto_tag_list) + len(pos_tag_list)):
                if i > 0:
                    search_button = Object.Tag_Button(
                        x=search_button_list[i - 1].x + search_button_list[i - 1].w + space, y=tag_y, w=15 * (len(pos_tag_list[i - len(auto_tag_list)])),
                        h=35, font=font_path, text=pos_tag_list[i - len(auto_tag_list)])
                elif i == 0:
                    search_button = Object.Tag_Button(
                        x=left_x, y=tag_y, w=15 * (len(pos_tag_list[i])),
                        h=35, font=font_path, text=pos_tag_list[i])

                if search_button.text in disable_search:
                    search_button.status = False
                    search_button.color = light_gray

                search_button_list.append(search_button)
                search_button.draw(screen)

                if i == len(auto_tag_list) + len(pos_tag_list) - 1:
                    image_positive.x = search_button_list[i].x + search_button_list[i].w + space

            neg_tag_list = box.search_q.neg_tag
            for i in range(len(auto_tag_list) + len(pos_tag_list), len(auto_tag_list) + len(pos_tag_list) + len(neg_tag_list)):
                if i > 0:
                    search_button = Object.Tag_Button(
                        x=search_button_list[i - 1].x + search_button_list[i - 1].w + space, y=tag_y, w=15 * (len(neg_tag_list[i - len(auto_tag_list) - len(pos_tag_list)])),
                        h=35, font=font_path, color=(255, 111, 136), text=neg_tag_list[i - len(auto_tag_list) - len(pos_tag_list)])
                elif i == 0:
                    search_button = Object.Tag_Button(
                        x=left_x, y=tag_y, w=15 * (len(neg_tag_list[i])),
                        h=35, font=font_path, color=(255, 111, 136), text=neg_tag_list[i])

                if search_button.text in disable_search:
                    search_button.status = False
                    search_button.color = light_gray

                search_button_list.append(search_button)
                search_button.draw(screen)

                if i == len(auto_tag_list) + len(pos_tag_list) + len(neg_tag_list) - 1:
                    image_positive.x = search_button_list[i].x + search_button_list[i].w + space


            if len(auto_tag_list) + len(pos_tag_list) + len(neg_tag_list) == 0:
                image_positive.x = left_x


            elif len(auto_tag_list) + len(pos_tag_list) + len(neg_tag_list) > 0:
                right_x = max(right_x, search_button_list[-1].x + search_button_list[-1].w + (2 * tag_height) + (2 * space) + image_space)


    for clear in clear_list:
        clear.draw(screen)

    for event in pg.event.get():
        for box in input_box:
            box.handle_event(event)
            box.update()
            box.draw(screen)

        for ask_button in ask_button_list:
            ask_button.handle_event(event)

        for search_button in search_button_list:
            search_button.handle_event(event)

        for clear in clear_list:
            clear.handle_event(event)

        for img in image_list:
            img.handle_event(event)
            if 'fill' in img.name:
                if 'manual' in img.name:
                    manual_box.active = True
                    manual_box.rect.x = img.x
                    manual_box.rect.w = manual_box.w
                    img.check_w = manual_box.rect.w

                elif 'positive' in img.name:
                    positive_box.active = True
                    positive_box.rect.w = positive_box.w
                    positive_box.rect.x = img.x
                    img.check_w = positive_box.rect.w

                elif 'negative' in img.name:
                    negative_box.active = True
                    negative_box.rect.w = negative_box.w
                    negative_box.rect.x = img.x
                    img.check_w = negative_box.rect.w

            elif 'fill' not in img.name:
                if 'manual' in img.name:
                    manual_box.active = False
                    img.check_w = tag_height
                    if manual_box.text != '':
                        ask_box.ask_q.add_manual_tag(manual_box.text)
                        manual_box.clear()

                elif 'positive' in img.name:
                    positive_box.active = False
                    positive_box.rect.w = 0
                    img.check_w = tag_height
                    image_negative.x = image_positive.x + tag_height + image_space
                    if positive_box.text != '':
                        search_box.search_q.add_pos_tag(positive_box.text)
                        positive_box.clear()

                elif 'negative' in img.name:
                    negative_box.active = False
                    img.check_w = tag_height
                    if negative_box.text != '':
                        search_box.search_q.add_neg_tag(negative_box.text)
                        negative_box.clear()

        for box in tag_box:
            box.handle_event(event)

        if event.type == pg.QUIT:
            run = False

    for ask_button in ask_button_list:
        if ask_button.status is False:
            new_disable_ask.append(ask_button.text)

    for search_button in search_button_list:
        if search_button.status is False:
            new_disable_search.append(search_button.text)

    if positive_box.active is True:
        positive_box.update()
        image_negative.x = image_positive.x + positive_box.rect.w + image_space

    for i in image_list:
        i.draw(screen)

    for box in tag_box:
        box.update()
        box.draw(screen)

    pg.time.delay(1)
    pg.display.update()
