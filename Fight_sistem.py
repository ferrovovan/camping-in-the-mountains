import pygame
from random import *


def main():
    pygame.init()
    clock = pygame.time.Clock()
    fps = 60
    size = 500, 500
    XP_band = 120
    XP_Hero = 120
    turn = False
    font = pygame.font.Font('freesansbold.ttf', 22)
    screen = pygame.display.set_mode(size)

    button_attack = pygame.Rect(10, 430, 120, 50)
    button_action = pygame.Rect(190, 430, 120, 50)
    button_item = pygame.Rect(370, 430, 120, 50)

    while True:
        Your_hit = randint(0, 40)
        Band_hit = randint(0, 30)
        heal = 40
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if button_attack.collidepoint(mouse_pos):
                    if XP_Hero - Band_hit <= 0:
                        XP_Hero = 0
                    else:
                        XP_Hero -= Band_hit
                        XP_band -= Your_hit
                    if XP_band - Your_hit <= 0:
                        XP_band = 0

                elif button_action.collidepoint(mouse_pos):
                    print('Кнопка действия нажата!!!')
                elif button_item.collidepoint(mouse_pos):
                    if XP_Hero + heal >= 120:
                        XP_Hero = 120
                        XP_Hero -= Band_hit
                    else:
                        XP_Hero += heal
                        XP_Hero -= Band_hit
                    if XP_band < 120:
                        XP_band += 1
        screen.fill('black')

        text = font.render('Атака', True, 'yellow')
        textRect = text.get_rect()
        textRect.center = button_attack.center
        screen.blit(text, textRect)
        pygame.draw.rect(screen, 'yellow', button_attack, 1)

        text = font.render('Действие', True, 'yellow')
        textRect = text.get_rect()
        textRect.center = button_action.center
        screen.blit(text, textRect)
        pygame.draw.rect(screen, 'yellow', button_action, 1)

        text = font.render('Предметы', True, 'yellow')
        textRect = text.get_rect()
        textRect.center = button_item.center
        screen.blit(text, textRect)
        pygame.draw.rect(screen, 'yellow', button_item, 1)

        #XP главного героя
        XP_Hero_rect = pygame.Rect(10, 10, 120, 50)

        XP_str = pygame.Rect(10, 60, 120, 50)
        pygame.draw.rect(screen, 'black', XP_Hero_rect)
        text = font.render(str(XP_Hero) + '/120', True, 'white')
        textRect = text.get_rect()
        textRect.center = XP_str.center
        screen.blit(text, textRect)

        pygame.draw.rect(screen, 'red', XP_Hero_rect)

        pygame.draw.rect(screen, 'yellow', (10, 10, XP_Hero, 50))

        #XP банды
        XP_band_rect = pygame.Rect(340, 10, 120, 50)

        XP_str = pygame.Rect(340, 60, 120, 50)
        pygame.draw.rect(screen, 'black', XP_band_rect)
        text = font.render(str(XP_band) + '/120', True, 'white')
        textRect = text.get_rect()
        textRect.center = XP_str.center
        screen.blit(text, textRect)

        pygame.draw.rect(screen, 'red', XP_band_rect)

        pygame.draw.rect(screen, 'yellow', (340, 10, XP_band, 50))

        pygame.display.update()
        clock.tick(fps)


pygame.quit()

if __name__ == '__main__':
    main()
