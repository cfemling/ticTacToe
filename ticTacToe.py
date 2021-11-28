#this is my tic tac toe
from random import choice
from tkinter import *
import time

class Toe():
    '''the tic tac toe class creates a matrix representation of the game
    in typical 3x3 layout and takes no arguments'''

    def __init__(self):
        self.width = 3
        self.height = 3
        self.data = []

        for row in range(self.height):
            boardRow = []
            for col in range(self.width):
                boardRow += [" "]
            self.data += [boardRow]
        
    def __repr__(self):
        #the string representation of the game for printing in terminal
        board = ""
        for row in range(self.height):
            board += str(row) + "|"
            for col in range(self.width):
                board += self.data[row][col] + "|"
            board += "\n"
        
        board += "--"*self.width +"-\n"

        board += " "
        for col in range(self.width):
            board += " " + str(col)
        board += "\n"

        return board

    def allowsMove(self, row, col):
        '''checks if move at row,col is valid if it is
        1. within the board constraints and 2. an empty space'''
        if 0 <= row < self.height and 0 <= col < self.width:
            return self.data[row][col] == " "
        else:
            return False

    def addMove(self, row, col, ox):
        '''assigns the current player's move to row,col in the board 
        data if the move is valid'''
        if self.allowsMove(row, col):
            self.data[row][col] = ox
            return True

    def clear(self):
        #empties the board
        for row in range(self.height):
            for col in range(self.width):
                self.data[row][col] = " "
    
    def delMove(self, row, col):
        #deletes the move at row,col
        if 0 <= row < self.height and 0 <= col < self.width:
            if self.data[row][col] != " ":
                self.data[row][col] = " "
                return

    def winsFor(self, ox):
        '''checks all directions for a win and records the three
        winning moves to self.win'''
        for row in range(self.height):
            if self.data[row][0] == ox and \
            self.data[row][1] == ox and \
            self.data[row][2] == ox:
                self.win = [[row, 0], [row, 1], [row, 2]]
                return True
    
        for col in range(self.width):
            if self.data[0][col] == ox and \
            self.data[1][col] == ox and \
            self.data[2][col] == ox:
                self.win = [[0,col], [1,col], [2,col]]
                return True

        if self.data[0][0] == ox and \
        self.data[1][1] == ox and \
        self.data[2][2] == ox:
            self.win = [[0,0], [1,1], [2,2]]
            return True

        if self.data[2][0] == ox and \
        self.data[1][1] == ox and \
        self.data[0][2] == ox:
            self.win = [[2,0], [1,1], [0,2]]
            return True
        return False

    def isFull(self):
        #checks if all board spaces are filled
        for row in range(self.height):
            for col in range(self.width):
                if self.allowsMove(row, col):
                    return False
        return True
    
    def switch(self, ox):
        #changes to opposite player
        if ox == "x":
            return "o"
        else:
            return "x"

    def hostGame(self, p):
        '''starts the game, each player's turn is carried
        out through self.turn'''
        self.turn("x", p)

    def turn(self, ox, p):
        '''carries out the current player's turn and then
        carries out the rest of the game recursively'''
        enemy = self.switch(ox)
        if self.isFull() == False and \
        self.winsFor("x") == False and \
        self.winsFor("o") == False:
            print(self)
            print(ox, "'s turn")
            if ox == p.ox:
                move = p.nextMove()
                row = move[0]
                col = move[1]
                self.addMove(row, col, ox)
            else:
                row = int(input("enter row:"))
                col = int(input("enter column:"))
                if self.allowsMove(row, col) == False:
                    print("invalid move")
                    self.turn(ox, p)
                self.addMove(row, col, ox)
            if self.winsFor(ox):
                print(self)
                print("Game over! ", ox, "wins!")
                return
            if self.isFull():
                print(self)
                print("Game over no winner")
                return
            else:
                self.turn(enemy, p)

class Player(object):
    '''the AI opponent initializes the board, a, playing piece, ox,
    and the level of difficulty, ply'''
    def __init__(self, a, ox, ply):
        self.a = a
        self.ox = ox
        self.ply = ply

    def scoreBoard(self, ox):
        '''assigns a score to the current board state'''
        if self.a.winsFor("x"):
            if ox == "x":
                return 100
            else:
                return 0
        if self.a.winsFor("o"):
            if ox == "o":
                return 100
            else:
                return 0
        else:
            return 50
    
    def scoresFor(self, ox, ply):
        '''the AI's train of thought based on their difficulty rating
        ply represents the number of moves the AI thinks ahead
        where 0 ply means the AI doesn't look ahead at all'''
        score = []
        for row in range(self.a.height):
            score.append([])
            for col in range(self.a.width):
                if self.a.allowsMove(row, col):
                    if ply == 0:
                        score[row].append(self.scoreBoard(ox))
                    else:
                        self.a.addMove(row, col, ox)
                        if self.a.winsFor(ox):
                            score[row].append(100)
                        else:
                            if ply > 1: #start alternating between which player fictionally moves
                                enemy = self.a.switch(ox)
                                enemyScore = []
                                for x in self.scoresFor(enemy, ply-1):
                                    for y in x:
                                        enemyScore.append(y)
                                score[row].append(100 - max(enemyScore))
                            else:
                                score[row].append(50)
                        self.a.delMove(row, col)
                else:
                    score[row].append(-1)
        return score

    def bestMove(self, score):
        #takes the score list and returns the highest scores
        maxRow = []
        best = []
        for index in range(self.a.height):
            maxRow.append(max(score[index]))
        s = max(maxRow)
        for row in range(len(maxRow)):
            for col in range(self.a.width):
                if score[row][col] == s:
                    best.append([row, col])
        return best

    def nextMove(self):
        '''creates a score for possible moves in self.scoresFor
        narrows the score to best moves in self.bestMove
        randomly chooses the next move out of best scores'''
        score = self.bestMove(self.scoresFor(self.ox, self.ply))
        count = 0
        for x in score:
            count += 1
        chosen = choice(range(count))
        return score[chosen]

class Gui(object):
    '''initializes the window, board a, and player p
    for the creation of the GUI'''

    def __init__(self, window, a, p):
        self.window = window
        self.a = a
        self.p = p
        self.dimension = 3
        self.squares = 150
        self.padding = 15
        self.footer = 25
        self.length = self.dimension*self.squares + self.padding*4
        
        self.frame = Frame(self.window)
        self.frame.pack()

        self.label = Label(self.frame, text="Difficulty: 0")
        self.label.pack(side="left")

        self.slider = Scale(self.frame, orient="horizontal", showvalue=0, to=3, length=200, command=self.plySlider)
        self.slider.pack(side="left")

        self.nButton = Button(self.frame, text="New Game", command=self.nButtonAction)
        self.nButton.pack(side="left")

        self.qButton = Button(self.frame, text="Quit", command=self.qButtonAction)
        self.qButton.pack(side="left")

        self.draw = Canvas(self.window, width=self.length, height=self.length+self.footer, bg="light blue")
        self.draw.bind("<Button-1>", self.mouse)
        self.draw.pack()

        #creates each square for playing in matrix self.boardsquares
        self.boardSquares = []
        y = self.padding
        for row in range(self.dimension):
            squareRow = []
            colorRow = []
            x = self.padding
            for col in range(self.dimension):
                squareRow += [self.draw.create_rectangle(x, y, x+self.squares, y+self.squares, fill="white")]
                colorRow += ["white"]
                x += self.squares + self.padding
            self.boardSquares +=[squareRow]
            y += self.squares + self.padding

        self.message = self.draw.create_text(150, self.length+(self.footer/2), text="Click to make a move", anchor="w", font="Cambria 20")

    def plySlider(self,num):
        #links the GUI difficulty to the player's ply
        self.p.ply = int(num)
        self.label["text"] = "Difficulty %s" % (num)
    
    def nButtonAction(self):
        #clears the board
        self.a.clear()
        self.changeColor()
        self.draw.itemconfig(self.message, text="Click to make a move")
    
    def qButtonAction(self):
        #exits
        self.window.destroy()

    def mouse(self, event):
        #contains the game playing mechanics
        if self.winX() or self.winO() or self.noWins():
            return
        else:
            row = int((event.y-self.footer)/self.squares)
            col = int(event.x/self.squares)
            if self.a.allowsMove(row, col) == False:
                return
            else:
                self.a.addMove(row, col, "x")
                self.changeColor()
                self.window.update()
                if self.winX() == False and self.noWins() == False:
                    self.draw.itemconfig(self.message, text="AI is moving...")
                    self.window.update()
                    time.sleep(0.5)
                    move = self.p.nextMove()
                    row = move[0]
                    col = move[1]
                    self.a.addMove(row, col, "o")
                    self.changeColor()
                    if not self.winX() or not self.winO() or not self.noWins():
                        self.draw.itemconfig(self.message, text="Click to make a move")

    def winX(self):
        #checks for x's win and updates board
        if self.a.winsFor("x"):
            self.window.after(50, self.winner("x"))
            self.draw.itemconfig(self.message, text="You win!")
            return True
        else:
            return False

    def winO(self):
        #checks for o's win and updates board
        if self.a.winsFor("o"):
            self.window.after(50, self.winner("o"))
            self.draw.itemconfig(self.message, text="AI wins!")
            return True
        else:
            return False

    def noWins(self):
        #checks if board is full and updates board
        if self.a.isFull():
            self.draw.itemconfig(self.message, text="Game over, no winner")
            return True
        else:
            return False

    def winner(self, ox):
        #makes the 3 winning moves change color to indicate the win
        for x in range(3):
            self.draw.itemconfig(self.boardSquares[self.a.win[x][0]][self.a.win[x][1]], fill="blue")

    def changeColor(self):
        #connects the colors of the board to the board data
        for row in range(3):
            for col in range(3):
                if self.a.data[row][col] == "x":
                    self.draw.itemconfig(self.boardSquares[row][col], fill="black")
                elif self.a.data[row][col] == "o":
                    self.draw.itemconfig(self.boardSquares[row][col], fill="red")
                else:
                    self.draw.itemconfig(self.boardSquares[row][col], fill="white")

def main():
    a = Toe()
    p = Player(a, 'o', 0)
    #a.hostGame(p)
    root = Tk()
    root.title("Tic Tac Toe")
    demo = Gui(root, a, p)
    root.mainloop()

if __name__ == '__main__':
    main()