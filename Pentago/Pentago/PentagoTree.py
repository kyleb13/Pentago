from PentagoTreeNode import PentagoTreeNode
from PentagoBoard import PentagoBoard
from multiprocessing import Process, Manager, Queue, Pipe, Array, Pool
from multiprocessing.managers import BaseManager

class LeafList:
    def __init__(self, inleaves):
        self.leaves = inleaves

    def getList(self):
        return self.leaves


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
            close = []
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
            close = self.getCloseIdx(val)
            self.adjacentMap[val] = [val[0], val[1], diags, close]
    
    def getCloseIdx(self, idx):
        temp = [(idx[0], idx[1]-1),(idx[0]-1, idx[1]-1),(idx[0]-1, idx[1]),(idx[0]-1, idx[1]+1),(idx[0], idx[1]+1),
                     (idx[0]+1, idx[1]+1),(idx[0]+1, idx[1]),(idx[0]+1, idx[1]-1)]
        result = []
        for el in temp:
            if el[0] in range(0,6) and el[1] in range(0, 6):
                result.append(el)
        return result

    def generateTree(self, depth):
        tempBoard = PentagoBoard(self.rootState.state)
        for x in range(1, depth+1):
            toadd = []
            for node in self.leaflist:
                self.createChildren(node, tempBoard, depth, x)
                toadd.extend(node.children)
            self.leaflist.clear()
            self.leaflist = toadd

    #def generateTree(self, depth):
    #    print()

    #def generate(self, node, depth):
    #    tempBoard = PentagoBoard(self.rootState.state)
    #    ll = [node]
    #    for x in range(1, depth+1):
    #        toadd = []
    #        for node in self.leaflist:
    #            self.createChildren(node, tempBoard, depth, x)
    #            toadd.extend(node.children)
    #        self.leaflist.clear()
    #        self.leaflist = toadd


    def createChildren(self, node:PentagoTreeNode, board:PentagoBoard, depthmax, depthcurrent) -> list:
        if node.moves != []:
            self.makeMoves(board, [node.moves])
        newowner = node.oppositeOwner()
        emptycnt = 0
        for coord in self.testvals:#iterate over coordinates
            y = coord[0]
            x = coord[1]
            if board.state[y][x] == "-":
                for dir in self.rotatevals:#iterate over squares for rotating
                    i = dir[0]
                    el = dir[1]
                    notempty = not(board.squareEmpty(i))
                    if notempty or emptycnt == 0:
                        if emptycnt == 0 and not(notempty):
                            emptycnt+=1
                            child = PentagoTreeNode(node, [node.owner,(y,x), "0*"], newowner, 0)
                        else:
                            child = PentagoTreeNode(node, [node.owner,(y,x), str(i) + el], newowner, 0)
                        node.children.append(child)
            emptycnt = 0

        if node.moves != []:
            self.undoMoves(board, [node.moves])


    def calculateMinmaxVals(self, node:PentagoTreeNode):
        if node.children[0].children != []:
            for child in node.children:
                self.calculateMinmaxVals(child)
        valarr = [x.minmax for x in node.children]
        if node.owner == "w":
            node.setMinmax(max(valarr))
        else:
            node.setMinmax(min(valarr))

    def initChildStateValues(self):
        p = Pool(processes=2)
        results = p.map(self.calcStateVals, [self.leaflist[0:len(self.leaflist)//2 + 1], self.leaflist[len(self.leaflist)//2 + 1: len(self.leaflist)]])
        cnt = 0
        for ls in results:
            for ch in ls:
                self.leaflist[cnt].minmax = ch.minmax
                cnt +=1

    def calcStateVals(self, llist):
        temp = PentagoBoard(self.rootState.state)
        prevParent = None
        moves = []
        for child in llist:
            if prevParent == None or child.parent != prevParent:
                if prevParent != None:
                    self.undoMoves(temp, moves)
                prevParent = child.parent
                moves = self.getMoves(child)
                self.makeMoves(temp, moves)
            else:
                self.undoMoves(temp, [moves[len(moves) - 1]])
                moves[len(moves) - 1] = child.moves
                self.makeMoves(temp, [moves[len(moves) - 1]])
            child.minmax = self.stateValue(temp)
        return llist

    def makeMoves(self, board:PentagoBoard, moves:[]):
        for el in moves:
            board.place(el[0], el[1])
            board.rotateSquare(int(el[2][0]), el[2][1])

    def undoMoves(self, board:PentagoBoard, moves:[]):
        for el in moves:
            rotate = "L"
            if el[2][1] == "L":
                rotate = "R"
            elif el[2] == "0*":
                rotate = "0*"
            board.rotateSquare(int(el[2][0]), rotate)
            board.remove(el[1])
            


    def getMoves(self, node:PentagoTreeNode):
        result = []
        current = node
        while current.moves != []:
            result.append(current.moves)
            current = current.parent
        result = [result[x] for x in range(len(result) - 1, -1, -1)]
        return result

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
        adjbonus = 0
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
            close = add[3]
            for  val in close:
                if val in warr:
                    adjbonus += 2
                if val in barr:
                    adjbonus += 1

        wcnt = self.getValFromCounts(rowcnt, colcnt, ldiagcnt, rdiagcnt) + adjbonus
        rowcnt = [0,0,0,0,0,0]
        colcnt = [0,0,0,0,0,0]
        ldiagcnt = [0,0,0]
        rdiagcnt = [0,0,0]
        adjbonus = 0
        for coord in barr:
            add = self.adjacentMap[coord]
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
            close = add[3]
            for  el in close:
                if el in barr:
                    adjbonus += 2
                if el in warr:
                    adjbonus += 1
        bcnt = self.getValFromCounts(rowcnt, colcnt, ldiagcnt, rdiagcnt) + adjbonus
        return wcnt-bcnt

    #def idxToSquare(self, idx):
    #    square = 0
    #    if idx[0]<=2 and idx[1] <=2:
    #        square =1
    #    elif idx[0]<=2 and idx[1] > 2:
    #        square =2
    #    elif idx[0]>2 and idx[1] <=2:
    #        square =3
    #    else:
    #        square = 4
    #    return square

    def getValFromCounts(self, rows, cols, ldiags, rdiags):
        total = 0
        for a in rows:
            total += a
        for b in cols:
            total += b
        for c in ldiags:
            total += c
        for d in rdiags:
            total += d

        return total

    def treeSize(self):
        current = None
        cnt = 1
        todo = []
        todo.append(self.head)
        while todo != []:
            current = todo.pop(0)
            if current.children == []:
                break
            else:
                cnt+= len(current.children)
                todo.extend(current.children)
        return cnt
