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
    def __init__(self, x=0, y=0, w=0, h=0, font=None, color=(230, 230, 230)):
        self.x = x  # Position X
        self.y = y  # Position Y
        self.w = w  # Width
        self.h = h  # Height
        self.font = font
        self.color = color  # light gray

    def draw(self, surface, text='', font_size=27, letter_color=(255, 255, 255), letter_back=None):
        pg.draw.rect(surface, self.color, (self.x, self.y, self.w, self.h))
        if text != '':
            text_on_button = Text(surface, text, font_size, self.font, letter_color, letter_back)
            text_on_button.write_c(self.x + self.w / 2, self.y + self.h / 2)


class Auto_Tag_Button(Rec):
    def __init__(self, x, y, w, h, font=None, color=(0, 200, 0)):
        self.color = color
        self.font = font
        self.status = True
        Rec.__init__(self, x, y, w, h, font, self.color)

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
                    self.color = (230, 230, 230)
                    self.status = False
                elif not self.status:
                    self.color = (0, 200, 0)
                    self.status = True


class Clear_Button(Rec):
    def __init__(self, x, y, w, h, input_box, font=None, color=(0, 200, 200)):
        self.color = color
        self.font = font
        self.input_box = input_box
        Rec.__init__(self, x, y, w, h, font, self.color)

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
                self.input_box.text = ''







class InputBox:
    def __init__(self, x, y, w, h, mode, text='', input_font=None, font_size=32):
        self.rect = pg.Rect(x, y, w, h)
        self.color = pg.Color('lightskyblue3')  # inactive color
        self.text = text
        self.font = pg.font.Font(input_font, font_size)
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False
        self.mode = mode
        if self.mode == 'A':
            self.ask_q = Ask_Question.Ask_Question()
        elif self.mode == 'S':
            self.search_q = Search_Question.Search_Question()

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:  # ทำการเช็คว่ามีการคลิก Mouse หรือไม่
            if self.rect.collidepoint(event.pos):  # ทำการเช็คว่าตำแหน่งของ Mouse อยู่บน InputBox นี้หรือไม่
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False

            self.color = pg.Color('dodgerblue2') if self.active else pg.Color('lightskyblue3')  # เปลี่ยนสีของ InputBox

        if event.type == pg.KEYDOWN:
            if self.active:
                tone_list = ['่', '้', '๊', '๋', '์']
                vowel_high_list = ['ิ', 'ี', 'ึ', 'ื', '็', 'ํ', 'ำ']
                vowel_low_list = ['ุ', 'ู', 'ฺ']

                if event.key == pg.K_RETURN:
                    self.active = not self.active
                    self.color = pg.Color('dodgerblue2') if self.active else pg.Color('lightskyblue3')
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif (len(self.text) > 1) and (self.text[len(self.text)-1] in tone_list) and (str(event.unicode) in tone_list):
                    pass
                elif (len(self.text) > 1) and (self.text[len(self.text)-1] in vowel_high_list) and (str(event.unicode) in vowel_high_list):
                    pass
                elif (len(self.text) > 1) and (self.text[len(self.text)-1] in vowel_low_list) and (str(event.unicode) in vowel_low_list):
                    pass
                else:
                    self.text += str(event.unicode)

                # Re-render the text.
                self.txt_surface = self.font.render(self.text, True, pg.Color('dodgerblue2'))

            if self.mode == 'A':
                self.ask_q.add_text(self.text)
                Auto_Tag.auto_tag(self.ask_q)

            elif self.mode == 'S':
                self.search_q.add_text(self.text)
                Auto_Tag.auto_tag(self.search_q)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+4))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)
