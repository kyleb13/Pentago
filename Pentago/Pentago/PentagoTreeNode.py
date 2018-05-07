class PentagoTreeNode:
    def __init__(self, newParent: PentagoTreeNode = None, newState: list = [], newOwner:str = "", newMinmaxVal = 0):
        self.parent = newParent
        self.state = [[i for i in row] for row in newState]
        self.children = []
        self.owner = newOwner
        self.minmax = newMinmaxVal





