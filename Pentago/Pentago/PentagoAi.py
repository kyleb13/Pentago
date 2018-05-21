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

    #generate the tree based on the current state.
    def setUp(self):
        if(self.tree.head.children != []):
            self.tree = PentagoTree(self.board, self.token)
            self.current = self.tree.head
        self.tree.generateTree(2)#create nodes for tree
        self.tree.initChildStateValues()#calculate the minmax for leaf level nodes
        self.tree.calculateMinmaxVals(self.tree.head)#run minmax algorithm
        self.prune(self.tree.head, self.tree.head.alpha, self.tree.head.beta)#run alpha-beta pruning
        self.atLeafLevel = False

    #update the tree with the move the player made
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
    
    #Make a move for the ai
    def makeMove(self):
        options = [x.minmax for x in self.current.children]
        optimalchoice = min(options) if self.token == "b" else max(options) #find what the optimal minmax value is
        for i in range(0, len(self.current.children)):#search for the node with that minmax value
            if self.current.children[i].minmax == optimalchoice:
                move = self.current.children[i].moves
                self.current = self.current.children[i]
                self.board.place(self.token, (move[1][0], move[1][1]))
                self.board.rotateSquare(int(move[2][0]), move[2][1])
                if self.current.children == []:
                    self.atLeafLevel = True
                return self.playerReadableMove(move)
    
    #convert an index to a square number
    def idxToSquare(self, idx):
        square = 0
        if idx[0]<=2 and idx[1] <=2:
            square =1
        elif idx[0]<=2 and idx[1] > 2:
            square =2
        elif idx[0]>2 and idx[1] <=2:
            square =3
        else:
            square = 4
        return square

    #convert a board readable move to the original input format
    def playerReadableMove(self, inmove):
        square = self.idxToSquare(inmove[1])
        spot = 0
        idx = inmove[1]
        if square == 1 or square == 2:
            #find which location the index corresponds to
            if idx[0] == 0:
                spot = idx[1]+1 if square == 1 else idx[1]-2
            elif idx[0] == 1:
                spot = idx[1]+4 if square == 1 else idx[1]+1
            elif idx[0] == 2:
                spot = idx[1]+7 if square == 1 else idx[1]+3
        else:
            #find which location the index corresponds to
            if idx[0] == 3:
                spot = idx[1]+1 if square == 3 else idx[1]-2
            elif idx[0] == 4:
                spot = idx[1]+4 if square == 3 else idx[1]+1
            elif idx[0] == 5:
                spot = idx[1]+7 if square == 3 else idx[1]+3
        return str(square) + "/" + str(spot) + " " + inmove[2]

    #a recursive implementation of the ab pruning algorithm
    def prune(self, node:PentagoTreeNode, inalpha, inbeta):
        if node.children == []:#base case
            return node.minmax#return nodes minmax val if at leaf level
        else:
            #inherit parent's ab values
            node.alpha = inalpha
            node.beta = inbeta
            idx = 0
            for child in node.children:
                val = self.prune(child, node.alpha, node.beta)#go further down the tree if not at leaf level
                if node.owner == "w":# w is MAX
                    node.alpha = val if val>node.alpha else node.alpha #update alpha if MAX
                else:#b is MIN
                    node.beta = val if val<node.beta else node.beta#Update beta if MIN
                if node.alpha>node.beta:
                    node.children = node.children[0:idx + 1]#delete nodes to the right if a>b
                    break
                idx += 1
            return node.minmax