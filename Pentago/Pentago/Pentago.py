#Pentago, TCSS 435
#By Kyle Beveridge
#
#This program simulates a game of pentago between
#a human player and an AI player


from PentagoBoard import PentagoBoard
from PentagoTree import PentagoTree
from PentagoTreeNode import PentagoTreeNode
from PentagoAi import PentagoAi

class Pentago:
    def __init__(self):
        self.board = PentagoBoard()
        self.winner = ""
        self.player = "w"
        self.ai = "b"
        self.currentTurn = ""
        self.gameLoop()

    #Check to see if the game is over by checking all of the rows,
    #columns, and diagonals for 5 in a row
    #
    #Returns True if a winner is found (and sets the self.winner var), False otherwise (self.winner is not set in this case)
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

    #convert a player move in the input format (ex "1/1 2R") to one the board
    #understands (a token to place, and index to place it at, and a rotation square/direction)
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
        return [self.player, (coordinates[0], coordinates[1]), rotate]

    #process a player turn and return the move (both the one for the board and the one the player input)
    def playerTurn(self):
        inmove = input("Enter Move: ").upper()
        move = self.readMove(inmove)
        self.board.place(self.player, (move[1][0], move[1][1]))
        if self.board.squareEmpty(int(move[2][0])):
            move[2] = "0*"
        else:
            self.board.rotateSquare(int(move[2][0]), move[2][1])
        return (move, inmove)

    #Runs the main game loop for a game of pentago. Sets up the basic features of the game, 
    #like who uses what token and who goes first, then runs the game until a winner is found
    def gameLoop(self):
        out = open("Output.txt", "w")
        self.player = input("Do you want (w)hite or (b)lack? ").lower()
        while (self.player != "w" and self.player != "b"):
            print("Invalid input! Please try again.")
            self.player = input("Do you want (w)hite or (b)lack? ")
        if self.player == "b":
            self.ai = "w"
        out.write("Player Token: %s\n" % self.player)
        out.write("AI Token: %s\n" % self.ai)
        choice = input("Do you want to go first (1) or second (2)? ")
        while choice!="1" and choice!="2":
            print("Invalid input! Please try again.")
            choice = input("Do you want to go first (1) or second (2)? ")

        self.currentTurn = "Player"
        if choice == "2":
            self.currentTurn = "AI"

        ai = PentagoAi(PentagoTree(self.board, self.ai), self.board, self.ai)
        while not(self.gameOver() or self.board.boardFull()):#while game isnt over and board isnt full
            self.board.printBoard(out)
            if self.currentTurn == "Player":
                playermove = self.playerTurn()
                out.write("Player Move: %s\n" % playermove[1])
                if not(ai.atLeafLevel):
                    ai.processPlayerMove(playermove[0])#Ai updates its tree based on the move the player made
                self.currentTurn = "AI"
            else:
                if(ai.atLeafLevel):
                    ai.setUp()#if the tree is exhausted, generate a new one from current state
                aimove = ai.makeMove()
                print("AI move: %s" % aimove)
                out.write("AI move: %s\n" % aimove)
                self.currentTurn = "Player"
        print("%s wins!" % self.winner)
        out.write("%s wins!\n" % self.winner)
        out.close()
            
if __name__ == "__main__":
    game = Pentago()