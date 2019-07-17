import API
import sys
import random

def log(string):
    sys.stderr.write("{}\n".format(string))


class ChoiceCell():
    def __init__(self, paths):
        self.paths = paths

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
