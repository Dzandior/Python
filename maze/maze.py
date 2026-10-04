from pygame import *

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - 80:
            self.rect.y += self.speed

class Enemy(GameSprite):
    naprav = 'left'
    def update(self):
        if self.rect.x <= self.min_x:
            self.naprav = 'right'
        if self.rect.x >= self.max_x:
            self.naprav = 'left'
        if self.naprav == 'left':
            self.rect.x -= self.speed
        if self.naprav == 'right':
            self.rect.x += self.speed

class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.width = wall_width
        self.height = wall_height
        self.image = Surface((self.width, self.height))
        self.image.fill((color_1, color_2, color_3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y

    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('labirint')

background = transform.scale(image.load('background.jpg'), (win_width, win_height))

player = Player('hero.png', 5, win_height - 80, 5)
monster = Enemy('cyborg.png', win_width - 80, 280, 2)
monster.min_x = win_width - 230
monster.max_x = win_width - 85
final = GameSprite('treasure.png', win_width - 120, win_height - 80, 0)

walls = []
level = 1
max_level = 5

def load_level(n):
    global walls, monster, final
    walls = []
    
    if n == 1:
        walls.append(Wall(150, 110, 190, 180, 0, 20, 350))
        walls.append(Wall(150, 110, 190, 360, 150, 20, 350))
        walls.append(Wall(150, 110, 190, 520, 0, 20, 350))
        monster.rect.x = 580
        monster.rect.y = 200
        monster.speed = 2
        monster.min_x = 550
        monster.max_x = 630
        final.rect.x = 610
        final.rect.y = 420

    elif n == 2:
        walls.append(Wall(150, 110, 190, 0, 320, 520, 20))
        walls.append(Wall(150, 110, 190, 180, 160, 520, 20))
        monster.rect.x = 550
        monster.rect.y = 50
        monster.speed = 3
        monster.min_x = 10
        monster.max_x = 600
        final.rect.x = 600
        final.rect.y = 50

    elif n == 3:
        walls.append(Wall(150, 110, 190, 160, 0, 20, 360))
        walls.append(Wall(150, 110, 190, 340, 140, 20, 360))
        walls.append(Wall(150, 110, 190, 520, 0, 20, 360))
        monster.rect.x = 380
        monster.rect.y = 50
        monster.speed = 3
        monster.min_x = 175
        monster.max_x = 480
        final.rect.x = 610
        final.rect.y = 420

    elif n == 4:
        walls.append(Wall(150, 110, 190, 150, 140, 20, 360))
        walls.append(Wall(150, 110, 190, 320, 0, 20, 360))
        walls.append(Wall(150, 110, 190, 490, 140, 20, 360))
        monster.rect.x = 360
        monster.rect.y = 50
        monster.speed = 4
        monster.min_x = 180
        monster.max_x = 450
        final.rect.x = 580
        final.rect.y = 420

    elif n == 5:
        walls.append(Wall(150, 110, 190, 140, 0, 20, 360))
        walls.append(Wall(150, 110, 190, 280, 140, 20, 360))
        walls.append(Wall(150, 110, 190, 420, 0, 20, 360))
        walls.append(Wall(150, 110, 190, 560, 140, 20, 360))
        monster.rect.x = 450
        monster.rect.y = 50
        monster.speed = 5
        monster.min_x = 300
        monster.max_x = 530
        final.rect.x = 610
        final.rect.y = 420

def restart_level():
    global finish, level
    finish = False
    player.rect.x = 5
    player.rect.y = win_height - 80
    load_level(level)
    mixer.music.play()

def full_restart():
    global level, finish
    level = 1
    finish = False
    player.rect.x = 5
    player.rect.y = win_height - 80
    load_level(level)
    mixer.music.play()

mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.play()

money = mixer.Sound('money.ogg')
kick = mixer.Sound('kick.ogg')

game = True
finish = False
clock = time.Clock()

font.init()
font_text = font.Font(None, 70)
font_small = font.Font(None, 36)
win = font_text.render('YOU WIN!', True, (255, 215, 0))
lose = font_text.render('YOU LOSE!', True, (100, 0, 0))
all_win = font_text.render('ALL LEVELS DONE!', True, (0, 255, 0))

load_level(level)

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_r:
                if finish:
                    if level > max_level:
                        full_restart()
                    else:
                        restart_level()

    if not finish:
        window.blit(background, (0, 0))

        player.update()
        monster.update()

        player.reset()
        monster.reset()
        final.reset()

        for w in walls:
            w.draw_wall()

        level_text = font_small.render('Уровень: ' + str(level) + ' / 5', True, (255, 255, 255))
        window.blit(level_text, (10, 10))

        hit_wall = False
        for w in walls:
            if sprite.collide_rect(player, w):
                hit_wall = True

        if hit_wall or sprite.collide_rect(player, monster):
            finish = True
            window.blit(lose, (200, 200))
            kick.play()
            mixer.music.stop()
            restart_text = font_small.render('Нажмите R для рестарта', True, (255, 255, 255))
            window.blit(restart_text, (180, 280))

        if sprite.collide_rect(player, final):
            money.play()
            level += 1
            if level > max_level:
                finish = True
                window.blit(all_win, (100, 200))
                mixer.music.stop()
                restart_text = font_small.render('Нажмите R для рестарта', True, (255, 255, 255))
                window.blit(restart_text, (180, 280))
            else:
                player.rect.x = 5
                player.rect.y = win_height - 80
                load_level(level)

    display.update()
    clock.tick(60)