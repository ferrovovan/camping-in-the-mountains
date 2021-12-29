import pygame
from random import *


def main():
    pygame.init()
    clock = pygame.time.Clock()
    fps = 60
    size = 500, 500
    XP_band = 120
    XP_Hero = 120
    Action = False
    font = pygame.font.Font('freesansbold.ttf', 22)
    screen = pygame.display.set_mode(size)
    words = '* Банда появляется!'

    button_attack = pygame.Rect(10, 430, 120, 50)
    button_action = pygame.Rect(190, 430, 120, 50)
    button_item = pygame.Rect(370, 430, 120, 50)

    Action_rect = pygame.Rect(10, 300, 480, 100)

    while True:
        Band_scare = False
        Your_hit = randint(5, 40)
        Band_hit = randint(5, 30)
        heal = 40
        end = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN and not end:
                mouse_pos = event.pos
                if button_attack.collidepoint(mouse_pos) and not Action:
                    words = '* Банда появляется!'
                    Band_scare = False
                    if XP_Hero - Band_hit <= 0:
                        XP_Hero = 0
                        words = 'Вы погибли!'
                        end = True
                    else:
                        XP_Hero -= Band_hit
                        XP_band -= Your_hit
                    if XP_band - Your_hit <= 0:
                        XP_band = 0
                        words = 'Вы победили!'
                        end = True
                elif button_action.collidepoint(mouse_pos):
                    words = ''
                    Action = True
                elif button_item.collidepoint(mouse_pos) and not Action:
                    words = '* Банда появляется!'
                    Band_scare = False
                    if XP_Hero + heal >= 120:
                        XP_Hero = 120
                        XP_Hero -= Band_hit
                    else:
                        XP_Hero += heal
                        XP_Hero -= Band_hit
                    if XP_band < 120:
                        XP_band += 1
                elif button_1.collidepoint(mouse_pos):
                    Band_scare = True
                    Action = False
        screen.fill('black')
        if Action:
            button_1 = pygame.Rect(20, 300, 120, 100)
            text = font.render('* Угрожать', True, 'white')
            textRect = text.get_rect()
            textRect.center = button_1.center
            screen.blit(text, textRect)
            pygame.draw.rect(screen, 'black', button_1, 1)

            button_2 = pygame.Rect(300, 300, 120, 100)
            text = font.render('* Поговорить', True, 'white')
            textRect = text.get_rect()
            textRect.center = button_2.center
            screen.blit(text, textRect)
            pygame.draw.rect(screen, 'black', button_2, 1)

            text = font.render('', True, 'white')
            textRect = text.get_rect()
            textRect.center = Action_rect.center
            screen.blit(text, textRect)
            pygame.draw.rect(screen, 'white', Action_rect, 1)
        else:
            if Band_scare:
                if XP_band - Your_hit <= 0:
                    XP_band = 0
                    words = 'Вы победили!'
                    end = True
                else:
                    XP_band -= 20
                    words = 'Банда в испуге! -20XP банды'
                    text = font.render(words, True, 'white')
                    textRect = text.get_rect()
                    textRect.center = Action_rect.center
                    screen.blit(text, textRect)
                    pygame.draw.rect(screen, 'white', Action_rect, 1)

        text = font.render(words, True, 'white')
        textRect = text.get_rect()
        textRect.center = Action_rect.center
        screen.blit(text, textRect)
        pygame.draw.rect(screen, 'white', Action_rect, 1)

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
