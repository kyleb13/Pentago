from PentagoTreeNode import PentagoTreeNode
from PentagoBoard import PentagoBoard

class PentagoTree:
    def __init__(self, initialState: PentagoBoard, playerTurn: str):
        self.head = PentagoTreeNode(None, [], playerTurn, 0)
        self.rootState = initialState
        self.leaflist = []
        self.leaflist.append(self.head)
        self.testvals = [(a,b) for a in range(0,6) for b in range(0,6)]
        self.rotatevals = [(c, d) for c in range(1,5) for d in ("L", "R")]
        self.adjacentMap = {}
        self.buildAdjacentcyMap()

    def buildAdjacentcyMap(self):
        lmdiag = [(x,x) for x in range(0,6)]
        ludiag = [(x,x+1) for x in range(0,5)]
        lldiag = [(x+1,x) for x in range(0,5)]
        rmdiag = [(5-x,x) for x in range(5, -1, -1)]
        rudiag = [(4-x,x) for x in range(4, -1, -1)]
        rldiag = [(6-x,x) for x in range(5, 0, -1)]
        for val in self.testvals:
            diags = []
            if val in lmdiag:
                diags.append("lm")
            if val in ludiag:
                diags.append("lu")
            if val in lldiag:
                diags.append("ll")
            if val in rmdiag:
                diags.append("rm")
            if val in rudiag:
                diags.append("ru")
            if val in rldiag:
                diags.append("rl")
            self.adjacentMap[val] = [val[0], val[1], diags]


    def generateTree(self, depth):
        tempBoard = PentagoBoard(self.rootState.state)
        for x in range(1, depth+1):
            toadd = []
            for node in self.leaflist:
                self.createChildren(node, tempBoard, depth, x)
                toadd.extend(node.children)
            self.leaflist.clear()
            self.leaflist = toadd


    def createChildren(self, node:PentagoTreeNode, board:PentagoBoard, depthmax, depthcurrent) -> list:
        if node.moves != []:
            board.place(node.moves[0], (node.moves[1][0], node.moves[1][1]))
            board.rotateSquare(int(node.moves[2][0]), node.moves[2][1])
        newowner = node.oppositeOwner()
        emptycnt = 0
        for coord in self.testvals:#iterate over coordinates
            y = coord[0]
            x = coord[1]
            if board.state[y][x] == "-":
                for dir in self.rotatevals:#iterate over squares for rotating
                    i = dir[0]
                    el = dir[1]
                    val = 0
                    notempty = not(board.squareEmpty(i))
                    child = None
                    if notempty or emptycnt == 0:
                        if depthcurrent == depthmax:
                            board.place(node.owner, (y, x))
                            if notempty: board.rotateSquare(i, el)
                            val = self.stateValue(board)
                            if notempty:
                                rotate = "L"
                                if el == "L":
                                    rotate = "R"
                                board.rotateSquare(int(i), rotate)
                            board.remove((y, x))
                        if emptycnt == 0 and not(notempty):
                            emptycnt+=1
                            child = PentagoTreeNode(node, [node.owner,[y,x], "0*"], newowner, val)
                        else:
                            child = PentagoTreeNode(node, [node.owner,[y,x], str(i) + el], newowner, val)
                        node.children.append(child)
            emptycnt = 0

        if node.moves != []:
            rotate = "L"
            if node.moves[2][1] == "L":
                rotate = "R"
            board.rotateSquare(int(node.moves[2][0]), rotate)
            board.remove((node.moves[1][0], node.moves[1][1]))


    def calculateMinmaxVals(self, node:PentagoTreeNode):
        if node.children[0].children != []:
            for child in node.children:
                self.calculateMinmaxVals(child)
        valarr = [x.minmax for x in node.children]
        if node.owner == "w":
            node.setMinmax(max(valarr))
        else:
            node.setMinmax(min(valarr))
            

    def stateValue(self, board:PentagoBoard):
        warr = []
        barr = []
        for r in range(0,6):
            for c in range(0,6):
                char = board.state[r][c]
                if char == "w":
                    warr.append((r,c))
                elif char == "b":
                    barr.append((r,c))

        rowcnt = [0,0,0,0,0,0]
        colcnt = [0,0,0,0,0,0]
        ldiagcnt = [0,0,0]
        rdiagcnt = [0,0,0]
        for idx in warr:
            add = self.adjacentMap[idx]
            rowcnt[add[0]] += 1
            colcnt[add[1]] += 1
            for diag in add[2]:
                if diag == "lm":
                    ldiagcnt[0] += 1
                elif diag == "lu":
                    ldiagcnt[1] += 1
                elif diag == "ll":
                    ldiagcnt[2] += 1
                elif diag == "rm":
                    rdiagcnt[0] += 1
                elif diag == "ru":
                    rdiagcnt[1] += 1
                elif diag == "rl":
                    rdiagcnt[2] += 1
        wcnt = self.getValFromCounts(rowcnt, colcnt, ldiagcnt, rdiagcnt)

        rowcnt = [0,0,0,0,0,0]
        colcnt = [0,0,0,0,0,0]
        ldiagcnt = [0,0,0]
        rdiagcnt = [0,0,0]
        for coord in barr:
            add = self.adjacentMap[coord]
            rowcnt[add[0]] -= 1
            colcnt[add[1]] -= 1
            for diag in add[2]:
                if diag == "lm":
                    ldiagcnt[0] -= 1
                elif diag == "lu":
                    ldiagcnt[1] -= 1
                elif diag == "ll":
                    ldiagcnt[2] -= 1
                elif diag == "rm":
                    rdiagcnt[0] -= 1
                elif diag == "ru":
                    rdiagcnt[1] -= 1
                elif diag == "rl":
                    rdiagcnt[2] -= 1
        bcnt = self.getValFromCounts(rowcnt, colcnt, ldiagcnt, rdiagcnt)
        return wcnt + bcnt

    def getValFromCounts(self, rows, cols, ldiags, rdiags):
        total = 0
        for a in rows:
            if a>1:
                total += a*2
            else:
                total += a
        for b in cols:
            if b>1:
                total += b*2
            else:
                total += b
        for c in ldiags:
            if c>1:
                total += c*2
            else:
                total += c
        for d in rdiags:
            if d>1:
                total += d*2
            else:
                total += d

        return total