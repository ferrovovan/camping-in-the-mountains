import pygame
import random
from os import path
from random import randint


#
# class Enemy(pygame.sprite.Sprite):
# def __init__(self):
# pygame.sprite.Sprite.__init__(self)
# self.image = pygame.transform.scale(enemy_img, (400, 500))
# self.image.set_colorkey('black')
# self.rect = self.image.get_rect()
# self.rect.centerx = W // 2
# self.rect.centery = H // 3


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (20, 20))
        self.image.set_colorkey('black')
        self.rect = self.image.get_rect()
        self.radius = 9
        # pygame.draw.circle(self.image, 'red', self.rect.center, self.radius)
        self.rect.centerx = H // 1.12
        self.rect.centery = W // 3.4
        self.speedx = 3
        self.speedy = 3

    def update(self):
        keystate = pygame.key.get_pressed()
        # x
        if keystate[pygame.K_a]:
            self.rect.x -= self.speedx
        elif keystate[pygame.K_LEFT]:
            self.rect.x -= self.speedx
        if keystate[pygame.K_d]:
            self.rect.x += 3
        elif keystate[pygame.K_RIGHT]:
            self.rect.x += 3
        # y
        if keystate[pygame.K_s]:
            self.rect.y += 3
        elif keystate[pygame.K_DOWN]:
            self.rect.y += 3
        if keystate[pygame.K_w]:
            self.rect.y -= 3
        elif keystate[pygame.K_UP]:
            self.rect.y -= 3
        if self.rect.right > 3 * W // 5:
            self.rect.right = 3 * W // 5
        if self.rect.left < W // 2.5:
            self.rect.left = W // 2.5
        if self.rect.top < H // 3:
            self.rect.top = H // 3
        if self.rect.bottom > H // 3 + W // 5:
            self.rect.bottom = H // 3 + W // 5


class Enemy_attacks(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = hit_img
        self.image.set_colorkey('black')
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        # pygame.draw.circle(self.image, 'red', self.rect.center, self.radius)
        self.rect.x = randint(W // 2.5, 3 * W // 5)
        self.rect.y = H // 3.5
        self.speedy = int(random.randrange(3, 5) * H / 800)
        self.speedx = int(random.randrange(-2, 2))

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if any((self.rect.top > H // 3 + W // 5,
               self.rect.left < W // 2.5,
               self.rect.right > 3 * W // 5)):  # если улетело за рамки
            self.rect.x = randint(W // 2.5, 3 * W // 5)
            self.rect.y = H // 3.5
            self.speedy = int(random.randrange(3, 4) * H / 800)
            self.speedx = int(random.randrange(-2, 2))


def main(scr_size=None, Your_hit=5):
    global Victory
    pygame.init()
    pygame.mixer.init()
    clock = pygame.time.Clock()
    FPS = 60
    global W
    global H
    infoObject = pygame.display.Info()
    if scr_size is None:
        W = infoObject.current_w
        H = infoObject.current_h
    else:
        W, H = scr_size
    screen = pygame.display.set_mode((W, H))
    # инициализация параметров
    XP_band = 200
    XP_Hero = 200
    Total_hit_enemy = int(W // 9.6)
    Total_hit_player = int(W // 9.6)
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
    Attack = False
    Item = False
    Mercy = False
    Hit = False
    Analysis = False
    Cont = False
    Back = False
    turn = 'player'
    items = ['Аптечка', 'Бутерброд', 'Бинт', 'Антибиотик', 'Обезболивающее', 'Консервы']
    heals = ['70', '50', '30', '60', '100', '20']
    font = pygame.font.Font('freesansbold.ttf', 35)
    font_small = pygame.font.Font('freesansbold.ttf', 20)
    words = '* Банда появляется!'

    # музыка
    sound = pygame.mixer.Sound(path.join('data/sounds/Hit.wav'))
    pygame.mixer.music.load(path.join('data/sounds/Battle_theme.mp3'))
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(loops=-1)

    # задание (становление) всех кнопок
    # батоны
    button_attack = pygame.Rect(W // 5.6, H - H // 14,
                                W // 8, H // 14)
    button_action = pygame.Rect(W // 2.8, H - H // 14,
                                W // 8, H // 14)
    button_item = pygame.Rect(W // 1.85, H - H // 14,
                              W // 8, H // 14)
    button_mercy = pygame.Rect(W // 1.4, H - H // 14,
                               W // 8, H // 14)
    button_talk = pygame.Rect(W // 1.45, H // 1.4,
                              W // 8, H // 16)
    button_threat = pygame.Rect(W // 4.6, H // 1.4,
                                W // 8, H // 16)
    button_information = pygame.Rect(W // 2.2, H // 1.4,
                                     W // 10, H // 16)
    button_id_1 = pygame.Rect(W // 4.2, H // 1.44,
                              W // 15, H // 30)
    button_id_2 = pygame.Rect(W // 4.2, H // 1.34,
                              W // 12, H // 30)
    button_id_3 = pygame.Rect(W // 2.1, H // 1.44,
                              W // 22, H // 30)
    button_id_4 = pygame.Rect(W // 2.1, H // 1.34,
                              W // 12, H // 30)
    button_id_5 = pygame.Rect(W // 1.6, H // 1.44,
                              W // 8, H // 30)
    button_id_6 = pygame.Rect(W // 1.6, H // 1.34,
                              W // 12, H // 30)
    Back_button = pygame.Rect(W // 1.35, H // 1.28,
                              H // 15, H // 34)
    button_continue = pygame.Rect(W // 1.4, H // 1.3, 20, 50)

    # квадратики
    Enemy_XP_rect = pygame.Rect(W // 2, H // 898, 10, 29)
    Hero_XP_rect = pygame.Rect(W // 1.5, H // 1.22, 10, 10)
    Action_rect = pygame.Rect(W // 6, H // 1.5,  # где написано событие
                              W // 1.47, H // 7)
    Fight_rect = pygame.Rect(W // 2.5, H // 3,  # где ходит персонаж, рамки
                             W // 5, W // 5)

    global player_img
    global hit_img
    global enemy_img
    player_img = pygame.image.load(path.join("data/gfx/textures/interface/heart.jpg")).convert()
    hit_img = pygame.image.load(path.join("data/gfx/textures/interface/Enemy_fire.jpg")).convert()
    # enemy_img = pygame.image.load(path.join("Enemy.jpg")).convert()

    all_sprites = pygame.sprite.Group()
    attacks = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    # enemy = Enemy()
    # enemies.add(enemy)
    player = Player()
    all_sprites.add(player)
    ammo = 5 * W // 500
    for i in range(ammo):
        attack = Enemy_attacks()
        all_sprites.add(attack)
        attacks.add(attack)

    while True:
        if end and XP_Hero > 0 and not Cont:
            return True
        elif end and XP_Hero == 0 and not Cont:
            return False
        screen.fill('black')
        enemies.draw(screen)
        # проверка на милосердие
        if mercy <= 2:
            Band_hit = randint(15, 20) + dop_attack
        else:
            dop_attack = 0
            Band_hit = randint(5, 10)

        # проверка на события
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False

            # события, если ход игрока
            if turn == 'player':
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if words == 'Вы победили!':
                            return True
                        elif turn == 'player' and not Action and not Item and not Attack\
                                and words != '* Банда появляется!' \
                                and words != '* Банда ждёт ваших действий!':
                            turn = 'enemy'
                            Cont = False
                    # hot keys
                    if event.key == pygame.K_t:  # attack
                        if turn == 'player' and not Action:
                            Attack = True
                #                    if event.key == pygame.K_y:  # действие
                #                        if turn == 'player' and not Action and not Item and not Attack:
                #                            Action = True
                #                    elif event.key == pygame.K_i:  # предметы
                #                        if turn == 'player' and not Item:
                #                            Item = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if Back_button.collidepoint(mouse_pos) and Back:
                        Mercy = False
                        Action = False
                        Item = False
                        words = '* Банда ждёт ваших действий!'
                        Back = False
                    # кнопка атаки
                    if button_attack.collidepoint(
                            mouse_pos) and not Action and not Item and not end and not Attack and not Mercy \
                            and not Cont:
                        Attack = True
                        Cont = True
                    # кнопка действия
                    elif button_action.collidepoint(
                            mouse_pos) and not Action and not Item and not end and not Attack and not Cont:
                        Back = True
                        words = ''
                        dop_attack = 0
                        Action = True
                    # кнопка предмета
                    elif button_item.collidepoint(
                            mouse_pos) and not Action and not Item and not end and not Attack and not Cont:
                        Item = True
                        Back = True
                        words = ''
                        Band_scare = False
                        if XP_band < 200:
                            XP_band += 1
                        dop_attack = 0
                    # кнопка пощады
                    elif button_mercy.collidepoint(
                            mouse_pos) and not Action and not Item and not end and not Attack and not Cont:
                        Mercy = True
                        Cont = True
                    # кнопка угрозы
                    elif button_threat.collidepoint(mouse_pos) and Action:
                        mercy = 0
                        chance = randint(0, 100)
                        if chance >= 60:
                            Band_scare = 'good'
                        else:
                            Band_scare = 'refuse'
                        Action = False
                        Cont = True
                        Back = False
                    # кнопка разговора
                    elif button_talk.collidepoint(mouse_pos) and Action:
                        chance = randint(0, 100)
                        if chance >= 10:
                            Band_talk = 'good'
                        else:
                            Band_talk = 'refuse'
                        Action = False
                        Cont = True
                        Back = False
                    # кнопка анализа
                    elif button_information.collidepoint(mouse_pos) and Action:
                        Analysis = True
                        Cont = True
                        Back = False
                    elif button_id_1.collidepoint(mouse_pos) and Item and items[0] != 'Пусто':
                        items[0] = 'Пусто'
                        heals[0] = ''
                        if XP_Hero + 70 >= 200:
                            XP_Hero = 200
                            Total_hit_player = (200 * int(infoObject.current_w // 9.6)) // 200
                        else:
                            XP_Hero += 70
                            Total_hit_player += (70 * int(infoObject.current_w // 9.6)) // 200
                        Item = False
                        words = '* Вы использовали аптечку. +70ХР'
                        Cont = True
                        Back = False
                    elif button_id_2.collidepoint(mouse_pos) and Item and items[1] != 'Пусто':
                        items[1] = 'Пусто'
                        heals[1] = ''
                        if XP_Hero + 50 >= 200:
                            XP_Hero = 200
                            Total_hit_player = (200 * int(infoObject.current_w // 9.6)) // 200
                        else:
                            XP_Hero += 50
                            Total_hit_player += (50 * int(infoObject.current_w // 9.6)) // 200
                        Item = False
                        words = 'Вы сьели бутерброд. +50ХР'
                        Cont = True
                        Back = False
                    elif button_id_3.collidepoint(mouse_pos) and Item and items[2] != 'Пусто':
                        items[2] = 'Пусто'
                        heals[2] = ''
                        if XP_Hero + 30 >= 200:
                            XP_Hero = 200
                            Total_hit_player = (200 * int(infoObject.current_w // 9.6)) // 200
                        else:
                            XP_Hero += 30
                            Total_hit_player += (30 * int(infoObject.current_w // 9.6)) // 200
                        Item = False
                        words = 'Вы использовали бинт. +30ХР'
                        Cont = True
                        Back = False
                    elif button_id_4.collidepoint(mouse_pos) and Item and items[3] != 'Пусто':
                        items[3] = 'Пусто'
                        heals[3] = ''
                        if XP_Hero + 60 >= 200:
                            XP_Hero = 200
                            Total_hit_player = (200 * int(infoObject.current_w // 9.6)) // 200
                        else:
                            XP_Hero += 60
                            Total_hit_player += (60 * int(infoObject.current_w // 9.6)) // 200
                        Item = False
                        words = 'Вы приняли антибиотик. +60ХР'
                        Cont = True
                        Back = False
                    elif button_id_5.collidepoint(mouse_pos) and Item and items[4] != 'Пусто':
                        items[4] = 'Пусто'
                        heals[4] = ''
                        if XP_Hero + 100 >= 200:
                            XP_Hero = 200
                            Total_hit_player = (200 * int(infoObject.current_w // 9.6)) // 200
                        else:
                            XP_Hero += 100
                            Total_hit_player += (100 * int(infoObject.current_w // 9.6)) // 200
                        Item = False
                        words = 'Вы приняли обезболивающее. +100ХР'
                        Cont = True
                        Back = False
                    elif button_id_6.collidepoint(mouse_pos) and Item and items[5] != 'Пусто':
                        items[5] = 'Пусто'
                        heals[5] = ''
                        if XP_Hero + 20 >= 200:
                            XP_Hero = 200
                            Total_hit_player = (200 * int(infoObject.current_w // 9.6)) // 200
                        else:
                            XP_Hero += 20
                            Total_hit_player += (20 * int(infoObject.current_w // 9.6)) // 200
                        Item = False
                        words = 'Вы сьели консервы. +20ХР'
                        Cont = True
                        Back = False

            # события, если ход противника
            if turn == 'enemy':
                pass

        # экран, если ход игрока
        if turn == 'player':
            if Attack:
                pygame.mouse.set_visible(False)
                mercy = 0
                Band_scare = False
                if XP_band - Your_hit <= 0:
                    XP_band = 0
                    words = 'Вы победили!'
                    end = True
                    Cont = True
                else:
                    words = '* Вы решили атаковать!'
                    XP_band -= Your_hit
                    Total_hit_enemy -= (Your_hit * int(W // 9.6)) // 200
                    Attack = False
                dop_attack = 0
            # механика пощады
            if Mercy:
                pygame.mouse.set_visible(False)
                if mercy >= 3:
                    end = True
                    words = 'Банда вас отпускает.)) Вы победили!)'
                    Band_talk = 'None'
                else:
                    words = 'Банда не отреагировала. Попробуйте с ней поговорить.'
                    Band_talk = 'None'
                    Mercy = False
            if Cont and not Action and not Item:
                if not end:
                    pygame.mouse.set_visible(False)
                    text = font_small.render('Нажите "Enter". Будте готовы к бою!', True, 'white')
                    textRect = text.get_rect()
                    textRect.center = button_continue.center
                    screen.blit(text, textRect)
                else:
                    pygame.mouse.set_visible(False)
                    text = font_small.render('Нажите "Enter".', True, 'white')
                    textRect = text.get_rect()
                    textRect.center = button_continue.center
                    screen.blit(text, textRect)
            if Back and not end:
                text = font_small.render('Назад', True, 'white')
                textRect = text.get_rect()
                textRect.center = Back_button.center
                screen.blit(text, textRect)
                pygame.draw.rect(screen, 'white', Back_button, 1)
            # механика действий
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

                text = font.render('* Анализ', True, 'white')
                textRect = text.get_rect()
                textRect.center = button_information.center
                screen.blit(text, textRect)
                pygame.draw.rect(screen, 'black', button_information, 1)

                text = font.render('', True, 'white')
                textRect = text.get_rect()
                textRect.center = Action_rect.center
                screen.blit(text, textRect)
            else:
                # угрожать
                if Band_scare == 'good':
                    dop_attack = -10
                    words = 'Банда в испуге! Атаки банды стали слабее.'
                    text = font.render(words, True, 'white')
                    textRect = text.get_rect()
                    textRect.center = Action_rect.center
                    screen.blit(text, textRect)
                    Band_scare = 'None'
                elif Band_scare == 'refuse':
                    dop_attack = 10
                    words = 'Банда посмеялась над вами! Атаки банды стали сильнее.'
                    text = font_small.render(words, True, 'white')
                    textRect = text.get_rect()
                    textRect.center = Action_rect.center
                    screen.blit(text, textRect)
                    Band_scare = 'None'
                # поговорить
                elif Band_talk == 'refuse':
                    dop_attack = 5
                    words = 'Банда не хочет говорить. Атаки банды стали сильнее.'
                    Band_talk = 'None'
                elif Band_talk == 'good':
                    mercy += 1
                    words = 'Вы хорошо побеседовали с бандой. Продолжайте в том же духе!)'
                    Band_talk = 'None'
                Action = False
            # механика предметов
            if Item and not end:
                words = ''
                text = font_small.render('*' + items[0] + ' ' + heals[0], True, 'white')
                textRect = text.get_rect()
                textRect.center = button_id_1.center
                screen.blit(text, textRect)
                pygame.draw.rect(screen, 'black', button_id_1, 1)

                text = font_small.render('*' + items[1] + ' ' + heals[1], True, 'white')
                textRect = text.get_rect()
                textRect.center = button_id_2.center
                screen.blit(text, textRect)
                pygame.draw.rect(screen, 'black', button_id_2, 1)

                text = font_small.render('*' + items[2] + ' ' + heals[2], True, 'white')
                textRect = text.get_rect()
                textRect.center = button_id_3.center
                screen.blit(text, textRect)
                pygame.draw.rect(screen, 'black', button_id_3, 1)

                text = font_small.render('*' + items[3] + ' ' + heals[3], True, 'white')
                textRect = text.get_rect()
                textRect.center = button_id_4.center
                screen.blit(text, textRect)
                pygame.draw.rect(screen, 'black', button_id_4, 1)

                text = font_small.render('*' + items[4] + ' ' + heals[4], True, 'white')
                textRect = text.get_rect()
                textRect.center = button_id_5.center
                screen.blit(text, textRect)
                pygame.draw.rect(screen, 'black', button_id_5, 1)

                text = font_small.render('*' + items[5] + ' ' + heals[5], True, 'white')
                textRect = text.get_rect()
                textRect.center = button_id_6.center
                screen.blit(text, textRect)
                pygame.draw.rect(screen, 'black', button_id_6, 1)
            # механика анализа
            if Analysis and not end:
                words = 'Банда - ' + str(Band_hit) + ' атаки; ' + str(XP_band) + ' - здоровья'
                Analysis = False
                Action = False

            # основное окно
            text = font.render(words, True, 'white')
            textRect = text.get_rect()
            textRect.center = Action_rect.center
            screen.blit(text, textRect)
            pygame.draw.rect(screen, 'white', Action_rect, 1)

        # экран, если ход противника
        if turn == 'enemy':
            pygame.draw.rect(screen, 'black', Fight_rect)  # поле
            # проверка на время
            if time < 25:
                all_sprites.update()
                # Проверка, не ударил ли моб игрока
                hits = pygame.sprite.spritecollide(player, attacks, False, pygame.sprite.collide_circle)
                if hits:
                    Hit = True
                all_sprites.draw(screen)
                pygame.mouse.set_visible(False)
                time += v * clock.tick() / 1000
                pygame.draw.rect(screen, 'white', Fight_rect, 1)  # рамки
                if time_hit <= 0 and Hit:
                    sound.play()
                    time_hit = 0.325
                    if abs(dop_attack) > Band_hit:
                        XP_Hero -= Band_hit
                        Total_hit_player -= ((Band_hit - dop_attack)
                                             * int(infoObject.current_w // 9.6)) // 200
                    else:
                        XP_Hero -= Band_hit
                        Total_hit_player -= ((Band_hit + dop_attack)
                                             * int(infoObject.current_w // 9.6)) // 200
                    # Нашему персонажу нанесён урон
                elif time_hit > 0:
                    time_hit -= v_hit * clock.tick() / 1000
                Hit = False
                # Наш персонаж
                if XP_Hero - (Band_hit + dop_attack) <= 0:
                    XP_Hero = 0
                    words = 'Вы погибли!'
                    end = True
                    Total_hit_player = 0
                    turn = 'player'
            elif time >= 25:
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
        XP_Hero_rect = pygame.Rect(infoObject.current_w // 1.62, infoObject.current_h // 1.18,
                                   int(infoObject.current_w // 9.6), int(infoObject.current_h // 20))
        XP_str = pygame.Rect(infoObject.current_w // 1.9, infoObject.current_h // 1.18,
                             int(infoObject.current_w // 10), int(infoObject.current_h // 20))
        pygame.draw.rect(screen, 'black', XP_Hero_rect)
        text = font_small.render(str(XP_Hero) + '/200', True, 'white')
        textRect = text.get_rect()
        textRect.center = XP_str.center
        screen.blit(text, textRect)

        pygame.draw.rect(screen, 'black', Hero_XP_rect)
        text = font_small.render('Ваше здоровье', True, 'white')
        textRect = text.get_rect()
        textRect.center = Hero_XP_rect.center
        screen.blit(text, textRect)

        pygame.draw.rect(screen, 'red', XP_Hero_rect)

        pygame.draw.rect(screen, 'yellow', (int(infoObject.current_w // 1.62), int(infoObject.current_h // 1.18),
                                            Total_hit_player, int(infoObject.current_h // 20)))

        # XP банды
        XP_band_rect = pygame.Rect(infoObject.current_w // 2.2, infoObject.current_h // 15,
                                   int(infoObject.current_w // 9.6),
                                   int(infoObject.current_h // 24))

        XP_str = pygame.Rect(infoObject.current_w // 2.2, infoObject.current_h // 60,
                             int(infoObject.current_w // 9.6),
                             int(infoObject.current_h // 20))
        pygame.draw.rect(screen, 'black', XP_str)
        text = font_small.render(str(XP_band) + '/200', True, 'white')
        textRect = text.get_rect()
        textRect.center = XP_str.center
        screen.blit(text, textRect)

        pygame.draw.rect(screen, 'black', Enemy_XP_rect)
        text = font_small.render('Здоровье врага', True, 'white')
        textRect = text.get_rect()
        textRect.center = Enemy_XP_rect.center
        screen.blit(text, textRect)

        pygame.draw.rect(screen, 'red', XP_band_rect)

        pygame.draw.rect(screen, 'yellow', (int(W // 2.2), int(H // 15),
                                            Total_hit_enemy, int(H // 24)))
        pygame.display.update()
        clock.tick(FPS)


pygame.quit()
