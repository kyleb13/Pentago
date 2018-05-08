from PentagoBoard import PentagoBoard
import sys

class PentagoTreeNode:
    def __init__(self, newParent = None, newMove: list = [], newOwner:str = "", newMinmaxVal = 0):
        self.parent = newParent
        if self.parent != None:
            self.moves = [x for x in newParent.moves]
            self.moves.append(newMove)
        else:
            self.moves = []
        self.children = []
        self.owner = newOwner
        self.minmax = newMinmaxVal
        self.alpha = -(sys.maxsize) -1
        self.beta = sys.maxsize

    def oppositeOwner(self):
        if self.owner == "w":
            return "b"
        else:
            return "w"