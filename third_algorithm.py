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

    def go_back(self, dirto):
        self.turn_to(dirto)
        self.go()
        self.path = self.paths[self.pos][0]

    def go(self):
        API.moveForward()
        moves = 1
        self.update_pos()
        choices = self.get_choices()
        while choices and len(choices) < 2:
            self.turn_to(choices[0])
            API.moveForward()
            moves += 1
            self.update_pos()
            choices = self.get_choices()
        self.path[1] += moves
        self.choices = choices

    def find_best(self, direction):
        self.turn_to(direction)
        if self.pos in self.paths:
            self.paths[self.pos][1] += str(self.face)
        self.go()
        if self.pos not in self.paths:
            self.paths[self.pos] = [[self.path[0], self.path[1]], "{}".format((self.face+2)%4)]
        elif self.paths[self.pos][0][1] > self.path[1]:
            self.paths[self.pos] = [[self.path[0], self.path[1]], "{}".format((self.face+2)%4)]
        if not self.choices:
            val = self.path[1]
            self.dead = True
            self.go_back((self.face-2)%4)
            return val
        options = []
        for choice in self.choices:
            if str(choice) not in self.paths[self.pos][1]:
                self.dead = False
                self.path[0] += str(choice)
                options.append(self.paths[self.pos][0][1] + self.find_best(choice))
        if self.dead:
            self.go_back(int(self.paths[self.pos][1][0]))
        else:
            val = self.path[1]
            self.dead = True
            self.go_back((self.face-2)%4)
            return val
        return max(options)

    def take_path(self, string):
        for char in string:
            self.go()
            self.turn_to(int(char))

def main():
    bob = Mouse()
    bob.paths[bob.pos] = [["", 0], ""]
    bob.find_best(bob.face)
    solution = bob.paths[(8, 8)][0][0]
    bob.turn_to(0)
    bob.take_path(solution)
