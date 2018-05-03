

class Pentago:
    def __init__(self):
        self.board = [["-" for x in range(6)] for y in range(6)]
        self.winner = ""
        self.gameLoop()

    def place(self, player, location = (0, 0)):
        self.board[location[0]][location[1]] = player

    def printBoard(self):
        print("+-------+-------+")
        for x in range(6):
            line = "| "
            for y in range(6):
                line += self.board[x][y] + " "
                if y==2 or y==5:
                    line += "| "
            print(line)
            if x == 2 or x == 5:
                print("+-------+-------+")

    def rotateSquare(self, square):
        start = (0, 0)
        end = (0, 0)
        rows = [["", "", ""], ["", "", ""], ["", "", ""]]
        #determine where the start and end points of the array are, based on square number
        if square == 1:
            end = (2,2)
        elif square == 2:
            start = (0,3)
            end = (2,5)
        elif square == 3:
            start = (3,0)
            end = (5,2)
        else:
            start = (3,3)
            end = (5,5)
        
        ridx = 0
        cidx = 0
        for y in range(start[0], end[0] + 1): #copy the elements that are going to be flipped
            for x in range(start[1], end[1] + 1):
                rows[ridx][cidx] = str(self.board[y][x])
                self.board[y][x] = "-"
                cidx += 1
            ridx += 1
            cidx = 0
        
        ridx = 0
        cidx = 0
        for c in range(end[1], start[1] - 1, -1): #read rows of copy into columns of board, from last column to first
            for d in range(start[0], end[0] + 1): #this essentially flips the board
                self.board[d][c] = rows[ridx][cidx]
                cidx += 1
            ridx += 1
            cidx = 0


    def gameOver(self):
        wcnt = 0
        bcnt = 0
        for a in range(0, 6):#check rows for 5 in a row
            wcnt = 0
            bcnt = 0
            for b in range(0, 6):
                char = self.board[a][b]
                wcnt = wcnt+1 if char == "w" else 0
                bcnt = bcnt+1 if char == "b" else 0
                if wcnt == 5 or bcnt == 5:
                    self.winner = "w" if wcnt == 5 else "b"
                    return True
        for d in range(0, 6):#check columns for 5 in a row
            wcnt = 0
            bcnt = 0
            for c in range(0, 6):
                char = self.board[c][d]
                wcnt = wcnt+1 if char == "w" else 0
                bcnt = bcnt+1 if char == "b" else 0
                if wcnt == 5 or bcnt == 5:
                    self.winner = "w" if wcnt == 5 else "b"
                    return True
        for e in range(-1, 2):#check diagonals (left to right) for 5 in a row
            wcnt = 0
            bcnt = 0
            for f in range(0, 6):
                char = self.board[f][f]
                if e==-1:
                    char = self.board[f+1][f]
                elif e == 1:
                    char = self.board[f][f+1]
                wcnt = wcnt+1 if char == "w" else 0
                bcnt = bcnt+1 if char == "b" else 0
                if wcnt == 5 or bcnt == 5:
                    self.winner = "w" if wcnt == 5 else "b"
                    return True
                if e!=0 and f==4:
                    break
        for e in range(-1, 2):#check diagonals (right to left) for 5 in a row
            wcnt = 0
            bcnt = 0
            for f in range(5, -1, -1):
                char = self.board[5 - f][f]
                if e==-1:
                    char = self.board[6-f][f]
                elif e == 1:
                    char = self.board[5-f][f-1]
                wcnt = wcnt+1 if char == "w" else 0
                bcnt = bcnt+1 if char == "b" else 0
                if wcnt == 5 or bcnt == 5:
                    self.winner = "w" if wcnt == 5 else "b"
                    return True
                if e!=0 and f==1:
                    break
        return False


    

    def gameLoop(self):
        self.place("w", (0,5))
        self.place("w", (1,4))
        self.place("w", (2,3))
        self.place("w", (3,2))
        self.place("w", (4,1))
        print(self.gameOver())
    

def test():
    for a in range(2):
        for b in range(2):
            print("inner loop")
            if True:
                break
        print("Outer Loop")

if __name__ == "__main__":
    game = Pentago()



