

class Pentago:

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

    def boardFull(self):
        for ls in self.board:
            for el in ls:
                if el == "-":
                    return False
        return True

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


    def readMove(self, move):
        offsetx = 0
        offsety = 0
        square, loc = move.split("/")
        temp = loc.split(" ")
        loc = temp[0]
        rotate = temp[1]
        if (square == "2" or square == "4"):
            offsetx = 3
        if (square == "3" or square == "4"):
            offsety = 3
        coordinates = [0, 0]
        if loc in ("1","2","3"):
            coordinates[1] = int(loc) - 1
        elif loc in ("4","5","6"):
            coordinates[0] = 1
            coordinates[1] = int(loc) - 4
        elif loc in ("7","8","9"):
            coordinates[0] = 2
            coordinates[1] = int(loc) - 7
        coordinates[0] += offsety
        coordinates[1] += offsetx
        return (coordinates[0], coordinates[1], rotate)

    def playerTurn(self):
        move = self.readMove(input("Enter Move: "))
        self.place(self.player, (move[0], move[1]))
        self.rotateSquare(int(move[2][0]))
        if move[2][1] == "L":
            #Rotate square only goes right, so
            #rotate right 3 times to simulate a left
            self.rotateSquare(int(move[2][0]))
            self.rotateSquare(int(move[2][0]))


    def gameLoop(self):
        self.player = input("Do you want (w)hite or (b)lack? ")
        while (self.player != "w" and self.player != "b"):
            print("Invalid input! Please try again.")
            self.player = input("Do you want (w)hite or (b)lack? ")
        if self.player == "b":
            self.ai = "w"
        choice = input("Do you want to go first (1) or second (2)? ")
        while choice!="1" and choice!="2":
            print("Invalid input! Please try again.")
            choice = input("Do you want to go first (1) or second (2)? ")
        self.currentTurn = "Player"
        if choice == "2":
            self.currentTurn = "AI"
        while not(self.gameOver() or self.boardFull()):#while game isnt over and board isnt full
            self.printBoard()
            if self.currentTurn == "Player":
                self.playerTurn()
                self.currentTurn = "AI"
            else:
                print("AI not yet implemented")
                self.currentTurn = "Player"
        print("%s wins!" % self.winner)

    def __init__(self):
        self.board = [["-" for x in range(6)] for y in range(6)]
        self.winner = ""
        self.player = "w"
        self.ai = "b"
        self.currentTurn = ""
        self.gameLoop()
            
                



    
if __name__ == "__main__":
    game = Pentago()



