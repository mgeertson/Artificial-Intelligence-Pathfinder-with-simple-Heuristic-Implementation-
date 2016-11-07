#!/usr/bin/env python3

'''
CPSC 481
Assignment 1
Maze

Python 3.5

Modified 7/18/16


'''


import sys
import ast
from grid import Cell   # from filename import className
from grid import AStar


# For Debug
def printCell(self):
    for x in range(len(self.graph)):
        for y in range(len(self.graph)):    
            print('x,y: ', self.graph[x][y].x, self.graph[x][y].y)
            print('Parent: ', self.graph[x][y].parent)
            print('{} = {} + {}: '.format(self.graph[x][y].f,self.graph[x][y].g,self.graph[x][y].h))
            print()
    print('len(graph): ', len(self.graph))


def main ():

    ### This gives us:
    ### start and end as tuples --> (x,y) 
    ### quicksandLocation and netLocation as lists --> [(x,y), (x,y)]
    ### toll as dictionary --> {value:(x,y), value:(x,y)}
    
    with open(sys.argv[-1], 'r') as f:
        startLocation = f.readline()
        startLocation = ast.literal_eval(startLocation)
        
            
        
        endLocation = f.readline()
        endLocation = ast.literal_eval(endLocation)
        
        
        quicksandLocation = f.readline()
        quicksandLocation = quicksandLocation.split()
        for i in range(len(quicksandLocation)):
            quicksandLocation[i] = ast.literal_eval(quicksandLocation[i])
            
        netLocation = f.readline()
        netLocation = netLocation.split()
        for i in range(len(netLocation)):
            netLocation[i] = ast.literal_eval(netLocation[i])
        # Implemented extended net locations in the init_grid() function.
        
        tollLocation = f.readline().strip().split()
        tollLocation = ','.join(tollLocation)
        tollLocation = '{' + tollLocation + '}'
        tollLocation = ast.literal_eval(tollLocation)
        

    ### The above code reads from file and creates tuples, 
    ### lists, and dictionary similar to below.
    ### startLocation = (2,3)
    ### endLocation = (19,10)
    ### quicksandLocation = [(0,0), (5,5), (15,15)]
    ### netLocation = [(10,10), (17,8)]
        # Spiderweb has expanded web values are implemented in init_grid() function
    ### tollLocation = {2:(1,3), 10:(3,3), 7:(10,15), 200:(19,9)}

    
    #startLocationObj = Cell(startLocation[0], startLocation[1])
    #endLocationObj = Cell(endLocation[0], endLocation[1])

    # Create AStar object with start and end locations
    mazeObj = AStar()
    
    # Initialize the grid with all trap locations. Start and end locations are not designated on grid, only to object.
    mazeObj.init_grid(startLocation, endLocation, quicksandLocation, netLocation, tollLocation)
    
    ##Just messing around with converting the Neighbor list to a list of Objects
    #temp = mazeObj.get_neighbor_cells(startLocationObj)
    
    # Hope for the best...
    finalPath = mazeObj.move(quicksandLocation, netLocation, tollLocation)
    
    
    
    
    
    
    
    with open ("output.txt", "wt") as out_file:
        out_file.write('Total cost: ${}\n'.format(mazeObj.cost))
    #print('Total cost: ${}'.format(mazeObj.cost))
        out_file.write('Total number of steps taken: {}\n'.format(mazeObj.steps))
    #print('Total number of steps taken: {}'.format(mazeObj.steps))
        out_file.write('Traveled route: {}\n'.format(finalPath))
    #print('Traveled route: {}'.format(finalPath))
    
    out_file.close()
    
    
    
    
    
    
    
    # For Debug
    #print('Calling get_heuristic()')
    #print(starObj.get_heuristic())
    #print(startLocationObj.parent)
    #print(starObj.get_path())



if __name__ == '__main__':
    main( )
