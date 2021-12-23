import pygame
from Classis import Button, load_image, ButtonGroup


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
    for i in range(1, n + 1):
        Button(button_sprites, scr_size[0] // 2 - butt_width // 2,
               scr_size[1] // 2 + int((n // 2 - i) * butt_height * 1.2) + int(butt_height * 3 / n),
               butt_width, butt_height, id=x[i - 1], image=images['button1'])

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

        button_sprites.draw(screen)
        button_sprites.draw_text(screen)
        pygame.display.flip()
        clock.tick(FPS)
