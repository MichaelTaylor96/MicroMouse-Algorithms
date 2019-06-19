import API
import sys
import random

def log(string):
    sys.stderr.write("{}\n".format(string))

def cell_state(X, Y, face, cells):
    newX = X + face[0]
    newY = Y + face[1]
    return cells[newX][newY]

def main():
    X = 0
    Y = 0
    face = 0
    dirs = [[0, 1], [1, 0], [0, -1], [-1, 0]]
    cards = ["n", "e", "s", "w"]
    dead = False
    cells = [["live" for num in range(API.mazeHeight())] for num in range(API.mazeWidth())]
    while True:
        i = 0
        walls = [API.wallLeft(), API.wallFront(), API.wallRight()]
        choices = [boolean for boolean in walls if not boolean]
        if len(choices) > 1:
            dead = False
        if dead:
            API.setColor(X, Y, "g")
            cells[X][Y] = "dead"
        if not API.wallLeft() and cell_state(X, Y, dirs[(face-1)%4], cells) == "live":
            face = (face-1) % 4
            API.turnLeft()
        while API.wallFront() or cell_state(X, Y, dirs[face], cells) == "dead":
            i += 1
            if i == 2:
                dead = True
                API.setColor(X, Y, "g")
                cells[X][Y] = "dead"
            face = (face+1) % 4
            API.turnRight()
        X += dirs[face][0]
        Y += dirs[face][1]
        string = "{X}, {Y}".format(X=X, Y=Y)
        log(string)
        API.moveForward()
        if API.wallLeft():
            API.setWall(X, Y, cards[(face-1)%4])
        if API.wallFront():
            API.setWall(X, Y, cards[face])
        if API.wallRight():
            API.setWall(X, Y, cards[(face+1)%4])


if __name__ == "__main__":
    main()
    
