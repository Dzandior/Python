from pygame import *
from random import *


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, x, y, sizex, sizey, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (sizex, sizey))
        self.speed = player_speed

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        pgrops.add(bullet)


lost = 0


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost += 1


class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()


pgrops = sprite.Group()

win_width = 700
win_height = 700
window = display.set_mode((win_width, win_height))
display.set_caption('Galaxy')

background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))
ship = Player('rocket.png', win_width // 2 - 40, win_height - 100, 80, 100, 10)

monsters = sprite.Group()

for i in range(1, 11):
    vrag = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 3))
    monsters.add(vrag)

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play(-1)
fire_sound = mixer.Sound('fire.ogg')
win_sound = mixer.Sound('win.mp3')

clock = time.Clock()
game = True
finish = False
win = False

score = 0
stop = 3
goal = 75

font.init()
font1 = font.Font(None, 70)
font2 = font.Font(None, 36)

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE and not finish:
                ship.fire()
                fire_sound.play()
            # Рестарт на R
            if e.key == K_r and finish:
                finish = False
                win = False
                score = 0
                lost = 0
                for b in pgrops:
                    b.kill()
                for m in monsters:
                    m.kill()
                for i in range(1, 11):
                    vrag = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 3))
                    monsters.add(vrag)
                ship.rect.x = win_width // 2 - 40
                ship.rect.y = win_height - 100
                mixer.music.play(-1)

    if not finish:
        window.blit(background, (0, 0))

        text = font2.render('Счёт:' + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lise = font2.render('Пропущено:' + str(lost), 1, (255, 255, 255))
        window.blit(text_lise, (10, 50))

        pgrops.update()
        ship.update()
        ship.reset()
        monsters.update()
        monsters.draw(window)
        pgrops.draw(window)

        collide = sprite.groupcollide(monsters, pgrops, True, True)
        for c in collide:
            score += 1
            vrag = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 3))
            monsters.add(vrag)

        if sprite.spritecollide(ship, monsters, False) or lost >= stop:
            finish = True
            win = False
            mixer.music.stop()

        if score >= goal:
            finish = True
            win = True
            mixer.music.stop()
            win_sound.play()

    else:
        window.blit(background, (0, 0))
        if win:
            text_win = font1.render('ПОБЕДА!', 1, (0, 255, 0))
            window.blit(text_win, (win_width // 2 - text_win.get_width() // 2, 300))
        else:
            text_lose = font1.render('ПРОИГРЫШ!', 1, (255, 0, 0))
            window.blit(text_lose, (win_width // 2 - text_lose.get_width() // 2, 300))

        text_restart = font2.render('Нажмите R для перезапуска', 1, (255, 255, 255))
        window.blit(text_restart, (win_width // 2 - text_restart.get_width() // 2, 380))

    display.update()
    clock.tick(60)