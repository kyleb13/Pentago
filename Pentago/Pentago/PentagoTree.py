
from PentagoTreeNode import PentagoTreeNode
from PentagoBoard import PentagoBoard
from copy import deepcopy 

class PentagoTree:
    def __init__(self, initialState: PentagoBoard, playerTurn: str):
        self.head = PentagoTreeNode(None, initialState, playerTurn, 0)
        self.leaflist = []
        self.leaflist.append(self.head)


    def generateTree(self, depth):
        for x in range(1, depth+1):
            toadd = []
            for node in self.leaflist:
                self.createChildren(node)
                toadd.extend(node.children)
            self.leaflist.clear()
            self.leaflist = toadd
            print("Level %d Created" % (x))


    def createChildren(self, node:PentagoTreeNode) -> list:
        newowner = node.oppositeOwner()
        for y in range(0,6):#iterate over rows
            for x in range(0,6):#iterate over columns
                if node.board.state[y][x] == "-":
                    for i in range(1,5):#iterate over squares for rotating
                        for el in ["L", "R"]: #square can be rotated left or right
                            newBoard = PentagoBoard(node.board.state)
                            newBoard.place(node.owner, (y,x))
                            newBoard.rotateSquare(i, el)
                            node.children.append(PentagoTreeNode(node, newBoard, newowner, 0))
        