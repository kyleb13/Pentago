from PentagoBoard import PentagoBoard

class PentagoTreeNode:
    def __init__(self, newParent = None, newBoard: PentagoBoard = None, newOwner:str = "", newMinmaxVal = 0):
        self.parent = newParent
        self.board = newBoard
        self.children = []
        self.owner = newOwner
        self.minmax = newMinmaxVal

    def oppositeOwner(self):
        if self.owner == "w":
            return "b"
        else:
            return "w"




