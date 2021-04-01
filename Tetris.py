import pygame

import math
class Tetromino:
    def __init__(self):
        pass

    def rotate(self):
        pass

class Tetris:
    def __init__(self):
        pygame.init()
        self.screen=pygame.display.set_mode((800, 640))
        pygame.display.set_caption("Tetris")
        self.running=True
        self.board=[[0 for x in range(10)] for x in range(40)]

    def __del__(self):
        pygame.quit()

    def drawRect(self,i,j):
        rectangle=pygame.Rect(i*50,j*50,40,40)
        pygame.draw.rect(self.screen,(200,10,10),rectangle)

    def drawBoard(self):
        self.board[5][5]=1
        for i in range(21):
            for j in range(10):
                if self.board[i][j]:
                    self.drawRect(i,j)
        pygame.display.update()




def main():
    tetris=Tetris()
    while(tetris.running):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                tetris.running = False
            else:
                tetris.drawBoard()
    

main()
