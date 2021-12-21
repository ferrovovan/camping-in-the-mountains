import pygame
from Classis import Map, Hero, Interface, MouseManager, Character
from menu import start_screen

pygame.init()
pygame.display.set_caption('Поход по горам')
a = 900
size = a, a
screen = pygame.display.set_mode(size)
FPS = 60


def main():
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
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                mouseManager.manage_click(event)
            if event.type == pygame.MOUSEMOTION:
                mouseManager.manage_motion(event)
            if event.type == pygame.MOUSEWHEEL:  # если мышь крутится
                mouseManager.manage_wheel(event)
        screen.fill('black')
        board.render(screen)
        interface.render(screen)
        pygame.display.flip()
        clock.tick(FPS)


if start_screen(screen, FPS):
    main()
pygame.quit()
