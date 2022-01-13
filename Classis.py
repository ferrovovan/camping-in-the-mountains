import pygame
import os
import sys
import random
from Fight_sistem import main as fight


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()

    image = pygame.image.load(fullname)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_localisation(directory, language='russian'):
    data = open(f'data/localisation/{directory}/{language}.txt', encoding='utf-8').read()
    table = [r.split(';') for r in data.split('\n')]
    return table


class SomeDisplay(pygame.Surface):
    def __init__(self, size, coords, color='gray'):
        super().__init__(size)
        self.coords = coords
        self.otherGroup = pygame.sprite.Group()
        self.buttonGroup = ButtonGroup()
        self.color = color
        self.fill(color)

    def is_click(self, mouse_pos):
        pass

    def render(self, screen, language='russian'):
        screen.blit(self, self.coords)
        self.fill(self.color)
        self.buttonGroup.draw(self)
        self.buttonGroup.draw_text(self, language=language)
        self.otherGroup.draw(self)


class MenuDisplay(SomeDisplay):
    def __init__(self, size, id_list, butt_im=None, t=0, indent=0, color='gray'):
        size, coords = self._auto_data(size, t=t)
        super().__init__(size, coords, color=color)
        self._made_buttons(id_list, butt_im=butt_im, indent=indent)

    @staticmethod
    def _auto_data(size, t=0):
        size1 = (560, size[1] // 3)
        coords1 = (size[0] // 2 - size1[0] // 2, size[1] // 3 + t)
        return size1, coords1

    def _made_buttons(self, id_list, butt_im=None, indent=20):
        """
        Ставит кнопки на себе
        """
        k = 4
        scr_size = self.get_size()
        if butt_im is None:
            butt_im = Button.image
        n = len(id_list)
        button_width = scr_size[0] - 2 * indent
        button_height = (scr_size[1] - 2 * indent) * k // (n * (k + 1) - 1)
        for i in range(1, n + 1):
            Button(self.buttonGroup,
                   indent,
                   indent + (i - 1) * (button_height * (1 + k) // k),
                   button_width, button_height,
                   id=id_list[i - 1], image=butt_im)

    def reset_button(self, id, sp_id=None, new_size=None, new_coords=None, new_im=None):
        button = self.buttonGroup.get_sprite(id, sp_id=sp_id)
        if button is not None:
            if new_size is not None:
                button.rect.width = new_size[0]
                button.rect.height = new_size[1]
            if new_coords is not None:
                button.rect.x = new_coords[0]
                button.rect.y = new_coords[1]
            if new_im is not None:
                button.image = new_im
            button.image = pygame.transform.scale(button.image, (button.rect.width, button.rect.height))

    def click_id(self, event):
        """
        :return button's id, if one of them was clicked? else return None
        """
        event.pos = (event.pos[0] - self.coords[0], event.pos[1] - self.coords[1])
        return self.buttonGroup.click_id(event)


class LoadDisplay(MenuDisplay):
    def _made_buttons(self, id_list, butt_im=None, indent=20):
        super()._made_buttons(id_list, butt_im=butt_im, indent=indent)


class InventoryDisplay(SomeDisplay):
    def __init__(self, size, coords, color='gray', indent=20):
        super().__init__(size, coords, color=color)
        space_size = (5, 4)
        self.inventory = Inventory(space_size, cell_size=((size[1] - indent) // space_size[1]),
                                   display_link=self)
        coords = ((size[0] + space_size[0] * self.inventory.cell_size) // 2, 0)
        # настройка строки названия
        self.item_name = StrokeSprite(self.otherGroup, '', size=50, color=pygame.color.Color(230, 100, 130))
        self.item_name.set_in_center((coords[0], coords[1] + 30))
        # настройка строки описания
        self.item_lore = StrokeSprite(self.otherGroup, '', coords=(space_size[0] * self.inventory.cell_size + 20, coords[1] + size[1] * (1 / 2)))

    def is_click(self, mouse_pos):
        return self.inventory.is_click((mouse_pos[0] - self.coords[0], mouse_pos[1] - self.coords[1]))

    def get_click(self, mouse_pos):
        self.inventory.get_click(mouse_pos)

    def render(self, screen, language='russian'):
        super().render(screen, language=language)
        self.inventory.render()


class SettingsDisplay(MenuDisplay):
    """
    Меню настроек
    """

    open_settings = open('data/common/all_settings.txt')
    all_settings = dict()
    for line in open_settings:
        line = line.split(' = ')  # [param, '[value1, value2, value3]\n']
        values = line[1][1:len(line[1]) - 2].split(', ')
        all_settings[line[0]] = values
    # настройка параметров, не соответсвующих стандарту
    all_settings['display'] = list(
        map(lambda value: tuple(value[1:len(value) - 1].split(',')), all_settings['display']))

    # готов
    def __init__(self, size, settingsDict, butt_im, t=0, indent=0, color='gray'):
        size, coords = self._auto_data(size, t=t)
        self.coords = coords
        super(SomeDisplay, self).__init__(size)
        self.otherGroup = pygame.sprite.Group()  # группа картинок
        self.buttonGroup = ButtonGroup()  # группа кнопок
        self.settingsDict = settingsDict
        self._made_buttons(butt_im, indent=indent)
        self.color = color
        self.fill(color)

    def _made_buttons(self, butt_im, indent=20):
        """
        Ставит кнопки на себе
        """
        k = 4
        n = len(self.all_settings) * 2
        scr_size = self.get_size()
        button_width = scr_size[0] - 2 * indent
        button_height = (scr_size[1] - 2 * indent) * k // (4 * (k + 1) - 1)
        set_list = list(self.all_settings)
        for i in range(n):
            Button(self.buttonGroup,
                   scr_size[0] // 2 + ((i % 2) * 2 - 1) * (scr_size[0] // 4) - indent,
                   indent + (scr_size[1] - indent - 2 * (button_height * (1 + k) // k)) * (i // 2) // (n // 2),
                   40, 40,
                   id=i % 2 + 8, sp_id=i // 2 + 1, image=butt_im)

            if i % 2 == 0:
                thisCoords = [0,
                              indent + (scr_size[1] - indent - 2 * (button_height * (1 + k) // k)) * (i // 2) // (
                                      n // 2)]
                # название
                StrokeSprite(self.otherGroup, set_list[i // 2], coords=thisCoords)
                # значение
                x = StrokeSprite(self.otherGroup, self.settingsDict[set_list[i // 2]], coords=thisCoords)
                x.rect.x = scr_size[0] // 2 - x.rect.width // 2

        Button(self.buttonGroup,  # применить
               indent,
               indent + 2 * (button_height * (1 + k) // k),
               button_width, button_height,
               id=10, image=butt_im)
        Button(self.buttonGroup,  # назад
               indent,
               indent + 3 * (button_height * (1 + k) // k),
               button_width, button_height,
               id=7, image=butt_im)

    def save_settings(self):
        settings1 = open('settings.txt', mode='w')
        for key in self.settingsDict.keys():
            if key == 'display':
                line = key + ' = ' + f'({self.settingsDict[key][0]},{self.settingsDict[key][1]})'
            else:
                line = key + ' = ' + self.settingsDict[key]
            line = line + '\n'
            settings1.write(line)

    def manage_settings(self, event):
        id, sp_id = self.buttonGroup.click_id(event, sp_id=True)
        if id == 8:
            self._change_settings(-1, sp_id)
        else:
            self._change_settings(1, sp_id)

    def _change_settings(self, step, i):
        """
        Изменяет настоящие настройки
        :return: True if settings was changed? else: False
        """
        set_list = list(self.all_settings)
        i -= 1
        # номер сейчас-него значения среди остальных в группе
        i1 = self.all_settings[set_list[i]].index(self.settingsDict[set_list[i]])
        if 0 <= i1 + step < len(self.all_settings[set_list[i]]):  # если есть такое значение
            self.settingsDict[set_list[i]] = self.all_settings[set_list[i]][i1 + step]
            # ставим новое значение
            i += 1
            j = i * 2
            for strokeSprite in self.otherGroup:
                j -= 1
                if j == 0:
                    strokeSprite.set_text(self.settingsDict[set_list[i - 1]])
                    break
            return True
        return False

    def render(self, screen, language='russian'):
        super().render(screen, language=language)
        self.otherGroup.draw(self)


class MessageWin(pygame.Surface):
    """
    Всплывающее сообщение
    """
    def __init__(self, size, message='', color='red', word_size=60, auto_words_size=False):
        super().__init__(size)
        self.rect = pygame.Rect(0, 0, size[0], size[1])
        self.color = color
        # рисуем надпись
        self.set_text(message=message, word_size=word_size, auto_words_size=auto_words_size)

    def _auto_words_size(self, message):
        if len(message) > 0:
            return int(2.5 * self.rect.width // len(message))
        else:
            return self.rect.width

    def set_text(self, message='', word_size=60, auto_words_size=False):
        if auto_words_size:
            word_size = self._auto_words_size(message)
        font = pygame.font.Font(None, word_size)
        string_rendered = font.render(message, True, pygame.Color(self.color))
        message_rect = string_rendered.get_rect()
        # ставим координаты
        message_rect.x = (self.rect.width - message_rect.width) // 2
        message_rect.y = (self.rect.height - message_rect.height) // 2
        # рисуем надпись на экране
        self.blit(string_rendered, message_rect)

    def render(self, screen, coords=(0, 0), centrees=False):
        if centrees:
            screen.blit(self, (coords[0] - (self.get_width() // 2), coords[1] - (self.get_height() // 2)))
        else:
            screen.blit(self, coords)


class ButtonGroup(pygame.sprite.Group):
    def draw_text(self, screen, language='russian', text_dict=None):
        if text_dict is None:
            for button in self:
                button.draw_text(screen, language=language)
        else:
            for button in self:
                button.draw_text(screen, text_dict=text_dict)

    # готов
    def get_sprite(self, id, sp_id=None):
        for button in self:
            if button.id == id and button.special_id == sp_id:
                return button
        return None

    # готов
    def click_id(self, event, sp_id=False):
        """
        :return button's id, if one of them was clicked? else return None
        """
        for button in self:
            if button.is_click(event):
                if sp_id:
                    return button.id, button.special_id
                return button.id
        return None


# готов
class Button(pygame.sprite.Sprite):
    """
    класс кнопки
    """

    image = load_image('gfx/buttons/button1.png', colorkey=-1)

    # готов
    def __init__(self, group, x, y, width, height, id=0, sp_id=None, image=None):
        """
        :param group: группа спрайтов
        :param x: left
        :param y: top
        """
        super().__init__(group)
        if image is not None:
            self.image = image
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = pygame.rect.Rect(x, y, width, height)
        self.id = id
        self.special_id = sp_id

    # готов
    def draw_text(self, screen, text_dict=None, language='russian'):
        font = pygame.font.Font(None, 30)
        if text_dict is None:
            data = open(f'data/localisation/buttons text/{language}.txt', encoding='utf-8').read()
            table = [r.split(';') for r in data.split('\n')]
            text = table[self.id][1]
        else:
            text = text_dict[self.id][1]
        string_rendered = font.render(text, True, pygame.Color('red'))
        blitRect = self.rect.copy()
        blitRect.top = self.rect.top + (self.rect.height - string_rendered.get_height()) // 5
        blitRect.left = self.rect.left + (self.rect.width - string_rendered.get_width()) // 2
        screen.blit(string_rendered, blitRect)

    # готов
    def is_click(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            return True
        return False

    def set_image(self, image):
        """
        Ставит новое изображение
        """
        self.image = pygame.transform.scale(image, (self.rect.width, self.rect.height))


class StrokeSprite(pygame.sprite.Sprite):
    """
    Является спрайтом, получаемый из строки
    """

    def __init__(self, group, blitObj, coords=None, size=30, color=pygame.color.Color('red')):
        super().__init__(group)
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.size = size
        self.color = color
        self.set_text(blitObj, coords=coords)

    def set_text(self, blitObj, coords=None):
        font = pygame.font.Font(None, self.size)
        if isinstance(blitObj, int):
            blitObj = str(blitObj)
        elif isinstance(blitObj, tuple):
            blitObj = str(blitObj)
        elif isinstance(blitObj, list):
            blitObj = str(tuple(blitObj))
        string_rendered = font.render(blitObj, True, pygame.Color(self.color))
        self.image = string_rendered
        self.rect = pygame.Rect(self.rect.x, self.rect.y, string_rendered.get_width(), string_rendered.get_height())
        if coords is not None:
            self.rect.x = coords[0]
            self.rect.y = coords[1]

    def set_size(self, new_size):
        self.size = new_size

    def set_color(self, new_color):
        self.color = new_color

    def set_in_center(self, coords=None):
        """
        ставит себя по центру
        """
        if coords is None:
            coords = (self.rect.x, self.rect.y)
        self.rect = pygame.Rect(coords[0] - self.rect.width // 2, coords[1], self.rect.width, self.rect.height)


class Interface:
    """
    Это класс пользовательского интерфейса в игре.
    """

    menu_close = True

    def __init__(self, screenBoards, cell_size, language='russian'):
        """
        :param screenBoards: (width, height)
        :param cell_size: int
        """
        self.rect = pygame.rect.Rect(0, 0, *screenBoards)
        self.localisation = load_localisation('buttons text', language=language)
        # группы спрайтов
        self.specificationsSpriteGroup = pygame.sprite.Group()  # рисунки, только отображающиеся
        self.menuButtGr = ButtonGroup()  # кнопка меню
        self.menuButtonsGroup = ButtonGroup()
        # окошко сообщения
        self.message_win = MessageWin((screenBoards[0] // 5, screenBoards[1] // 4), '', color='red', auto_words_size=True)
        self.draw_message = False

        # меню кнопки
        self.menuButt = Button(self.menuButtGr, screenBoards[0] - cell_size // 2,
                               0, cell_size // 2, cell_size // 2)
        x = [6]
        n = len(x)  # количество кнопок
        width = 240
        height = 120
        k = 1.2  # коэффициент удалённости кнопок
        for i in range(n):
            Button(self.menuButtonsGroup, (screenBoards[0] - width) // 2,
                   screenBoards[1] // 2 + int((n // 2 - i) * height * k),
                   width, height, id=x[i])

    def change_message(self, text=None, set_visible=None):
        if text is not None and isinstance(text, str):
            self.message_win.set_text(message=text, auto_words_size=True)
        if set_visible is not None and isinstance(set_visible, bool):
            self.draw_message = set_visible

    def get_click(self, event):
        for button in self.menuButtGr:
            if button.is_click(event):
                if button == self.menuButt:
                    self._close_menu(not self.menu_close)
                    break
        if not self.menu_close:
            id = self.menuButtonsGroup.click_id(event)
            if id is not None:
                if id == 6:  # выйти в главное меню
                    return "return"

    def is_click(self, event):
        for button in self.menuButtGr:
            if button.is_click(event):
                return True
        if not self.menu_close and self.menuButtonsGroup.click_id(event):
            return True
        return False

    def _close_menu(self, a=None):
        if a is None:
            a = not self.menu_close
        self.menu_close = a
        self.mouseManager_linc.modifications['character'] = not a
        self.mouseManager_linc.modifications['map'] = not a

    def render(self, screen):
        self.specificationsSpriteGroup.draw(screen)
        self.menuButtGr.draw(screen)
        self.menuButtGr.draw_text(screen, text_dict=self.localisation)
        if not self.menu_close:
            self.menuButtonsGroup.draw(screen)
            self.menuButtonsGroup.draw_text(screen, text_dict=self.localisation)
        if self.draw_message:
            self.message_win.render(screen, (screen.get_width() // 2, screen.get_height() // 2), centrees=True)


class Character:
    """
    Это класс, в котором игрок сможет увидеть свои вещи, свои навыки, летопись действий и прочее
    """

    def __init__(self, screenBoards, hero_link=None, language='russian'):
        self.is_open = False
        if isinstance(hero_link, Hero):  # если дали ссылку
            self.hero_link = hero_link
            hero_link.character_link = self
        # загружаем локализацию
        self.item_names = load_localisation('items name', language=language)
        self.items_depiction = load_localisation('items depiction', language=language)
        self.messages = load_localisation('messages', language=language)
        # настройки экрана
        self.rect = pygame.Rect(screenBoards[0] / 8, screenBoards[1] / 5, screenBoards[0] * (3 / 4),
                                screenBoards[1] * (3 / 5))
        self.color = 'red'
        # характеристики персонажа
        self.health = 10
        self.defense = 10
        self.attack = 10
        self.coins = 0
        # данные для построения страниц
        indent = 20
        page_size = (self.rect.width - 2 * indent, self.rect.height - 2 * indent)
        coords = (self.rect.left + indent, self.rect.top + indent)
        color = 'orange'
        # строительство инвентаря
        self.inventory = InventoryDisplay(page_size, coords, color=color, indent=indent)
        self.inventory.inventory.character_link = self
        # строительство умений
        self.skills = SomeDisplay(page_size, coords, color=color)
        # строительство ?
        self.stats = SomeDisplay(page_size, coords, color=color)
        # строительство летописи
        self.eventlog = SomeDisplay(page_size, coords, color=color)
        #
        self.pages = {'inventory': self.inventory,
                      'stats': self.stats,
                      'skills': self.skills,
                      'eventlog': self.eventlog}
        self.open_page = 'inventory'

    def move_hero(self, vCoords):
        # запускаем ход игрока
        if self.hero_link.move(vCoords) is False:  # если нельзя пройти
            victory = fight()  # запускаем битву
            pygame.mouse.set_visible(True)
            if not victory:
                self.keyManager_linc.interface_linc.change_message(text=self.messages[1][1], set_visible=True)
                pygame.time.set_timer(30, 3000)  # ставим таймер
                self.keyManager_linc.is_died = True  # ставим флажок
            else:
                pygame.mixer.music.stop()
                self.keyManager_linc.interface_linc.change_message(text=self.messages[2][1], set_visible=True)
                chans = random.randrange(1, 10)
                if chans > 8:
                    item = Item('gfx/textures/items/stalk.png', id=1)
                elif chans > 9:
                    item = Item('gfx/textures/items/shovel.png', id=2)
                else:
                    item = Item('gfx/textures/items/shield.png', id=3)
                self.inventory.inventory.add_item(item)

    def get_click(self, mouse_pos):
        mouse_pos = (mouse_pos[0] - self.rect.x, mouse_pos[1] - self.rect.y)
        if self.open_page == 'inventory':
            self.inventory.get_click(mouse_pos)

    def is_click(self, event):
        return self.pages[self.open_page].is_click(event.pos)

    def set_open(self, a=None):
        """
        :param a: True or False
        """
        if a is None:
            a = not self.is_open
        self.is_open = a

    def render(self, screen, language='russian'):
        pygame.draw.rect(screen, self.color, self.rect)
        self.pages[self.open_page].render(screen, language=language)


class Item:
    """
    Класс предмета
    """

    def __init__(self, filename, id=0):
        self.image = load_image(filename, colorkey=-1)
        self.rect = self.image.get_rect()
        self.id = id

    def render(self, screen, x=0, y=0):
        screen.blit(self.image, (x, y, self.image.get_width(), self.image.get_height()))


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[None] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def is_click(self, mouse_pos):
        if any((mouse_pos[0] <= self.left, mouse_pos[0] >= self.left + self.cell_size * self.width,
                mouse_pos[1] <= self.top, mouse_pos[1] >= self.top + self.cell_size * self.height)):
            return False
        return True

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def get_cell(self, mouse_pos):
        if self.is_click(mouse_pos):
            return None
        return ((mouse_pos[0] - self.left) // self.cell_size,
                (mouse_pos[1] - self.top) // self.cell_size)

    def on_click(self, cell_coord):
        pass

    def render(self, screen):
        for i in range(self.width):
            for j in range(self.height):
                pygame.draw.rect(screen, 'white',
                                 ((self.left + i * self.cell_size, self.top + j * self.cell_size),
                                  (self.cell_size, self.cell_size)), width=2)


class Inventory(Board):
    """
    Хранит в себе предметы персонажа
    """

    def __init__(self, space=(5, 5), cell_size=None, display_link=None, character_link=None):
        super().__init__(*space)
        if cell_size is not None:
            self.cell_size = cell_size
        self.space = space
        self.board = [None for _ in range(space[0] * space[1])]
        self.display_link = display_link
        self.character_link = character_link

    def render(self):
        super().render(self.display_link)
        for i in range(len(self.board)):
            item = self.board[i]
            if item is None:
                break
            if isinstance(item, Item):
                item.render(self.display_link, x=(i % self.space[0]) * self.cell_size + self.cell_size // 2,
                            y=(i // self.space[0]) * self.cell_size + self.cell_size // 2)

    def add_item(self, item):
        if not isinstance(item, Item):
            raise Exception('into inventory added not Item object')
        if None in self.board:  # если осталось место
            i = self.board.index(None)
            self.board[i] = item
            self.sort_board()
        else:
            return False

    def del_item(self, id=0):
        if None in self.board:
            x = self.board.index(None)
        else:
            x = len(self.board)
        for i in range(x):
            if self.board[i].id == id:
                x = self.board.pop(i)
                self.sort_board()
                return x
        else:
            return None

    def sort_board(self):
        if None in self.board:
            x = self.board.index(None)
        else:
            x = len(self.board)
        board = self.board[:x]
        board.sort(key=lambda item: item.id)
        self.board = board
        for i in range(self.width * self.height - x):
            self.board.append(None)

    def get_cell(self, mouse_pos):
        if self.is_click(mouse_pos):
            return sum(((mouse_pos[0] - self.left) // self.cell_size,  # строка
                        ((mouse_pos[1] - self.top) // self.cell_size) * self.space[0]))  # столбец
        return None

    def on_click(self, cell_coord):
        if cell_coord is not None:
            item = self.board[cell_coord]
            if isinstance(item, Item) and self.character_link.item_names[item.id][1] != self.display_link.item_name:
                self.display_link.item_name.set_text(self.character_link.item_names[item.id][1])
                self.display_link.item_name.set_in_center(((self.display_link.get_size()[0] + self.space[0] * self.cell_size) // 2, 30))
                self.display_link.item_lore.set_text(self.character_link.items_depiction[item.id][1])


class Map(Board):
    """
    Это класс поля, на котором всё будет отображаться.
    """
    # допустимые размеры поля
    zoom_sizes = [20, 30, 40, 50, 60, 70, 80, 90, 100, 120, 140, 160, 180]

    # готов
    def __init__(self, width, height, screenBoards=None):
        super().__init__(width, height)
        if screenBoards is None:  # если не заданы координаты окна
            self.cell_size = self.zoom_sizes[len(self.zoom_sizes) // 2]
        else:
            # маштабирует равномерно
            q = min(screenBoards[0] - 40, screenBoards[1] - 40) // max(self.width, self.height)
            for i in range(len(self.zoom_sizes) - 1):
                if self.zoom_sizes[i] <= q <= self.zoom_sizes[i + 1]:
                    if q <= (self.zoom_sizes[i + 1] + self.zoom_sizes[i]) // 2:
                        q = self.zoom_sizes[i]
                    else:
                        q = self.zoom_sizes[i + 1]
                    break
            else:
                if q > self.zoom_sizes[-1]:
                    q = self.zoom_sizes[-1]
                else:
                    q = self.zoom_sizes[0]
            self.set_view((screenBoards[0] - q * self.width) // 2,
                          (screenBoards[1] - q * self.height) // 2,
                          q)

    # готов
    def set_board_in_center(self, screenBoards):
        """
        Ставит доску по центру
        :param screenBoards: (width: int, height: int)
        """
        self.left = (screenBoards[0] - self.width * self.cell_size) // 2
        self.top = (screenBoards[1] - self.height * self.cell_size) // 2

    # готов
    def zoom(self, k, screenBoards):
        """
        Маштабирует доску относительно центра экрана
        :param screenBoards: (width: int, height: int)
        :param k: int
        """
        centerX = screenBoards[0] / 2
        centerY = screenBoards[1] / 2
        i = self.zoom_sizes.index(self.cell_size)
        if 0 <= i + k < len(self.zoom_sizes):
            deltaX = (centerX - self.left)
            deltaY = (centerY - self.top)
            deltaX *= (self.zoom_sizes[i + k] / self.zoom_sizes[i])
            deltaY *= (self.zoom_sizes[i + k] / self.zoom_sizes[i])
            self.left = round(centerX - deltaX)
            self.top = round(centerY - deltaY)
            self.cell_size = self.zoom_sizes[i + k]

    # готов
    def move(self, x=0, y=0):
        self.left += x
        self.top += y

    # готов
    def load_map(self, filename, screenBoards=None):
        """
        Загружает карту с файла
        :param filename: txt filename
        """
        with open(filename, 'r') as mapFile:
            map = [line.strip() for line in mapFile]
        self.__init__(len(map[0]), len(map))  # переконструируем класс
        for i in range(len(map)):  # высота
            for j in range(len(map[0])):  # ширина
                if map[i][j] == '#':  # стена
                    Wall(self.board, j, i)
                elif map[i][j] == '@':  # герой
                    is_in_circle = True
                    if 1 < i < self.height and 1 < j < self.width:
                        is_in_circle = False
                    Hero(self.board, j, i, is_in_circle=is_in_circle)
                elif map[i][j] == '!':  # банда
                    is_in_circle = True
                    if 1 < i < self.height and 1 < j < self.width:
                        is_in_circle = False
                    BadGroup(self.board, j, i, is_in_circle=is_in_circle)
        if screenBoards is not None:
            self.set_board_in_center(screenBoards)

    # готов
    def render(self, screen):
        for i in range(self.width):
            for j in range(self.height):
                pygame.draw.rect(screen, 'white',
                                 ((self.left + i * self.cell_size, self.top + j * self.cell_size),
                                  (self.cell_size, self.cell_size)), width=2)

                if isinstance(self.board[j][i], Hero):  # рисуем героя
                    pygame.draw.circle(screen, 'blue',
                                       (self.left + i * self.cell_size + self.cell_size // 2,
                                        self.top + j * self.cell_size + self.cell_size // 2),
                                       radius=self.cell_size // 2 - 4)
                elif isinstance(self.board[j][i], Wall):  # рисуем стену
                    pygame.draw.rect(screen, 'gray',
                                     ((self.left + i * self.cell_size + 2, self.top + j * self.cell_size + 2),
                                      (self.cell_size - 3, self.cell_size - 3)))
                elif isinstance(self.board[j][i], BadGroup):  # рисуем банду
                    pygame.draw.circle(screen, 'red',
                                       (self.left + i * self.cell_size + self.cell_size // 2,
                                        self.top + j * self.cell_size + self.cell_size // 2),
                                       radius=self.cell_size // 2 - 4)


class MouseManager:
    modifications = {'interface': True,
                     'character': True,
                     'map': True}

    # готов
    def __init__(self, screen, interface, map1, character):
        self.screen = screen
        self.interface_linc = interface
        interface.mouseManager_linc = self
        self.map_linc = map1
        map1.mouseManager_linc = self
        self.character_linc = character
        character.mouseManager_linc = self

    def manage_click(self, event):
        if self.interface_linc.draw_message:
            self.interface_linc.draw_message = False
        else:
            if self.interface_linc.is_click(event) and self.modifications['interface']:  # интерфейс
                message = self.interface_linc.get_click(event)
                if message is not None:
                    return message
            elif self.character_linc.is_click(event) and self.modifications['character']:  # инвентарь
                self.character_linc.get_click(pygame.mouse.get_pos())
            elif self.map_linc.is_click(pygame.mouse.get_pos()) and self.modifications['map']:  # карта
                self.map_linc.on_click(pygame.mouse.get_pos())

    def manage_motion(self, event):
        pass

    def manage_wheel(self, event):
        if self.map_linc.is_click(pygame.mouse.get_pos()):
            self.map_linc.zoom(event.y, self.screen.get_size())


class KeyBoardManager:
    modifications = {}

    def __init__(self, screen, interface, map1, character):
        self.screen = screen
        self.interface_linc = interface
        interface.keyManager_linc = self
        self.map_linc = map1
        map1.keyManager_linc = self
        self.character_link = character
        character.keyManager_linc = self

    def manage_keydown(self, event):
        if self.interface_linc.draw_message:
            self.interface_linc.draw_message = False
        else:
            kPressed = pygame.key.get_pressed()  # нажатые кнопки
            if kPressed[pygame.K_ESCAPE]:
                self.interface_linc._close_menu()
            if self.interface_linc.menu_close:
                # стрелки
                if kPressed[pygame.K_UP]:
                    self.map_linc.move(y=-10)
                if kPressed[pygame.K_DOWN]:
                    self.map_linc.move(y=10)
                if kPressed[pygame.K_RIGHT]:
                    self.map_linc.move(x=10)
                if kPressed[pygame.K_LEFT]:
                    self.map_linc.move(x=-10)
                #
                if kPressed[pygame.K_w]:
                    self.character_link.move_hero((1, 0))
                elif kPressed[pygame.K_s]:
                    self.character_link.move_hero((-1, 0))
                elif kPressed[pygame.K_i]:
                    self.character_link.set_open()
                elif kPressed[pygame.K_d]:  # черенок
                    self.character_link.inventory.inventory.add_item(Item('gfx/textures/items/stalk.png', id=1))
                elif kPressed[pygame.K_f]:  # лопата
                    self.character_link.inventory.inventory.add_item(Item('gfx/textures/items/shovel.png', id=2))
                elif kPressed[pygame.K_g]:  # щит
                    self.character_link.inventory.inventory.add_item(Item('gfx/textures/items/shield.png', id=3))
                elif kPressed[pygame.K_r]:  # удалить элемент
                    self.character_link.inventory.inventory.del_item(0)

    def manage_keyup(self, event):
        self.manage_keydown(event)


class StaticObj:
    """
    родитель всех не перемещяющихся объектов
    """

    def __init__(self, board, x, y):
        # объекты могут обращаться к доске
        self.board = board  # это ссылка!!!
        self.x = x
        self.y = y
        self.board[y][x] = self


class Wall(StaticObj):
    """
    класс стены.
    """
    pass


class Shop(StaticObj):
    pass


class Battle:
    """
    класс битвы, здесь происходит механика боя.
    """

    def battle(self, hero, enemy):
        """
        как-то меняет параметры вводных объектов
        """
        sum1 = sum(hero.character_link.health, hero.character_link.defense, hero.character_link.attack)
        sum2 = sum(enemy.health, enemy.defense, enemy.attack)
        if sum1 >= sum2:
            return hero
        return enemy


class MoveObj(StaticObj):
    """
    родитель всех двигающихся объектов.
    """

    # готов
    def __init__(self, board, x, y, is_in_circle=True):
        super().__init__(board, x, y)
        self.in_circle = is_in_circle

    # готов
    def move(self, vCoords):
        """
        меняет своё положение на доске
        :param vCoords: (deltaX: int, deltaY: int)
        """
        dX = vCoords[0]
        boardHeight = len(self.board)
        boardWight = len(self.board[0])
        if self.in_circle:  # если в кругу
            def coords_in_num(coords):
                """
                Переводит координаты в число
                """
                x, y = coords
                if y == boardHeight - 1:  # если находится на нижней стороне доски
                    return x
                elif x == boardWight - 1:  # если находится на правой стороне доски
                    return x + (boardHeight - (y + 1))
                elif self.y == 0:  # если находится на верхней стороне доски
                    return (boardWight - 1) + (boardHeight - 1) + (boardWight - (self.x + 1))
                elif self.x == 0:  # если находится на левой стороне доски
                    return 2 * (boardWight - 1) + (boardHeight - 1) + self.y
                else:
                    raise Exception("Hero is in circle, but locate not there")

            def num_in_coords(num):
                """
                Переводит число в координаты
                """
                if num < boardWight:  # если находится на нижней стороне доски
                    return num, boardHeight - 1
                elif num < boardWight + boardHeight - 1:  # если находится на правой стороне доски
                    return boardWight - 1, (boardHeight - 1) - (num - boardWight + 1)
                elif num < 2 * boardWight + boardHeight - 2:  # если находится на верхней стороне доски
                    return boardWight - (num - (boardHeight - 1) - (boardWight - 1)) - 1, 0
                else:  # если находится на левой стороне доски
                    return 0, num - 2 * (boardWight - 1) - (boardHeight - 1)

            #  [
            #   [8,7,6,5],
            #   [9, , ,4],
            #   [0,1,2,3]
            #  ]
            s = coords_in_num((self.x, self.y))
            if dX > 0:  # если двигаемся против часовой стрелки
                dX = dX % (2 * (boardWight + boardHeight))  # убираем обороты
                if s + dX > 2 * (boardWight + boardHeight - 2):
                    s -= 2 * (boardWight + boardHeight - 2)
            else:  # если двигаемся по часовой стрелке
                dX = -(-dX % (2 * (boardWight + boardHeight)))  # убираем обороты
                if s + dX < 0:
                    s += 2 * (boardWight + boardHeight - 2)

            x1, y1 = num_in_coords(s + dX)
            if self.board[y1][x1] is None:  # производим замену
                self.board[y1][x1] = self
                self.board[self.y][self.x] = None
                self.x = x1
                self.y = y1
            else:
                return False
        else:
            dY = vCoords[1]
            if 0 < self.x + dX < boardWight and 0 < self.y + dY < boardHeight and \
                    self.board[self.y + dY][self.x + dX] is None:
                self.board[self.y + dY][self.x + dX] = self
                self.board[self.y][self.x] = None


class Hero(MoveObj):
    """
    класс главного героя.
    """

    def __init__(self, board, x, y, is_in_circle=True, character_link=None):
        super().__init__(board, x, y, is_in_circle=is_in_circle)
        if isinstance(character_link, Character):  # если дали ссылку
            self.character_link = character_link
            character_link.hero_link = self


class BadGroup(MoveObj):
    """
    класс банды
    """

    # готов
    def __init__(self, board, x, y, group_size=1, is_in_circle=False):
        super().__init__(board, x, y, is_in_circle=is_in_circle)
        self.group_size = group_size
        # характеристики
        self.health = 12
        self.defense = 4
        self.attack = 2
