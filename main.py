from os import path  # для музыки

import pygame.mixer_music

from Classis import *

pygame.init()
pygame.display.set_caption('Поход по горам')
pygame.display.set_icon(pygame.image.load('icon.ico'))

# открытие настроек
settingsDict = {}
with open('settings.txt', 'r') as settings:
    for line in settings:
        x = line[:-1].split(' = ')
        settingsDict[x[0]] = x[1]
settingsDict['display'] = tuple(settingsDict['display'][1:-1].split(','))
# заполняем поля
FPS = int(settingsDict['FPS'])
language = settingsDict['language']
size = (int(settingsDict['display'][0]), int(settingsDict['display'][1]))
load_map = settingsDict['map']

if settingsDict.get('First_open'):  # если открывается в первый раз
    # все настройки
    open_settings = open('data/common/all_settings.txt')
    all_settings = dict()
    for line in open_settings:
        line = line.split(' = ')  # [param, '[value1, value2, value3]\n']
        values = line[1][1:len(line[1]) - 2].split(', ')
        all_settings[line[0]] = values
    # настройка параметров, не соответсвующих стандарту
    all_settings['display'] = list(
        map(lambda value: tuple(value[1:len(value) - 1].split(',')), all_settings['display']))
    display_set = all_settings['display']
    display_set = list(map(lambda x1: (int(x1[0]), int(x1[1])), display_set))
    display_set.sort(key=lambda x1: x1[1])
    open_settings.close()
    # находим ближайший экран
    inf_obj = pygame.display.Info()
    W = inf_obj.current_w
    H = inf_obj.current_h
    # находим новый размер экрана
    H1 = 9 * W / 16
    if H1 >= display_set[-1][1]:  # если больше наибольшего
        size = display_set[-1]
    elif H1 <= display_set[0][1]:  # если меньше наименьшего
        size = display_set[0]
    else:
        for i in range(len(display_set) - 1):
            if H1 > display_set[i][1]:
                if H1 - display_set[i][1] < display_set[i + 1][1] - H1:
                    size = display_set[i]
                else:
                    size = display_set[i + 1]
                break

    settingsDict['display'] = (str(size[0]), str(size[1]))
    # переписываем настройки, без первого открытия
    settings1 = open('settings.txt', mode='w')
    for key in settingsDict.keys():
        if key != 'First_open':
            if key == 'display':
                line = key + ' = ' + f'({settingsDict[key][0]},{settingsDict[key][1]})'
            else:
                line = key + ' = ' + settingsDict[key]
            line = line + '\n'
            settings1.write(line)
    settings1.close()

screen = pygame.display.set_mode(size)  # ставим размер экрана


def start_screen(screen, FPS):
    # инициализация
    # музон
    pygame.mixer.music.load(path.join('data/sounds/TNO Burgundian Lullaby.mp3'))
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(loops=-1)

    menuIm = load_image('gfx/textures/interface/fone.png')  # загружаем фон
    nameIm = load_image('gfx/Name_prog.png')  # загружаем название
    # ставим на экран
    screen.blit(menuIm, menuIm.get_rect())
    screen.blit(nameIm, ((size[0] - nameIm.get_width()) // 2, size[1] // 5))

    # изображения
    images = {'button1': load_image('gfx/buttons/button1.png'),
              'button2': load_image('gfx/buttons/button2.png')}
    # сообщение
    message = load_localisation('messages', language=language)[3][1]
    messageWin = MessageWin((300, size[1] // 9), message=message, auto_words_size=True)
    draw_message = False
    # ставим кнопки
    menu_id = [1, 2, 3, 14, 4]  # id кнопок меню
    load_id = [11, 12, 13, 7]  # а кто-то поверил...

    butt_indent = 20  # отступ от кнопок
    y_indent = 50  # отступ от верхнего края экрана
    menuWin = MenuDisplay(screen.get_size(), menu_id, images['button1'], t=y_indent, indent=butt_indent)
    settingsWin = SettingsDisplay(screen.get_size(), settingsDict, images['button1'], t=y_indent, indent=butt_indent)
    loadWin = LoadDisplay(screen.get_size(), load_id, settingsDict, butt_im=images['button1'], t=y_indent,
                          indent=butt_indent)
    isnIm = load_image('gfx/instruction.png')
    instruction = InstructionDisplay(screen.get_size(), butt_im=images['button1'], instructionImage=isnIm, t=y_indent, indent=butt_indent)

    # страницы
    screens_dict = {'menuWin': menuWin,
                    'settingsWin': settingsWin,
                    'loadWin': loadWin,
                    'instruction': instruction}
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
                    elif id == 11:  # карта 1
                        loadWin.set_map(1)
                        draw_message = True  # включаем рисование сообщения
                    elif id == 12:  # карта 2
                        loadWin.set_map(2)
                        draw_message = True  # включаем рисование сообщения
                    elif id == 13:  # карта 3
                        loadWin.set_map(3)
                        draw_message = True  # включаем рисование сообщения
                    elif id == 14:  # инструкция
                        draw_screen = 'instruction'
        # рендер
        if draw_message:
            scrRect = screens_dict[draw_screen].get_rect()
            messageWin.render(screens_dict[draw_screen], coords=(
                (scrRect.width - messageWin.get_width()) // 2, (scrRect.height - messageWin.get_height()) // 2))
        screens_dict[draw_screen].render(screen, language=language)
        pygame.display.flip()
        clock.tick(FPS)


def main():
    # инициализация
    pygame.mixer.music.stop()  # останавливаем музон
    is_return = False  # если нужно вернуться
    # данные игры
    board = Map(16, 16, screenBoards=size)  # создаём доску
    board.load_map(f'data/maps/{load_map}', size)  # загружаем карту
    interface = Interface(size, board.cell_size, language=language)  # создаём интерфейс
    hero1 = Hero(board.board, 0, 7, is_in_circle=True)  # создаём героя
    character = Character(size, hero_link=hero1, map_linc=board)  # создаём интерфейс героя
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
                message = keyManager.manage_keydown(event)
                if message == "return":
                    is_return = True
                    running = False
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
