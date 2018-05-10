from PentagoTree import PentagoTree
from PentagoBoard import PentagoBoard
from PentagoTreeNode import PentagoTreeNode

class PentagoAi:
    def __init__(self, newTree:PentagoTree, newBoard: PentagoBoard, newToken: str):
        self.tree = newTree
        self.board = newBoard
        self.atLeafLevel = True
        self.current = self.tree.head
        self.currentState = PentagoBoard(newBoard.state)
        self.token = newToken

    def setUp(self):
        if(self.tree.head.children != []):
            self.tree = PentagoTree(self.board, self.token)
            self.current = self.tree.head
        self.tree.generateTree(2)
        self.tree.calculateMinmaxVals(self.tree.head)
        print()
        self.atLeafLevel = False

    def processPlayerMove(self, move):
        childMoves = [x.moves for x in self.current.children]
        idx = -1
        for x in range(0, len(childMoves)):
            cm = childMoves[x]
            if cm[0] == move[0] and cm[1][0] == move[1][0] and cm[1][1] == move[1][1] and cm[2] == move[2]:
                idx = x
                break

        self.current = self.current.children[idx]
        if self.current.children == []:
            self.atLeafLevel = True
        
    def makeMove(self):
        options = [x.minmax for x in self.current.children]
        optimalchoice = min(options) if self.token == "b" else max(options)
        for i in range(0, len(self.current.children)):
            if self.current.children[i].minmax == optimalchoice:
                move = self.current.children[i].moves
                self.current = self.current.children[i]
                self.board.place(self.token, (move[1][0], move[1][1]))
                self.board.rotateSquare(int(move[2][0]), move[2][1])
                if self.current.children == []:
                    self.atLeafLevel = True
                return  