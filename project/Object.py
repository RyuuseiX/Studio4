import pygame as pg
import Ask_Question
import Search_Question
import Auto_Tag

pg.init()


class Text:
    def __init__(self, surface, input_text, font_size=32, input_font=None, letter_color=(0, 0, 0), letter_back=None):
        self.surface = surface
        self.input_font = input_font
        self.font = pg.font.Font(self.input_font, font_size)
        self.input_text = input_text
        self.font_size = font_size
        self.letter_color = letter_color
        self.letter_back = letter_back
        self.text = self.font.render(self.input_text, True, self.letter_color, self.letter_back)

    def write_c(self, x, y):  # center
        text_rect = self.text.get_rect()  # text size
        text_rect.center = (x, y)
        self.surface.blit(self.text, text_rect)

    def write_tl(self, x, y):  # topleft
        text_rect = self.text.get_rect()  # text size
        text_rect.topleft = (x, y)
        self.surface.blit(self.text, text_rect)


class Rec(Text):
    def __init__(self, x=0, y=0, w=0, h=0, font=None, color=(230, 230, 230), text=''):
        self.x = x  # Position X
        self.y = y  # Position Y
        self.w = w  # Width
        self.h = h  # Height
        self.font = font
        self.color = color  # light gray
        self.text = text

    def draw(self, surface, font_size=27, letter_color=(255, 255, 255), letter_back=None):
        pg.draw.rect(surface, self.color, (self.x, self.y, self.w, self.h))
        if self.text != '':
            text_on_button = Text(surface, self.text, font_size, self.font, letter_color, letter_back)
            text_on_button.write_c(self.x + self.w / 2, self.y + self.h / 2)


class Auto_Tag_Button(Rec):
    def __init__(self, x, y, w, h, font=None, color=(112, 173, 71), text=''):
        self.font = font
        self.status = True
        Rec.__init__(self, x, y, w, h, font, color, text)

    def mouse_on(self):
        (pos_x, pos_y) = pg.mouse.get_pos()
        if self.x <= pos_x <= self.x + self.w and self.y <= pos_y <= self.y + self.h:
            is_mouse_on = True
        else:
            is_mouse_on = False
        return is_mouse_on

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.mouse_on():
                if self.status:
                    self.status = False
                elif not self.status:
                    self.status = True


class Clear_Button(Rec):
    def __init__(self, x, y, w, h, input_box, font=None, color=(0, 200, 200), text=''):
        self.font = font
        self.input_box = input_box
        Rec.__init__(self, x, y, w, h, font, color, text)

    def mouse_on(self):
        (pos_x, pos_y) = pg.mouse.get_pos()
        if self.x <= pos_x <= self.x + self.w and self.y <= pos_y <= self.y + self.h:
            is_mouse_on = True
        else:
            is_mouse_on = False
        return is_mouse_on

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.mouse_on():
                self.input_box.clear()
                if self.input_box.mode == 'A':
                    self.input_box.ask_q.add_text(self.input_box.text)
                    Auto_Tag.auto_tag(self.input_box.ask_q)

                elif self.input_box.mode == 'S':
                    self.input_box.search_q.add_text(self.input_box.text)
                    Auto_Tag.auto_tag(self.input_box.search_q)


class InputBox:
    def __init__(self, x, y, w, h, mode, text='', input_font=None, font_size=32, resizable=False):
        self.rect = pg.Rect(x, y, w, h)
        self.w = self.rect.w
        self.text = text
        self.mode = mode
        self.resizable = resizable
        self.mpn_list = ['M', 'P', 'N']
        self.as_list = ['A', 'S']

        if self.mode in self.as_list:
            self.active = False
            self.active_color = pg.Color('dodgerblue2')
            self.inactive_color = pg.Color('lightskyblue3')
            self.color = self.inactive_color  # inactive color
            if self.mode == 'A':
                self.ask_q = Ask_Question.Ask_Question()
            elif self.mode == 'S':
                self.search_q = Search_Question.Search_Question()
        elif self.mode in self.mpn_list:
            self.active = True
            self.active_color = (112, 173, 71)
            if self.mode == 'N':
                self.active_color = (255, 111, 136)
            self.inactive_color = pg.Color('lightskyblue3')
            self.color = self.active_color

        self.font = pg.font.Font(input_font, font_size)
        self.txt_surface = self.font.render(text, True, self.color)

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:  # ทำการเช็คว่ามีการคลิก Mouse หรือไม่
            if self.mode in self.as_list:
                if self.rect.collidepoint(event.pos):  # ทำการเช็คว่าตำแหน่งของ Mouse อยู่บน InputBox นี้หรือไม่
                    # Toggle the active variable.
                    if self.mode in self.as_list:
                        self.active = not self.active
                else:
                    self.active = False

                self.color = self.active_color if self.active else self.inactive_color  # เปลี่ยนสีของ InputBox

        if event.type == pg.KEYDOWN:
            tone_list = ['่', '้', '๊', '๋', '์']
            vowel_high_list = ['ิ', 'ี', 'ึ', 'ื', '็', 'ํ', 'ำ']
            vowel_low_list = ['ุ', 'ู', 'ฺ']

            if self.active is True:
                if event.key == pg.K_RETURN:
                    self.active = False
                    self.color = self.inactive_color
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif (len(self.text) > 1) and (self.text[len(self.text) - 1] in tone_list) and (str(event.unicode) in tone_list):
                    pass
                elif (len(self.text) > 1) and (self.text[len(self.text) - 1] in vowel_high_list) and (str(event.unicode) in vowel_high_list):
                    pass
                elif (len(self.text) > 1) and (self.text[len(self.text) - 1] in vowel_low_list) and (str(event.unicode) in vowel_low_list):
                    pass
                else:
                    self.text += str(event.unicode)

                self.txt_surface = self.font.render(self.text, True, self.active_color)

                if self.mode in self.as_list:
                    if self.mode == 'A':
                        self.ask_q.add_text(self.text)
                        Auto_Tag.auto_tag(self.ask_q)

                    elif self.mode == 'S':
                        self.search_q.add_text(self.text)
                        Auto_Tag.auto_tag(self.search_q)

    def update(self):
        # Resize the box if the text is too long.
        if self.resizable:
            width = max(self.w, self.txt_surface.get_width() + 50)
            self.rect.w = width

    def clear(self):
        self.text = ''
        self.txt_surface = self.font.render(self.text, True, self.active_color)

    def draw(self, screen):
        # Blit the text.
        if self.mode in self.as_list:
            screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
            pg.draw.rect(screen, self.color, self.rect, 2)
        elif self.mode in self.mpn_list:
            if self.active:
                screen.blit(self.txt_surface, (self.rect.x + 40, self.rect.y + 5))
                pg.draw.rect(screen, self.color, self.rect, 2)



class Image:
    def __init__(self, x=0, y=0, name='', status=True):
        self.name = name
        self.img = self.load()
        self.x = x  # Position X
        self.y = y  # Position Y
        self.w = self.img.get_width()
        self.check_w = self.w
        self.h = self.img.get_height()
        self.status = status

        # self.img = pg.image.load('/Users/Peace/Desktop/Studio4-main/project/image/'+name+'.png')

    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))

    def resize(self, new_size):
        self.img = pg.transform.scale(self.img, new_size)
        self.w = self.img.get_width()
        self.h = self.img.get_height()

    def load(self):
        img = pg.image.load('./image/' + self.name + '.png')
        return img

    def mouse_on(self):
        (pos_x, pos_y) = pg.mouse.get_pos()
        if self.x <= pos_x <= self.x + self.check_w and self.y <= pos_y <= self.y + self.h:
            is_mouse_on = True
        else:
            is_mouse_on = False
        return is_mouse_on

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.mouse_on():
                if 'fill' not in self.name:
                    self.name += ' fill'
                    self.img = self.load()
                    self.resize((self.w, self.h))

            elif not self.mouse_on():
                if 'fill' in self.name:
                    self.name = self.name.replace(' fill', '')
                    self.img = self.load()
                    self.resize((self.w, self.h))

