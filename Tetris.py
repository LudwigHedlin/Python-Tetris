import pygame
import time
import random



class Tetromino:
    def __init__(self):
        self.shape=[[0 for i in range(3)] for i in range(3)]
        self.offSetX=0
        self.offSetY=19
        self.color=None
        self.lastAction=None #set when taking an action
    
        self.kicked=False
        

    def rotate(self):
        size = len(self.shape)
        rotated = [[0 for i in range(size)] for i in range(size)]
        for i in range(size):
            for j in range(size):
                rotated[i][j] = self.shape[size-1-j][i]
        self.shape=rotated

    def freezePiece(self,tetris):
        board=tetris.board
        for i in range(len(self.shape)):
            for j in range(len(self.shape[0])):
                if self.shape[i][j]:
                    board[i+self.offSetY][j+self.offSetX]=self.shape[i][j]
        
    def displayPiece(self):
        self.offSetX=15
        self.offsetY=23

    def boardPiece(self):
        self.offSetX=0
        self.offSetY=19          

    def action(self, event,tetris):
        self.lastAction=event
        if event==pygame.K_a:
            self.moveLeft()
        elif event==pygame.K_d:
            self.moveRight()
        elif event==pygame.K_w:
            self.moveUp()
        elif event==pygame.K_s:
            self.drop(tetris)
        elif event==pygame.K_z:
            self.rotate()
            if self.collision(tetris.board):
                self.kick(tetris.board)

        if self.collision(tetris.board):
            self.undoAction(event)
        
    def undoAction(self,event):
        if event == pygame.K_a:
            self.moveRight()
        elif event == pygame.K_d:
            self.moveLeft()
        elif event == pygame.K_z:
            self.rotate()
            self.rotate()
            self.rotate()
        

    def moveLeft(self):
        self.offSetX-=1
    
    def moveRight(self):
        self.offSetX+=1
    
    def moveDown(self,tetris):
        board=tetris.board
        self.offSetY+=1
        if self.collision(board):
            self.moveUp()
            #self.freezePiece(tetris)
            tetris.freezePiece(self)
    
    def drop(self, tetris):
        board=tetris.board
        while not self.collision(board):
            self.moveDown(tetris)
        

    def moveUp(self):
        self.offSetY-=1

    
    def collision(self,board):
        for i in range(len(self.shape)):
            for j in range(len(self.shape[0])):
                if self.shape[i][j]:
                    if self.offSetY+i > 39 or self.offSetX+j > 9 or self.offSetX+j < 0 or board[self.offSetY+i][self.offSetX+j]:
                        return True

        return False
    
    def kick(self,board):
        self.moveRight()
        if self.collision(board):
            self.moveLeft()
        else:
            return
        self.moveLeft()
        if self.collision(board):
            self.moveRight()
        else:
            return
        self.moveUp()
        if self.collision(board):
            self.moveDown()
        else:
            return
    
        

class TetrominoI(Tetromino):
    def __init__(self):
        super().__init__()
        self.shape = [[0 for x in range(4)] for x in range(4)]
        self.color=(0,200,0)
        for i in range(4):
            self.shape[1][i] = "I"

    


class TetrominoJ(Tetromino):
    def __init__(self):
        super().__init__()
        
        self.color = (100, 0, 200)
        self.shape[0][0]="J"
        for i in range(3):
            self.shape[1][i] = "J"


class TetrominoL(Tetromino):
    def __init__(self):
        super().__init__()

        self.color = (100, 0, 200)
        self.shape[0][2] = "L"
        for i in range(3):
            self.shape[1][i] = "L"


class TetrominoO(Tetromino):
    def __init__(self):
        super().__init__()
        self.color = (100, 0, 200)
        self.shape[0][1] = "O"
        self.shape[0][2] = "O"
        self.shape[1][1] = "O"
        self.shape[1][2] = "O"

    def rotate(self):
        pass


class TetrominoS(Tetromino):
    def __init__(self):
        super().__init__()

        self.color = (100, 0, 200)
        self.shape[0][1] = "S"
        self.shape[0][2] = "S"
        self.shape[1][0] = "S"
        self.shape[1][1] = "S"


class TetrominoZ(Tetromino):
    def __init__(self):
        super().__init__()

        self.color = (100, 0, 200)
        self.shape[0][0] = "Z"
        self.shape[0][1] = "Z"
        self.shape[1][1] = "Z"
        self.shape[1][2] = "Z"


class TetrominoT(Tetromino):
    def __init__(self):
        super().__init__()

        self.color = (100, 0, 200)
        self.shape[0][1] = "T"
        for i in range(3):
            self.shape[1][i] = "T"
        

        





class Tetris:
    def __init__(self):
        pygame.init()
        self.screen=pygame.display.set_mode((1000, 800))
        pygame.display.set_caption("Tetris")
        self.tetromino=self.newTetromino(random.randint(1,7))
        self.nextTetromino = self.newTetromino(random.randint(1, 7))
        self.nextTetromino.displayPiece()
        self.drawTetromino(self.nextTetromino)
        self.running=True
        self.board=[[0 for x in range(10)] for x in range(40)]
        self.speed=1.0
        self.time=time.process_time()

        self.score=0

    def __del__(self):
        pygame.quit()

    def start(self):
        pass
    
    def color(self,tetrominoType):
        if tetrominoType=="I":
            return (0, 200, 0)
        elif tetrominoType=="J":
            return TetrominoJ().color
        elif tetrominoType=="L":
            return TetrominoL().color
        elif tetrominoType=="O":
            return TetrominoO().color
        elif tetrominoType=="S":
            return TetrominoS().color
        elif tetrominoType=="Z":
            return TetrominoZ().color
        elif tetrominoType=="T":
            return TetrominoT().color


    def newTetromino(self,id):
        if id==1:
            return TetrominoI()
        elif id==2:
            return TetrominoJ()
        elif id==3:
            return TetrominoL()
        elif id==4:
            return TetrominoO()
        elif id==5:
            return TetrominoS()
        elif id==6:
            return TetrominoZ()
        elif id==7:
            return TetrominoT()

    def freezePiece(self,tetromino):
        #probably better to use this one so that it can call checkRows and clearRow
        for i in range(len(tetromino.shape)):
            for j in range(len(tetromino.shape)):
                if tetromino.shape[i][j]:
                    print(i+tetromino.offSetY, j+tetromino.offSetX)
                    self.board[i+tetromino.offSetY][j+tetromino.offSetX] = tetromino.shape[i][j]
        self.tetromino=self.nextTetromino
        self.tetromino.boardPiece()
        print(self.tetromino.offSetX,self.tetromino.offSetY)
        self.nextTetromino=self.newTetromino(random.randint(1,7))
        self.nextTetromino.displayPiece()
        self.clearFullRows()

    def checkRows(self):
        #ascending indexes of full rows
        indexes=[]
        for i in range(40):
            count=0
            for j in range(10):
                if(self.board[i][j]):
                    count+=1
            if count==10:
                indexes.append(i)
        self.addScore(len(indexes))
        return indexes
    
    def addScore(self,numRows):
        if numRows==0:
            return
        if numRows==1:
            self.score+=40
        elif numRows==2:
            self.score+=100
        elif numRows==3:
            self.score+=300
        elif numRows==4:
            self.score+=1200
        
    def drawScore(self):
        font=pygame.font.SysFont('bold', 30)

        surface = font.render(str(self.score), 1, (255,255,255))

        self.screen.blit(surface,(500,200))


    def gameTick(self):
        if time.process_time()-self.time>self.speed:
            self.time=time.process_time()
            return True
        else:
            return False

    def clearRow(self,index):
        for i in range(0,index-1):
            for j in range(10):
                self.board[index-i][j]=self.board[index-i-1][j]
    
    def clearFullRows(self):
        rows=self.checkRows()
        for i in rows:
            self.clearRow(i)


    def drawRect(self, i, j, color=(200, 150, 10)):
        rectangle = pygame.Rect(100+i*25, 100+j*25, 25, 25)
        pygame.draw.rect(self.screen,color,rectangle)
    
    def drawBorder(self,upperLeft,lowerRight,color):
        pygame.draw.line(self.screen,color,upperLeft,(lowerRight[0],upperLeft[1]))
        pygame.draw.line(self.screen,color,upperLeft,(upperLeft[0],lowerRight[1]))
        pygame.draw.line(self.screen,color,lowerRight,(lowerRight[0],upperLeft[1]))
        pygame.draw.line(self.screen,color,lowerRight,(upperLeft[0],lowerRight[1]))
        

    def drawBoard(self):
        self.screen.fill((0, 0, 0))
        self.drawTetromino(self.tetromino)
        self.drawTetromino(self.nextTetromino)
        self.drawScore()
        self.drawBorder((100,125),(350,625),(255,255,255))
        for i in range(19,40):
            for j in range(10):
                if self.board[i][j]:
                    self.drawRect(j,i-19,color=self.color(self.board[i][j]))
        
    
    def drawTetromino(self,tetromino):
        for i in range(len(tetromino.shape)):
            for j in range(len(tetromino.shape[0])):
                if tetromino.shape[i][j] and i+tetromino.offSetY>19:

                    self.drawRect(j+tetromino.offSetX, i+tetromino.offSetY-19,color=tetromino.color)

    def unDrawTetromino(self,tetromino):
        for i in range(len(tetromino.shape)):
            for j in range(len(tetromino.shape[0])):
                if tetromino.shape[i][j]:
                    self.drawRect(j+tetromino.offSetX, i+tetromino.offSetY-19,color=(0,0,0))
                    


def main():
    tetris=Tetris()
    while(tetris.running):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                tetris.running = False
            else:
                if event.type==pygame.KEYDOWN:
                    #tetris.unDrawTetromino(tetris.tetromino)
                    tetris.tetromino.action(event.key,tetris)
                    
        if tetris.gameTick():
            tetris.tetromino.moveDown(tetris)
        tetris.drawBoard()
        pygame.display.update()

main()
