import API
import sys
import random

def log(string):
    sys.stderr.write("{}\n".format(string))

class Mouse():
    def __init__(self):
        self.X = 0
        self.Y = 0
        self.pos = (0, 0)
        self.face = 0
        self.choices = []
        self.dead = False
        self.loop = False
        self.cells = []

    def get_choices(self):
        options = [3, 0, 1]
        walls = [API.wallLeft(), API.wallFront(), API.wallRight()]
        choices = [(opt+self.face)%4 for i, opt in enumerate(options) if not walls[i]]
        return choices

    def turn_to(self, dirto):
        if (self.face-1)%4 == int(dirto):
            API.turnLeft()
            self.face = (self.face-1)%4
        else:
            while self.face != int(dirto):
                API.turnRight()
                self.face = (self.face+1)%4

    def update_pos(self):
        dirs = [[0, 1], [1, 0], [0, -1], [-1, 0]]
        dis = dirs[self.face]
        self.X += dis[0]
        self.Y += dis[1]
        self.pos = (self.X, self.Y)

    def go_back(self):
        self.turn_to((self.face+2)%4)
        self.go()

    def go(self):
        API.setColor(self.X, self.Y, "g")
        if not self.dead:
            self.cells.append(self.pos)
        API.moveForward()
        self.update_pos()
        if self.pos not in self.cells:
            self.cells.append(self.pos)
        choices = self.get_choices()
        while choices and len(choices) < 2:
            API.setColor(self.X, self.Y, "g")
            if not self.dead:
                self.cells.append(self.pos)
            self.turn_to(choices[0])
            API.moveForward()
            self.update_pos()
            if self.pos not in self.cells:
                self.cells.append(self.pos)
            choices = self.get_choices()
        self.choices = choices

def main():
    bob = Mouse()
    bob.go()
    while True:
        if not bob.choices:
            bob.go_back()
        else:
            dirs = [[0, 1], [1, 0], [0, -1], [-1, 0]]
            cell_choices = [(bob.pos[0]+dirs[choice][0], bob.pos[1]+dirs[choice][1]) for choice in bob.choices]
            for i, choice in enumerate(cell_choices):
                if choice not in bob.cells:
                    bob.turn_to(bob.choices[i])
                    bob.go()
                    break
                elif cell_choices[i] == cell_choices[-1]:
                    bob.turn_to(bob.choices[i])
                    bob.go()
                    break
        


if __name__ == "__main__":
    main()
    
    