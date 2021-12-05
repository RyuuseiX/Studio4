import pygame as pg
import Ask_Question
import Search_Question
import Auto_Tag
import time
import platform

os = platform.platform()[0].upper()
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


class RoundRec:
    def __init__(self, x=0, y=0, w=0, h=0, r=0, t=0, color=(0, 0, 0)):
        self.x = x   # Position X
        self.y = y   # Position Y
        self.w = w   # Width
        self.h = h   # Height
        self.round = r       # Roundness
        self.r = int(r*h/2)  # Radius
        self.t = t   # Thinkness
        self.color = color

    def draw(self, surface):
        pg.draw.rect  (surface, self.color, (self.x+self.r,        self.y,                self.w-2*self.r, self.h))
        pg.draw.rect  (surface, self.color, (self.x,               self.y+self.r,         self.w,          self.h-2*self.r))
        pg.draw.circle(surface, self.color, (self.x+self.r,        self.y+self.r),        self.r)
        pg.draw.circle(surface, self.color, (self.x+self.w-self.r, self.y+self.r),        self.r)
        pg.draw.circle(surface, self.color, (self.x+self.r,        self.y+self.h-self.r), self.r)
        pg.draw.circle(surface, self.color, (self.x+self.w-self.r, self.y+self.h-self.r), self.r)

        if self.t != 0:
            x2 = self.x + self.t
            y2 = self.y + self.t
            w2 = self.w - self.t*2
            h2 = self.h - self.t*2

            FillRoundRec = RoundRec(x2, y2, w2, h2, self.round, 0, (255,255,255))
            FillRoundRec.draw(surface)



class Rec(Text):
    def __init__(self, x=0, y=0, w=0, h=0, font=None, color=(230, 230, 230), text='', adjust=False):
        self.x = x  # Position X
        self.y = y  # Position Y
        self.w = w  # Width
        self.h = h  # Height
        self.font = font
        self.color = color  # light gray
        self.text = text
        self.adjust = adjust

    def draw(self, surface, font_size=27, letter_color=(255, 255, 255), letter_back=None):
        if self.text != '':
            text_on_button = Text(surface, self.text, font_size, self.font, letter_color, letter_back)
            if self.adjust is True:
                self.w = text_on_button.text.get_rect().w + 10
            NewRoundRec = RoundRec(self.x, self.y, self.w, self.h, 0.4, 0, self.color)
            NewRoundRec.draw(surface)
            # pg.draw.rect(surface, self.color, (self.x, self.y, self.w, self.h))
            text_on_button.write_c(self.x + self.w / 2, self.y + self.h / 2)
        else:
            pg.draw.rect(surface, self.color, (self.x, self.y, self.w, self.h))



class Tag_Button(Rec):
    def __init__(self, x, y, w, h, font=None, color=(112, 173, 71), text=''):
        self.font = font
        self.status = True
        Rec.__init__(self, x, y, w, h, font, color, text, adjust=True)

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
                if event.button == 1:
                    if self.status:
                        self.status = False
                    elif not self.status:
                        self.status = True


class Clear_Button(Rec):
    def __init__(self, x, y, w, h, input_box, font=None, color=(247, 28, 27), text=''):
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
                if event.button == 1:
                    self.input_box.clear()
                    if self.input_box.mode == 'A':
                        self.input_box.ask_q.add_text(self.input_box.text)
                        Auto_Tag.auto_tag(self.input_box.ask_q)
                        self.input_box.ask_q.del_manual_tag('!CLEAR_ALL!')

                    elif self.input_box.mode == 'S':
                        self.input_box.search_q.add_text(self.input_box.text)
                        Auto_Tag.auto_tag(self.input_box.search_q)
                        self.input_box.search_q.del_pos_tag('!CLEAR_ALL!')
                        self.input_box.search_q.del_neg_tag('!CLEAR_ALL!')


class Submit_Button(Rec):
    def __init__(self, x, y, w, h, input_box, db, font=None, color=(27, 116, 247), text=''):
        self.font = font
        self.input_box = input_box
        Rec.__init__(self, x, y, w, h, font, color, text)
        self.database = db

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
                if event.button == 1:
                    tagged_q = self.input_box.ask_q.save()
                    self.database.database_update(tagged_q['Question'], tagged_q['Tag'])
                    self.input_box.clear()
                    self.input_box.ask_q.add_text(self.input_box.text)
                    Auto_Tag.auto_tag(self.input_box.ask_q)
                    self.input_box.ask_q.del_manual_tag('!CLEAR_ALL!')



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
            if event.button == 1:
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
                    if self.mode in self.as_list:
                        self.color = self.inactive_color
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif (len(self.text) > 1) and (self.text[len(self.text) - 1] in tone_list) and (
                        str(event.unicode) in tone_list):
                    pass
                elif (len(self.text) > 1) and (self.text[len(self.text) - 1] in vowel_high_list) and (
                        str(event.unicode) in vowel_high_list):
                    pass
                elif (len(self.text) > 1) and (self.text[len(self.text) - 1] in vowel_low_list) and (
                        str(event.unicode) in vowel_low_list):
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

    def database_search(self, db):
        tagged_q = self.search_q.save()
        return db.database_query(tagged_q['Tag'], tagged_q['Neg_Tag'])

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

    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))

    def resize(self, new_size):
        self.img = pg.transform.scale(self.img, new_size)
        self.w = self.img.get_width()
        self.h = self.img.get_height()

    def load(self):
        if os == 'W':
            img = pg.image.load('./image/' + self.name + '.png')
        elif os == 'M':
            img = pg.image.load('/Users/Peace/Desktop/Studio4-main/project/image/' + self.name + '.png')

        return img

    def mouse_on(self):
        (pos_x, pos_y) = pg.mouse.get_pos()
        if self.x <= pos_x <= self.x + self.check_w and self.y <= pos_y <= self.y + self.h:
            is_mouse_on = True
        else:
            is_mouse_on = False
        return is_mouse_on

    def fill(self):
        if 'fill' not in self.name:
            self.name += ' fill'
            self.img = self.load()
            self.resize((self.w, self.h))

    def unfill(self):
        if 'fill' in self.name:
            self.name = self.name.replace(' fill', '')
            self.img = self.load()
            self.resize((self.w, self.h))

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if 'positive' in self.name or 'negative' in self.name or 'manual' in self.name:
                    if self.mouse_on():
                        self.fill()

                    elif not self.mouse_on():
                        self.unfill()


class Vertical_ScrollBar(object):
    def __init__(self, window_height):
        self.y_axis = 0
        self.window_height = window_height
        self.change_y = 0
        self.win_x = 1280
        self.win_y = 720

        self.bar_up = pg.Rect(self.win_x - 20, 0, 20, 20)
        self.bar_down = pg.Rect(self.win_x - 20, self.win_y - 40, 20, 20)


        if os == 'W':
            self.bar_up_image = pg.image.load('./image/up.png').convert()
            self.bar_down_image = pg.image.load('./image/down.png').convert()
        elif os == 'M':
            self.bar_up_image = pg.image.load('/Users/Peace/Desktop/Studio4-main/project/image/up.png').convert()
            self.bar_down_image = pg.image.load('/Users/Peace/Desktop/Studio4-main/project/image/down.png').convert()


        self.on_bar = False
        self.mouse_diff = 0
        self.scroll = 0
        self.scrollTimeStamp = 0

    def update(self):

        bar_height = int((self.win_y - 40) / (self.window_height / (self.win_y * 1.0)))
        self.bar_rect = pg.Rect(self.win_x - 20, 20, 20, bar_height)

        self.y_axis += self.change_y

        if self.y_axis > 0:
            self.y_axis = 0
        elif (self.y_axis + self.window_height) < self.win_y:
            self.y_axis = self.win_y - self.window_height

        height_diff = self.window_height - self.win_y

        scroll_length = self.win_y - self.bar_rect.height - 60
        bar_half_length = self.bar_rect.height / 2 + 20

        if self.on_bar:
            pos = pg.mouse.get_pos()
            self.bar_rect.y = pos[1] - self.mouse_diff
            if self.bar_rect.top < 20:
                self.bar_rect.top = 20
            elif self.bar_rect.bottom > (self.win_y - 40):
                self.bar_rect.bottom = self.win_y - 40

            self.y_axis = int(height_diff / (scroll_length * 1.0) * (self.bar_rect.centery - bar_half_length) * -1)
        else:
            if height_diff != 0:
                self.bar_rect.centery = scroll_length / (height_diff * 1.0) * (self.y_axis * -1) + bar_half_length
            else:
                self.bar_rect.centery = scroll_length * (self.y_axis * -1) + bar_half_length

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 4:  # scroll up
                self.change_y = 20
                self.scroll = 1
                self.scrollTimeStamp = time.time()
            elif event.button == 5:  # scroll down
                self.change_y = -20
                self.scroll = 1
                self.scrollTimeStamp = time.time()

            else:
                pos = pg.mouse.get_pos()
                if self.bar_rect.collidepoint(pos):
                    self.mouse_diff = pos[1] - self.bar_rect.y
                    self.on_bar = True
                elif self.bar_up.collidepoint(pos):
                    self.change_y = 5
                elif self.bar_down.collidepoint(pos):
                    self.change_y = -5

        if event.type == pg.MOUSEBUTTONUP:
            if not self.scroll:
                self.change_y = 0
                self.on_bar = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                self.change_y = 5
            elif event.key == pg.K_DOWN:
                self.change_y = -5

        if event.type == pg.KEYUP:
            if event.key == pg.K_UP:
                self.change_y = 0
            elif event.key == pg.K_DOWN:
                self.change_y = 0

    def draw(self, screen):
        pg.draw.rect(screen, (197, 194, 197), self.bar_rect)

        screen.blit(self.bar_up_image, (self.win_x - 20, 0))
        screen.blit(self.bar_down_image, (self.win_x - 20, self.win_y - 40))


# --------------------------------------------------------------------------------

class Horizontal_ScrollBar(object):
    def __init__(self, window_width):
        self.x_axis = 0
        self.window_width = window_width
        self.change_x = 0
        self.win_x = 1280
        self.win_y = 720
        self.bar_left = pg.Rect(0, self.win_y - 20, 20, 20)
        self.bar_right = pg.Rect(self.win_x - 40, self.win_y - 20, 20, 20)

        if os == 'W':
            self.bar_left_image = pg.image.load('./image/left.png').convert()
            self.bar_right_image = pg.image.load('./image/right.png').convert()

        elif os == 'M':
            self.bar_left_image = pg.image.load('/Users/Peace/Desktop/Studio4-main/project/image/left.png').convert()
            self.bar_right_image = pg.image.load('/Users/Peace/Desktop/Studio4-main/project/image/right.png').convert()

        self.on_bar = False
        self.mouse_diff = 0

    def update(self):
        bar_length = int((self.win_x - 40) / (self.window_width / (self.win_x * 1.0)))
        self.bar_rect = pg.Rect(20, self.win_y - 20, bar_length, 20)

        self.x_axis += self.change_x

        if self.x_axis > 0:
            self.x_axis = 0
        elif (self.x_axis + self.window_width) < self.win_x:
            self.x_axis = self.win_x - self.window_width

        width_diff = self.window_width - self.win_x

        scroll_length = self.win_x - self.bar_rect.width - 60
        bar_half_height = self.bar_rect.width / 2 + 20

        if self.on_bar:
            pos = pg.mouse.get_pos()
            self.bar_rect.x = pos[0] - self.mouse_diff
            if self.bar_rect.left < 20:
                self.bar_rect.left = 20
            elif self.bar_rect.right > (self.win_x - 40):
                self.bar_rect.right = self.win_x - 40
            self.x_axis = int(width_diff / (scroll_length * 1.0) * (self.bar_rect.centerx - bar_half_height) * -1)
        else:
            if width_diff != 0:
                self.bar_rect.centerx = scroll_length / (width_diff * 1.0) * (self.x_axis * -1) + bar_half_height
            else:
                self.bar_rect.centerx = scroll_length * (self.x_axis * -1) + bar_half_height

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            pos = pg.mouse.get_pos()
            if self.bar_rect.collidepoint(pos):
                self.mouse_diff = pos[0] - self.bar_rect.x
                self.on_bar = True
            elif self.bar_left.collidepoint(pos):
                self.change_x = 5
            elif self.bar_right.collidepoint(pos):
                self.change_x = -5

        if event.type == pg.MOUSEBUTTONUP:
            self.change_x = 0
            self.on_bar = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RIGHT:
                self.change_x = -5
            elif event.key == pg.K_LEFT:
                self.change_x = 5

        if event.type == pg.KEYUP:
            if event.key == pg.K_RIGHT:
                self.change_x = 0
            elif event.key == pg.K_LEFT:
                self.change_x = 0

    def draw(self, screen):
        pg.draw.rect(screen, (197, 194, 197), self.bar_rect)
        screen.blit(self.bar_left_image, (0, self.win_y - 20))
        screen.blit(self.bar_right_image, (self.win_x - 40, self.win_y - 20))
