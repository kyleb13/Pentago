#Models the state space tree for a game of pentago

from PentagoTreeNode import PentagoTreeNode
from PentagoBoard import PentagoBoard
from multiprocessing import Pool

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

    #builds a map that details which rows, columns, and diagonals an index is in,
    #as well as all of the indexes that are adjacent to it
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
    
    #get the indexes of locations adjacent to a certain index
    def getCloseIdx(self, idx):
        temp = [(idx[0], idx[1]-1),(idx[0]-1, idx[1]-1),(idx[0]-1, idx[1]),(idx[0]-1, idx[1]+1),(idx[0], idx[1]+1),
                     (idx[0]+1, idx[1]+1),(idx[0]+1, idx[1]),(idx[0]+1, idx[1]-1)]
        result = []
        for el in temp:
            if el[0] in range(0,6) and el[1] in range(0, 6):#only add indexes that are in bounds of the array
                result.append(el)
        return result

    #routine for generating the tree. Also sets self.leaflist so it has a reference to all of the leaf level nodes
    def generateTree(self, depth):
        tempBoard = PentagoBoard(self.rootState.state)
        for x in range(1, depth+1):#generate nodes in a breadth first manner
            toadd = []
            for node in self.leaflist:
                self.createChildren(node, tempBoard, depth, x)#create child nodes of current node
                toadd.extend(node.children)
            self.leaflist.clear()
            self.leaflist = toadd#set leaf list equal to the newly generated children

    #create the children of a node
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
                        if emptycnt == 0 and not(notempty):#generate a child where no square is rotated. Only happens once per index at most
                            emptycnt+=1
                            child = PentagoTreeNode(node, [node.owner,(y,x), "0*"], newowner, 0)
                        else:
                            child = PentagoTreeNode(node, [node.owner,(y,x), str(i) + el], newowner, 0)
                        node.children.append(child)#add child to child list
            emptycnt = 0

        if node.moves != []:
            self.undoMoves(board, [node.moves])

    #calculate the minmax values for all of the nodes in the tree recursively
    def calculateMinmaxVals(self, node:PentagoTreeNode):
        if node.children[0].children != []:#if the next level is not at leaf level, recursively go to that level
            for child in node.children:
                self.calculateMinmaxVals(child)
        valarr = [x.minmax for x in node.children]#get minmax values of children
        #set minmax value based on node owner
        if node.owner == "w":
            node.setMinmax(max(valarr))
        else:
            node.setMinmax(min(valarr))

    #initalizes minmax values of leaf level nodes by making 2 worker processes (which call self.calcStateVals) process half
    #of the leaf list each (mostly to improve wait times)
    def initChildStateValues(self):
        p = Pool(processes=2)
        #Run the worker processes and get back the leaf list in two parts with updated minmax vals
        results = p.map(self.calcStateVals, [self.leaflist[0:len(self.leaflist)//2 + 1], self.leaflist[len(self.leaflist)//2 + 1: len(self.leaflist)]])
        cnt = 0
        #copy returned minmax values into the leaflist nodes,
        #since processes don't share memory
        for ls in results:
            for ch in ls:
                self.leaflist[cnt].minmax = ch.minmax
                cnt +=1

    #calculate state values for a portion of the leaf list, and return the updated list.
    #called by the worker processes in function above (initChildStateValues)
    def calcStateVals(self, llist):
        temp = PentagoBoard(self.rootState.state)#temporary board for processing moves
        moves = []
        for child in llist:
            moves = self.getMoves(child)
            self.makeMoves(temp, moves)#make moves required to get from inital state to child state
            child.minmax = self.stateValue(temp)#calculate value of that state
            self.undoMoves(temp, [moves[i] for i in range(len(moves) - 1, -1, -1)])#undo moves in reverse order they were made
        return llist 

    #make all of the moves in a list of moves
    def makeMoves(self, board:PentagoBoard, moves:[]):
        for el in moves:
            board.place(el[0], el[1])
            board.rotateSquare(int(el[2][0]), el[2][1])
    
    #undo all of the moves in a list of moves
    def undoMoves(self, board:PentagoBoard, moves:[]):
        for el in moves:
            rotate = "L"
            if el[2][1] == "L":
                rotate = "R"
            elif el[2] == "0*":
                rotate = "0*"
            if(rotate != "0*"):
                board.rotateSquare(int(el[2][0]), rotate)
            board.remove(el[1])
            
    #get the moves required to get to child's state
    def getMoves(self, node:PentagoTreeNode):
        result = []
        current = node
        while current.moves != []:
            result.append(current.moves)
            current = current.parent
        result = [result[x] for x in range(len(result) - 1, -1, -1)]
        return result

    #calculate the minmax value of a particular state
    def stateValue(self, board:PentagoBoard):
        warr = []
        barr = []
        #find indexes of all of the tokens
        for r in range(0,6):
            for c in range(0,6):
                char = board.state[r][c]
                if char == "w":
                    warr.append((r,c))
                elif char == "b":
                    barr.append((r,c))

        #make count variables for every row, column, and diagonal
        rowcnt = [0,0,0,0,0,0]
        colcnt = [0,0,0,0,0,0]
        ldiagcnt = [0,0,0]
        rdiagcnt = [0,0,0]
        adjbonus = 0 #bonus for having tokens adjacent to a token
        for idx in warr:
            add = self.adjacentMap[idx]#get diagonal and adjacency data from the map
            #increment relevant row, column, and diagonal counters
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
                #give an adjacency bonus for being near other tokens
                if val in warr:
                    adjbonus += 1
                if val in barr:
                    adjbonus += 1

        wcnt = self.getValFromCounts(rowcnt, colcnt, ldiagcnt, rdiagcnt) + adjbonus
        #do the same thing but for the 'b' tokens
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
                    adjbonus += 1
                if el in warr:
                    adjbonus += 1
        bcnt = self.getValFromCounts(rowcnt, colcnt, ldiagcnt, rdiagcnt) + adjbonus
        return wcnt-bcnt


    #add up all of the counts, used by stateValue()
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