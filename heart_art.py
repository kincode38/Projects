import turtle
import math 
import random

screen = turtle.Screen()
screen.bgcolor("black")

t = turtle.Turtle()  # FIX 1: Create turtle first
t.speed(0)
t.hideturtle()
t.pensize(1)

colors = ["red", "pink", "yellow", "indigo", "violet", "magenta", "crimson"]

for i in range(120):
    t.penup()  # FIX 2
    t.goto(0, 0)
    
    angle = i * (math.pi * 2) / 120  # FIX 3: use i not 1
    
    # FIX 4: Heart formula in ONE block
    x = 16 * (math.sin(angle) ** 3) * 10
    y = (13 * math.cos(angle) 
         - 5 * math.cos(2 * angle) 
         - 2 * math.cos(3 * angle) 
         - math.cos(4 * angle)) * 10
    
    c = random.choice(colors)
    t.color(c)  # FIX 5
    t.pendown()
    t.goto(x, y)
    
    for _ in range(8):
        t.forward(6)
        t.backward(6)
        t.right(45)

turtle.done()