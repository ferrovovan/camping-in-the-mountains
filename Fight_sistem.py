import pygame
from random import *


def main():
    pygame.init()
    clock = pygame.time.Clock()
    fps = 60
    size = 900, 900
    XP_band = 200
    XP_Hero = 200
    Action = False
    end = False
    Band_scare = 'None'
    Band_talk = 'None'
    dop_attack = 0
    mercy = 0
    Item = False
    items = ['Аптечка', 'Бутерброд', 'Бинт', 'Антибиотик', 'Обезболивающее', 'Консервы']
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
    button_restart = pygame.Rect(10, 10, 20, 20)
    button_id_1 = pygame.Rect(80, 480, 120, 100)
    button_id_2 = pygame.Rect(80, 540, 120, 100)

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
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                # кнопка атаки
                if button_attack.collidepoint(mouse_pos) and not Action and not Item and not end:
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
                #кнопка перезапуска. Она только для проверки
                elif button_restart.collidepoint(mouse_pos):
                    words = '* Банда появляется!'
                    XP_band = 200
                    XP_Hero = 200
                    Action = False
                    end = False
                    Band_scare = 'None'
                    Band_talk = 'None'
                    dop_attack = 0
                    mercy = 0
                    Item = False
                    items = ['Аптечка', 'Бутерброд', 'Бинт', 'Антибиотик', 'Обезболивающее', 'Консервы']
                # кнопка действия
                elif button_action.collidepoint(mouse_pos) and not Action and not Item and not end:
                    if XP_Hero - (Band_hit + dop_attack) <= 0:
                        XP_Hero = 0
                        words = 'Вы погибли!'
                        end = True
                    else:
                        XP_Hero -= Band_hit + dop_attack
                        words = ''
                    dop_attack = 0
                    Action = True
                # кнопка предмета
                elif button_item.collidepoint(mouse_pos) and not Action and not Item and not end:
                    Item = True
                    words = ''
                    if dop_attack < 0:
                        dop_attack = 0
                    Band_scare = False
                    if XP_band < 120:
                        XP_band += 1
                    dop_attack = 0
                # кнопка пощады
                elif button_mercy.collidepoint(mouse_pos) and not Action and not Item and not end:
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
                # кнопка угрозы
                elif button_threat.collidepoint(mouse_pos) and Action:
                    mercy = 0
                    chance = randint(0, 100)
                    if chance >= 60:
                        Band_scare = 'good'
                    else:
                        Band_scare = 'refuse'
                    Action = False
                # кнопка разговора
                elif button_talk.collidepoint(mouse_pos) and Action:
                    chance = randint(0, 100)
                    if chance >= 20:
                        Band_talk = 'good'
                    else:
                        Band_talk = 'refuse'
                    Action = False
                elif button_id_1.collidepoint(mouse_pos) and Item and items[0] != 'Пусто':
                    items[0] = 'Пусто'
                    if XP_Hero + 70 >= 120:
                        XP_Hero = 120
                        XP_Hero -= Band_hit + dop_attack
                    else:
                        XP_Hero += 70
                        if abs(dop_attack) < Band_hit:
                            XP_Hero -= Band_hit + dop_attack
                    Item = False
                    words = 'Банда ждёт ваших действий'
                elif button_id_2.collidepoint(mouse_pos) and Item and items[1] != 'Пусто':
                    items[1] = 'Пусто'
                    if XP_Hero + 50 >= 120:
                        XP_Hero = 120
                        XP_Hero -= Band_hit + dop_attack
                    else:
                        XP_Hero += 50
                        if abs(dop_attack) < Band_hit:
                            XP_Hero -= Band_hit + dop_attack
                    Item = False
                    words = 'Банда ждёт ваших действий'

        screen.fill('black')
        # механника действий
        if Action and not end:
            text = font.render('* Угрожать', True, 'white')
            textRect = text.get_rect()
            textRect.center = button_threat.center
            screen.blit(text, textRect)
            pygame.draw.rect(screen, 'black', button_threat, 1)

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
            # угрожать
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
            # поговорить
            elif Band_talk == 'refuse':
                dop_attack = 5
                words = 'Банда не хочет с вами говорить. +5 к атаке банды'
                Band_scare = 'None'
            elif Band_talk == 'good':
                mercy += 1
                if mercy != 3:
                    words = 'Вы хорошо побеседовали с бандой.))'
                    Band_talk = 'None'
            Action = False
        # механника предметов
        if Item and not end:
            text = font.render('*' + items[0], True, 'white')
            textRect = text.get_rect()
            textRect.center = button_id_1.center
            screen.blit(text, textRect)
            pygame.draw.rect(screen, 'black', button_id_1, 1)

            text = font.render('*' + items[1], True, 'white')
            textRect = text.get_rect()
            textRect.center = button_id_2.center
            screen.blit(text, textRect)
            pygame.draw.rect(screen, 'black', button_id_2, 1)

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

        if mercy < 3:
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
        XP_Hero_rect = pygame.Rect(500, 700, 200, 50)
        XP_str = pygame.Rect(650, 700, 200, 50)
        pygame.draw.rect(screen, 'black', XP_Hero_rect)
        text = font.render(str(XP_Hero) + '/200', True, 'white')
        textRect = text.get_rect()
        textRect.center = XP_str.center
        screen.blit(text, textRect)

        pygame.draw.rect(screen, 'red', XP_Hero_rect)

        pygame.draw.rect(screen, 'yellow', (500, 700, XP_Hero, 50))

        # XP банды
        XP_band_rect = pygame.Rect(340, 10, 200, 50)

        XP_str = pygame.Rect(340, 60, 200, 50)
        pygame.draw.rect(screen, 'black', XP_band_rect)
        text = font.render(str(XP_band) + '/200', True, 'white')
        textRect = text.get_rect()
        textRect.center = XP_str.center
        screen.blit(text, textRect)

        pygame.draw.rect(screen, 'red', XP_band_rect)

        pygame.draw.rect(screen, 'yellow', (340, 10, XP_band, 50))

        text = font.render('R', True, 'red')
        textRect = text.get_rect()
        textRect.center = button_restart.center
        screen.blit(text, textRect)
        pygame.draw.rect(screen, 'blue', button_restart, 1)

        pygame.display.update()
        clock.tick(fps)


pygame.quit()

if __name__ == '__main__':
    main()
