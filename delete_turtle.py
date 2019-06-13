import turtle
wn = turtle.Screen()
wn.bgcolor("lightgreen")
tess = turtle.Turtle()
tess.color("blue")
tess.shape("turtle")

# print(range(5,60,2))
tess.up()                       # this is another way to pick up the pen
for dist in range(5,60,2):      # start with dist = 5 and grow by 2
    tess.stamp()                # leave an impression on the canvas
    tess.forward(dist)          # move tess along
    tess.right(24)              # and turn her

wn.exitonclick()