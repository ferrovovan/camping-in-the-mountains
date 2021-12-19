import pygame
from Classis import Button


def start_screen(screen, FPS):
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    screen.fill('blue')
    font = pygame.font.Font(None, 30)
    text_coord = 50
    clock = pygame.time.Clock()
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    button_sprites = pygame.sprite.Group()
    scr_size = screen.get_size()
    butt_width = 120
    butt_height = 60
    n = 4
    for i in range(1, n + 1):
        Button(button_sprites, scr_size[0] // 2, scr_size[1] // 2 + int((n // 2 - i) * butt_width * 0.75), butt_width,
               butt_height, '', id=i)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return True
        button_sprites.draw(screen)
        #        button_sprites.draw_text(screen)
        pygame.display.flip()
        clock.tick(FPS)
