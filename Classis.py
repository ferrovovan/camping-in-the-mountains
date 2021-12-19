import pygame
import os
import sys


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

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def get_cell(self, mouse_pos):
        if any((mouse_pos[0] <= self.left, mouse_pos[0] >= self.left + self.cell_size * self.width,
                mouse_pos[1] <= self.top, mouse_pos[1] >= self.top + self.cell_size * self.height)):
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


class Button(pygame.sprite.Sprite):
    """
    класс кнопки
    """

    image = load_image('gfx/buttons/button1.png', colorkey=-1)

    def __init__(self, group, x, y, width, height, id=0):
        """
        :param group: группа спрайтов
        :param x: left
        :param y: top
        """
        super().__init__(group)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = pygame.rect.Rect(x, y, width, height)
        self.id = id

    def draw_text(self, screen):
#        font = pygame.font.Font(None, 30)
#        string_rendered = font.render(self.text, 1, pygame.Color('white'))
#        intro_rect = string_rendered.get_rect()
#        screen.blit(string_rendered, intro_rect)
        pass

    def click(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            return True
        return False


class Interface:
    """
    Это класс пользовательского интерфейса в игре.
    """
    pass


class Map(Board):
    """
    Это класс поля, на котором всё будет отображаться.
    """
    # допустимые размеры поля
    zoom_sizes = [20, 30, 40, 50, 60, 70, 80, 90, 100, 120, 140, 160, 180]

    # готов
    def __init__(self, width, height, screenBoards=None):
        super().__init__(width, height)
        if screenBoards is None:  # если не заданны координаты окна
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


class StaticObj:
    """
    родитель всех не перемещяющихся объектов
    """

    def __init__(self, board, x, y):
        #  объекты могут обращаться к доске
        self.board = board  # это ссылка!!!
        self.x = x
        self.y = y
        self.board[y][x] = self


class Wall(StaticObj):
    """
    класс стены.
    """
    pass


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
            dY = vCoords[1]
            if 0 < self.x + dX < boardWight and 0 < self.y + dY < boardHeight and \
                    self.board[self.y + dY][self.x + dX] is None:
                self.board[self.y + dY][self.x + dX] = self
                self.board[self.y][self.x] = None


class Hero(MoveObj):
    """
    класс главного героя.
    """
    pass


class BadGroup(MoveObj):
    """
    класс банды
    """

    # готов
    def __init__(self, board, x, y, group_size=1, is_in_circle=False):
        super().__init__(board, x, y, is_in_circle=is_in_circle)
        self.group_size = group_size