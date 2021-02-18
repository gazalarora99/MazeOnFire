'''
Created on Jan 30, 2021

@author: Jishan Desai
@author: Gazal Arora
'''
import pygame
from timeit import default_timer as timer
import time
import datetime
import random
import heapq
from collections import deque
from math import sqrt
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
        self.current_dist = 0
        self.heuristic = self.current_dist + sqrt(((dimension - 1 - self.row)**2) + ((dimension - 1 - self.col)**2))
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
    def set_distance(self, n, mode, q, fr, fc):
        if mode == 0:  #regular A star
            self.current_dist = n
            self.heuristic = n + sqrt(((dimension - 1 - self.row)**2) + ((dimension - 1 - self.col)**2))
        elif mode==1 : #strategy 3 A star
            self.heuristic =  (sqrt(((dimension - 1 - self.row)**2) + ((dimension - 1 - self.col)**2))) - ((sqrt(((fr - self.row)**2) + ((fc - self.col)**2)))*q)
            #print(f'{self.row}, {self.col}: dist from end {(sqrt(((dimension - 1 - self.row)**2) + ((dimension - 1 - self.col)**2)))} - dist from fire {(q * (sqrt(((fr - self.row)**2) + ((fc - self.col)**2))))}')
    def set_type(self, n):
        self.Square_type = n
    def is_wall(self):
        r,c = self.get_pos()
        return c == 0 or c == dimension - 1 or r == 0 or r == dimension - 1
    def __lt__(self, other):
        return self.heuristic < other.heuristic
    def __str__(self):
        return str("({} , {}) : dist {}".format(self.row, self.col, self.heuristic))
class Maze:
    def __init__(self,dimension,pr):
        self.rows = dimension
        self.cols = dimension
        self.grid = []
        self.fire_squares = []
    def print_grid(self,currloc):
        for i in range(0,self.rows):
            print()
            for j in range(0,self.cols):
                if self.grid[(self.cols * i) + j].get_type() == 3:
                    print("S", end = " ")
                if ((self.cols*i) + j)  == currloc:
                    print("*", end=" ") 
                elif self.grid[(self.cols*i) + j].get_type() == 0:
                    print("_", end = " ")
                elif self.grid[(self.cols*i) + j].get_type() == 1:
                    print("@", end = " ")
                elif self.grid[(self.cols*i) + j].get_type() == 4:
                    print("F", end = " ")       
                elif self.grid[(self.cols*i) + j].get_type() == 2:
                    print("E", end = " ")                           
    ### makes 2d array with given dimensions and has square objects in it.
    def populate_grid(self,dimension,pr):
        
        for i in range(0,self.rows):
            #print()
            
            for j in range(0,self.cols):
                if i == 0 and j == 0:
                    #self.grid.append()
                    self.grid.append(Square(i,j,dimension,3))
                    
                    #print("S", end = " ")
                elif i == self.rows -1 and j == self.cols -1 :
                    #self.grid.append([])
                    self.grid.append(Square(i,j,dimension,2))
                    
                    #print("E ", end = " ")
                else:
                    
                    x = random.uniform(0, 1)
                    if x <= pr:
                        #self.grid.append([])
                        self.grid.append(Square(i,j,dimension,1))
                        
                        #print("@",end = " ")
                    else:
                        #self.grid.append([])
                        self.grid.append(Square(i,j,dimension,0))
                        
                        #print("_",end = " ")  
                        
                    
            
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
    
    def create_fire(self, dim):
        x = random.randint(0, dim-1)
        y = random.randint(0, dim-1)
        self.grid[(self.cols * x)+y].set_type(4)
        return x, y
    
    def advance_fire(self,q):
        fire_list=[]
        for Square in self.grid:
            r,c = Square.get_pos()
            right = (self.cols*r) + c +1
            left = (self.cols*r) + c - 1
            top =  (self.cols * (r-1)) + c
            bottom = (self.cols * (r+1)) + c
            k = 0;
            if Square.get_type() != 4 and Square.get_type() != 1:
                if Square.is_wall():
                    if r != self.rows -1:
                        if self.grid[bottom].get_type() == 4:
                            k = k+1
                    elif r != 0:
                        if self.grid[top].get_type() ==4:
                            k = k+1
                    if c != 0:
                        if self.grid[left].get_type() == 4:
                            k = k+1
                    elif c != self.cols:
                        if self.grid[right].get_type() == 4:
                            k = k+1
                else:
                    if self.grid[top].get_type() == 4:
                        k = k+1
                    if self.grid[left].get_type() == 4:
                        k = k+1
                    if self.grid[right].get_type() ==4:
                        k = k+1
                    if self.grid[bottom].get_type() == 4:
                        k = k+1
                prob = 1 - (1 - q)**k
                if random.uniform(0,1) <= prob:
                    fire_list.append(Square.get_pos())
                    self.fire_squares.append(Square.get_pos())
        for pair in fire_list:
            i,j = pair
            curr = (self.cols*i) + j 
            self.grid[curr].set_type(4)                                         
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
    
    def printPath(self,curr_loc, start_square):
        solution = []
        while curr_loc != start_square:
            solution.append(self.grid[curr_loc].get_pos())
            r,c = self.grid[curr_loc].get_parent();
            curr_loc = (self.cols*r) + c 
        solution.reverse()
        #print(solution)
        return solution
    
    def closest_fire_loc(self, r, c):
        if self.fire_squares==[]:
            return r, c
        r1, c1 = self.fire_squares[0]
        ed = sqrt( ((r-r1)**2) + ((c-c1)**2) )
        
        for pair in self.fire_squares:
            i, j = pair
            if (ed > sqrt( ((r-i)**2) + ((c-j)**2) )):
                r1 = i 
                c1 = j
                ed = sqrt( ((r-i)**2) + ((c-j)**2) )
        
        return r1, c1
    
    def strat3_a_star(self, start_square, q, mode, fire_row, fire_col):
        
        t1=time.time()
        
        if (self.grid[1].get_type()==1) and (self.grid[(self.cols*1) + 0].get_type()==1):
            t2 = time.time()
           # print(time.strftime("%H:%M:%S", time.gmtime(t2-t1)))
          #  print( "No solution")
            return 2
        elif (self.grid[(self.cols * (self.rows-1)) + self.cols -2].get_type()==1) and (self.grid[(self.cols * (self.rows-2)) + self.cols - 1].get_type()==1):
            t2 = time.time()
           # print(time.strftime("%H:%M:%S", time.gmtime(t2-t1)))
           # print( "No solution")
            return 2
        
        fringe = []
        heapq.heappush(fringe, start_square)
        i = 0
        while fringe :
            i = i + 1
            curr = heapq.heappop(fringe)
            curr.set_visited()
            r,c  = curr.get_pos()
            p1, p2 = curr.get_parent()
            #curr.set_distance(self.grid[(self.cols*p1) + p2].current_dist + 1)
            #print("dist = " + str(curr.current_dist) + ", heur = " + str(curr.heuristic) + ", r = " + str(r) + ", c = " + str(c))
            #print(curr.__str__())
            right = (self.cols*r) + c + 1
            left = (self.cols*r) + c - 1
            top =  (self.cols * (r-1)) + c
            bottom = (self.cols * (r+1)) + c
            curr_loc = (self.cols*r) + c 
            #fr, fc = self.closest_fire_loc(r,c)
            
            if mode == 1 and r == self.rows-1 and c == self.cols - 1:
                #self.printPath(curr_loc)
                t2 = time.time()
               # print(time.strftime("%H:%M:%S", time.gmtime(t2-t1)))
                #print("success, goal reached")
                #print( "done")
                return 0
            
            if mode == 2 and r == fire_row and c == fire_col:
                print("path exists from start to fire")
                return 1
            
            if curr.get_isStart():
                if self.grid[right].get_type() == 0 :
                    fr, fc = self.closest_fire_loc(r,c+1)
                    print(fr, fc)
                    self.grid[right].set_distance(0, 1, q, fr, fc)
                    self.grid[right].set_parent(r,c)
                    heapq.heappush(fringe, self.grid[right])
                    #print(f'{self.grid[right].current_dist}')
                    
                if self.grid[bottom].get_type() == 0 : 
                    fr, fc = self.closest_fire_loc(r+1,c)
                    #print(fr, fc)
                    self.grid[bottom].set_distance(0, 1, q, fr, fc)
                    self.grid[bottom].set_parent(r,c)
                    heapq.heappush(fringe, self.grid[bottom])
                    #print(f'{self.grid[bottom].current_dist}')
                    
            elif curr.is_wall():
                if (c != self.cols - 1) and (self.grid[right].is_visited() is False) and (self.grid[right].get_type() == 0 or self.grid[right].get_type() == 2) and (self.is_parent(p1, p2, right) is False):
                    if self.grid[right] not in fringe :
                        fr, fc = self.closest_fire_loc(r,c+1)
                        #print(fr, fc)
                        self.grid[right].set_distance(self.grid[curr_loc].current_dist + 1, 1, q, fr, fc)
                        self.grid[right].set_parent(r,c)
                        heapq.heappush(fringe, self.grid[right]) 
                elif (c != 0) and (self.grid[left].is_visited() is False) and (self.grid[left].get_type()==0) and (self.is_parent(p1, p2, left) is False):
                    if self.grid[left] not in fringe :
                        fr, fc = self.closest_fire_loc(r,c-1)
                       # print(fr, fc)
                        self.grid[left].set_distance(self.grid[curr_loc].current_dist + 1, 1, q, fr, fc)
                        self.grid[left].set_parent(r,c)
                        heapq.heappush(fringe, self.grid[left])     
                if (r != self.rows -1) and (self.grid[bottom].is_visited() is False) and (self.grid[bottom].get_type()==0 or self.grid[right].get_type() == 2) and (self.is_parent(p1, p2, bottom) is False):
                    if self.grid[bottom] not in fringe :
                        fr, fc = self.closest_fire_loc(r+1,c)
                        #print(fr, fc)
                        self.grid[bottom].set_distance(self.grid[curr_loc].current_dist + 1, 1, q, fr, fc)
                        self.grid[bottom].set_parent(r,c)
                        heapq.heappush(fringe, self.grid[bottom])    
                elif (r != 0) and (self.grid[top].is_visited() is False) and (self.grid[top].get_type()==0) and (self.is_parent(p1, p2, top) is False):
                    if self.grid[top] not in fringe :
                        fr, fc = self.closest_fire_loc(r-1,c)
                        #print(fr, fc)
                        self.grid[top].set_distance(self.grid[curr_loc].current_dist + 1, 1, q, fr, fc)
                        self.grid[top].set_parent(r,c)
                        heapq.heappush(fringe, self.grid[top])         
            else:
                if (self.grid[right].get_type()==0) and (self.grid[right].is_visited() is False) and (self.is_parent(p1, p2, right) is False):
                    if self.grid[right] not in fringe :
                        fr, fc = self.closest_fire_loc(r,c+1)
                        #print(fr, fc)
                        self.grid[right].set_distance(self.grid[curr_loc].current_dist + 1, 1, q, fr, fc)
                        self.grid[right].set_parent(r,c)
                        heapq.heappush(fringe, self.grid[right]) 
                if (self.grid[bottom].get_type()==0) and (self.grid[bottom].is_visited() is False) and (self.is_parent(p1, p2, bottom) is False):
                    if self.grid[bottom] not in fringe :
                        fr, fc = self.closest_fire_loc(r+1,c)
                        #print(fr, fc)
                        self.grid[bottom].set_distance(self.grid[curr_loc].current_dist + 1, 1, q, fr, fc)
                        self.grid[bottom].set_parent(r,c)
                        heapq.heappush(fringe, self.grid[bottom])  
                if (self.grid[left].get_type()==0) and (self.grid[left].is_visited() is False) and (self.is_parent(p1, p2, left) is False):
                    if self.grid[left] not in fringe :
                        fr, fc = self.closest_fire_loc(r,c-1)
                        #print(fr, fc)
                        self.grid[left].set_distance(self.grid[curr_loc].current_dist + 1, 1, q, fr, fc)
                        self.grid[left].set_parent(r,c)
                        heapq.heappush(fringe, self.grid[left])
                if (self.grid[top].get_type()==0) and (self.grid[top].is_visited() is False) and (self.is_parent(p1, p2, top) is False):
                    if self.grid[top] not in fringe :
                        fr, fc = self.closest_fire_loc(r-1,c)
                        #print(fr, fc)
                        self.grid[top].set_distance(self.grid[curr_loc].current_dist + 1, 1, q, fr, fc)
                        self.grid[top].set_parent(r,c)
                        heapq.heappush(fringe, self.grid[top])  
                         
        t2 = time.time()
        #print(time.strftime("%H:%M:%S", time.gmtime(t2-t1)))
        #print("Not Done")
        return 2 
                    
    
    
    
    def a_star(self, start_square):
        
        t1=time.time()
        
        if (self.grid[1].get_type()==1) and (self.grid[(self.cols*1) + 0].get_type()==1):
            t2 = time.time()
            print(time.strftime("%H:%M:%S", time.gmtime(t2-t1)))
            return "No solution"
        elif (self.grid[(self.cols * (self.rows-1)) + self.cols -2].get_type()==1) and (self.grid[(self.cols * (self.rows-2)) + self.cols - 1].get_type()==1):
            t2 = time.time()
            print(time.strftime("%H:%M:%S", time.gmtime(t2-t1)))
            return "No solution"
        
        fringe = []
        heapq.heappush(fringe, start_square)
        i = 0
        while fringe :
            i = i + 1
            curr = heapq.heappop(fringe)
            curr.set_visited()
            r,c  = curr.get_pos()
            p1, p2 = curr.get_parent()
            #curr.set_distance(self.grid[(self.cols*p1) + p2].current_dist + 1)
            #print("dist = " + str(curr.current_dist) + ", heur = " + str(curr.heuristic) + ", r = " + str(r) + ", c = " + str(c))
            #print(curr.__str__())
            right = (self.cols*r) + c + 1
            left = (self.cols*r) + c - 1
            top =  (self.cols * (r-1)) + c
            bottom = (self.cols * (r+1)) + c
            curr_loc = (self.cols*r) + c 
            
            if r == self.rows-1 and c == self.cols - 1:
                #self.printPath(curr_loc)
                t2 = time.time()
                print(time.strftime("%H:%M:%S", time.gmtime(t2-t1)))
                print("success, goal reached")
                return "done"
            
            
            
            if curr.get_isStart():
                if self.grid[right].get_type() == 0 :
                    self.grid[right].set_distance(1, 0, 0, 0, 0)
                    self.grid[right].set_parent(r,c)
                    heapq.heappush(fringe, self.grid[right])
                    #print(f'{self.grid[right].current_dist}')
                    
                if self.grid[bottom].get_type() == 0 : 
                    self.grid[bottom].set_distance(1, 0, 0, 0, 0)
                    self.grid[bottom].set_parent(r,c)
                    heapq.heappush(fringe, self.grid[bottom])
                    #print(f'{self.grid[bottom].current_dist}')
                    
            elif curr.is_wall():
                if (c != self.cols - 1) and (self.grid[right].is_visited() is False) and (self.grid[right].get_type() != 1) and (self.is_parent(p1, p2, right) is False):
                    if self.grid[right] not in fringe :
                        self.grid[right].set_distance(self.grid[curr_loc].current_dist + 1, 0, 0, 0, 0)
                        self.grid[right].set_parent(r,c)
                        heapq.heappush(fringe, self.grid[right]) 
                elif (c != 0) and (self.grid[left].is_visited() is False) and (self.grid[left].get_type()==0) and (self.is_parent(p1, p2, left) is False):
                    if self.grid[left] not in fringe :
                        self.grid[left].set_distance(self.grid[curr_loc].current_dist + 1, 0, 0, 0, 0)
                        self.grid[left].set_parent(r,c)
                        heapq.heappush(fringe, self.grid[left])     
                if (r != self.rows -1) and (self.grid[bottom].is_visited() is False) and (self.grid[bottom].get_type()!=1) and (self.is_parent(p1, p2, bottom) is False):
                    if self.grid[bottom] not in fringe :
                        self.grid[bottom].set_distance(self.grid[curr_loc].current_dist + 1, 0, 0, 0, 0)
                        self.grid[bottom].set_parent(r,c)
                        heapq.heappush(fringe, self.grid[bottom])    
                elif (r != 0) and (self.grid[top].is_visited() is False) and (self.grid[top].get_type()==0) and (self.is_parent(p1, p2, top) is False):
                    if self.grid[top] not in fringe :
                        self.grid[top].set_distance(self.grid[curr_loc].current_dist + 1, 0, 0, 0, 0)
                        self.grid[top].set_parent(r,c)
                        heapq.heappush(fringe, self.grid[top])         
            else:
                if (self.grid[right].get_type()==0) and (self.grid[right].is_visited() is False) and (self.is_parent(p1, p2, right) is False):
                    if self.grid[right] not in fringe :
                        self.grid[right].set_distance(self.grid[curr_loc].current_dist + 1, 0, 0, 0, 0)
                        self.grid[right].set_parent(r,c)
                        heapq.heappush(fringe, self.grid[right]) 
                if (self.grid[bottom].get_type()==0) and (self.grid[bottom].is_visited() is False) and (self.is_parent(p1, p2, bottom) is False):
                    if self.grid[bottom] not in fringe :
                        self.grid[bottom].set_distance(self.grid[curr_loc].current_dist + 1, 0, 0, 0, 0)
                        self.grid[bottom].set_parent(r,c)
                        heapq.heappush(fringe, self.grid[bottom])  
                if (self.grid[left].get_type()==0) and (self.grid[left].is_visited() is False) and (self.is_parent(p1, p2, left) is False):
                    if self.grid[left] not in fringe :
                        self.grid[left].set_distance(self.grid[curr_loc].current_dist + 1, 0, 0, 0, 0)
                        self.grid[left].set_parent(r,c)
                        heapq.heappush(fringe, self.grid[left])
                if (self.grid[top].get_type()==0) and (self.grid[top].is_visited() is False) and (self.is_parent(p1, p2, top) is False):
                    if self.grid[top] not in fringe :
                        self.grid[top].set_distance(self.grid[curr_loc].current_dist + 1, 0, 0, 0, 0)
                        self.grid[top].set_parent(r,c)
                        heapq.heappush(fringe, self.grid[top])  
                         
        t2 = time.time()
        print(time.strftime("%H:%M:%S", time.gmtime(t2-t1)))
        #print("Not Done")
        return  "Not Done"
                    
                        
            ##mode = 1 for start to end
            # mode = 2 for start to fire  
    def bfs(self, start_square, fire_row, fire_col, mode):
        
        
        t1=time.time()
        if (self.grid[1].get_type()==1) and (self.grid[(self.cols*1) + 0].get_type()==1):
            t2 = time.time()
            #print(time.strftime("%H:%M:%S", time.gmtime(t2-t1)))
            #print("no solution")
            return 2
        elif (self.grid[(self.cols * (self.rows-1)) + self.cols -2].get_type()==1) and (self.grid[(self.cols * (self.rows-2)) + self.cols - 1].get_type()==1):
            t2 = time.time()
            #print(time.strftime("%H:%M:%S", time.gmtime(t2-t1)))
            #print("no solution")
            return 2
        
        fringe = deque()
        fringe.appendleft(start_square)
        i = 0
        while fringe :
            i = i + 1
            curr = fringe.pop()
            #need to set curr.set_visited() here
            #print(str(i) + "Querying: " + str(curr.get_pos()))
            r,c  = curr.get_pos()
            right = (self.cols*r) + c +1
            left = (self.cols*r) + c - 1
            top =  (self.cols * (r-1)) + c
            bottom = (self.cols * (r+1)) + c
            curr_loc = (self.cols*r) + c 
            if mode == 1 and r == self.rows-1 and c == self.cols - 1:
                #self.printPath(curr_loc)
                t2 = time.time()
                #print(time.strftime("%H:%M:%S", time.gmtime(t2-t1)))
                #print("solved")
                return 0
            
            if mode == 2 and r == fire_row and c == fire_col:
                #print("path exists from start to fire")
                return 1
            
            if curr.get_isStart():
                if self.grid[right].get_type() !=1 :
                    fringe.appendleft(self.grid[right])
                    self.grid[right].set_parent(r,c)
                if self.grid[bottom].get_type() !=1 :    
                    fringe.appendleft(self.grid[bottom])
                    self.grid[bottom].set_parent(r,c)
            elif curr.is_wall():
                if(mode==1):
                    if c != self.cols - 1 and self.grid[right].is_visited() is False and (self.grid[right].get_type()== 0 or self.grid[right].get_type()== 2):
                        if self.grid[right] not in fringe :
                            self.grid[right].set_parent(r,c)
                            fringe.appendleft(self.grid[right]) 
                    elif c != 0 and self.grid[left].is_visited() is False and self.grid[left].get_type()== 0:
                        if self.grid[left] not in fringe :
                            self.grid[left].set_parent(r,c)
                            fringe.appendleft(self.grid[left])    
                    if r != self.rows -1 and self.grid[bottom].is_visited() is False and (self.grid[bottom].get_type()== 0 or self.grid[bottom].get_type()==2):
                        if self.grid[bottom] not in fringe :
                            self.grid[bottom].set_parent(r,c)
                            fringe.appendleft(self.grid[bottom])    
                    elif r != 0 and self.grid[top].is_visited() is False and self.grid[top].get_type()==0:
                        if self.grid[top] not in fringe :
                            self.grid[top].set_parent(r,c)
                            fringe.appendleft(self.grid[top])
                elif mode==2:
                    if c != self.cols - 1 and self.grid[right].is_visited() is False and (self.grid[right].get_type()== 0 or self.grid[right].get_type()== 4):
                        if self.grid[right] not in fringe :
                            self.grid[right].set_parent(r,c)
                            fringe.appendleft(self.grid[right]) 
                    elif c != 0 and self.grid[left].is_visited() is False and (self.grid[left].get_type()== 0 or self.grid[left].get_type()== 4):
                        if self.grid[left] not in fringe :
                            self.grid[left].set_parent(r,c)
                            fringe.appendleft(self.grid[left])    
                    if r != self.rows -1 and self.grid[bottom].is_visited() is False and (self.grid[bottom].get_type()== 0 or self.grid[bottom].get_type()==4):
                        if self.grid[bottom] not in fringe :
                            self.grid[bottom].set_parent(r,c)
                            fringe.appendleft(self.grid[bottom])    
                    elif r != 0 and self.grid[top].is_visited() is False and (self.grid[top].get_type()==0 or self.grid[top].get_type()== 4):
                        if self.grid[top] not in fringe :
                            self.grid[top].set_parent(r,c)
                            fringe.appendleft(self.grid[top])       
            else:
                if(mode==1):
                    if self.grid[right].get_type()== 0 and self.grid[right].is_visited() is False:
                        if self.grid[right] not in fringe :
                            self.grid[right].set_parent(r,c)
                            fringe.appendleft(self.grid[right])
                    if self.grid[left].get_type()== 0 and self.grid[left].is_visited() is False:
                        if self.grid[left] not in fringe :
                            self.grid[left].set_parent(r,c)
                            fringe.appendleft(self.grid[left]) 
                    if self.grid[bottom].get_type()== 0 and self.grid[bottom].is_visited() is False:
                        if self.grid[bottom] not in fringe :
                            self.grid[bottom].set_parent(r,c)
                            fringe.appendleft(self.grid[bottom]) 
                    if self.grid[top].get_type()== 0 and self.grid[top].is_visited() is False:
                        if self.grid[top] not in fringe :
                            self.grid[top].set_parent(r,c)
                            fringe.appendleft(self.grid[top])
                elif mode==2:
                    if (self.grid[right].get_type()== 0 or self.grid[right].get_type()== 4)  and self.grid[right].is_visited() is False:
                        if self.grid[right] not in fringe :
                            self.grid[right].set_parent(r,c)
                            fringe.appendleft(self.grid[right])
                    if (self.grid[left].get_type()== 0 or self.grid[left].get_type()== 4) and self.grid[left].is_visited() is False:
                        if self.grid[left] not in fringe :
                            self.grid[left].set_parent(r,c)
                            fringe.appendleft(self.grid[left]) 
                    if (self.grid[bottom].get_type()== 0 or self.grid[bottom].get_type()== 4) and self.grid[bottom].is_visited() is False:
                        if self.grid[bottom] not in fringe :
                            self.grid[bottom].set_parent(r,c)
                            fringe.appendleft(self.grid[bottom]) 
                    if (self.grid[top].get_type()== 0 or self.grid[top].get_type()== 4)and self.grid[top].is_visited() is False:
                        if self.grid[top] not in fringe :
                            self.grid[top].set_parent(r,c)
                            fringe.appendleft(self.grid[top])  
                            
            self.grid[(self.cols*r) + c ].set_visited()
        t2 = time.time()
        #print(time.strftime("%H:%M:%S", time.gmtime(t2-t1)))
        #print("No solution")
        return 2
    
    def clear_visited(self):
        for i in self.grid:
            if (i.is_visited()):
                i.visited = False 
                
    
    def agent_moves(self, path):
        r, c = path[0]
        return r, c
    
    def strategy3(self, dim, q,x):
        #x = self.strat3_a_star(self.grid[0], q, 1, -1, -1)
        #fire_row, fire_col = m.create_fire(dim)
        #self.print_grid(-1)
        #self.fire_squares.append((fire_row, fire_col))
        end = (self.cols * (dim - 1)) + (dim - 1)
        path = None
        if(x==0):
            path = self.printPath(end, 0)
        
        while(x==0):
            self.clear_visited()
            r1, c1 = self.agent_moves(path)
            #path.pop(0)
            curr_loc = (self.cols*r1) + c1
            self.advance_fire(q)
            #print()
            #self.print_grid(curr_loc)
            if (r1==dim-1) and (c1==dim-1):
                return "goal reached"
            if (self.grid[end].get_type()==4):
                return "goal is on fire"
            if self.grid[curr_loc].get_type()== 4:
                    #print("on" + str(curr_loc))
                    print("Tu jaal gya bc")
                    return "agent's current loc caught fire"
            x = self.strat3_a_star(self.grid[ (self.cols * r1) + c1 ], q, 1, -1, -1)
            if(x==0):
                path = self.printPath(end, (self.cols * r1) + c1 )
        return "agent has no path left to the end"
    
    def strategy2(self, dim, q, x):
        #x = self.bfs(self.grid[0], -1, -1, 1)
        #fire_row, fire_col = m.create_fire(dim)
        end = (self.cols * (dim - 1)) + (dim - 1)
        path = None
        if(x==0):
            path = self.printPath(end, 0)
        
        while(x==0):
            self.clear_visited()
            r1, c1 = self.agent_moves(path)
            #path.pop(0)
            curr_loc = (self.cols*r1) + c1
            self.advance_fire(q)
            #print()
            #self.print_grid(curr_loc)
            if (r1==dim-1) and (c1==dim-1):
                return "goal reached"
            if (self.grid[end].get_type()==4):
                return "goal is on fire"
            if self.grid[curr_loc].get_type()== 4:
                    print("on" + str(curr_loc))
                    print("Tu jaal gya bc")
                    return "agent's current loc caught fire"
            x = self.bfs (self.grid[ (self.cols * r1) + c1 ], -1, -1, 1)
            if(x==0):
                path = self.printPath(end, (self.cols * r1) + c1 )
        return "agent has no path left to the end"
    
    def strategy1(self,dim, q):
        x = self.bfs(self.grid[0],-1,-1,1)
        fire_row, fire_col = m.create_fire(dim)
        end = (self.cols * (dim - 1)) + (dim - 1)
        path = self.printPath(end, 0)
        self.clear_visited()
        if(x==0):
            while(path!=[]):
                r1, c1 = self.agent_moves(path)
                path.pop(0)
                curr_loc = (self.cols*r1) + c1
                self.advance_fire(q)
                print()
                self.print_grid(curr_loc)
                if (r1==dim-1) and (c1==dim-1):
                    return "goal reached"
                if (self.grid[end].get_type()==4):
                    return "goal is on fire"
                if self.grid[curr_loc].get_type()== 4:
                    print("on" + str(curr_loc))
                    print("Tu jaal gya bc")
                    return "agent's current loc caught fire"
        return "agent has no path to the end"
        
        
    def dfs(self, fringe, path): 
        #path = []  
        #fringe = self.get_fringe(0,0)
        t1=time.time()
        if (self.grid[1].get_type()==1) and (self.grid[(self.cols*1) + 0].get_type()==1):
            t2 = time.time()
            print(time.strftime("%H:%M:%S", time.gmtime(t2-t1)))
            print("No solution")
            return 0
        elif (self.grid[(self.cols * (self.rows-1)) + self.cols -2].get_type()==1) and (self.grid[(self.cols * (self.rows-2)) + self.cols - 1].get_type()==1):
            t2 = time.time()
            print(time.strftime("%H:%M:%S", time.gmtime(t2-t1)))
            print("No solution")
            return 0
        i = 0;
        
        while (path!=[] or i==0):
            if(fringe==[]):
                #temp =
                #path.pop() #remove the last object with no children
                if path==[]:
                    t2 = time.time()
                    print(time.strftime("%H:%M:%S", time.gmtime(t2-t1)))
                    print("No solution")
                    return 0
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
                print("success, goal reached")
                return 1
            
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
        print("failed")
        return 0
            
            
        
        
          
#Initializing the grid
if __name__ == '__main__':
    dimension = int(input("Enter Dimension: "))
    probability = float(input("Enter Probability: "))
    flammability = float(input("Enter Flammability rate: "))
    
    m = Maze(dimension,probability)
    ##screen = pygame.display.set_mode((500, 500))
    m.populate_grid(dimension, probability)
    #start = datetime.datetime.now()
    #print(f'{start.hour}:{start.minute}:{start.second}')
    #m.dfs(m.get_fringe(0,0), [])
    #start=timer()
    #m.dfs(m.get_fringe(0,0), [])
    #m.bfs(m.grid[0],-1, -1,1)
    #print(m.a_star(m.grid[0]))
    #m.strat3_a_star(m.grid[0],flammability,1,4,8)
    #m.strategy3(dimension, flammability)
    c=0
    mazes = []
    for i in range(30):
        mazes.append(Maze(dimension,probability))
        mazes[i].populate_grid(dimension, probability)
        mazes[i].clear_visited()
        x = mazes[i].strat3_a_star(mazes[i].grid[0],flammability, 1, -1, -1)
        #mazes[i].bfs(mazes[i].grid[0], -1, -1, 1)
        #self.print_grid(-1)
        fire_row, fire_col = mazes[i].create_fire(dimension)
        mazes[i].fire_squares.append((fire_row, fire_col))
        #mazes[i].fire_squares.append((fire_row, fire_col))
        mazes[i].clear_visited()
        y = mazes[i].bfs(mazes[i].grid[0], fire_row, fire_col, 2)
        mazes[i].clear_visited()
        #print(f'{x}, {y}')
        
        
        if (x == 0 and y==1):
            c=c+1
            #mazes[i].print_grid(-1)
            #print()
            #print("here2")
            print(mazes[i].strategy3(dimension, flammability, x))
        if(c==10):
            break
        mazes[i].clear_visited()
        #print(str(i+1) + " iteration: " + mazes[i].dfs(mazes[i].get_fringe(0,0), []))
    ##m.build_maze(probability, screen)
    print(c)
    
    #end = timer()
    #print(end - start)
    #end = datetime.datetime.now()
    #print(f'{end.hour}:{end.minute}:{end.second}')
    #x = m.bfs(m.grid[0],fire_row, fire_col,1)
    #fire_row, fire_col = m.create_fire(dimension)
   # m.advance_fire(flammability)
    #print(m.strategy1(dimension, flammability))
    #print(m.strategy2(dimension, flammability))
    #print(m.strategy3(dimension, flammability))
    #m.print_grid()
    #print()
    #print(m.strategy1(fire_row, fire_col, dimension, flammability))
    #print()
    #for i in range(0, len(m.grid)):
    #    print(m.grid[i].get_pos())
    #m.grid[0].set_parent(0, 0)
    #m.bfs(m.grid[0], fire_row, fire_col)
    #print(m.a_star(m.grid[0]))
    
''' running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # update pygame's display to display everything
        pygame.display.update()'''
            
