from pygame import *

SHOW_HITBOX = False

# Инициализация музыки и звуков
mixer.init()
mixer.music.load('bgm.mp3')
mixer.music.set_volume(0.6)
mixer.music.play(-1)

hit_sound = mixer.Sound('hit.mp3')
end_sound = mixer.Sound('end.mp3')

duck_timer = 0


# Классы
class GameSprite(sprite.Sprite):
    def __init__(self, image1, x, y, speed, width, height):
        super().__init__()

        surf = image.load(image1).convert_alpha()
        surf = transform.scale(surf, (width, height))
        

        for px in range(surf.get_width()):
            for py in range(surf.get_height()):
                r, g, b, a = surf.get_at((px, py))
                if abs(r - g) < 15 and abs(g - b) < 15 and abs(r - b) < 15 and r > 180:
                    surf.set_at((px, py), (0, 0, 0, 0))
                    
        self.image = surf
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def __init__(self, image1, x, y, speed, width, height):
        super().__init__(image1, x, y, speed, width, height)
        
        self.hitbox_offset_x = 15
        self.hitbox_offset_y = 8
        hb_width = max(5, width - (self.hitbox_offset_x * 2))
        hb_height = max(5, height - (self.hitbox_offset_y * 2))
        
        self.hitbox = Rect(x + self.hitbox_offset_x, y + self.hitbox_offset_y, hb_width, hb_height)

    def update_hitbox(self):
        self.hitbox.x = self.rect.x + self.hitbox_offset_x
        self.hitbox.y = self.rect.y + self.hitbox_offset_y

    def update_r(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.bottom < win_height - 5:
            self.rect.y += self.speed
        self.update_hitbox()

    def update_l(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.bottom < win_height - 5:
            self.rect.y += self.speed
        self.update_hitbox()

    def draw_hitbox(self):
        if SHOW_HITBOX:
            draw.rect(window, (255, 0, 0), self.hitbox, 2)
            draw.rect(window, (0, 0, 255), self.rect, 1)


def reset_ball():
    global speed_x, speed_y
    ball.rect.x = win_width // 2 - 20
    ball.rect.y = win_height // 2 - 20
    speed_x = 3
    speed_y = 3


def restart_game():
    global score1, score2, finish, paused
    score1 = 0
    score2 = 0
    finish = False
    paused = False
    racket1.rect.x = 30
    racket1.rect.y = 175
    racket1.update_hitbox()
    racket2.rect.x = 510
    racket2.rect.y = 175
    racket2.update_hitbox()
    reset_ball()
    mixer.music.play(-1)


def check_collision(player, ball_sprite):
    return player.hitbox.colliderect(ball_sprite.rect)


win_width = 600
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Ping-Pong")
back_color = (200, 255, 255)

clock = time.Clock()
FPS = 60
game = True
finish = False
paused = False

score1 = 0
score2 = 0
MAX_SCORE = 3

racket1 = Player('14.png', 30, 175, 4, 60, 150)
racket2 = Player('14.png', 510, 175, 4, 60, 150)
ball = GameSprite('13.png', win_width // 2 - 20, win_height // 2 - 20, 4, 40, 40)

font.init()
score_font = font.Font(None, 50)
result_font = font.Font(None, 45)
hint_font = font.Font(None, 30)

speed_x = 3
speed_y = 3

# Главный игровой цикл
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        
        if e.type == KEYDOWN:
            if e.key == K_r:
                restart_game()
            if e.key == K_ESCAPE and not finish:
                paused = not paused
                if paused:
                    mixer.music.pause()
                else:
                    mixer.music.unpause()

    if not finish and not paused:
        window.fill(back_color)

        racket1.update_l()
        racket2.update_r()

        ball.rect.x += speed_x
        ball.rect.y += speed_y

        if duck_timer > 0:
            duck_timer -= 1
            if duck_timer == 0:
                mixer.music.set_volume(0.6)

        if check_collision(racket1, ball) and speed_x < 0:
            speed_x *= -1
            ball.rect.left = racket1.hitbox.right
            hit_sound.play()
            mixer.music.set_volume(0.1)
            duck_timer = 60

        if check_collision(racket2, ball) and speed_x > 0:
            speed_x *= -1
            ball.rect.right = racket2.hitbox.left
            hit_sound.play()
            mixer.music.set_volume(0.1)
            duck_timer = 60

        if ball.rect.top <= 0:
            speed_y = abs(speed_y)
        if ball.rect.bottom >= win_height:
            speed_y = -abs(speed_y)

        if ball.rect.right < 0:
            score2 += 1
            if score2 >= MAX_SCORE:
                finish = True
                mixer.music.stop()
                end_sound.play()
            else:
                reset_ball()

        if ball.rect.left > win_width:
            score1 += 1
            if score1 >= MAX_SCORE:
                finish = True
                mixer.music.stop()
                end_sound.play()
            else:
                reset_ball()

        for y_pos in range(0, win_height, 20):
            draw.rect(window, (150, 150, 150), (win_width // 2 - 1, y_pos, 2, 10))

        score_text = score_font.render(f"{score1} : {score2}", True, (0, 0, 0))
        window.blit(score_text, score_text.get_rect(center=(win_width // 2, 30)))

        racket1.reset()
        racket2.reset()
        ball.reset()
        
        racket1.draw_hitbox()
        racket2.draw_hitbox()

    elif paused and not finish:
        pause_text = result_font.render("ПАУЗА", True, (50, 50, 50))
        window.blit(pause_text, pause_text.get_rect(center=(win_width // 2, win_height // 2)))

    elif finish:
        window.fill(back_color)
        score_text = score_font.render(f"{score1} : {score2}", True, (0, 0, 0))
        window.blit(score_text, score_text.get_rect(center=(win_width // 2, 30)))

        if score1 >= MAX_SCORE:
            win_text = result_font.render("Игрок 1 победил!", True, (0, 150, 0))
        else:
            win_text = result_font.render("Игрок 2 победил!", True, (0, 150, 0))
        
        window.blit(win_text, win_text.get_rect(center=(win_width // 2, win_height // 2 - 20)))
        hint_text = hint_font.render("Нажмите R для перезапуска", True, (100, 100, 100))
        window.blit(hint_text, hint_text.get_rect(center=(win_width // 2, win_height // 2 + 30)))

    display.update()
    clock.tick(FPS)