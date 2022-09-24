import numpy as np


def carve_maze(grid, height, width):
  """
  Here we generate a maze given the grid we've recieved
  """
  output_grid = np.empty([height*3, width*3], dtype=str)
  output_grid[:] = '#'
  i = 0
  j = 0
  while i < height:
    w = i*3 + 1
    while j < width:
      k = j*3 + 1
      toss = grid[i,j]
      output_grid[w,k] = 'U'
      if toss == 0 and k+2 < width*3:
        output_grid[w,k+1] = 'U'
        output_grid[w,k+2] = 'U'
      if toss == 1 and w-2 >=0:
        output_grid[w-1,k] = 'U'
        output_grid[w-2,k] = 'U'
      j += 1
    i += 1
    j = 0
  return output_grid


from colorama import init, Fore
# colorama needs to be initialized in order to be used
init()


def print_maze(maze):
    """
    Here we print the initial maze
    """
    for i in range(0, len(maze)):
        for j in range(0, len(maze[0])):
            if maze[i][j] == '#':
                print(Fore.BLUE, f'{maze[i][j]}', end="")
            elif maze[i][j] == 'U':
                print(Fore.LIGHTBLACK_EX, f'{maze[i][j]}', end="")
            else:
                print(Fore.RED, f'{maze[i][j]}', end="")
        print('\n')


def dim(grid):
  """Returns a touple with the height (on the left side) and the width (on the right side)"""
  return (len(grid), len(grid[0]))


def create_maze(height, width, p=0.5):
    """
    Generate a random maze with the required height and width. Then print the maze.
    Parameter p is the level of complexity, the greater p the greater is the complexity, and 0 < p < 1 
    """
    if type(height) != int and type(width) != int and type(p) != float:
        raise TypeError("One of the dimensional inputs are of the wrong data type.")
    
    if height <= 0 or width <= 0 or p <= 0 or p >= 1:
      raise ValueError("Invalid dimensional value.")

    n = 1                                                 # The number of possibilities including 0; e.g. n=2 then we can randomly have numbers from {0,1,2}, if n=1 then from {0,1}
    grid = np.random.binomial(n, p, size=(height, width))
    
    first_row = grid[0]
    first_row[first_row == 1] = 0
    grid[0] = first_row
    
    for i in range(1, height):
        grid[i, width-1] = 1
    
    maze = carve_maze(grid, height, width)
    
    return maze
