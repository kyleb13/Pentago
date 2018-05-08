
from PentagoTreeNode import PentagoTreeNode
from PentagoBoard import PentagoBoard

class PentagoTree:
    def __init__(self, initialState: PentagoBoard, playerTurn: str):
        self.head = PentagoTreeNode(None, initialState, playerTurn, 0)
        self.rootState = PentagoBoard(initialState.state)
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


    def createChildren(self, node:PentagoTreeNode, depth) -> list:
        master = PentagoBoard(self.rootState.state)
        for cmd in node.moves:
            master.place(cmd[0], (cmd[1][0], cmd[1][1]))
            master.rotateSquare(int(cmd[2][0]), cmd[2][1])
        newowner = node.oppositeOwner()
        for y in range(0,6):#iterate over rows
            for x in range(0,6):#iterate over columns
                if master.state[y][x] == "-":
                    for i in range(1,5):#iterate over squares for rotating
                        for el in ["L", "R"]: #square can be rotated left or right
                            child = PentagoTreeNode(node, [node.owner,[y,x], str(i) + el], newowner, 0)
                            node.children.append(PentagoTreeNode(node, child)


    def calculateMinmaxVals(self, node:PentagoTreeNode, board: PentagoBoard):
        if node.children == []:
            node.minmax = self.stateValue(node.moves[len(node.moves) - 1], board)
        else:
            move = None
            if node.moves != []:
                move = node.moves[len(node.moves) - 1]
                board.place(move[0], (move[1][0], move[1][1]))
                board.rotateSquare(int(move[2][0]), move[2][1])
            #calculate minmax for all children
            for child in node.children:
                self.calculateMinmaxVals(child, board)
            #undo changes to the board
            if move != None:
                board.remove((move[1][0], move[1][1]))
                undo = "L"
                if move[2][1] == "L":
                    undo = "R"
                board.rotateSquare(int(move[2][0]), undo)
            #get min or max minmax value from children
            valarr = [x.minmax for x in node.children]
            if node.owner == "w":
                node.minmax = max(valarr)
            else:
                node.minmax = min(valarr)
            


    def testChar(self, char, counts, totals):
        if char != "-":
            if char == "w":
                counts[0] = counts[0]*2 if counts[0]>0 else 1
                totals[1] += counts[1]
                counts[1] = 0
            elif char == "b":
                counts[1] = counts[1]*2 if counts[1]<0 else -1
                totals[0] += counts[0]
                counts[0] = 0
        else:
            totals[1] += counts[1]
            counts[1] = 0
            totals[0] += counts[0]
            counts[0] = 0

    #get the minmax value of a particular state given
    #the moves needed to get to that state
    def stateValue(self, move:list, pboard:PentagoBoard):
        pboard.place(move[0], (move[1][0], move[1][1]))
        pboard.rotateSquare(int(move[2][0]), move[2][1])
        counts = [0,0]
        totals = [0,0]
        for a in range(0,6):
            for b in range(0,6):
                char = pboard.state[a][b]
                self.testChar(char, counts, totals)

        counts = [0,0]
        for d in range(0, 6):#check columns for chars in a row
            for c in range(0, 6):
                char = pboard.state[c][d]
                self.testChar(char, counts, totals)

        counts = [0,0]
        for e in range(-1, 2):#check diagonals (left to right) for 5 in a row
            for f in range(0, 6):
                char = pboard.state[f][f]
                if e == -1:
                    char = pboard.state[f+1][f]
                elif e == 1:
                    char = pboard.state[f][f+1]
                self.testChar(char, counts, totals)
                if e!=0 and f==4:
                    break

        counts = [0,0]
        for e in range(-1, 2):#check diagonals (right to left) for 5 in a row
            wcnt = 0
            bcnt = 0
            for f in range(5, -1, -1):
                char = pboard.state[5 - f][f]
                if e==-1:
                    char = pboard.state[6-f][f]
                elif e == 1:
                    char = pboard.state[5-f][f-1]
                self.testChar(char, counts, totals)
                if e!=0 and f==1:
                    break

        pboard.remove((move[1][0], move[1][1]))
        undo = "L"
        if move[2][1] == "L":
            undo = "R"
        pboard.rotateSquare(int(move[2][0]), undo)
        return totals[0] + totals[1]
        