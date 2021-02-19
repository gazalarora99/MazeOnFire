'''
Created on Feb 17, 2021

@author: Gazal Arora and Jishan Desai
'''
import matplotlib.pyplot as plt

def problem2():
    # x axis values 
    x = [0, 0.05,
    0.1,
    0.15,
    0.2,
    0.25,
    0.3,
    0.35,
    0.4,
    0.45,
    0.5,
    0.55,
    0.6,
    0.65,
    0.7,
    0.75,
    0.8,
    0.85,
    0.9,
    0.95,
    1] 
    # corresponding y axis values 
    y = [1,
    1,
    0.98,
    0.94,
    0.8,
    0.7,
    0.52,
    0.34,
    0.04,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0] 
      
    # plotting the points  
    plt.plot(x, y) 
      
    # naming the x axis 
    plt.xlabel("Obstacle Density 'p'") 
    # naming the y axis 
    plt.ylabel('Probability that G can be reached from S') 
      
    # giving a title to my graph 
    plt.title('Problem 2: DFS on Maze of dimension 50') 
      
    # function to show the plot 
    plt.show()
    
def strategy2():
    # x axis values 
    x = [0,
0.05,
0.1,
0.15,
0.2,
0.25,
0.3,
0.35,
0.4,
0.45,
0.5,
0.55,
0.6,
0.65,
0.7,
0.75,
0.8,
0.85,
0.9,
0.95,
1] 
    # corresponding y axis values 
    y = [1,
1,
0.9,
0.8,
0.8,
0.6,
0.5,
0.4,
0.4,
0.4,
0.2,
0.2,
0.1,
0,
0,
0,
0,
0,
0,
0,
0]
      
    # plotting the points  
    plt.plot(x, y) 
      
    # naming the x axis 
    plt.xlabel("Flammability rate 'q'") 
    # naming the y axis 
    plt.ylabel('Average strategy 2 success rate out of 1') 
      
    # giving a title to my graph 
    plt.title('Problem 6: Strategy 2 on Maze of dimension 50 and p=0.3') 
      
    # function to show the plot 
    plt.show()
def prob3():
        # x axis values 
    x = [0,
0.05,
0.1,
0.15,
0.2,
0.25,
0.3,
0.35,
0.4,
0.45,
0.5,
0.55,
0.6,
0.65,
0.7,
0.75,
0.8,
0.85,
0.9,
0.95,
1] 
    # corresponding y axis values 
    y = [18.3,
19.9,
25.8,
34.1,
52.9,
108.4,
118.0,
85.6,
68.7,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0]
      
    # plotting the points  
    plt.plot(x, y) 
      
    # naming the x axis 
    plt.xlabel("Obstacle Density 'p'") 
    # naming the y axis 
    plt.ylabel('Average (number of nodes explored by BFS - number of nodes explored by A*)') 
      
    # giving a title to my graph 
    plt.title('Problem 3: At dimension = 100') 
      
    # function to show the plot 
    plt.show()
if __name__ == '__main__':
    prob3() 