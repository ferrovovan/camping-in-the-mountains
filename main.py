from Classis import *

pygame.init()
pygame.display.set_caption('Поход по горам')

settingsDict = {}
with open('settings.txt', 'r') as settings:
    for line in settings:
        x = line[:-1].split(' = ')
        settingsDict[x[0]] = x[1]
for key in settingsDict.keys():
    if key == 'FPS':
        FPS = int(settingsDict[key])
    elif key == 'language':
        language = settingsDict[key]
    elif key == 'display':
        size = tuple(map(int, settingsDict[key].split(', ')))

screen = pygame.display.set_mode(size)


def start_screen(screen, FPS):
    screen.fill([255, 255, 255])
    menuIm = load_image('gfx/textures/interface/fone.png')
    screen.blit(menuIm, menuIm.get_rect())
    clock = pygame.time.Clock()

    images = {'button1': load_image('gfx/buttons/button1.png')}

    menu_id = [1, 2, 3, 4]  # id кнопок меню
    settings_id = [8, 8, 9, 9, 7]  # id кнопок настроек
    load_id = [0, 0, 0, 7]  # а кто-то поверил...

    butt_indent = 20  # отступ от кнопок
    y_indent = 50  # отступ от верхнего края экрана
    menuWin = SomeDisplay(screen.get_size(), menu_id, images['button1'], t=y_indent, indent=butt_indent)
    settingsWin = SomeDisplay(screen.get_size(), settings_id, images['button1'], t=y_indent, indent=butt_indent)
    loadWin = SomeDisplay(screen.get_size(), load_id, images['button1'], t=y_indent, indent=butt_indent)

    # расставляем кнопки в меню настроек
    r = 0
    for button in settingsWin.spriteGroup:
        if button.id == 8 and r == 0:  # <-
            r = 1
            button.special_id = 1
            settingsWin.reset_button(8, sp_id=1, new_size=(40, 40),
                                     new_coords=(butt_indent + 100, 20))
        elif button.id == 8 and r == 1:  # <-
            r = 0
            button.special_id = 2
            settingsWin.reset_button(8, sp_id=2, new_size=(40, 40),
                                     new_coords=(butt_indent + 100, 80))
        elif button.id == 9 and r == 0:  # ->
            r = 1
            button.special_id = 1
            settingsWin.reset_button(9, sp_id=1, new_size=(40, 40),
                                     new_coords=(butt_indent + 160, 80))
        elif button.id == 9 and r == 1:  # ->
            button.special_id = 2
            settingsWin.reset_button(9, sp_id=2, new_size=(40, 40),
                                     new_coords=(butt_indent + 160, 20))
        else:
            pass

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
                    # готово
                    if id == 1:  # играть
                        return True
                    elif id == 2:  # загрузить
                        draw_screen = 'loadWin'
                    elif id == 3:  # настройки
                        draw_screen = 'settingsWin'
                    # готово
                    elif id == 4:  # выход
                        pygame.quit()
                        exit()
                    elif id == 7:  # назад
                        draw_screen = 'menuWin'

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
    character = Character()
    mouseManager = MouseManager(screen, interface, board, character)
    # основной цикл
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                kPressed = pygame.key.get_pressed()  # нажатые кнопки
                if kPressed[pygame.K_ESCAPE]:
                    running = False
                if kPressed[pygame.K_UP]:
                    board.move(y=-10)
                if kPressed[pygame.K_DOWN]:
                    board.move(y=10)
                if kPressed[pygame.K_RIGHT]:
                    board.move(x=10)
                if kPressed[pygame.K_LEFT]:
                    board.move(x=-10)
                if kPressed[pygame.K_w]:
                    hero1.move((1, 0))
                elif kPressed[pygame.K_s]:
                    hero1.move((-1, 0))
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
        pygame.display.flip()
        clock.tick(FPS)
    if is_return:
        if start_screen(screen, FPS):
            main()


if start_screen(screen, FPS):
    main()
pygame.quit()
