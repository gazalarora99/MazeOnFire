'''
Created on Jan 30, 2021

@author: Jishan
'''
import pygame
import time
import random

#Initializing pygame
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
#Initializing colors
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0, 255, 0)
GRAY = (128,128,128)
class Square:
    def __init__(self,row_num, col_num, dimension,type):
        self.row = row_num
        self.col = col_num
        self.width = dimension // 500
        self.Square_type = type
        self.isStart = row_num == 0 and col_num == 0;
        if self.Square_type == 1:
            self.color = BLACK
        elif self.Square_type == 2:
            self.color = GREEN
        else :
            self.color = WHITE        
    def get_pos(self):
        return self.row,self.col
    def get_type(self):
        return self.Square_type
    def get_isStart(self):
        return self.isStart
class Maze:
    def __init__(self,dimension,pr):
        self.rows = dimension
        self.cols = dimension
        self.grid = []
    ### makes 2d array with given dimensions and has square objects in it.
    def populate_grid(self,dimension,pr):
        for i in range(0,self.rows):
            print()
            self.grid.append([])
            for j in range(0,self.cols):
                if i == 0 and j == 0:
                    self.grid[i].append(Square(i,j,dimension,0))
                    print("S", end = " ")
                elif i == self.rows -1 and j == self.cols -1 :
                    self.grid[i].append(Square(i,j,dimension,2))
                    print("E ", end = " ")
                else:
                    x = random.uniform(0, 1)
                    if x <= pr:
                        self.grid[i].append(Square(i,j,dimension,1))
                        print("@",end = " ")
                    else:
                        self.grid[i].append(Square(i,j,dimension,0))
                        print("_",end = " ")      
    def build_maze(self,pr,screen): 
        #Locations of obstacles/barriers
        ###self.populate_grid(pr,screen)
        self.x = 0
        self.y = 0
        self.entry_size =   dimension // 500
        if self.entry_size < 1:
            self.entry_size = 20
        for i in range(0,self.rows):
            self.x = 20;
            self.y +=20; #change rows
            for j in range(0,self.cols):
                pygame.display.flip()
                if self.grid[i][j].get_isStart(): ##Encountered start node!
                     start_rect =  pygame.Rect(self.x, self.y, self.entry_size, self.entry_size)
                     pygame.draw.rect(screen,GREEN,start_rect)  
                elif self.grid[i][j].get_type() == 0:
                     normal_rect = pygame.Rect(self.x, self.y, self.entry_size, self.entry_size)
                     pygame.draw.rect(screen,WHITE,normal_rect)   
                elif self.grid[i][j].get_type() == 1:
                     block_rect = pygame.Rect(self.x, self.y, self.entry_size, self.entry_size)
                     pygame.draw.rect(screen,BLACK,block_rect)    
                else:
                     end_rect =  pygame.Rect(self.x, self.y, self.entry_size, self.entry_size)
                     pygame.draw.rect(screen,GREEN,end_rect)        
                pygame.display.update()
                self.x+=20                                   
        #Initializing the grid
if __name__ == '__main__':
    dimension = int(input("Enter Dimension: "))
    probability = float(input("Enter Probability: "))
    
    m = Maze(dimension,probability)
    ##screen = pygame.display.set_mode((500, 500))
    m.populate_grid(dimension, probability)
    ##m.build_maze(probability, screen)
''' running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # update pygame's display to display everything
        pygame.display.update()'''
            
