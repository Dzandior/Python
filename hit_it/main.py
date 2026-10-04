from turtle import *
import time
from pygame import mixer

mixer.init()
mixer.music.load('bgm.mp3')
mixer.music.set_volume(0.6)
mixer.music.play(-1)
end_sound = mixer.Sound('end.mp3')

class Sprite(Turtle):
    def __init__(self, x, y, color_name, shape_name, step=10):
        super().__init__()
        self.penup()
        self.speed(0)
        self.goto(x, y)
        self.color(color_name)
        self.shape(shape_name)
        self.step = step

    def is_collide(self, sprite_target):
        dist = self.distance(sprite_target.xcor(), sprite_target.ycor())
        return dist <= 25

    def set_move(self, x_start, y_start, x_finish, y_finish):
        self.x_start = x_start
        self.y_start = y_start
        self.x_finish = x_finish
        self.y_finish = y_finish
        self.goto(x_start, y_start)
        self.setheading(self.towards(x_finish, y_finish))

    def make_step(self):
        self.forward(self.step)
        if self.distance(self.x_finish, self.y_finish) < self.step:
            self.set_move(self.x_finish, self.y_finish, self.x_start, self.y_start)

scr = Screen()
scr.setup(width=500, height=500)
scr.bgcolor("white")
scr.title("Аркада: Обойди врагов")
scr.tracer(0)

player = Sprite(0, -220, 'blue', 'circle', 5)
finish = Sprite(0, 220, 'gold', 'square', 0)
enemies = []

pen = Turtle()
pen.hideturtle()
pen.penup()

def update_text(current_level):
    pen.clear()
    pen.goto(0, 220)
    pen.color("black")
    pen.write(f"Уровень: {current_level} / 5", align="center", font=("Arial", 16, "bold"))

def load_level(level):
    global enemies
    for e in enemies:
        e.hideturtle()
    enemies.clear()

    player.goto(0, -220)
    player.showturtle()
    finish.showturtle()

    if level == 1:
        e1 = Sprite(-230, -70, 'red', 'triangle', 3)
        e1.set_move(-230, -70, 230, -70)
        e2 = Sprite(230, 70, 'red', 'triangle', 6)
        e2.set_move(230, 70, -230, 70)
        enemies.extend([e1, e2])

    elif level == 2:
        e1 = Sprite(-230, -100, 'red', 'triangle', 4)
        e1.set_move(-230, -100, 230, -100)
        e2 = Sprite(230, 0, 'red', 'triangle', 7)
        e2.set_move(230, 0, -230, 0)
        e3 = Sprite(-230, 100, 'red', 'triangle', 3)
        e3.set_move(-230, 100, 230, 100)
        enemies.extend([e1, e2, e3])

    elif level == 3:
        e1 = Sprite(-230, -120, 'red', 'triangle', 5)
        e1.set_move(-230, -120, 230, -120)
        e2 = Sprite(230, -40, 'red', 'triangle', 8)
        e2.set_move(230, -40, -230, -40)
        e3 = Sprite(-230, 40, 'red', 'triangle', 3)
        e3.set_move(-230, 40, 230, 40)
        e4 = Sprite(230, 120, 'red', 'triangle', 6)
        e4.set_move(230, 120, -230, 120)
        enemies.extend([e1, e2, e3, e4])

    elif level == 4:
        speeds = [4, 7, 3, 8, 5]
        ys = [-140, -70, 0, 70, 140]
        for i, y in enumerate(ys):
            start_x = -230 if i % 2 == 0 else 230
            end_x = 230 if i % 2 == 0 else -230
            e = Sprite(start_x, y, 'red', 'triangle', speeds[i])
            e.set_move(start_x, y, end_x, y)
            enemies.append(e)

    elif level == 5:
        speeds = [5, 9, 4, 7, 3, 8, 6]
        ys = [-150, -100, -50, 0, 50, 100, 150]
        for i, y in enumerate(ys):
            start_x = -230 if i % 2 == 0 else 230
            end_x = 230 if i % 2 == 0 else -230
            e = Sprite(start_x, y, 'red', 'triangle', speeds[i])
            e.set_move(start_x, y, end_x, y)
            enemies.append(e)

    update_text(level)

keys = {'w': False, 'a': False, 's': False, 'd': False}

def key_press(k):
    keys[k] = True

def key_release(k):
    keys[k] = False

scr.listen()
for k in keys:
    scr.onkeypress(lambda key=k: key_press(key), k)
    scr.onkeyrelease(lambda key=k: key_release(key), k)

def restart_game():
    global level, game_over, waiting_restart
    level = 1
    game_over = False
    waiting_restart = False
    pen.clear()
    mixer.music.play(-1)
    load_level(level)

scr.onkey(restart_game, 'r')
scr.onkey(restart_game, 'R')

level = 1
load_level(level)
game_over = False
waiting_restart = False

while True:
    if not game_over and not waiting_restart:
        if keys['w'] and player.ycor() < 230:
            player.goto(player.xcor(), player.ycor() + player.step)
        if keys['s'] and player.ycor() > -230:
            player.goto(player.xcor(), player.ycor() - player.step)
        if keys['a'] and player.xcor() > -230:
            player.goto(player.xcor() - player.step, player.ycor())
        if keys['d'] and player.xcor() < 230:
            player.goto(player.xcor() + player.step, player.ycor())

        for e in enemies:
            e.make_step()
            if player.is_collide(e):
                game_over = True

        if player.is_collide(finish):
            level += 1
            if level <= 5:
                load_level(level)
            else:
                waiting_restart = True
                mixer.music.stop()
                end_sound.play()
                for e in enemies:
                    e.hideturtle()
                player.hideturtle()
                finish.hideturtle()
                pen.clear()
                pen.goto(0, 20)
                pen.color("green")
                pen.write("ВЫ ПРОШЛИ ИГРУ!", align="center", font=("Arial", 26, "bold"))
                pen.goto(0, -30)
                pen.color("black")
                pen.write("Нажмите R для рестарта", align="center", font=("Arial", 14, "normal"))

        scr.update()
        time.sleep(0.02)

    elif game_over:
        mixer.music.stop()
        end_sound.play()
        for e in enemies:
            e.hideturtle()
        player.hideturtle()
        finish.hideturtle()
        pen.clear()
        pen.goto(0, 20)
        pen.color("red")
        pen.write("ВЫ ПРОИГРАЛИ!", align="center", font=("Arial", 28, "bold"))
        pen.goto(0, -30)
        pen.color("black")
        pen.write("Нажмите R для рестарта", align="center", font=("Arial", 14, "normal"))
        scr.update()
        waiting_restart = True
        game_over = False

    else:
        scr.update()
        time.sleep(0.05)