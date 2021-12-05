import pygame as pg
import Object
import Database
import platform
import time

pg.init()

# system
os = platform.platform()[0].upper()
win_x, win_y = 1280, 720
screen = pg.display.set_mode((win_x, win_y))

# font
if os == 'W':
    font_path = './font/FC Minimal Regular.ttf'
    font_bold_path = './font/FC Minimal Bold.otf'
elif os == 'M':
    font_path = '/Users/Peace/Desktop/Studio4-main/project/font/FCMinimalRegular.otf'
    font_bold_path = '/Users/Peace/Desktop/Studio4-main/project/font/FC Minimal Bold.otf'
font_size = 30

# color
black = (0, 0, 0)
white = (255, 255, 255)
gray = (200, 200, 200)
light_gray = (230, 230, 230)
green = (0, 200, 0)
red = (200, 0, 0)

# position
left_x = 200
top_y = 350
right_x = win_x
bottom_y = win_y
ask_y = top_y + 250
ask_y_start = ask_y
search_y = top_y + 50

# dimension
box_height = 37
box_width = 750
tag_height = 35
tag_width = 80
space = 5
image_space = 5
button_size = (tag_height, tag_height)

# image
image_title = Object.Image(x=left_x-10-50, y=0, name='108')

image_icon_search = Object.Image(x=left_x-75, y=top_y-20, name='search')
image_icon_ask = Object.Image(x=left_x-75, y=top_y+203, name='ask')

image_manual = Object.Image(x=left_x, y=top_y + 250, name='manual')
image_positive = Object.Image(x=left_x, y=top_y + 50, name='positive')
image_negative = Object.Image(x=left_x + button_size[0] + image_space, y=top_y + 50, name='negative')
image_list = [image_title, image_icon_search, image_icon_ask, image_manual, image_negative, image_positive]

# question box
search_box = Object.InputBox(x=left_x, y=top_y, w=box_width, h=box_height, mode='S',
                             input_font=font_path, font_size=font_size, resizable=False)
ask_box = Object.InputBox(x=left_x, y=top_y+200, w=box_width, h=box_height, mode='A',
                          input_font=font_path, font_size=font_size, resizable=False)

# tag box
manual_box = Object.InputBox(x=image_manual.x, y=image_manual.y, w=tag_width, h=tag_height, mode='M',
                             input_font=font_path, font_size=font_size, resizable=True)
positive_box = Object.InputBox(x=image_positive.x, y=image_positive.y, w=tag_width, h=tag_height, mode='P',
                               input_font=font_path, font_size=font_size, resizable=True)
negative_box = Object.InputBox(x=image_negative.x, y=image_negative.y, w=tag_width, h=tag_height, mode='N',
                               input_font=font_path, font_size=font_size, resizable=True)
input_box = [search_box, ask_box]
tag_box = [manual_box, positive_box, negative_box]
for box in tag_box:
    box.rect.w = 0

# clear button
clear_search = Object.Clear_Button(x=left_x + box_width, y=top_y, w=100, h=box_height, input_box=search_box, text='Clear')
clear_ask = Object.Clear_Button(x=left_x + box_width, y=top_y+200, w=100, h=box_height, input_box=ask_box, text='Clear')
clear_list = [clear_search, clear_ask]

# database
excel_database = Database.Excel_Database() 
submit_button = Object.Submit_Button(x=left_x + box_width + 100, y=top_y + 200, w=100, h=box_height, input_box=ask_box, db=excel_database, text='Submit')

# text
search_txt = Object.Text(screen, 'ค้นหา', input_font=font_bold_path, font_size=font_size+10)
ask_txt = Object.Text(screen, 'เขียน', input_font=font_bold_path, font_size=font_size+10)
in_search_txt = Object.Text(screen, 'พิมพ์ปัญหาที่ต้องการค้นหา', input_font=font_path, font_size=font_size-1, letter_color=pg.Color('lightskyblue3'))
in_ask_txt = Object.Text(screen, 'พิมพ์ปัญหาที่ต้องการเพิ่ม', input_font=font_path, font_size=font_size-1, letter_color=pg.Color('lightskyblue3'))

# disable tag
disable_search = []
new_disable_search = []
disable_ask = []
new_disable_ask = []

# scroll bar
vertical_scrollbar = Object.Vertical_ScrollBar(win_y)
horizontal_scrollbar = Object.Horizontal_ScrollBar(win_x)
expand_horizontal = False
expand_vertical = False

middle_y = 550 + vertical_scrollbar.y_axis

run = True
while run:

    left_x = 200 + horizontal_scrollbar.x_axis
    top_y = 350 + vertical_scrollbar.y_axis

    search_y = top_y + 50

    screen.fill(white)

    search_txt.write_tl(left_x, top_y - 40)

    disable_search = new_disable_search
    new_disable_search = []

    disable_ask = new_disable_ask
    new_disable_ask = []

    image_title.x = left_x - 10 - 50
    image_title.y = top_y - 350
    image_icon_search.x = left_x - 75
    image_icon_search.y = top_y - 20
    image_icon_ask.x = left_x - 75
    image_icon_ask.y = middle_y - 18
    image_positive.y = top_y + 50
    image_negative.y = top_y + 50

    # middle_y = 550 + vertical_scrollbar.y_axis
    ask_txt.write_tl(left_x, middle_y - 40)
    submit_button.x = left_x + box_width + 100
    submit_button.y = middle_y 
    ask_y = middle_y + 50       #max(ask_y_start, result_y + tag_height + space) + top_y - 350
    image_manual.y = middle_y + 50

    # input_box
    for box in input_box:
        box.rect.x = left_x
        search_box.rect.y = top_y
        ask_box.rect.y    = middle_y
        
        box.update()
        box.draw(screen)

        # ask box
        if box.mode == 'A':
            box.ask_q.disable_tag = disable_ask
            ask_button_list = []

            # auto tag
            auto_tag_list = box.ask_q.auto_tag
            for i in range(len(auto_tag_list)):
                if i > 0:
                    ask_button = Object.Tag_Button(
                        x=ask_button_list[i - 1].x + ask_button_list[i - 1].w + space, y=ask_y, w=15 * (len(auto_tag_list[i])),
                        h=tag_height, font=font_path, text=auto_tag_list[i])
                elif i == 0:
                    ask_button = Object.Tag_Button(
                        x=left_x, y=ask_y, w=15 * (len(auto_tag_list[i])),
                        h=tag_height, font=font_path, text=auto_tag_list[i])

                if ask_button.text in disable_ask:
                    ask_button.status = False
                    ask_button.color = light_gray

                ask_button_list.append(ask_button)
                ask_button.draw(screen)

                if i == len(auto_tag_list) - 1:
                    image_manual.x = ask_button_list[i].x + ask_button_list[i].w + space

            # manual tag
            manual_tag_list = box.ask_q.manual_tag
            for tag in manual_tag_list:
                if tag in disable_ask:
                    manual_tag_list.remove(tag)
            for i in range(len(auto_tag_list), len(auto_tag_list) + len(manual_tag_list)):
                if i > 0:
                    ask_button = Object.Tag_Button(
                        x=ask_button_list[i - 1].x + ask_button_list[i - 1].w + space, y=ask_y, w=15 * (len(manual_tag_list[i-len(auto_tag_list)])),
                        h=tag_height, font=font_path, text=manual_tag_list[i-len(auto_tag_list)])
                elif i == 0:
                    ask_button = Object.Tag_Button(
                        x=left_x, y=ask_y, w=15 * (len(manual_tag_list[i])),
                        h=tag_height, font=font_path, text=manual_tag_list[i])

                ask_button_list.append(ask_button)
                ask_button.draw(screen)

                if i == len(manual_tag_list) + len(auto_tag_list) - 1:
                    image_manual.x = ask_button_list[i].x + ask_button_list[i].w + space

            if len(auto_tag_list) + len(manual_tag_list) == 0:
                image_manual.x = left_x

            ask_button_wide = 200 + 200
            for a in ask_button_list:
                ask_button_wide += a.w
                ask_button_wide += space


        # search box
        elif box.mode == 'S':
            box.search_q.disable_tag = disable_search
            search_button_list = []

            # auto tag
            auto_tag_list = box.search_q.auto_tag
            for i in range(len(auto_tag_list)):
                if i > 0:
                    search_button = Object.Tag_Button(
                        x=search_button_list[i - 1].x + search_button_list[i - 1].w + space, y=search_y, w=15 * (len(auto_tag_list[i])),
                        h=tag_height, font=font_path, text=auto_tag_list[i])
                elif i == 0:
                    search_button = Object.Tag_Button(
                        x=left_x, y=search_y, w=15 * (len(auto_tag_list[i])),
                        h=tag_height, font=font_path, text=auto_tag_list[i])

                if search_button.text in disable_search:
                    search_button.status = False
                    search_button.color = light_gray

                search_button_list.append(search_button)
                search_button.draw(screen)

                if i == len(auto_tag_list) - 1:
                    image_positive.x = search_button_list[i].x + search_button_list[i].w + space

            # positive tag
            pos_tag_list = box.search_q.pos_tag
            for tag in pos_tag_list:
                if tag in disable_search:
                    pos_tag_list.remove(tag)
            for i in range(len(auto_tag_list), len(auto_tag_list) + len(pos_tag_list)):
                if i > 0:
                    search_button = Object.Tag_Button(
                        x=search_button_list[i - 1].x + search_button_list[i - 1].w + space, y=search_y, w=15 * (len(pos_tag_list[i - len(auto_tag_list)])),
                        h=tag_height, font=font_path, text=pos_tag_list[i - len(auto_tag_list)])
                elif i == 0:
                    search_button = Object.Tag_Button(
                        x=left_x, y=search_y, w=15 * (len(pos_tag_list[i])),
                        h=tag_height, font=font_path, text=pos_tag_list[i])

                search_button_list.append(search_button)
                search_button.draw(screen)

                if i == len(auto_tag_list) + len(pos_tag_list) - 1:
                    image_positive.x = search_button_list[i].x + search_button_list[i].w + space

            # negative tag
            neg_tag_list = box.search_q.neg_tag
            for tag in neg_tag_list:
                if tag in disable_search:
                    neg_tag_list.remove(tag)
            for i in range(len(auto_tag_list) + len(pos_tag_list), len(auto_tag_list) + len(pos_tag_list) + len(neg_tag_list)):
                if i > 0:
                    search_button = Object.Tag_Button(
                        x=search_button_list[i - 1].x + search_button_list[i - 1].w + space, y=search_y, w=15 * (len(neg_tag_list[i - len(auto_tag_list) - len(pos_tag_list)])),
                        h=tag_height, font=font_path, color=(255, 111, 136), text=neg_tag_list[i - len(auto_tag_list) - len(pos_tag_list)])
                elif i == 0:
                    search_button = Object.Tag_Button(
                        x=left_x, y=search_y, w=15 * (len(neg_tag_list[i])),
                        h=tag_height, font=font_path, color=(255, 111, 136), text=neg_tag_list[i])

                search_button_list.append(search_button)
                search_button.draw(screen)

                if i == len(auto_tag_list) + len(pos_tag_list) + len(neg_tag_list) - 1:
                    image_positive.x = search_button_list[i].x + search_button_list[i].w + space

            if len(auto_tag_list) + len(pos_tag_list) + len(neg_tag_list) == 0:
                image_positive.x = left_x

            search_button_wide = 250 + 200
            for s in search_button_list:
                search_button_wide += s.w
                search_button_wide += space
            
    # expand vertical
    if expand_vertical:
        if time.time() - vertical_scrollbar.scrollTimeStamp >= 0.05 and vertical_scrollbar.scroll == 1:
            vertical_scrollbar.scroll = 0
            vertical_scrollbar.change_y = 0
    
    for clear in clear_list:
        clear.x = left_x + box_width
        clear_search.y = top_y
        clear_ask.y = middle_y
        clear.draw(screen)

    submit_button.draw(screen)

    for img in image_list:
        if 'fill' in img.name:
            if 'manual' in img.name:
                manual_box.active = True
                manual_box.rect.x = img.x
                manual_box.rect.y = img.y
                manual_box.rect.w = manual_box.w
                img.check_w = manual_box.rect.w
            elif 'positive' in img.name:
                positive_box.active = True
                positive_box.rect.w = positive_box.w
                positive_box.rect.x = img.x
                positive_box.rect.y = img.y
                img.check_w = positive_box.rect.w
            elif 'negative' in img.name:
                negative_box.active = True
                negative_box.rect.w = negative_box.w
                negative_box.rect.x = img.x
                negative_box.rect.y = img.y
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


    result_question, result_tag, pos_key = search_box.database_search(submit_button.database)
    result_y = top_y + 50 + space + tag_height
    for i in range(len(result_question)):
        result_list = []
        result_text = Object.Text(surface=screen, input_text=result_question[i], font_size=27, input_font=font_path)
        result_text.write_tl(left_x, result_y + 2)
        # tag_list = []
        if result_question[i] == 'No Results Match':
            break
        for j in range(0, len(result_tag[i])):
            tag = result_tag[i][j]
            if j == 0:
                if tag in pos_key:
                    result = Object.Rec(x=left_x + result_text.text.get_rect().w + space, y=result_y,
                                        h=tag_height, font=font_path, color=(112, 173, 71), text=tag, adjust=True)

                elif tag not in pos_key:
                    result = Object.Rec(x=left_x + result_text.text.get_rect().w + space, y=result_y,
                                        h=tag_height, font=font_path, color=light_gray, text=tag, adjust=True)

            elif j > 0:
                if tag in pos_key:
                    result = Object.Rec(x=result_list[j - 1].x + result_list[j - 1].w + space, y=result_y,
                                        h=tag_height, font=font_path, color=(112, 173, 71), text=tag, adjust=True)
                elif tag not in pos_key:
                    result = Object.Rec(x=result_list[j - 1].x + result_list[j - 1].w + space, y=result_y,
                                        h=tag_height, font=font_path, color=light_gray, text=tag, adjust=True)

            result_list.append(result)
            result.draw(screen)

        result_y += tag_height + space

    # print(result_question)
    middle_y = 575 + vertical_scrollbar.y_axis + max(0, len(result_question)-2) * 40

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

        submit_button.handle_event(event)

        for img in image_list:
            img.handle_event(event)

        if expand_vertical:
            vertical_scrollbar.handle_event(event)
        if expand_horizontal:
            horizontal_scrollbar.handle_event(event)

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

        if box.active is False:
            if box.mode == 'M':
                if box.text != '':
                    ask_box.ask_q.add_manual_tag(box.text)
                    box.clear()
                    image_manual.unfill()
            elif box.mode == 'P':
                if box.text != '':
                    search_box.search_q.add_pos_tag(box.text)
                    box.clear()
                    image_positive.unfill()
            elif box.mode == 'N':
                if box.text != '':
                    search_box.search_q.add_neg_tag(box.text)
                    box.clear()
                    image_negative.unfill()


    right_x = max( win_x, max(search_button_wide, ask_button_wide)  )
    bottom_y = max( win_y, 600 + max(0, len(result_question)-2)*40 + 80 + 30)
    # right_x = win_x + 543
    # bottom_y = win_y + 543

    vertical_scrollbar.update()
    horizontal_scrollbar.update()

    if bottom_y > win_y:
        expand_vertical = True
        vertical_scrollbar.window_height = bottom_y
    else:
        vertical_scrollbar.y_axis = 0
        expand_vertical = False

    if right_x > win_x:
        expand_horizontal = True
        horizontal_scrollbar.window_width = right_x
    else:
        horizontal_scrollbar.x_axis = 0
        expand_horizontal = False

    if expand_vertical:
        vertical_scrollbar.draw(screen)

    if expand_horizontal:
        horizontal_scrollbar.draw(screen)

    if search_box.active is False and search_box.text == '':
        in_search_txt.write_tl(left_x + 10, top_y + 5)
    if ask_box.active is False and ask_box.text == '':
        in_ask_txt.write_tl(left_x + 10, ask_y - 45)

    pg.time.delay(1)
    pg.display.update()
