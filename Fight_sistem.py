import pygame
import random
from os import path
from random import randint


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (20, 20))
        self.image.set_colorkey('black')
        self.rect = self.image.get_rect()
        self.radius = 9
        # pygame.draw.circle(self.image, 'red', self.rect.center, self.radius)
        self.rect.centerx = 425
        self.rect.bottom = 545
        self.speedx = 0
        self.speedy = 0

    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a]:
            self.speedx = -3
        if keystate[pygame.K_d]:
            self.speedx = 3
        if keystate[pygame.K_s]:
            self.speedy = 3
        if keystate[pygame.K_w]:
            self.speedy = -3
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right > 550:
            self.rect.right = 550
        if self.rect.left < 300:
            self.rect.left = 300
        if self.rect.top < 400:
            self.rect.top = 400
        if self.rect.bottom > 650:
            self.rect.bottom = 650


class Enemy_attacks(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = meteor_img
        self.image.set_colorkey('black')
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        # pygame.draw.circle(self.image, 'red', self.rect.center, self.radius)
        self.rect.x = randint(300, 500)
        self.rect.y = 400
        self.speedy = random.randrange(1, 4)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > 650 + 10 or self.rect.left < -25 or self.rect.right > 650 + 20:
            self.rect.x = randint(300, 500)# random.randrange(1000 - self.rect.width)
            self.rect.y = 400
            self.speedy = random.randrange(1, 4)


def main():
    global Victory
    pygame.init()
    pygame.mixer.init()
    img_dir = path.join(path.dirname(__file__), 'img')
    clock = pygame.time.Clock()
    FPS = 60
    size = 900, 900
    screen = pygame.display.set_mode(size)
    XP_band = 200
    XP_Hero = 200
    Action = False
    end = False
    Band_scare = 'None'
    Band_talk = 'None'
    dop_attack = 0
    mercy = 0
    v = 50
    v_hit = 100
    time = 0
    time_hit = 0
    time_read = 5
    Item = False
    Mercy = False
    Hit = False
    Analysis = False
    global color
    color = 'red'
    turn = 'player'
    items = ['Аптечка', 'Бутерброд', 'Бинт', 'Антибиотик', 'Обезболивающее', 'Консервы']
    heals = ['70', '50', '30', '60', '100', '10']
    font = pygame.font.Font('freesansbold.ttf', 20)
    font_small = pygame.font.Font('freesansbold.ttf', 27)
    words = '* Банда появляется!'
    enemy_attacks_group = pygame.sprite.Group()

    # задание всех кнопок
    button_attack = pygame.Rect(20, 800, 160, 50)
    button_action = pygame.Rect(245, 800, 160, 50)
    button_item = pygame.Rect(470, 800, 160, 50)
    button_mercy = pygame.Rect(695, 800, 160, 50)
    button_talk = pygame.Rect(650, 510, 140, 60)
    button_threat = pygame.Rect(80, 510, 120, 60)
    button_information = pygame.Rect(80, 580, 120, 60)
    button_restart = pygame.Rect(10, 10, 20, 20)
    button_id_1 = pygame.Rect(80, 480, 100, 80)
    button_id_2 = pygame.Rect(80, 540, 100, 80)
    button_id_3 = pygame.Rect(300, 480, 100, 80)
    button_id_4 = pygame.Rect(300, 540, 100, 80)
    button_id_5 = pygame.Rect(520, 480, 100, 80)
    button_id_6 = pygame.Rect(520, 540, 100, 80)
    Action_rect = pygame.Rect(20, 500, 870, 150)
    Fight_rect = pygame.Rect(300, 400, 250, 250)
    global player_img
    global meteor_img
    player_img = pygame.image.load(path.join("heard.jpg")).convert()
    meteor_img = pygame.image.load(path.join("Enemy_fire.jpg")).convert()

    all_sprites = pygame.sprite.Group()
    attacks = pygame.sprite.Group()
    player = Player()
    all_sprites.add(player)
    for i in range(5):
        attack = Enemy_attacks()
        all_sprites.add(attack)
        attacks.add(attack)

    while True:
        # if end and XP_Hero > 0:
        # Victory = True
        # return False
        # elif end and XP_Hero == 0:
        # return False
        screen.fill('black')
        # проверка на милосердие
        if mercy <= 1:
            Your_hit = randint(30, 70)
            Band_hit = randint(11, 30) + dop_attack
        else:
            dop_attack = 0
            Your_hit = randint(30, 70)
            Band_hit = 0

        # проверка на события
        for event in pygame.event.get():

            # события, если ход игрока
            if turn == 'player':
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        Mercy = False
                        Action = False
                        Item = False
                        words = '* Банда ждёт ваших действий!'
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    # кнопка атаки
                    if button_attack.collidepoint(mouse_pos) and not Action and not Item and not end:
                        mercy = 0
                        Band_scare = False
                        words = '* Банда ждёт ваших действий!'
                        if XP_band - Your_hit <= 0:
                            XP_band = 0
                            words = 'Вы победили!'
                            end = True
                        else:
                            if abs(dop_attack) < Band_hit:
                                turn = 'enemy'
                                XP_band -= Your_hit
                        dop_attack = 0
                    # кнопка перезапуска. Она только для проверки
                    elif button_restart.collidepoint(mouse_pos):
                        pygame.mouse.set_visible(True)
                        time_hit = 0
                        Hit = 0
                        turn = 'player'
                        words = '* Банда появляется!'
                        XP_band = 200
                        XP_Hero = 200
                        Action = False
                        end = False
                        Analysis = False
                        Band_scare = 'None'
                        Band_talk = 'None'
                        dop_attack = 0
                        mercy = 0
                        Item = False
                        items = ['Аптечка', 'Бутерброд', 'Бинт', 'Антибиотик', 'Обезболивающее', 'Консервы']
                        heals = ['70', '50', '30', '60', '100', '10']
                    # кнопка действия
                    elif button_action.collidepoint(mouse_pos) and not Action and not Item and not end:
                        words = ''
                        dop_attack = 0
                        Action = True
                    # кнопка предмета
                    elif button_item.collidepoint(mouse_pos) and not Action and not Item and not end:
                        Item = True
                        words = ''
                        Band_scare = False
                        if XP_band < 200:
                            XP_band += 1
                        dop_attack = 0
                    # кнопка пощады
                    elif button_mercy.collidepoint(mouse_pos) and not Action and not Item and not end:
                        Mercy = True
                        turn = 'enemy'
                    # кнопка угрозы
                    elif button_threat.collidepoint(mouse_pos) and Action:
                        mercy = 0
                        chance = randint(0, 100)
                        if chance >= 60:
                            Band_scare = 'good'
                        else:
                            Band_scare = 'refuse'
                        Action = False
                        turn = 'enemy'
                    # кнопка разговора
                    elif button_talk.collidepoint(mouse_pos) and Action:
                        chance = randint(0, 100)
                        if chance >= 20:
                            Band_talk = 'good'
                        else:
                            Band_talk = 'refuse'
                        Action = False
                        turn = 'enemy'
                    # кнопка анализа
                    elif button_information.collidepoint(mouse_pos) and Action:
                        Analysis = True
                    elif button_id_1.collidepoint(mouse_pos) and Item and items[0] != 'Пусто':
                        items[0] = 'Пусто'
                        heals[0] = ''
                        if XP_Hero + 70 >= 200:
                            XP_Hero = 200
                        else:
                            XP_Hero += 70
                        Item = False
                        words = 'Банда ждёт ваших действий.'
                        turn = 'enemy'
                    elif button_id_2.collidepoint(mouse_pos) and Item and items[1] != 'Пусто':
                        items[1] = 'Пусто'
                        heals[1] = ''
                        if XP_Hero + 50 >= 200:
                            XP_Hero = 200
                        else:
                            XP_Hero += 50
                        Item = False
                        words = 'Банда ждёт ваших действий.'
                        turn = 'enemy'
                    elif button_id_3.collidepoint(mouse_pos) and Item and items[2] != 'Пусто':
                        items[2] = 'Пусто'
                        heals[2] = ''
                        if XP_Hero + 30 >= 200:
                            XP_Hero = 200
                        else:
                            XP_Hero += 30
                        Item = False
                        words = 'Банда ждёт ваших действий.'
                        turn = 'enemy'
                    elif button_id_4.collidepoint(mouse_pos) and Item and items[3] != 'Пусто':
                        items[3] = 'Пусто'
                        heals[3] = ''
                        if XP_Hero + 60 >= 200:
                            XP_Hero = 200
                        else:
                            XP_Hero += 60
                        Item = False
                        words = 'Банда ждёт ваших действий.'
                        turn = 'enemy'
                    elif button_id_5.collidepoint(mouse_pos) and Item and items[4] != 'Пусто':
                        items[4] = 'Пусто'
                        heals[4] = ''
                        if XP_Hero + 100 >= 200:
                            XP_Hero = 200
                        else:
                            XP_Hero += 100
                        Item = False
                        words = 'Банда ждёт ваших действий.'
                        turn = 'enemy'
                    elif button_id_6.collidepoint(mouse_pos) and Item and items[5] != 'Пусто':
                        items[5] = 'Пусто'
                        heals[5] = ''
                        if XP_Hero + 20 >= 200:
                            XP_Hero = 200
                        else:
                            XP_Hero += 20
                        Item = False
                        words = 'Банда ждёт ваших действий.'
                        turn = 'enemy'

            # события, если ход противника
            if turn == 'enemy':
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if button_restart.collidepoint(mouse_pos):
                        pygame.mouse.set_visible(True)
                        turn = 'player'
                        Analysis = False
                        words = '* Банда появляется!'
                        XP_band = 200
                        XP_Hero = 200
                        Action = False
                        end = False
                        time_hit = 0
                        Hit = False
                        Band_scare = 'None'
                        Band_talk = 'None'
                        dop_attack = 0
                        mercy = 0
                        Item = False
                        Mercy = False
                        items = ['Аптечка', 'Бутерброд', 'Бинт', 'Антибиотик', 'Обезболивающее', 'Консервы']
                        heals = ['70', '50', '30', '60', '100', '10']

        # экран, если ход игрока
        if turn == 'player':
            # механника пощады
            if Mercy:
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
                    text = font.render(words, True, 'white')
                    textRect = text.get_rect()
                    textRect.center = Action_rect.center
                    screen.blit(text, textRect)
                    pygame.draw.rect(screen, 'white', Action_rect, 1)
                    Band_talk = 'None'
                    Mercy = False
                    turn = 'enemy'
            # механника действий
            if Action and not end:
                text = font.render('* Угрожать', True, 'white')
                textRect = text.get_rect()
                textRect.center = button_threat.center
                screen.blit(text, textRect)
                pygame.draw.rect(screen, 'white', button_threat, 1)

                text = font.render('* Поговорить', True, 'white')
                textRect = text.get_rect()
                textRect.center = button_talk.center
                screen.blit(text, textRect)
                pygame.draw.rect(screen, 'white', button_talk, 1)

                text = font.render('* Анализ', True, 'white')
                textRect = text.get_rect()
                textRect.center = button_information.center
                screen.blit(text, textRect)
                pygame.draw.rect(screen, 'white', button_information, 1)

                text = font.render('', True, 'white')
                textRect = text.get_rect()
                textRect.center = Action_rect.center
                screen.blit(text, textRect)
                pygame.draw.rect(screen, 'white', Action_rect, 1)
            else:
                # угрожать
                if Band_scare == 'good':
                    dop_attack = -10
                    words = 'Банда в испуге! Атаки банды стали слабее.'
                    text = font.render(words, True, 'white')
                    textRect = text.get_rect()
                    textRect.center = Action_rect.center
                    screen.blit(text, textRect)
                    pygame.draw.rect(screen, 'white', Action_rect, 1)
                    Band_scare = 'None'
                elif Band_scare == 'refuse':
                    dop_attack = 10
                    words = 'Банда посмеялась над вами! Атаки банды стали сильнее.'
                    text = font_small.render(words, True, 'white')
                    textRect = text.get_rect()
                    textRect.center = Action_rect.center
                    screen.blit(text, textRect)
                    pygame.draw.rect(screen, 'white', Action_rect, 1)
                    Band_scare = 'None'
                # поговорить
                elif Band_talk == 'refuse':
                    dop_attack = 5
                    words = 'Банда не хочет говорить. Атаки банды стали сильнее.'
                    Band_scare = 'None'
                elif Band_talk == 'good':
                    mercy += 1
                    if mercy != 3:
                        words = 'Вы хорошо побеседовали с бандой.))'
                        Band_talk = 'None'
                Action = False
            # механника предметов
            if Item and not end:
                words = ''
                text = font.render('*' + items[0] + ' ' + heals[0], True, 'white')
                textRect = text.get_rect()
                textRect.center = button_id_1.center
                screen.blit(text, textRect)
                pygame.draw.rect(screen, 'black', button_id_1, 1)

                text = font.render('*' + items[1] + ' ' + heals[1], True, 'white')
                textRect = text.get_rect()
                textRect.center = button_id_2.center
                screen.blit(text, textRect)
                pygame.draw.rect(screen, 'black', button_id_2, 1)

                text = font.render('*' + items[2] + ' ' + heals[2], True, 'white')
                textRect = text.get_rect()
                textRect.center = button_id_3.center
                screen.blit(text, textRect)
                pygame.draw.rect(screen, 'black', button_id_3, 1)

                text = font.render('*' + items[3] + ' ' + heals[3], True, 'white')
                textRect = text.get_rect()
                textRect.center = button_id_4.center
                screen.blit(text, textRect)
                pygame.draw.rect(screen, 'black', button_id_4, 1)

                text = font.render('*' + items[4] + ' ' + heals[4], True, 'white')
                textRect = text.get_rect()
                textRect.center = button_id_5.center
                screen.blit(text, textRect)
                pygame.draw.rect(screen, 'black', button_id_5, 1)

                text = font.render('*' + items[5] + ' ' + heals[5], True, 'white')
                textRect = text.get_rect()
                textRect.center = button_id_6.center
                screen.blit(text, textRect)
                pygame.draw.rect(screen, 'black', button_id_6, 1)
            # механника анализа
            if Analysis and not end:
                words = 'Банда - ' + str(Band_hit) + ' атаки; ' + str(XP_band) + ' - здоровья'
                Analysis = False
                Action = False

            # основное окно
            text = font_small.render(words, True, 'white')
            textRect = text.get_rect()
            textRect.center = Action_rect.center
            screen.blit(text, textRect)
            pygame.draw.rect(screen, 'white', Action_rect, 1)

        # экран, если ход противника
        if turn == 'enemy':
            # проверка на время
            if time < 9:
                all_sprites.update()
                # Проверка, не ударил ли моб игрока
                hits = pygame.sprite.spritecollide(player, attacks, False, pygame.sprite.collide_circle)
                if hits:
                    Hit = True
                all_sprites.draw(screen)
                pygame.mouse.set_visible(False)
                time += v * clock.tick() / 1000
                pygame.draw.rect(screen, 'white', Fight_rect, 1)
                if time_hit <= 0 and Hit:
                    time_hit = 0.3
                    if abs(dop_attack) > Band_hit:
                        XP_Hero -= Band_hit - dop_attack
                    else:
                        XP_Hero -= Band_hit + dop_attack
                    # Нашему персонажу нанесён урон
                elif time_hit > 0:
                    time_hit -= v_hit * clock.tick() / 1000
                Hit = False
                # Наш персонаж
                if XP_Hero - (Band_hit + dop_attack) <= 0:
                    XP_Hero = 0
                    words = 'Вы погибли!'
                    end = True
                    turn = 'player'
            elif time >= 9:
                pygame.mouse.set_visible(True)
                all_sprites.update()
                time_hit = 0
                time = 0
                turn = 'player'
                Mercy = False
                Action = False
                Item = False
                Analysis = False
                words = '* Банда ждёт ваших действий!'
        # кнопка атаки
        text = font.render('Атака', True, 'yellow')
        textRect = text.get_rect()
        textRect.center = button_attack.center
        screen.blit(text, textRect)
        pygame.draw.rect(screen, 'yellow', button_attack, 1)

        # кнопка действия
        text = font.render('Действие', True, 'yellow')
        textRect = text.get_rect()
        textRect.center = button_action.center
        screen.blit(text, textRect)
        pygame.draw.rect(screen, 'yellow', button_action, 1)

        # кнопка инвентаря
        text = font.render('Предметы', True, 'yellow')
        textRect = text.get_rect()
        textRect.center = button_item.center
        screen.blit(text, textRect)
        pygame.draw.rect(screen, 'yellow', button_item, 1)

        # Проверка кнопки милосердия
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

        # кнопка перезапуска
        text = font.render('R', True, 'red')
        textRect = text.get_rect()
        textRect.center = button_restart.center
        screen.blit(text, textRect)
        pygame.draw.rect(screen, 'blue', button_restart, 1)
        pygame.display.update()
        clock.tick(FPS)


pygame.quit()

if __name__ == '__main__':
    Victory = False
    main()
    if Victory:
        print('Победа!')
    else:
        print('Ну всё....')
