from pygame import *

font.init()
mixer.init()

mixer.music.load('bgm.mp3')
mixer.music.set_volume(0.6)
mixer.music.play(-1)
end_sound = mixer.Sound('end.mp3')

win_width = 1000
win_height = 700
window = display.set_mode((win_width, win_height))
display.set_caption('Догонялки')
background = transform.scale(image.load('background.png'), (win_width, win_height))
clock = time.Clock()

main_font = font.Font(None, 60)
info_font = font.Font(None, 40)

x1 = 100
y1 = 300
x2 = 800
y2 = 300

sprite1 = transform.scale(image.load('sprite1.png').convert_alpha(), (100, 100)) # Синий
sprite2 = transform.scale(image.load('sprite2.png').convert_alpha(), (100, 100)) # Красный
speed = 10

score1 = 0
score2 = 0
MAX_SCORE = 3

blue_is_chaser = True
round_time = 10 * 60

run = True
finish = False

def reset_round():
    global x1, y1, x2, y2, round_time, blue_is_chaser, finish
    x1 = 100
    y1 = 300
    x2 = 800
    y2 = 300
    round_time = 10 * 60
    blue_is_chaser = not blue_is_chaser

    if score1 >= MAX_SCORE or score2 >= MAX_SCORE:
        finish = True
        mixer.music.stop()
        end_sound.play()

def restart_game():
    global score1, score2, blue_is_chaser, finish, x1, y1, x2, y2, round_time
    score1 = 0
    score2 = 0
    blue_is_chaser = True
    finish = False
    x1 = 100
    y1 = 300
    x2 = 800
    y2 = 300
    round_time = 10 * 60
    mixer.music.play(-1)


while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_r and finish:
                restart_game()

    if not finish:
        window.blit(background, (0, 0))
        window.blit(sprite1, (x1, y1))
        window.blit(sprite2, (x2, y2))

        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and x1 > 5:
            x1 -= speed
        if keys_pressed[K_RIGHT] and x1 < win_width - 105:
            x1 += speed
        if keys_pressed[K_UP] and y1 > 5:
            y1 -= speed
        if keys_pressed[K_DOWN] and y1 < win_height - 105:
            y1 += speed

        if keys_pressed[K_a] and x2 > 5:
            x2 -= speed
        if keys_pressed[K_d] and x2 < win_width - 105:
            x2 += speed
        if keys_pressed[K_w] and y2 > 5:
            y2 -= speed
        if keys_pressed[K_s] and y2 < win_height - 105:
            y2 += speed

        round_time -= 1
        time_seconds = round_time // 60

        rect1 = Rect(x1 + 10, y1 + 10, 80, 80)
        rect2 = Rect(x2 + 10, y2 + 10, 80, 80)

        if rect1.colliderect(rect2):
            if blue_is_chaser:
                score1 += 1
            else:
                score2 += 1
            reset_round()

        elif round_time <= 0:
            if blue_is_chaser:
                score2 += 1
            else:
                score1 += 1
            reset_round()

        # Отрисовка интерфейса
        score_text = main_font.render(f"Синий {score1} : {score2} Красный", True, (255, 255, 255))
        window.blit(score_text, (win_width // 2 - score_text.get_width() // 2, 20))

        # Время
        timer_text = main_font.render(f"Время: {time_seconds}", True, (255, 255, 0))
        window.blit(timer_text, (win_width // 2 - timer_text.get_width() // 2, 70))

        if blue_is_chaser:
            role_text = info_font.render("Синий догоняет!", True, (0, 0, 255))
        else:
            role_text = info_font.render("Красный догоняет!", True, (200, 0, 0))
        window.blit(role_text, (win_width // 2 - role_text.get_width() // 2, 120))

    else:
        # Экран конца игры
        window.blit(background, (0, 0))
        
        if score1 >= MAX_SCORE:
            win_text = main_font.render("СИНИЙ ИГРОК ПОБЕДИЛ!", True, (0, 0, 255))
        else:
            win_text = main_font.render("КРАСНЫЙ ИГРОК ПОБЕДИЛ!", True, (255, 0, 0))
            
        window.blit(win_text, (win_width // 2 - win_text.get_width() // 2, win_height // 2 - 50))
        
        hint_text = info_font.render("Нажмите R для начала новой игры", True, (255, 255, 255))
        window.blit(hint_text, (win_width // 2 - hint_text.get_width() // 2, win_height // 2 + 30))

    display.update()
    clock.tick(60)