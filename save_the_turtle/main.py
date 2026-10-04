from time import time, sleep
from turtle import *
from random import randint, random
from pygame import mixer

mixer.init()
mixer.music.load('bgm.mp3')
mixer.music.set_volume(0.6)

win_sound = mixer.Sound('win.mp3')
lose_sound = mixer.Sound('lose.mp3')

scr = Screen()
scr.setup(600, 600)
scr.title("save turtles")
scr.tracer(0)

t1 = Turtle()
t2 = Turtle()
t3 = Turtle()

pen = Turtle()
pen.hideturtle()
pen.penup()

def setup_turtles():
    configs = [(t1, "cyan", 135), (t2, 'green', 270), (t3, 'yellow', 45)]
    for t, color, angle in configs:
        t.penup()
        t.clear()
        t.shape('turtle')
        t.color(color)
        t.goto(0, 0)
        t.setheading(angle)
        t.pendown()
        t.showturtle()

def rand_move(t):
    if not game_over:
        t.penup()
        t.goto(randint(-125, 125), randint(-90, 90))
        t.pendown()
        t.setheading(randint(0, 360))

t1.onclick(lambda x, y: rand_move(t1))
t2.onclick(lambda x, y: rand_move(t2))
t3.onclick(lambda x, y: rand_move(t3))

game_duration = 120
start_time = 0
game_over = False

def restart_game():
    global start_time, game_over
    mixer.music.stop()
    mixer.music.play(-1)
    setup_turtles()
    start_time = time()
    game_over = False
    pen.clear()

scr.listen()
scr.onkey(restart_game, 'r')
scr.onkey(restart_game, 'R')

restart_game()

while True:
    scr.update()
    sleep(0.02)

    if not game_over:
        elapsed = time() - start_time
        time_left = max(0, game_duration - int(elapsed))

        speed_multiplier = round(1.0 + (int(elapsed) // 10) * 0.1, 1)

        pen.clear()
        pen.goto(0, 250)
        pen.color('black')
        pen.write(f"Осталось: {time_left} сек  |  Ускорение: x{speed_multiplier:.1f}", align="center", font=('Arial', 14, 'bold'))

        for t in (t1, t2, t3):
            t.forward(1.2 * speed_multiplier)
            if random() < 0.25:
                t.left(randint(-35, 35))

        lost = False
        for t in (t1, t2, t3):
            if abs(t.xcor()) > 250 or abs(t.ycor()) > 250:
                lost = True
                break

        if lost:
            game_over = True
            mixer.music.stop()
            lose_sound.play()
            pen.goto(0, 0)
            pen.color('red')
            pen.write('You lose!\nНажмите R для рестарта', align="center", font=('Arial', 24, 'bold'))

        elif time_left <= 0:
            game_over = True
            mixer.music.stop()
            win_sound.play()
            pen.goto(0, 0)
            pen.color('green')
            pen.write('You win!\nНажмите R для рестарта', align="center", font=('Arial', 24, 'bold'))

scr.mainloop()