import pygame
from random import *


def main():
    pygame.init()
    clock = pygame.time.Clock()
    fps = 60
    size = 900, 900
    XP_band = 120
    XP_Hero = 120
    Action = False
    end = False
    item_col = 0
    Band_scare = 'None'
    Band_talk = 'None'
    heal = 40
    dop_attack = 0
    mercy = 0
    font = pygame.font.Font('freesansbold.ttf', 20)
    font_small = pygame.font.Font('freesansbold.ttf', 30)
    screen = pygame.display.set_mode(size)
    words = '* Банда появляется!'

    button_attack = pygame.Rect(20, 800, 160, 50)
    button_action = pygame.Rect(245, 800, 160, 50)
    button_item = pygame.Rect(470, 800, 160, 50)
    button_mercy = pygame.Rect(695, 800, 160, 50)
    button_talk = pygame.Rect(650, 500, 120, 100)
    button_threat = pygame.Rect(80, 500, 120, 100)

    Action_rect = pygame.Rect(20, 500, 870, 150)

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
                elif button_item.collidepoint(mouse_pos) and not Action and item_col < 5:
                    item_col += 1
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
                #кнопка пощады
                elif button_mercy.collidepoint(mouse_pos) and not Action:
                    if mercy >= 4:
                        end = True
                        words = 'Банда вас отпускает.)) Вы победили!)'
                        text = font_small.render(words, True, 'white')
                        textRect = text.get_rect()
                        textRect.center = Action_rect.center
                        screen.blit(text, textRect)
                        pygame.draw.rect(screen, 'white', Action_rect, 1)
                        Band_talk = 'None'
                    else:
                        words = 'Ничего не произошло.'
                        text = font_small.render(words, True, 'white')
                        textRect = text.get_rect()
                        textRect.center = Action_rect.center
                        screen.blit(text, textRect)
                        pygame.draw.rect(screen, 'white', Action_rect, 1)
                        Band_talk = 'None'
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
            #button_threat = pygame.Rect(80, 500, 120, 100)
            text = font.render('* Угрожать', True, 'white')
            textRect = text.get_rect()
            textRect.center = button_threat.center
            screen.blit(text, textRect)
            pygame.draw.rect(screen, 'black', button_threat, 1)

            #button_talk = pygame.Rect(650, 500, 120, 100)
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
                if mercy != 4:
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

        if item_col < 5:
            text = font.render('Предметы', True, 'yellow')
            textRect = text.get_rect()
            textRect.center = button_item.center
            screen.blit(text, textRect)
            pygame.draw.rect(screen, 'yellow', button_item, 1)
        else:
            text = font.render('Предметы', True, 'white')
            textRect = text.get_rect()
            textRect.center = button_item.center
            screen.blit(text, textRect)
            pygame.draw.rect(screen, 'white', button_item, 1)

        if mercy < 4:
            text = font.render('Пощада', True, 'white')
            textRect = text.get_rect()
            textRect.center = button_mercy.center
            screen.blit(text, textRect)
            pygame.draw.rect(screen, 'white', button_mercy, 1)
        else:
            text = font.render('Пощада', True, 'yellow')
            textRect = text.get_rect()
            textRect.center = button_mercy.center
            screen.blit(text, textRect)
            pygame.draw.rect(screen, 'yellow', button_mercy, 1)

        # XP главного героя
        XP_Hero_rect = pygame.Rect(500, 700, 120, 50)
        XP_str = pygame.Rect(640, 700, 120, 50)
        pygame.draw.rect(screen, 'black', XP_Hero_rect)
        text = font.render(str(XP_Hero) + '/120', True, 'white')
        textRect = text.get_rect()
        textRect.center = XP_str.center
        screen.blit(text, textRect)

        pygame.draw.rect(screen, 'red', XP_Hero_rect)

        pygame.draw.rect(screen, 'yellow', (500, 700, XP_Hero, 50))

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
