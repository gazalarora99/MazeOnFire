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
    
    
if __name__ == '__main__':
    problem2() 