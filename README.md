# target-locator
Python project that compares 6 different path planning algorithms in 3 different ways.

This project has three different means of running. It was built to be run in Python's Anaconda command line.

### To run:
$ python .\paths.py [-d] -e [# of entities per map] -l [length of map] -w [width of map] -h [height of map]

### The parameters:
###### -d     An optional flag. If used, the -h parameter becomes important and will be used. This flag tells indicates whether the program should run the on a two-dimensional map (a plane), or a three-dimensional one (a cube). The flag indicates the user wants the latter.
###### -e     Number of entities. When the user inputs 1, the program runs with each algorithm on it's own map all by itself. At 6, one of each of the algorithms is on the same map seeking out the same end from different start points. Any other number (numbers greater than 6 are turned to 5 by the program), tells the program to place that many of the SAME algorithm on the same map to find the same endpoint from different start points.
###### -l     Length of the map.
###### -w     Width of the map.
###### -h     Height of the map. This number is always required, but it can be anything if the -d flag is absent.

The program automatically sets the map to be no bigger than 5000 spaces and shrinks the map if the passed variables create a map that is larger.
The program also accounts for collision of entities. When run, the resulting graphs give an idea of what each algorithm did and how long they took to allow for comparison.

This program uses A* Algorithm, Dijkstra's Algorithm, Randomly-Reaching Tree, Best First Search, Breadth First Search, and Depth First Search.
