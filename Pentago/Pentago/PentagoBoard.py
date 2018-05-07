
class PentagoBoard:

    def __init__(self, newState = []):
        if newState == []:
            self.state = [["-" for x in range(6)] for y in range(6)]
        else:
            self.state = [[newState[y][x] for x in range(0, 6)] for y in range(0,6)]


    def place(self, player, location = (0, 0)):
        self.state[location[0]][location[1]] = player

    def printBoard(self):
        print("+-------+-------+")
        for x in range(6):
            line = "| "
            for y in range(6):
                line += self.state[x][y] + " "
                if y==2 or y==5:
                    line += "| "
            print(line)
            if x == 2 or x == 5:
                print("+-------+-------+")

    def boardFull(self):
        for ls in self.state:
            for el in ls:
                if el == "-":
                    return False
        return True

    def squareEmpty(self, square)->bool:
        start = self.squareToIdx(square)
        end = start[1]
        start = start[0] 
        for y in range(start[0], end[0] + 1):
            for x in range(start[1], end[1] + 1):
                if self.state[y][x] != "-":
                    return False
        return True

    def rotateSquare(self, square, dir):
        if(self.squareEmpty(square)):
            return
        start = self.squareToIdx(square)
        end = start[1]
        start = start[0]
        addnum = 1
        if(dir == "L"):#swap start/end positions so square is read upside down and backwards
            #when this is turned right, it is functionally the same as rotating left
            temp = start
            start = end
            end = temp
            addnum = -1
        rows = [["", "", ""], ["", "", ""], ["", "", ""]]
        ridx = 0
        cidx = 0
        for y in range(start[0], end[0] + addnum, addnum): #copy the elements that are going to be flipped
            for x in range(start[1], end[1] + addnum, addnum):
                rows[ridx][cidx] = self.state[y][x]
                self.state[y][x] = "-"
                cidx += 1
            ridx += 1
            cidx = 0
        
        ridx = 0
        cidx = 0
        if(dir == "L"): #restore original start and end positions if left
            temp = start
            start = end
            end = temp
        for c in range(end[1], start[1] - 1, -1): #read rows of copy into columns of board, from last column to first
            for d in range(start[0], end[0] + 1): #this essentially flips the board
                self.state[d][c] = rows[ridx][cidx]
                cidx += 1
            ridx += 1
            cidx = 0

    def squareToIdx(self, square):
        start = [0, 0]
        end = [0, 0]
        #determine where the start and end points of the array are, based on square number
        if square == 1:
            end = [2,2]
        elif square == 2:
            start = [0,3]
            end = [2,5]
        elif square == 3:
            start = [3,0]
            end = [5,2]
        else:
            start = [3,3]
            end = [5,5]
        return [start, end]