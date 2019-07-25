import API
import sys
import random

ChoiceCells = []

def log(string):
    sys.stderr.write("{}\n".format(string))


class ChoiceCell():
    def __init__(self, paths, coord):
        self.paths = paths
        self.coord = coord

    def con_cells(self):
        cells =[]
        for path in self.paths:
            if path.cell1 == self:
                cells.append(path.cell2)
            else:
                cells.append(path.cell1)
        return cells

    def is_con(self, cell):
        cells = self.con_cells
        if cells.contains(cell):
            return True
        return False

class Path():
    def __init__(self, length, turns, cell1, cell2):
        self.length = length
        self.turns = turns
        self.cell1 = cell1
        self.cell2 = cell2

    def goes_to(self, cell):
        if self.cell1 == cell:
            return self.cell2
        return self.cell1

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
        self.paths = {}
        self.path = ["", 0]

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

    def explore(self):
        self.go()
        while True:
            if not self.choices:
                self.go_back()
            else:
                dirs = [[0, 1], [1, 0], [0, -1], [-1, 0]]
                cell_choices = [(self.pos[0]+dirs[choice][0], self.pos[1]+dirs[choice][1]) for choice in self.choices]
                for i, choice in enumerate(cell_choices):
                    if choice not in self.cells:
                        self.turn_to(self.choices[i])
                        self.go()
                        break
                    elif cell_choices[i] == cell_choices[-1]:
                        self.turn_to(self.choices[i])
                        self.go()
                        break

    def find_best(self):
        return

    def go_to_cell(self):
        return

    def take_path(self, string):
        for char in string:
            self.go()
            self.turn_to(int(char))

def main():
    bob = Mouse()
    
