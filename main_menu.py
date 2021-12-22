import pygame
from Classis import Button


def start_screen(screen, FPS):
    screen.fill('blue')
    clock = pygame.time.Clock()

    button_sprites = pygame.sprite.Group()
    scr_size = screen.get_size()
    butt_width = 300
    butt_height = 100
    x = [4, 3, 6, 1]
    n = 4
    for i in range(1, n + 1):
        Button(button_sprites, scr_size[0] // 2 - butt_width // 2,
               scr_size[1] // 2 + int((n // 2 - i) * butt_height * 1.2) + int(butt_height * 3 / n),
               butt_width, butt_height, id=n - i + 1)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for butt in button_sprites:
                    if butt.is_click(event):
                        return True
        button_sprites.draw(screen)
        for butt in button_sprites:
            butt.draw_text(screen)
        pygame.display.flip()
        clock.tick(FPS)
