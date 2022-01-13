from os import path  # для музыки

import pygame.mixer_music

from Classis import *

pygame.init()
pygame.display.set_caption('Поход по горам')

# открытие настроек
settingsDict = {}
with open('settings.txt', 'r') as settings:
    for line in settings:
        x = line[:-1].split(' = ')
        settingsDict[x[0]] = x[1]
# меняем display
settingsDict['display'] = tuple(settingsDict['display'][1:-1].split(','))
for key in settingsDict.keys():
    if key == 'FPS':
        FPS = int(settingsDict[key])
    elif key == 'language':
        language = settingsDict[key]
    elif key == 'display':
        size = (int(settingsDict[key][0]), int(settingsDict[key][1]))

screen = pygame.display.set_mode(size)  # ставим размер экрана


def start_screen(screen, FPS):
    # инициализация
    # музон
    pygame.mixer.music.load(path.join('data/sounds/TNO Burgundian Lullaby.mp3'))
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(loops=-1)

    menuIm = load_image('gfx/textures/interface/fone.png')  # загружаем картинку
    screen.blit(menuIm, menuIm.get_rect())  # ставим на экран

    # изображения
    images = {'button1': load_image('gfx/buttons/button1.png'),
              'button2': load_image('gfx/buttons/button2.png')}
    # сообщение
    message = load_localisation('messages', language=language)[3][1]
    messageWin = MessageWin((300, size[1] // 9), message=message, auto_words_size=True)
    draw_message = False
    # ставим кнопки
    menu_id = [1, 2, 3, 4]  # id кнопок меню
    load_id = [0, 0, 0, 7]  # а кто-то поверил...

    butt_indent = 20  # отступ от кнопок
    y_indent = 50  # отступ от верхнего края экрана
    menuWin = MenuDisplay(screen.get_size(), menu_id, images['button1'], t=y_indent, indent=butt_indent)
    settingsWin = SettingsDisplay(screen.get_size(), settingsDict, images['button1'], t=y_indent, indent=butt_indent)
    loadWin = LoadDisplay(screen.get_size(), load_id, images['button1'], t=y_indent, indent=butt_indent)

    # страницы
    screens_dict = {'menuWin': menuWin,
                    'settingsWin': settingsWin,
                    'loadWin': loadWin}
    draw_screen = 'menuWin'  # текущая страница
    # цикл
    running = True
    clock = pygame.time.Clock()  # часы
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                draw_message = False
                id = screens_dict[draw_screen].click_id(event)  # id нажатой кнопки
                if id is not None:
                    if id == 1:  # играть
                        return True
                    elif id == 2:  # загрузить
                        draw_screen = 'loadWin'
                    elif id == 3:  # настройки
                        draw_screen = 'settingsWin'
                    elif id == 4:  # выход
                        pygame.quit()
                        exit()
                    elif id == 7:  # назад
                        draw_screen = 'menuWin'
                    elif id == 8:  # <-
                        screens_dict[draw_screen].manage_settings(event)
                    elif id == 9:  # ->
                        screens_dict[draw_screen].manage_settings(event)
                    elif id == 10:  # применить
                        screens_dict[draw_screen].save_settings()
                        draw_message = True  # включаем рисование сообщения
        # рендер
        if draw_message:
            scrRect = screens_dict[draw_screen].get_rect()
            messageWin.render(screens_dict[draw_screen], coords=((scrRect.width - messageWin.get_width()) // 2, (scrRect.height - messageWin.get_height()) // 2))
        screens_dict[draw_screen].render(screen, language=language)
        pygame.display.flip()
        clock.tick(FPS)


def main():
    # инициализация
    pygame.mixer.music.stop()  # останавливаем музон
    is_return = False  # если нужно вернуться
    # данные игры
    board = Map(16, 16, screenBoards=size)  # создаём доску
    board.load_map('data/maps/main_map.txt', size)  # загружаем карту
    interface = Interface(size, board.cell_size, language=language)  # создаём интерфейс
    hero1 = Hero(board.board, 0, 7, is_in_circle=True)  # создаём героя
    character = Character(size, hero_link=hero1)  # создаём интерфейс героя
    mouseManager = MouseManager(screen, interface, board, character)  # создаём менеджера мыши
    keyManager = KeyBoardManager(screen, interface, board, character)  # создаём менеджера клавиатуры
    #
    DIE_EVENT = 30
    is_died = False
    keyManager.is_died = is_died
    # цикл
    running = True
    clock = pygame.time.Clock()  # часы
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            #  клавиатура
            if event.type == pygame.KEYDOWN:
                keyManager.manage_keydown(event)
            elif event.type == pygame.KEYUP:
                keyManager.manage_keyup(event)
            #  мышь
            if event.type == pygame.MOUSEWHEEL:  # если мышь крутится
                mouseManager.manage_wheel(event)
            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                message = mouseManager.manage_click(event)
                if message == "return":
                    is_return = True
                    running = False
            elif event.type == pygame.MOUSEMOTION:
                mouseManager.manage_motion(event)
            elif keyManager.is_died and event.type == DIE_EVENT:
                is_return = True
                running = False
        # рендер
        screen.fill('black')  # перекрашиваем экран
        board.render(screen)  # рисуем доску
        if character.is_open:
            character.render(screen, language=language)  # рисуем инвентарь героя
        interface.render(screen)  # рисуем интерфейс
        pygame.display.flip()
        clock.tick(FPS)

    if is_return:  # если нужно вернуться
        if start_screen(screen, FPS):  # запускаем заново стартовый экран
            main()


if start_screen(screen, FPS):
    main()
pygame.quit()
