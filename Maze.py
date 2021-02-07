'''
Created on Jan 30, 2021

@author: Jishan Desai
@author: Gazal Arora
'''
import pygame
import time
import random
from collections import deque
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
    def __init__(self,row_num, col_num, dimension, square_type):
        self.row = row_num
        self.col = col_num
        self.width = dimension // 500
        self.Square_type = square_type
        self.parent_row = -1
        self.parent_col = -1
        self.visited = False
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
    def set_parent(self, parent_row, parent_col):
        self.parent_row = parent_row
        self.parent_col = parent_col
    def get_parent(self):
        return self.parent_row, self.parent_col
    def is_visited(self):
        return self.visited
    def set_visited(self):
        self.visited = True
    def is_wall(self):
        r,c = self.get_pos()
        return c == 0 or c == dimension -1 or r == 0 or r == dimension -1
class Maze:
    def __init__(self,dimension,pr):
        self.rows = dimension
        self.cols = dimension
        self.grid = []
    ### makes 2d array with given dimensions and has square objects in it.
    def populate_grid(self,dimension,pr):
        
        for i in range(0,self.rows):
            print()
            
            for j in range(0,self.cols):
                if i == 0 and j == 0:
                    #self.grid.append()
                    self.grid.append(Square(i,j,dimension,3))
                    
                    print("S", end = " ")
                elif i == self.rows -1 and j == self.cols -1 :
                    #self.grid.append([])
                    self.grid.append(Square(i,j,dimension,2))
                    
                    print("E ", end = " ")
                else:
                    x = random.uniform(0, 1)
                    if x <= pr:
                        #self.grid.append([])
                        self.grid.append(Square(i,j,dimension,1))
                        
                        print("@",end = " ")
                    else:
                        #self.grid.append([])
                        self.grid.append(Square(i,j,dimension,0))
                        
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
    
    
    def is_parent(self, p1, p2, pos):
        r1, r2 = self.grid[pos].get_pos()
        
        if  (r1==p1 and r2==p2):
            #print("not child")
            return True
        #print("yes, child")
        return False
    
    def add_to_fringe(self, pos, i, j, stack, p1, p2):
        #print("checking (" + str(i) + ", " + str(j) + ")'s child "+ str(pos))
        if (self.grid[pos].get_type()==0) and (not self.is_parent(p1, p2, pos)) and (self.grid[pos].is_visited() == False): 
            self.grid[pos].set_parent(i,j)
            stack.append(self.grid[pos]) 
            #print("yes, child")       
    
    #function to get fringe from current state located at Square(r,c)
    def get_fringe(self, r, c):
        p1, p2 = self.grid[(self.cols*r) + c].get_parent()
        
        right = (self.cols*r) + c +1
        left = (self.cols*r) + c - 1
        top =  (self.cols * (r-1)) + c
        bottom = (self.cols * (r+1)) + c
        stack = []
        i = r
        j = c
        
            
        if i==self.rows-1 and j==self.cols-1: #check if its goal state
            k = (self.cols*i) + j
            self.grid[k].set_parent(i,j)
            stack.append(self.grid[k])
            return stack
        
        if i==0 and j==0:
            self.add_to_fringe(right, i, j, stack, p1, p2)
            self.add_to_fringe(bottom, i, j, stack, p1, p2)
            return stack
        
        if i==self.rows-1 and j==self.cols-2:
            k = (self.cols*i) + j 
            self.grid[right].set_parent(i,j)
            stack.append(self.grid[k+1]) #right square that is goal
            return stack
        
        if j==self.cols -1 and i==self.rows-2:
            k =  (self.cols * (i+1)) + j
            self.grid[k].set_parent(i,j)
            stack.append(self.grid[k]) #bottom square that is the goal
            return stack
        
        if i==0 and j==self.cols-1: #top-right corner so can only go left or bottom here
            self.add_to_fringe(left, i, j, stack, p1, p2)
            self.add_to_fringe(bottom, i, j, stack, p1, p2)
            return stack
        
        if j==0 and i==self.rows-1: #bottom-left corner so can only go top or right here
            self.add_to_fringe(top, i, j, stack, p1, p2)
            self.add_to_fringe(right, i, j, stack, p1, p2)
            return stack
        
        #to save an index out of bound exception, 
        #following if statements will take care of corner Squares
        #which may not have a square at either its left or right or top or bottom
        #when looking for next possible position (children)
        
        if i==0 and j>0 and j<self.cols -1:
            self.add_to_fringe(left, i, j, stack, p1, p2)
            self.add_to_fringe(right, i, j, stack, p1, p2)
            self.add_to_fringe(bottom, i, j, stack, p1, p2)
            
        if j==0 and i>0 and i<self.rows -1:
            self.add_to_fringe(top, i, j, stack, p1, p2)
            self.add_to_fringe(right, i, j, stack, p1, p2)
            self.add_to_fringe(bottom, i, j, stack, p1, p2)
            
        if i==self.rows -1 and j>0 and j<self.cols-1:
            self.add_to_fringe(top, i, j, stack, p1, p2)
            self.add_to_fringe(left, i, j, stack, p1, p2)
            self.add_to_fringe(right, i, j, stack, p1, p2)
            
        if j==self.cols -1 and i>0 and i<self.rows-1:
            self.add_to_fringe(top, i, j, stack, p1, p2)
            self.add_to_fringe(left, i, j, stack, p1, p2)
            self.add_to_fringe(bottom, i, j, stack, p1, p2)
                
        if i>0 and i<self.rows-1 and j>0 and j<self.cols-1 :
            self.add_to_fringe(top, i, j, stack, p1, p2)
            self.add_to_fringe(left, i, j, stack, p1, p2)
            self.add_to_fringe(right, i, j, stack, p1, p2)
            self.add_to_fringe(bottom, i, j, stack, p1, p2)
        
        return stack
    def printPath(self,curr_loc):
        solution = []
        while self.grid[curr_loc].get_type() != 3:
            solution.append(self.grid[curr_loc].get_pos())
            r,c = self.grid[curr_loc].get_parent();
            curr_loc = (self.cols*r) + c 
        solution.reverse()
        print(solution)
    def bfs(self,start_square):
        fringe = deque()
        fringe.appendleft(start_square)
        i = 0;
        while fringe :
            i = i + 1
            curr = fringe.pop()
            #print(str(i) + "Querying: " + str(curr.get_pos()))
            r,c  = curr.get_pos()
            right = (self.cols*r) + c +1
            left = (self.cols*r) + c - 1
            top =  (self.cols * (r-1)) + c
            bottom = (self.cols * (r+1)) + c
            curr_loc = (self.cols*r) + c 
            if r == self.rows-1 and c == self.cols - 1:
                self.printPath(curr_loc)
                ##print(curr.get_parent())
                return
            if curr.get_isStart():
                if self.grid[right].get_type() !=1 :
                    fringe.appendleft(self.grid[right])
                    self.grid[right].set_parent(r,c)
                if self.grid[bottom].get_type() !=1 :    
                    fringe.appendleft(self.grid[bottom])
                    self.grid[bottom].set_parent(r,c)
            elif curr.is_wall():
                if c != self.cols - 1 and self.grid[right].is_visited() is False and self.grid[right].get_type()!= 1:
                    if self.grid[right] not in fringe :
                        self.grid[right].set_parent(r,c)
                        fringe.appendleft(self.grid[right]) 
                elif c != 0 and self.grid[left].is_visited() is False and self.grid[left].get_type()!= 1:
                    if self.grid[left] not in fringe :
                        self.grid[left].set_parent(r,c)
                        fringe.appendleft(self.grid[left])    
                if r != self.rows -1 and self.grid[bottom].is_visited() is False and self.grid[bottom].get_type()!= 1:
                    if self.grid[bottom] not in fringe :
                        self.grid[bottom].set_parent(r,c)
                        fringe.appendleft(self.grid[bottom])    
                elif r != 0 and self.grid[top].is_visited() is False and self.grid[top].get_type()!= 2:
                    if self.grid[top] not in fringe :
                        self.grid[top].set_parent(r,c)
                        fringe.appendleft(self.grid[top])       
            else:
                if self.grid[right].get_type()!= 1 and self.grid[right].is_visited() is False:
                    if self.grid[right] not in fringe :
                        self.grid[right].set_parent(r,c)
                        fringe.appendleft(self.grid[right])
                if self.grid[left].get_type()!= 1 and self.grid[left].is_visited() is False:
                    if self.grid[left] not in fringe :
                        self.grid[left].set_parent(r,c)
                        fringe.appendleft(self.grid[left]) 
                if self.grid[bottom].get_type()!= 1 and self.grid[bottom].is_visited() is False:
                    if self.grid[bottom] not in fringe :
                        self.grid[bottom].set_parent(r,c)
                        fringe.appendleft(self.grid[bottom]) 
                if self.grid[top].get_type()!= 1 and self.grid[top].is_visited() is False:
                    if self.grid[top] not in fringe :
                        self.grid[top].set_parent(r,c)
                        fringe.appendleft(self.grid[top])  
                            
            self.grid[(self.cols*r) + c ].set_visited()
        print("Not Done")
        return
    def dfs(self, fringe, path): 
        #path = []  
        #fringe = self.get_fringe(0,0)
        t1=time.time()
        if (self.grid[1].get_type()==1) and (self.grid[(self.cols*1) + 0].get_type()==1):
            t2 = time.time()
            print(time.strftime("%H:%M:%S", time.gmtime(t2-t1)))
            return "No solution"
        elif (self.grid[(self.cols * (self.rows-1)) + self.cols -2].get_type()==1) and (self.grid[(self.cols * (self.rows-2)) + self.cols - 1].get_type()==1):
            t2 = time.time()
            print(time.strftime("%H:%M:%S", time.gmtime(t2-t1)))
            return "No solution"
        i = 0;
        
        while (path!=[] or i==0):
            if(fringe==[]):
                #temp =
                #path.pop() #remove the last object with no children
                if path==[]:
                    t2 = time.time()
                    print(time.strftime("%H:%M:%S", time.gmtime(t2-t1)))
                    return "No solution"
                current = path.pop() #go to parent
                m, n = current.get_pos()
                fringe = self.get_fringe(m, n)
                continue
                
            current = fringe.pop() #current is of type Square
            #print("Exploring " + str(current.get_pos()) + "'s children")
            #print(type(current))
            current.set_visited()
            if current.get_type() == 2: #goal state if Square's type is 2
                print("i value is "+str(i))
                t2 = time.time()
                print(time.strftime("%H:%M:%S", time.gmtime(t2-t1)))
                return "success, goal reached"
            
            m, n = current.get_pos()
            position = (self.cols * m) + n
            path.append(self.grid[position])
            fringe = self.get_fringe(m, n) #temporary list from get_fringe method
            #if(temp != []):
                #for k in range(0, len(temp)): #iterate through temp in fifo order and add it to fringe so that peek of fringe is the last element visited in get_fringe
                    #fringe.append(temp[k])
            
                
                #if(temp_fringe!=[]):
                    #for k in range(0, len(temp_fringe)):
                        #if(temp_fringe[k].get_pos() != temp.get_pos()):
                            #fringe.append(temp_fringe[k])
                
            i= i+1
            #if i==25:
                #print("i value is 25")
                #break
            #self.dfs(fringe, path)
            #print("idhar"+str(type(self.get_fringe(m, n))))
            #prev = current
        t2 = time.time()
        print(time.strftime("%H:%M:%S", time.gmtime(t2-t1)))    
        print("i value is " + str(i))
        return "failed"
            
            
        
        
          
#Initializing the grid
if __name__ == '__main__':
    dimension = int(input("Enter Dimension: "))
    probability = float(input("Enter Probability: "))
    
    m = Maze(dimension,probability)
    ##screen = pygame.display.set_mode((500, 500))
    m.populate_grid(dimension, probability)
    print()
    #for i in range(0, len(m.grid)):
    #    print(m.grid[i].get_pos())
    m.grid[0].set_parent(0, 0)
    m.bfs(m.grid[0])
    #print(m.dfs(m.get_fringe(0,0),[]))
    ##m.build_maze(probability, screen)
    
    
''' running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # update pygame's display to display everything
        pygame.display.update()'''
            
