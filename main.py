from Classis import *

pygame.init()
pygame.display.set_caption('Поход по горам')

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

screen = pygame.display.set_mode(size)


def start_screen(screen, FPS):
    screen.fill([255, 255, 255])
    menuIm = load_image('gfx/textures/interface/fone.png')
    screen.blit(menuIm, menuIm.get_rect())
    clock = pygame.time.Clock()

    images = {'button1': load_image('gfx/buttons/button1.png'),
              'button2': load_image('gfx/buttons/button2.png')}

    menu_id = [1, 2, 3, 4]  # id кнопок меню
    load_id = [0, 0, 0, 7]  # а кто-то поверил...

    butt_indent = 20  # отступ от кнопок
    y_indent = 50  # отступ от верхнего края экрана
    menuWin = MenuDisplay(screen.get_size(), menu_id, images['button1'], t=y_indent, indent=butt_indent)
    settingsWin = SettingsDisplay(screen.get_size(), settingsDict, images['button1'], t=y_indent, indent=butt_indent)
    loadWin = MenuDisplay(screen.get_size(), load_id, images['button1'], t=y_indent, indent=butt_indent)

    screens_dict = {'menuWin': menuWin,
                    'settingsWin': settingsWin,
                    'loadWin': loadWin}
    draw_screen = 'menuWin'

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                id = screens_dict[draw_screen].click_id(event)
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

        screens_dict[draw_screen].render(screen, language=language)
        pygame.display.flip()
        clock.tick(FPS)


def main():
    is_return = False  # если нужно вернуться
    # данные игры
    board = Map(16, 16, screenBoards=size)
    board.load_map('data/maps/main_map.txt', size)
    interface = Interface(size, board.cell_size, language=language)
    hero1 = Hero(board.board, 0, 7, is_in_circle=True)
    character = Character(size, hero_link=hero1)
    mouseManager = MouseManager(screen, interface, board, character)
    keyManager = KeyBoardManager(screen, interface, board, character)
    # основной цикл
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                keyManager.manage_keydown(event)
            elif event.type == pygame.KEYUP:
                keyManager.manage_keyup(event)
            if event.type == pygame.MOUSEWHEEL:  # если мышь крутится
                mouseManager.manage_wheel(event)
            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                message = mouseManager.manage_click(event)
                if message == "return":
                    is_return = True
                    running = False
            elif event.type == pygame.MOUSEMOTION:
                mouseManager.manage_motion(event)
        screen.fill('black')
        board.render(screen)
        interface.render(screen)
        if character.is_open:
            character.render(screen, language=language)
        pygame.display.flip()
        clock.tick(FPS)
    if is_return:
        if start_screen(screen, FPS):
            main()


if start_screen(screen, FPS):
    main()
pygame.quit()
