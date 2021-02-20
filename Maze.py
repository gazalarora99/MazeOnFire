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
import numpy as np
from collections import deque
from math import sqrt

#A Square represents each cell in a Maze
class Square:
    
    #initializing a square
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
    #sets the heuristic based on regular A* without fire or A* with fire in strategy3 
    def set_distance(self, n, mode, q, fr, fc):
        if mode == 0:  #regular A star
            self.current_dist = n
            self.heuristic = n + sqrt(((dimension - 1 - self.row)**2) + ((dimension - 1 - self.col)**2))
        elif mode==1 : #strategy 3 A star
            self.heuristic =  (sqrt(((dimension - 1 - self.row)**2) + ((dimension - 1 - self.col)**2))) - ((sqrt(((fr - self.row)**2) + ((fc - self.col)**2))))
            #print(f'{self.row}, {self.col}: dist from end {(sqrt(((dimension - 1 - self.row)**2) + ((dimension - 1 - self.col)**2)))} - dist from fire {((sqrt(((fr - self.row)**2) + ((fc - self.col)**2))))}')
    def set_type(self, n):
        self.Square_type = n
    def is_wall(self):
        r,c = self.get_pos()
        return c == 0 or c == dimension - 1 or r == 0 or r == dimension - 1
    #comparator between 2 squares
    def __lt__(self, other):
        return self.heuristic < other.heuristic
    def __str__(self):
        return str("({} , {}) : dist {}".format(self.row, self.col, self.heuristic))


#Represents a Maze
class Maze:
    #initializer
    def __init__(self,dimension,pr):
        self.rows = dimension
        self.cols = dimension
        self.grid = [] #we store the matrix of squares in a 1-D array and access it using row-major order
        self.fire_squares = []
        self.num_node_exp = 0
        self.a_star_exp = 0
    #prints the currrent state of the maze with currloc being the agent's position represented by a * in the Maze
    def print_grid(self,currloc):
        for i in range(0,self.rows):
            print()
            for j in range(0,self.cols):
                if self.grid[(self.cols * i) + j].get_type() == 3: #type 3 = start
                    print("S", end = " ")
                if ((self.cols*i) + j)  == currloc:
                    print("*", end=" ") 
                elif self.grid[(self.cols*i) + j].get_type() == 0: #type 0 = open cell
                    print("_", end = " ")
                elif self.grid[(self.cols*i) + j].get_type() == 1: #type 1 = obstruction cell
                    print("@", end = " ")
                elif self.grid[(self.cols*i) + j].get_type() == 4: #type 4 = burning cell
                    print("F", end = " ")       
                elif self.grid[(self.cols*i) + j].get_type() == 2: # type 2 = goal
                    print("E", end = " ")                           
    
    ### makes 2d array with given dimensions and has square objects in it.
    def populate_grid(self,dimension,pr):
        for i in range(0,self.rows):
            for j in range(0,self.cols):
                if i == 0 and j == 0:
                    self.grid.append(Square(i,j,dimension,3))
                elif i == self.rows -1 and j == self.cols -1 :
                    self.grid.append(Square(i,j,dimension,2))
                else:
                    x = random.uniform(0, 1)
                    if x <= pr:
                        self.grid.append(Square(i,j,dimension,1))
                    else:
                        self.grid.append(Square(i,j,dimension,0))

    #starts fire at a random cell
    def create_fire(self, dim):
        x = random.randint(0, dim-1)
        y = random.randint(0, dim-1)
        self.grid[(self.cols * x)+y].set_type(4)
        return x, y
    
    #advances fire based on q and k burning neighbors at each time step its called
    def advance_fire(self,q):
        fire_list=[]
        for Square in self.grid:
            r,c = Square.get_pos()
            #row-major order to access the 1-D grid of squares which represents the Maze
            right = (self.cols*r) + c +1
            left = (self.cols*r) + c - 1
            top =  (self.cols * (r-1)) + c
            bottom = (self.cols * (r+1)) + c
            k = 0;
            #finding burning neighbors k at position above(top), below(bottom), left and right of the current square
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
                    #making a list of squares that will start burning based on this k
                    fire_list.append(Square.get_pos())
                    self.fire_squares.append(Square.get_pos())
        #setting the type = 4 for burning squares
        for pair in fire_list:
            i,j = pair
            curr = (self.cols*i) + j 
            self.grid[curr].set_type(4)  
            
    #checks if p1, p2 is parents of pos(current cell)                                               
    def is_parent(self, p1, p2, pos):
        r1, r2 = self.grid[pos].get_pos()
        
        if  (r1==p1 and r2==p2):
            #print("not child")
            return True
        #print("yes, child")
        return False
    
    #adds pos to the fringe if its open (type==0) and not visited
    def add_to_fringe(self, pos, i, j, stack, p1, p2):
        #print("checking (" + str(i) + ", " + str(j) + ")'s child "+ str(pos))
        if (self.grid[pos].get_type()==0) and (not self.is_parent(p1, p2, pos)) and (self.grid[pos].is_visited() == False): 
            self.grid[pos].set_parent(i,j)
            stack.append(self.grid[pos]) 
            #print("yes, child")       
    
    #function to get fringe from current position located at Square(r,c)
    def get_fringe(self, r, c):
        p1, p2 = self.grid[(self.cols*r) + c].get_parent()
        
        #neighbor indices which could possibly be added to the fringe
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
        
        #to save an index out of bound exception, 
        #following if statements will take care of corner Squares
        #which may not have a square at either its left or right or top or bottom
        #when looking for next possible position (children)
        
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
    
    #prints and returns the path from start_square to current location
    def printPath(self,curr_loc, start_square):
        solution = []
        while curr_loc != start_square:
            solution.append(self.grid[curr_loc].get_pos())
            r,c = self.grid[curr_loc].get_parent();
            #self.print_grid(curr_loc)
            curr_loc = (self.cols*r) + c 
            #print(solution)
        solution.reverse()
        print(solution)
        return solution
    
    #finds the row, col location of a burning square closest to current square r, c
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
    
    #modified A* that uses a specific heuristic for strategy 3
    #heuristic = euclidean distance from current node to goal - euclidean dist from current nod eto closest location of fire
    def strat3_a_star(self, start_square, q, mode, fire_row, fire_col):
        
        t1=time.time()
        
        if (self.grid[1].get_type()==1) and (self.grid[(self.cols*1) + 0].get_type()==1):
            t2 = time.time()
            print(time.strftime("%H:%M:%S", time.gmtime(t2-t1)))
            #  print( "No solution")
            return 2
        elif (self.grid[(self.cols * (self.rows-1)) + self.cols -2].get_type()==1) and (self.grid[(self.cols * (self.rows-2)) + self.cols - 1].get_type()==1):
            t2 = time.time()
            print(time.strftime("%H:%M:%S", time.gmtime(t2-t1)))
            # print( "No solution")
            return 2
        
        fringe = []
        heapq.heappush(fringe, start_square) #min-heap
        i = 0
        while fringe :
            i = i + 1
            curr = heapq.heappop(fringe) #exploring curr cell
            curr.set_visited()
            r,c  = curr.get_pos()
            p1, p2 = curr.get_parent()
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
            #specific condition for 0,0
            if curr.get_isStart():
                if self.grid[right].get_type() == 0 :
                    fr, fc = self.closest_fire_loc(r,c+1)
                    #print(fr, fc)
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
            #if we are exploring nodes at corner rows/cols, we need to avoid index out of bounds so using
            #is_wall to check that       
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
            else: #else when not on corner rows/col, we can explore all neighbors
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
                    
    
    
    #A * algorithm using the heuristic = distance traveled from start to current + euclidean distance from current to end
    def a_star(self, start_square):
        
        t1=time.time()
        
        if (self.grid[1].get_type()==1) and (self.grid[(self.cols*1) + 0].get_type()==1):
            t2 = time.time()
            #print(time.strftime("%H:%M:%S", time.gmtime(t2-t1)))
            return "No solution"
        elif (self.grid[(self.cols * (self.rows-1)) + self.cols -2].get_type()==1) and (self.grid[(self.cols * (self.rows-2)) + self.cols - 1].get_type()==1):
            t2 = time.time()
            #print(time.strftime("%H:%M:%S", time.gmtime(t2-t1)))
            return "No solution"
        
        fringe = []
        
        heapq.heappush(fringe, start_square) #min heap that compares squares based on heuristic
        i = 0
        while fringe :
            i = i + 1
            curr = heapq.heappop(fringe) #exploring curr cell
            self.a_star_exp = self.a_star_exp+1
            curr.set_visited()
            r,c  = curr.get_pos()
            p1, p2 = curr.get_parent()
            right = (self.cols*r) + c + 1
            left = (self.cols*r) + c - 1
            top =  (self.cols * (r-1)) + c
            bottom = (self.cols * (r+1)) + c
            curr_loc = (self.cols*r) + c 
            
            if r == self.rows-1 and c == self.cols - 1:
                #self.printPath(curr_loc)
                t2 = time.time()
                print(time.strftime("%H:%M:%S", time.gmtime(t2-t1)))
                # print("success, goal reached")
                #self.printPath(curr_loc,0)
                return "done"
            
            
            #specific condition for start
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
                    
            #if we are exploring nodes at corner rows/cols, we need to avoid index out of bounds so using
            #is_wall to check that         
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
            else:#else when not on corner rows/col, we can explore all neighbors
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
        #print(time.strftime("%H:%M:%S", time.gmtime(t2-t1)))
        #print("Not Done")
        return  "Not Done"
                    
                        
    # mode = 1 for start to end
    # mode = 2 for start to fire  
    #BFS to find a path from start_square till the goal or the first location of the fire
    def bfs(self, start_square, fire_row, fire_col, mode):
        
        
        t1=time.time()
        if (self.grid[1].get_type()==1) and (self.grid[(self.cols*1) + 0].get_type()==1):
            t2 = time.time()
            #print(time.strftime("%H:%M:%S", time.gmtime(t2-t1)))
            #print("no solution")
            return -1
        elif (self.grid[(self.cols * (self.rows-1)) + self.cols -2].get_type()==1) and (self.grid[(self.cols * (self.rows-2)) + self.cols - 1].get_type()==1):
            t2 = time.time()
            #print(time.strftime("%H:%M:%S", time.gmtime(t2-t1)))
            #print("no solution")
            return -1
        
        fringe = deque() #fringe is a queue
        fringe.appendleft(start_square)
        i = 0
        while fringe :
            i = i + 1
            curr = fringe.pop() #exploring the curr cell
            self.num_node_exp = self.num_node_exp + 1 #counting number of nodes explored
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
            
            if curr.get_isStart(): #special condition to start
                if self.grid[right].get_type() !=1 :
                    fringe.appendleft(self.grid[right])
                    self.grid[right].set_parent(r,c)
                if self.grid[bottom].get_type() !=1 :    
                    fringe.appendleft(self.grid[bottom])
                    self.grid[bottom].set_parent(r,c)
            #if we are exploring nodes at corner rows/cols, we need to avoid index out of bounds so using
            #is_wall to check that
            elif curr.is_wall():
                if(mode==1): #for finding a fringe to get to the goal
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
                elif mode==2: #for finding a fringe to get to the first fire location
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
            else:#else when not on corner rows/col, we can explore all neighbors
                if(mode==1): #for finding a fringe to get to the goal
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
                elif mode==2: #for finding a fringe to get to the first fire location
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
        print(time.strftime("%H:%M:%S", time.gmtime(t2-t1)))
        #print("No solution")
        return 2
    
    #marks the boolean "visited" as for false for visited nodes 
    #so that BFS/A* can be run again on the same maze to find path from a new location to the goal
    def clear_visited(self):
        for i in self.grid:
            if (i.is_visited()):
                i.visited = False 
                
    #moves the agent by one step onto the path
    def agent_moves(self, path):
        r, c = path[0]
        return r, c
    
    #strategy 3 uses A* with a new heuristic 
    #heuristic = euclidean distance from current node to goal - euclidean dist from current nod eto closest location of fire
    # x is the return value after initial call to A* that checks if the maze is solvable
    def strategy3(self, dim, q, x):
        #x = self.strat3_a_star(self.grid[0], q, 1, -1, -1)
        #fire_row, fire_col = m.create_fire(dim)
        #self.print_grid(-1)
        #self.fire_squares.append((fire_row, fire_col))
        end = (self.cols * (dim - 1)) + (dim - 1)
        path = None
        #if maze is solvable, we get the path as agent will take its first step on this path
        if(x==0):
            path = self.printPath(end, 0)
        
        while(x==0):
            self.clear_visited()
            r1, c1 = self.agent_moves(path) #agent takes one step on the path
            #path.pop(0)
            curr_loc = (self.cols*r1) + c1
            self.advance_fire(q) #fire increases at one time step to neighbors of current cells on fire based on q and k
            if (r1==dim-1) and (c1==dim-1): #agent succesfully reached goal before burning
                return "goal reached"
            if (self.grid[end].get_type()==4): #if fire gets to the goal, there is no path left
                return "goal is on fire"
            if self.grid[curr_loc].get_type()== 4: #the fire spreads and burns the agent's curr location
                    return "agent's current loc caught fire"
            #once both agent and fire have taken their steps, 
            #path is re-computed from agent's current location based on how far the 
            #closest fire is and how fast it would get to the agent
            x = self.strat3_a_star(self.grid[ (self.cols * r1) + c1 ], q, 1, -1, -1) 
            if(x==0):
                path = self.printPath(end, (self.cols * r1) + c1 )
        return "agent has no path left to the end" #if x is not 0 then there was no path left to the end for the agent without burning
    
    #strategy 2 uses BFS to find the shortest path to the end
    #if it does find a path that is the maze is solvable, then it sets x to 0
    def strategy2(self, dim, q, x):
        #x = self.bfs(self.grid[0], -1, -1, 1)
        #fire_row, fire_col = m.create_fire(dim)
        end = (self.cols * (dim - 1)) + (dim - 1)
        path = None
        #if maze is solvable, we get the path as agent will take its first step on this path
        if(x==0):
            path = self.printPath(end, 0)
        
        while(x==0):
            self.clear_visited()
            r1, c1 = self.agent_moves(path)#agent takes one step on the path
            curr_loc = (self.cols*r1) + c1
            self.advance_fire(q) #fire increases at one time step to neighbors of current cells on fire based on q and k
            if (r1==dim-1) and (c1==dim-1): #agent succesfully reached goal before burrning
                return "goal reached"
            if (self.grid[end].get_type()==4): #if fire gets to the goal, there is no path left
                return "goal is on fire"
            if self.grid[curr_loc].get_type()== 4: #the fire spreads and burns the agent's curr location
                    return "agent's current loc caught fire"
            #once both agent and fire have taken their steps, 
            #path is re-computed from agent's current location using bfs
            x = self.bfs (self.grid[ (self.cols * r1) + c1 ], -1, -1, 1)
            if(x==0):
                path = self.printPath(end, (self.cols * r1) + c1 )
        return "agent has no path left to the end" #if x is not 0 then there was no path left to the end for the agent without burning
    
    #strategy 2 uses BFS to find the shortest path to the end
    #if it does find a path that is the maze is solvable, then it sets x to 0
    def strategy1(self,dim, q,x):
        #x = self.bfs(self.grid[0],-1,-1,1)
        #fire_row, fire_col = m.create_fire(dim)
        end = (self.cols * (dim - 1)) + (dim - 1)
        path = self.printPath(end, 0) #path that agent will follow
        self.clear_visited()
        if(x==0):
            while(path!=[]):
                #agent never re-computes its path based on current state of fire
                r1, c1 = self.agent_moves(path) #agent continues to move on the same path, one step at one iteration
                path.pop(0)
                curr_loc = (self.cols*r1) + c1
                self.advance_fire(q) #fire advances at each iteration to its neighbors based on q
                if (r1==dim-1) and (c1==dim-1):
                    return "goal reached"
                if (self.grid[end].get_type()==4):
                    return "goal is on fire"
                if self.grid[curr_loc].get_type()== 4:
                    return "agent's current loc caught fire"
        return "agent has no path to the end"
        
    #DFS runs deep, that is it goes to the child then its child and keeps going till it finds the goal or needs to backtrack
    #fringe is a stack and pops the last child for DFS to explore next
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
        #until path is not empty because we are backtracking using path
        while (path!=[] or i==0):
            if(fringe==[]):
                if path==[]: #no path possible when both fringe & path are empty
                    t2 = time.time()
                    print(time.strftime("%H:%M:%S", time.gmtime(t2-t1)))
                    print("No solution")
                    return 0
                current = path.pop() #go to parent of current to backtrack
                m, n = current.get_pos()
                fringe = self.get_fringe(m, n) #get fringe using parent's non-visited cells (curr's siblings)
                continue
                
            current = fringe.pop() #current is of type Square
            current.set_visited()
            if current.get_type() == 2: #goal state if Square's type is 2
                print("i value is "+str(i))
                t2 = time.time()
                print(time.strftime("%H:%M:%S", time.gmtime(t2-t1)))
                print("success, goal reached")
                return 1
            m, n = current.get_pos()
            position = (self.cols * m) + n
            path.append(self.grid[position]) #add the node being explored to path after its popped off from fringe
            fringe = self.get_fringe(m, n) 
            i= i+1
            
        t2 = time.time()
        print(time.strftime("%H:%M:%S", time.gmtime(t2-t1)))    
        print("i value is " + str(i))
        print("failed")
        return 0
     
#Initializing the grid
if __name__ == '__main__':
    dimension = int(input("Enter Dimension: "))
    probability = float(input("Enter Probability: "))
    m = Maze(dimension,probability)
    m.populate_grid(dimension,probability)
    
    #m.a_star(m.grid[0])
    flammability = float(input("Enter Flammability rate: "))
    md = int(input("Strat check: "))
    m = Maze(dimension,probability)
    m.populate_grid(dimension,probability)
    m.a_star(m.grid[0])
    
    #following code is getting avg number of nodes explorred by bfs-A*
    c = 0
    i = 0
    itr = 0
    mazes = []
    prob_rate = np.linspace(0,1,21)
    avg = np.zeros(len(prob_rate))
    curr_avg = 0
    for itr in range(21):
        c = 0
        while(c != 50):
            curr_avg = 0
            mazes.append(Maze(dimension,prob_rate[itr]))
            mazes[i].populate_grid(dimension,prob_rate[itr])
            #mazes[i].print_grid(-1)
            mazes[i].clear_visited()
            mazes[i].num_node_exp = 0
            mazes[i].a_star_exp = 0
            x = mazes[i].bfs(mazes[i].grid[0], -1, -1, 1)
            mazes[i].clear_visited()
            #if x != -1 and x!=2 :
                #mazes[i].bfs(mazes[i].grid[0], -1, -1, 1)
                #mazes[i].clear_visited()
            mazes[i].a_star(mazes[i].grid[0])
            curr_avg = (mazes[i].num_node_exp)-(mazes[i].a_star_exp)
            #print(str(mazes[i].num_node_exp) + " " + str(mazes[i].a_star_exp))
            #print(str(prob_rate[itr]) + str(" : ") + str((mazes[i].num_node_exp)-(mazes[i].a_star_exp)))
            c= c+1
            i= i+1
        avg[itr] = curr_avg/c  
        print(str(itr) +" : " +str(avg[itr])) 
    #print(c)      
'''  Following code is testing avg success rate for each strategy  
 c=0
    i=0
    correct = 0
    mazes = []
    if md == 0:
        while(c!=50):
            mazes.append(Maze(dimension,probability))
            mazes[i].populate_grid(dimension, probability)
            mazes[i].clear_visited()
            x = mazes[i].bfs(mazes[i].grid[0],-1,-1,1)#mazes[i].strat3_a_star(mazes[i].grid[0],flammability, 1, -1, -1)
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
                ret = mazes[i].strategy1(dimension, flammability, x)
                if ret == "goal reached":
                    correct=correct+1
                print(c, end=" ")
                print(ret)
            mazes[i].clear_visited()
            i=i+1
        print(c)
        print(correct/c)
    #------------------------------------------#
    # Strategy 2 Tester
    #------------------------------------------#
    elif md == 1:
        while(c!=50):
            mazes.append(Maze(dimension,probability))
            mazes[i].populate_grid(dimension, probability)
            mazes[i].clear_visited()
            x = mazes[i].bfs(mazes[i].grid[0],-1,-1,1)#mazes[i].strat3_a_star(mazes[i].grid[0],flammability, 1, -1, -1)
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
                ret = mazes[i].strategy2(dimension, flammability, x)
                if ret == "goal reached":
                    correct=correct+1
                print(c, end=" ")
                print(ret)
            mazes[i].clear_visited()
            i=i+1
            #print(str(i+1) + " iteration: " + mazes[i].dfs(mazes[i].get_fringe(0,0), []))
        ##m.build_maze(probability, screen)
        print(c)
        print(correct/c)
    #------------------------------------------#
    # Strategy 3 Tester
    #------------------------------------------#
    elif md == 2:
        while(c!=100):
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
                ret = mazes[i].strategy3(dimension, flammability, x)
                if ret == "goal reached":
                    correct=correct+1
                print(c, end=" ")
                print(ret)
            mazes[i].clear_visited()
            i=i+1
            #print(str(i+1) + " iteration: " + mazes[i].dfs(mazes[i].get_fringe(0,0), []))
        ##m.build_maze(probability, screen)
        print(c)
        print(correct/c)'''