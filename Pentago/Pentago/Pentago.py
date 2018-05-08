from PentagoBoard import PentagoBoard
from PentagoTree import PentagoTree
from PentagoTreeNode import PentagoTreeNode

class Pentago:

    def __init__(self):
        self.board = PentagoBoard()
        self.winner = ""
        self.player = "w"
        self.ai = "b"
        self.currentTurn = ""
        self.gameLoop()

    def gameOver(self):
        wcnt = 0
        bcnt = 0
        for a in range(0, 6):#check rows for 5 in a row
            wcnt = 0
            bcnt = 0
            for b in range(0, 6):
                char = self.board.state[a][b]
                wcnt = wcnt+1 if char == "w" else 0
                bcnt = bcnt+1 if char == "b" else 0
                if wcnt == 5 or bcnt == 5:
                    self.winner = "w" if wcnt == 5 else "b"
                    return True
        for d in range(0, 6):#check columns for 5 in a row
            wcnt = 0
            bcnt = 0
            for c in range(0, 6):
                char = self.board.state[c][d]
                wcnt = wcnt+1 if char == "w" else 0
                bcnt = bcnt+1 if char == "b" else 0
                if wcnt == 5 or bcnt == 5:
                    self.winner = "w" if wcnt == 5 else "b"
                    return True
        for e in range(-1, 2):#check diagonals (left to right) for 5 in a row
            wcnt = 0
            bcnt = 0
            for f in range(0, 6):
                char = self.board.state[f][f]
                if e==-1:
                    char = self.board.state[f+1][f]
                elif e == 1:
                    char = self.board.state[f][f+1]
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
                char = self.board.state[5 - f][f]
                if e==-1:
                    char = self.board.state[6-f][f]
                elif e == 1:
                    char = self.board.state[5-f][f-1]
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
        self.board.place(self.player, (move[0], move[1]))
        self.board.rotateSquare(int(move[2][0]), move[2][1])


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
        while not(self.gameOver() or self.board.boardFull()):#while game isnt over and board isnt full
            self.board.printBoard()
            if self.currentTurn == "Player":
                self.playerTurn()
                self.currentTurn = "AI"
            else:
                print("AI not yet implemented")
                self.currentTurn = "Player"
        print("%s wins!" % self.winner)
            
                

    
if __name__ == "__main__":
    #game = Pentago()
    tree = PentagoTree(PentagoBoard(), "w")
    
