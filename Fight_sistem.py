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
    end = False
    Band_scare = 'None'
    Band_talk = 'None'
    heal = 40
    dop_attack = 0
    mercy = 0
    font = pygame.font.Font('freesansbold.ttf', 22)
    font_small = pygame.font.Font('freesansbold.ttf', 18)
    screen = pygame.display.set_mode(size)
    words = '* Банда появляется!'

    button_attack = pygame.Rect(10, 430, 120, 50)
    button_action = pygame.Rect(190, 430, 120, 50)
    button_item = pygame.Rect(370, 430, 120, 50)

    Action_rect = pygame.Rect(10, 300, 480, 100)

    while True:
        if mercy <= 1:
            Your_hit = randint(10, 40)
            Band_hit = randint(11, 30) + dop_attack
        else:
            dop_attack = 0
            Your_hit = randint(10, 40)
            Band_hit = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN and not end:
                mouse_pos = event.pos
                #кнопка атаки
                if button_attack.collidepoint(mouse_pos) and not Action:
                    mercy = 0
                    words = '* Банда ждёт ваших действий!'
                    Band_scare = False
                    if XP_Hero - (Band_hit + dop_attack) <= 0:
                        XP_Hero = 0
                        words = 'Вы погибли!'
                        end = True
                    elif XP_band - Your_hit <= 0:
                        XP_band = 0
                        words = 'Вы победили!'
                        end = True
                    else:
                        if abs(dop_attack) < Band_hit:
                            XP_Hero -= Band_hit + dop_attack
                            XP_band -= Your_hit
                    dop_attack = 0
                #кнопка действия
                elif button_action.collidepoint(mouse_pos) and not Action:
                    if XP_Hero - (Band_hit + dop_attack) <= 0:
                        XP_Hero = 0
                        words = 'Вы погибли!'
                        end = True
                    else:
                        XP_Hero -= Band_hit + dop_attack
                        words = ''
                    dop_attack = 0
                    Action = True
                #кнопка предмета
                elif button_item.collidepoint(mouse_pos) and not Action:
                    words = '* Банда ждёт ваших действий!'
                    if dop_attack < 0:
                        dop_attack = 0
                    Band_scare = False
                    if XP_Hero + heal >= 120:
                        XP_Hero = 120
                        XP_Hero -= Band_hit + dop_attack
                    else:
                        XP_Hero += heal
                        if abs(dop_attack) < Band_hit:
                            XP_Hero -= Band_hit + dop_attack
                    if XP_band < 120:
                        XP_band += 1
                    dop_attack = 0
                #кнопка угрозы
                elif button_threat.collidepoint(mouse_pos):
                    mercy = 0
                    chance = randint(0, 100)
                    if chance >= 60:
                        Band_scare = 'good'
                    else:
                        Band_scare = 'refuse'
                    Action = False
                #кнопка разговора
                elif button_talk.collidepoint(mouse_pos):
                    chance = randint(0, 100)
                    if chance >= 20:
                        Band_talk = 'good'
                    else:
                        Band_talk = 'refuse'
                    Action = False
        screen.fill('black')
        #механника действий
        if Action and not end:
            button_threat = pygame.Rect(20, 300, 120, 100)
            text = font.render('* Угрожать', True, 'white')
            textRect = text.get_rect()
            textRect.center = button_threat.center
            screen.blit(text, textRect)
            pygame.draw.rect(screen, 'black', button_threat, 1)

            button_talk = pygame.Rect(300, 300, 120, 100)
            text = font.render('* Поговорить', True, 'white')
            textRect = text.get_rect()
            textRect.center = button_talk.center
            screen.blit(text, textRect)
            pygame.draw.rect(screen, 'black', button_talk, 1)

            text = font.render('', True, 'white')
            textRect = text.get_rect()
            textRect.center = Action_rect.center
            screen.blit(text, textRect)
            pygame.draw.rect(screen, 'white', Action_rect, 1)
        else:
            #угрожать
            if Band_scare == 'good':
                dop_attack = -10
                words = 'Банда в испуге! -10 к атаке банды'
                text = font.render(words, True, 'white')
                textRect = text.get_rect()
                textRect.center = Action_rect.center
                screen.blit(text, textRect)
                pygame.draw.rect(screen, 'white', Action_rect, 1)
                Band_scare = 'None'
            elif Band_scare == 'refuse':
                dop_attack = 10
                words = 'Банда посмеялась над вами! +10 к атаке банды'
                text = font_small.render(words, True, 'white')
                textRect = text.get_rect()
                textRect.center = Action_rect.center
                screen.blit(text, textRect)
                pygame.draw.rect(screen, 'white', Action_rect, 1)
                Band_scare = 'None'
            #поговорить
            elif Band_talk == 'refuse':
                dop_attack = 5
                words = 'Банда не хочет с вами говорить. +5 к атаке банды'
                text = font_small.render(words, True, 'white')
                textRect = text.get_rect()
                textRect.center = Action_rect.center
                screen.blit(text, textRect)
                pygame.draw.rect(screen, 'white', Action_rect, 1)
                Band_scare = 'None'
            elif Band_talk == 'good':
                mercy += 1
                if mercy == 4:
                    end = True
                    words = 'Банда вас отпускает.)) Вы победили!)'
                    text = font_small.render(words, True, 'white')
                    textRect = text.get_rect()
                    textRect.center = Action_rect.center
                    screen.blit(text, textRect)
                    pygame.draw.rect(screen, 'white', Action_rect, 1)
                    Band_talk = 'None'
                else:
                    words = 'Вы хорошо побеседовали с бандой.))'
                    text = font_small.render(words, True, 'white')
                    textRect = text.get_rect()
                    textRect.center = Action_rect.center
                    screen.blit(text, textRect)
                    pygame.draw.rect(screen, 'white', Action_rect, 1)
                    Band_talk = 'None'
            Action = False

        text = font_small.render(words, True, 'white')
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

        # XP главного героя
        XP_Hero_rect = pygame.Rect(10, 10, 120, 50)

        XP_str = pygame.Rect(10, 60, 120, 50)
        pygame.draw.rect(screen, 'black', XP_Hero_rect)
        text = font.render(str(XP_Hero) + '/120', True, 'white')
        textRect = text.get_rect()
        textRect.center = XP_str.center
        screen.blit(text, textRect)

        pygame.draw.rect(screen, 'red', XP_Hero_rect)

        pygame.draw.rect(screen, 'yellow', (10, 10, XP_Hero, 50))

        # XP банды
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
