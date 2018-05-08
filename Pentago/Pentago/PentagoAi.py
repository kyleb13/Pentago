from PentagoTree import PentagoTree
from PentagoBoard import PentagoBoard
from PentagoTreeNode import PentagoTreeNode

class PentagoAi:
    def __init__(self, newTree:PentagoTree, newBoard: PentagoBoard):
        self.tree = newTree
        self.board = newBoard
        self.calculateMinmaxVals(self.tree.head)


   