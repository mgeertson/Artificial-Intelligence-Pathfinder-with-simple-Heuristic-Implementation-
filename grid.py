import random
import operator
'''
TIEBREAKER IS THE ISSUE, If you guys can help fix my tiebreaker in the update cell function to randomly pick a f value on the pop, thank you
i am thinking of even getting rid of the heapq and just making it a list and using min to select
'''
class Cell():
    def __init__(self, x, y, g=0, h=0):      # parent is not in the constructor, don't know if we want it to be
        self.x = x  # x coordinate
        self.y = y  # y coordinate
        self.parent = None
        self.g = g  # cost to move from starting cell to this cell
        self.h = h  # estimation of the cost to move from this cell to goal cell
        self.f = g + h
      
    def __lt__(self, neighbor):
        return random.randint(self.f,neighbor.f)  
    
class AStar(Cell):
    def __init__(self):     #Changed it to pass in the original list. No extra objects created.
        self.opened = []  # is the open list
        # Transform list self.opened into a heap, in-place, in linear time.
        ## Why is self.closed a set rather than a list?
        self.closed = []  # visited  list
        self.graph = []  # is our grid 20x20
        self.grid_height = 20
        self.grid_width = 20
        self.cost = 1
        self.steps = -1
        self.costKey = 0
        self.keyList = []
        


    
    ## I think we should run a test to see if we can get 1 grid square to do the following:
    ## 1. Determine neighbors
    ## 2. Calculate heuristic value
    ## 3. Add to open/closed queue.
    
    
    ## "if current_cell not in self.closed:" in move function gives the error.

    ##Sets can't contain duplicates  <---- probably the main reason why
    ##Sets are unordered
    ##In order to find an element in a set, a hash lookup is used (which is why sets are unordered). This makes __contains__ (in operator) a lot more efficient for sets than lists.
    ##Sets can only contain hashable items (see #3). If you try: set(([1],[2])) you'll get a TypeError.


    def init_grid(self, startLocation, endLocation, quicksandLocation, netLocation, tollLocation): # start --> (x,y)
        # Creates a graph as a list
        #   Ex) If 4x4 grid of just coordinates:
        #   graph = [[(0, 0), (0, 1), (0, 2), (0, 3)], [(1, 0), (1, 1), (1, 2), (1, 3)], [(2, 0), (2, 1), (2, 2), (2, 3)], [(3, 0), (3, 1), (3, 2), (3, 3)]]
        #       where list could be looked at as having rows and columns
        self.graph = [[Cell(x,y) for y in range(self.grid_width)] for x in range(self.grid_height)]
        # self.graph[x][y]
        
       
        # Then iterate through qicksand, spiderweb, and toll lists  
        # and updates graph cells to be populated with appropriate values
        
        self.start = Cell(startLocation[0], startLocation[1])
        self.start.x = startLocation[0]
        self.start.y = startLocation[1]
        self.end = Cell(endLocation[0], endLocation[1])
        self.end.x = endLocation[0]
        self.end.y = endLocation[1]
        self.graph[startLocation[0]][startLocation[1]] = self.start
        self.graph[endLocation[0]][endLocation[1]] = self.end
        

        

        
        #populating graph with quicksand
        for i in range(len(quicksandLocation)):
            x,y = quicksandLocation[i]
            self.graph[x][y] = Cell(x,y,50)   
            
        #populating graph with spiderwebs
        for i in range(len(netLocation)):
            x,y = netLocation[i]
            self.graph[x][y] = Cell(x,y,100) # We can make the trap values whatever we want.
            # This extends the web locations and places them on the graph
            if x-1 >= 0:
                self.graph[x-1][y] = Cell(x-1,y,100)
            if y-1 >= 0:
                self.graph[x][y-1] = Cell(x,y-1,100)
            if x+1 <= 19:
                self.graph[x+1][y] = Cell(x+1,y,100)
            if y+1 <= 19:
                self.graph[x][y+1] = Cell(x,y+1,100)
        
        #populating graph with tolls
        val = tollLocation.keys()
        for i in val:
            x,y = tollLocation[i]
            self.graph[x][y] = Cell(x,y,i)   # since tollLocation is a dictionary, i represents the key which is
                                        # the costs of that location's toll. i gets set as that cell's g value.
     
        for key,value in tollLocation.items():  #TESTING
                self.keyList.append(key)
     
        
    def get_heuristic(self, cell): # need to worry about other values
        # this function just calculates the heuristic value H for the cell, we find the distance between cell and goal cell, then * by D value
        return 1 * abs(cell.x - self.end.x) + abs(cell.y - self.end.y)  # need to figure out D value, maybe 1 since g is 1
    

    def get_neighbor_cells(self, cell):  # made the neighbor cells have a combined F value down in update cells and tiebreaker, so this function is all good :D
        neighborCells = []
        
        if cell.x < 19:
            neighborCells.append(Cell(cell.x+1, cell.y))
        if cell.y > 0:
            neighborCells.append(Cell(cell.x, cell.y-1))
        if cell.x > 0:
            neighborCells.append(Cell(cell.x-1, cell.y))
        if cell.y < 19:
            neighborCells.append(Cell(cell.x, cell.y+1))
        return neighborCells
    
        
    def update_cell(self, neighbor, cell, quicksandLocation, netLocation, tollLocation):
        
        
        for i in range(len(quicksandLocation)):
            x,y = quicksandLocation[i]
            if(neighbor.x == x and neighbor.y == y):
                neighbor.g += 100
                    
        #checks if in spiderwebs
        for i in range(len(netLocation)):
            x,y = netLocation[i]
            if(neighbor.x == x and neighbor.y == y):
                neighbor.g += 100
                    
                    
        
        #checks if uses a toll
        for key,value in tollLocation.items():
            if ((neighbor.x,neighbor.y) == value):
                neighbor.g += key
        
        
        
        
        
        
        if(neighbor.g <= 0):
            neighbor.g = cell.g + 1  # The 1 is the $1 cost to move
            neighbor.parent = cell
            neighbor.h = self.get_heuristic(neighbor)   
            neighbor.parent = cell
        else:
            neighbor.h = self.get_heuristic(neighbor) 
        
        
        
        if (neighbor.y > 1):
            secondStep = Cell(neighbor.x, neighbor.y - 2)
        if (neighbor.x < 18):
            secondStep = Cell(neighbor.x + 2, neighbor.y)
        if (neighbor.y < 18):
            secondStep = Cell(neighbor.x, neighbor.y + 2)
        if (neighbor.x > 1):
            secondStep = Cell(neighbor.x - 2, neighbor.y)
        secondStep.h = self.get_heuristic(secondStep)  # grabs the second step H VALUE
        
        
        
        neighbor.f = neighbor.h + neighbor.g + secondStep.h + secondStep.g   #adds the two f values together, so it knows the 2 steps ahead, but wont travel 2 steps
    
    
        
    def printCost(self):
        return self.cost
    def printSteps(self):
        return self.steps

    def __lt__(self, neighbor):
        return random.randint(self, neighbor)  
        
    def move(self, quicksandLocation, netLocation, tollLocation):
      
        self.opened.append((self.start.f, self.start))
        path = []
      
        while self.opened: # while it is not empty 
            f,cell = min(self.opened)
            self.opened.remove((f,cell))
            path.append([cell.x, cell.y])
        
            self.cost = cell.g +1
            self.steps += 1
            self.closed.append(cell) # add cell to closed list so we don't process it twice
            
              #checks if in quicksand
            for i in range(len(quicksandLocation)):
                x,y = quicksandLocation[i]
                if(cell.x == x and cell.y == y):
                    self.cost += 100
                    
                    self.cost += self.costKey
                    return path
            #checks if in spiderwebs
            for i in range(len(netLocation)):
                x,y = netLocation[i]
                if(cell.x == x and cell.y == y):
                    self.cost += 100
                    
                    self.cost += self.costKey
                    return path
        
            #checks if uses a toll
            for key,value in tollLocation.items():
                if ((cell.x,cell.y) == value):
                    self.costKey += key
                    

            if cell.x == self.end.x and cell.y == self.end.y:  # if current == goal then return path
                self.cost += self.costKey
                return path
            
            neighbor_cells = self.get_neighbor_cells(cell) # get neighbor cells for the smallest value from the OPEN LIST
            for current_cell in neighbor_cells: #neighbor_cells is our 4 possible directions
                if current_cell not in self.closed:
                    if (current_cell.f, current_cell) in self.opened: # if neighbor cell in open list, check if current path is
                        
                       # this if statement checks if a current path is better than the one previously found for this current_cell
                        
                        if (current_cell.g > cell.g + 1): # if it has a lower f than parent then skip
                            self.update_cell(current_cell, cell, quicksandLocation, netLocation, tollLocation)
                            
                    else:
                        self.update_cell(current_cell, cell, quicksandLocation, netLocation, tollLocation)
                        self.opened.append((current_cell.f , current_cell))
                        