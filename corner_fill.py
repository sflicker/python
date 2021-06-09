import enum
from graphics import *

# define a Direction Enum with x and y directions
class Direction(enum.Enum):
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    DOWN = (0, -1)
    UP = (0, 1)

# define a pattern for the turtle to follow everytime it needs to turn
pattern = [Direction.RIGHT,
           Direction.UP,
           Direction.LEFT,
           Direction.DOWN,
           Direction.LEFT,
           Direction.UP]

# define a simple turtle class that tracks x and y positions, directions and a turn count.
class Turtle(object):
    def __init__(self):
        self.xpos = 0
        self.ypos = 0
        self.xdir = 0
        self.ydir = 0
        self.turn_count = 0;

#determine if the turtle needs to turn.
#if turtle would go off the grid
#if the turtle would revisit a cell
#every third turns the turtle only move once.
def need_to_turn_turtle(turtle, dim, visited):
    (nextx, nexty) = next_move_turtle(turtle)
    if nextx < 0 or nexty < 0 or nextx > dim-1 or nexty > dim-1 or turtle.turn_count % 3 == 0:
        return True
    if visited[nexty][nextx]:
        return True
    return False;

#get the next position if the turtle were to move
def next_move_turtle(turtle):
    nextx = turtle.xpos + 1 * turtle.xdir
    nexty = turtle.ypos + 1 * turtle.ydir
    return (nextx, nexty)

#turn turtle using pattern
def turn_turtle(turtle):
    (turtle.xdir, turtle.ydir) = pattern[turtle.turn_count % len(pattern)].value
    turtle.turn_count += 1

# move the turtle in using the directions
def move_turtle(turtle):
    turtle.xpos += turtle.xdir
    turtle.ypos += turtle.ydir

def corner_fill(square):
    print(square, len(square))

    if len(square) == 0:
        return []

    if len(square) == 1:
        return [square[0][0]];

    dim = len(square)
    # make a visited matrix so the turtle doesn't visit the same
    # cell more than once
    visited = [[False for i in range(dim)] for j in range(dim)]

    turtle = Turtle()

    v = []

    # start with initial turn and record starting pos
    turn_turtle(turtle)
    v.append(square[turtle.ypos][turtle.xpos])
    visited[0][0] = True

    # repeat until the turtle has visited dim^2 cells
    while len(v) < dim**2:
        #check if the turtle needs to turn
        if need_to_turn_turtle(turtle, dim, visited):
            turn_turtle(turtle)

        #move turtle and record position
        move_turtle(turtle)
        v.append(square[turtle.ypos][turtle.xpos])
        visited[turtle.ypos][turtle.xpos] = True

    return v


def main():
    win = GraphWin("My Circle", 1000, 1000)
    c = Circle(Point(50,50), 10)
    c.draw(win)
    win.getMouse() # Pause to view result
    win.close()    # Close window when done

main()

#
#
# square = [[1]]
# expected = [1]
# ans = corner_fill(square)
# print(ans)
# print(ans == expected)
#
# square = [[1,2],
#           [4,5]]
# expected = [1,2,5,4]
# ans = corner_fill(square)
# print(ans)
# print(ans == expected)
#
# square = [[1,2,3],
#           [4,5,6],
#           [7,8,9]]
# expected = [1,2,3,6,9,8,5,4,7]
# ans = corner_fill(square)
# print(ans)
# print(ans == expected)
