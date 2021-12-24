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

    button_sprites = ButtonGroup()
    scr_size = screen.get_size()
    butt_width = 300
    butt_height = 100
    x = [4, 3, 6, 1]
    n = 4
    t = int(butt_height * 3 / n)
    for i in range(1, n + 1):
        Button(button_sprites, scr_size[0] // 2 - butt_width // 2,
               scr_size[1] // 2 + int((n // 2 - i) * butt_height * 1.2) + t,
               butt_width, butt_height, id=x[i - 1], image=images['button1'])

    indent = 20  # отступ
    menuWindow = SomeDisplay((butt_width + indent * 2,
                              2 * (n // 2 * butt_height * 1.2 + indent) - butt_height * 0.2),
                             button_sprites,
                             coords=(scr_size[0] // 2 - (butt_width // 2 + indent),
                                     scr_size[1] // 2 - (n // 2 * butt_height * 1.2 - t + indent)))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                id = button_sprites.click_id(event)
                if id is not None:
                    # готово
                    if id == 1:
                        return True
                    elif id == 3:
                        pass
                    # готово
                    elif id == 4:
                        pygame.quit()
                        exit()
                    elif id == 6:
                        pass

#        button_sprites.draw(screen)
        button_sprites.draw_text(screen)
        menuWindow.render(screen)
        pygame.display.flip()
        clock.tick(FPS)


def main():
    is_return = False  # если нужно вернуться
    # данные игры
    board = Map(16, 16, screenBoards=size)
    board.load_map('data/maps/main_map.txt', size)
    interface = Interface(size, board.cell_size)
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
