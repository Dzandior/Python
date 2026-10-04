from random import randint
from turtle import *
from pygame import mixer

mixer.init()
mixer.music.load('bgm.mp3')
mixer.music.set_volume(0.6)
win_sound = mixer.Sound('win.mp3')

scr = Screen()
scr.title("Turtle Race")

drawer = Turtle()
drawer.hideturtle()
drawer.speed(0)

t1 = Turtle()
t2 = Turtle()
t3 = Turtle()

turtles_data = [
    (t1, "red", "Черепашка 1 (Красная)"),
    (t2, "blue", "Черепашка 2 (Синяя)"),
    (t3, "orange", "Черепашка 3 (Оранжевая)")
]

def draw_track():
    drawer.clear()
    drawer.setheading(270)
    a = -190
    b = 150
    for i in range(22):
        drawer.penup()
        drawer.goto(a, b)
        drawer.pendown()
        drawer.forward(320)
        a += 20

def start_race():
    mixer.music.stop()
    mixer.music.play(-1)
    
    draw_track()

    y_positions = [100, 0, -100]
    for i, (t, color, name) in enumerate(turtles_data):
        t.penup()
        t.shape("turtle")
        t.color(color)
        t.goto(-200, y_positions[i])
        t.setheading(0)
        t.pendown()
    
    finish_line = 230
    winner = None

    racing = True
    while racing:
        for t, color, name in turtles_data:
            t.forward(randint(1, 7))
            if t.xcor() >= finish_line:
                winner = (color, name)
                racing = False
                break

    mixer.music.stop()
    win_sound.play()

    drawer.penup()
    drawer.goto(0, 180)
    drawer.color(winner[0])
    drawer.write(f"{winner[1]} победила!\nНажмите R для рестарта", align="center", font=("Arial", 18, "bold"))

scr.listen()
scr.onkey(start_race, 'r')
scr.onkey(start_race, 'R')

start_race()

done()