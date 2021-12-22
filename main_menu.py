import pygame
from Classis import Button, load_image, ButtonGroup


def start_screen(screen, FPS):
    screen.fill([255, 255, 255])
    menuIm = load_image('gfx/textures/interface/fone.png')
    screen.blit(menuIm, menuIm.get_rect())
    clock = pygame.time.Clock()

    button_sprites = ButtonGroup()
    scr_size = screen.get_size()
    butt_width = 300
    butt_height = 100
    x = [4, 3, 6, 1]
    n = 4
    for i in range(1, n + 1):
        Button(button_sprites, scr_size[0] // 2 - butt_width // 2,
               scr_size[1] // 2 + int((n // 2 - i) * butt_height * 1.2) + int(butt_height * 3 / n),
               butt_width, butt_height, id=x[i - 1])

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for butt in button_sprites:
                    if butt.is_click(event):
                        if butt.id == 1:
                            return True
                        elif butt.id == 4:
                            pygame.quit()
                            exit()

        button_sprites.draw(screen)
        button_sprites.draw_text(screen)
        pygame.display.flip()
        clock.tick(FPS)
