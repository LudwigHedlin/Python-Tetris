import pygame
import time
import math

class Tetromino:
    def __init__(self):
        self.shape=[[0 for i in range(3)] for i in range(3)]
        self.offSetX=0
        self.offSetY=19
        self.color=None
        self.lastAction=None #set when taking an action
        

    def rotate(self):
        size = len(self.shape)
        rotated = [[0 for i in range(size)] for i in range(size)]
        for i in range(size):
            for j in range(size):
                rotated[i][j] = self.shape[j][size-1-i]
        self.shape=rotated

    def __kick__(self,board,direction):
        pass

    def freezePiece(self,tetris):
        board=tetris.board
        for i in range(4):
            for j in range(4):
                if self.shape[i][j]:
                    board[i+self.offSetY][j+self.offSetX]=self.shape[i][j]
        
    def displayPiece(self):
        self.offSetX=15
        self.offsetY=23

    def boardPiece(self):
        self.offsetX=0
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
            self.freezePiece(tetris)
    
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


    
        

class Tetromino1(Tetromino):
    def __init__(self):
        super().__init__()
        self.shape = [[0 for x in range(4)] for x in range(4)]
        self.color=(0,200,0)
        for i in range(4):
            self.shape[i][1] = 1



class Tetris:
    def __init__(self):
        pygame.init()
        self.screen=pygame.display.set_mode((1000, 800))
        pygame.display.set_caption("Tetris")
        self.tetromino=Tetromino1()
        self.displayTetromino=Tetromino1()
        self.displayTetromino.displayPiece()
        self.drawTetromino(self.displayTetromino)
        self.running=True
        self.board=[[0 for x in range(10)] for x in range(40)]
        self.speed=1.0
        self.time=time.process_time()

        self.score=0

    def __del__(self):
        pygame.quit()
    
    def color(tetrominoType):
        pass

    def freezePiece(self,tetromino):
        #probably better to use this one so that it can call checkRows and clearRow
        for i in range(len(tetromino.shape)):
            for j in range(len(tetromino.shape[0])):
                if tetromino.shape[i][j]:
                    self.board[i+tetromino.offSetY][j+tetromino.offSetX] = tetromino.shape[i][j]

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
        font=pygame.font.SysFont('bold', 20)

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
        
        

    def start(self):
        pass


    def drawRect(self, i, j, color=(200, 150, 10)):
        rectangle = pygame.Rect(100+i*25, 100+j*25, 25, 25)
        pygame.draw.rect(self.screen,color,rectangle)

    def drawBoard(self):
        self.screen.fill((0, 0, 0))
        self.drawTetromino(self.tetromino)
        self.drawScore()
        for i in range(19,40):
            for j in range(10):
                if self.board[i][j]:
                    self.drawRect(j,i-19)
        
    
    def drawTetromino(self,tetromino):
        for i in range(len(tetromino.shape)):
            for j in range(len(tetromino.shape[0])):
                if tetromino.shape[i][j]:

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
                    tetris.drawTetromino(tetris.tetromino)
                    tetris.clearFullRows()
                    
                
            
                
        if tetris.gameTick():
            tetris.tetromino.moveDown(tetris)
        tetris.drawBoard()
        pygame.display.update()

main()
