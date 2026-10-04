from turtle import *

scr = Screen()
scr.setup(width=900, height=600)
scr.title("Графический редактор")
scr.tracer(0)

t = Turtle()
t.color('blue')
t.width(5)
t.speed(0)
t.shape('circle')
t.pendown()

ui = Turtle()
ui.hideturtle()
ui.penup()
ui.speed(0)

sep = Turtle()
sep.hideturtle()
sep.penup()
sep.speed(0)
sep.width(2)
sep.color('gray')
sep.goto(210, 280)
sep.pendown()
sep.goto(210, -280)

hints = [
    ("УПРАВЛЕНИЕ:", 14, "bold"),
    ("ЛКМ (зажать) — Рисовать", 10, "normal"),
    ("ПКМ — Переместить перо", 10, "normal"),
    ("", 8, "normal"),
    ("ЦВЕТА:", 12, "bold"),
    ("1 — Красный", 10, "normal"),
    ("2 — Зеленый", 10, "normal"),
    ("3 — Желтый", 10, "normal"),
    ("4 — Черный", 10, "normal"),
    ("5 — Синий", 10, "normal"),
    ("6 — Серый", 10, "normal"),
    ("7 — Фиолетовый", 10, "normal"),
    ("", 8, "normal"),
    ("КОМАНДЫ:", 12, "bold"),
    ("C — Нарисовать круг", 10, "normal"),
    ("Q — Начать заливку", 10, "normal"),
    ("E — Закончить заливку", 10, "normal"),
    ("Z — Очистить холст", 10, "normal"),
    ("", 8, "normal"),
    ("ДВИЖЕНИЕ:", 12, "bold"),
    ("Стрелки — Точный сдвиг", 10, "normal"),
]

y_pos = 250
for text, font_size, font_type in hints:
    ui.goto(225, y_pos)
    ui.write(text, font=("Arial", font_size, font_type))
    y_pos -= 22

def draw(x, y):
    t.goto(x, y)
    scr.update()

t.ondrag(draw)

def move(x, y):
    t.penup()
    t.goto(x, y)
    t.pendown()
    scr.update()

scr.onscreenclick(move, btn=3)
scr.listen()

def setRed():
    t.color('red')
    scr.update()

def setGreen():
    t.color('green')
    scr.update()

def setBlue():
    t.color('blue')
    scr.update()

def setYellow():
    t.color('yellow')
    scr.update()

def setBlack():
    t.color('black')
    scr.update()

def setGray():
    t.color('gray')
    scr.update()

def setViolet():
    t.color('violet')
    scr.update()

def clear():
    t.clear()
    scr.update()

def detCircle():
    t.circle(25)
    scr.update()

def setbegin_fill():
    t.begin_fill()

def setend_fill():
    t.end_fill()
    scr.update()

def stepRight():
    t.goto(t.xcor() + 5, t.ycor())
    scr.update()

def stepLeft():
    t.goto(t.xcor() - 5, t.ycor())
    scr.update()

def stepUP():
    t.goto(t.xcor(), t.ycor() + 5)
    scr.update()

def stepDown():
    t.goto(t.xcor(), t.ycor() - 5)
    scr.update()

scr.onkey(setRed, '1')
scr.onkey(setGreen, '2')
scr.onkey(setYellow, '3')
scr.onkey(setBlack, '4')
scr.onkey(setBlue, '5')
scr.onkey(setGray, '6')
scr.onkey(setViolet, '7')
scr.onkey(clear, 'z')
scr.onkey(detCircle, 'c')
scr.onkey(setbegin_fill, 'q')
scr.onkey(setend_fill, 'e')
scr.onkey(stepRight, 'Right')
scr.onkey(stepLeft, 'Left')
scr.onkey(stepUP, 'Up')
scr.onkey(stepDown, 'Down')

scr.update()
done()