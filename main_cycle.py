import pygame
from Classis import Map, Hero, Interface, MouseManager, Character
from main_menu import start_screen

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
