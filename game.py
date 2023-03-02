import pygame
from pygame import mixer
from PIL import Image
import math
import random
import time
from datetime import datetime

class FSM():
    def __init__(self, state):
        self.activeState = state

    def setState(self, state):
        self.activeState = state

    def act(self):
        if self.activeState == 1:
            self.wander()
        elif self.activeState == 2:
            self.attack()

    def wander(self):
        if self.activeState != 1:
            return

        print("Wandering...")

    def attack(self):
        if self.activeState != 2:
            return
        
        print("Attacking...")

class Node():
    def __init__(self, name):
        self.name = name
        self.children = []

    def sayHello(self):
        print(self.name)

# A composite node can have 1 or more children. They will process one or more 
# of these children in either a first to last sequence or random order. After,
# they will pass either success or failure to their parent node. During the
# time they are processing the children nodes they will return running to the
# parent node.
# There are two main types of composite nodes:
#   1. Sequence
#   2. Selector
class CompositeNode(Node):
    def __init__(self, name):
        super().__init__(name)

class Tree():
    def __init__(self, root):
        self.root = root

    def traverseNode(self, node):
        node.sayHello()

        if len(node.children) == 0:
            return

    def traverse(self):
        self.traverseNode(self.root)

class Link():
    def __init__(self, row, col, imgPath):
        self.pos = [row, col]
        self.sprite = pygame.image.load(imgPath)


class Gannon():
    def __init__(self, row, col, imgPath):
        self.pos = [row, col]
        self.sprite = pygame.image.load(imgPath)

class Cell():
    def __init__(self, row, col):
        self.col = col
        self.row = row
        self.name = str(row) + str(col)

        self.x = row * 40
        self.y = col * 40

        self.connections = []

        self.blocked = False

    def setConnections(self, connections):
        self.connections = connections

class Board():
    def __init__(self):
        self.grid = [[Cell(0, 0), Cell(0, 1), Cell(0, 2), Cell(0, 3), Cell(0, 4), Cell(0, 5), Cell(0, 6), Cell(0, 7), Cell(0, 8), Cell(0, 9)],
                     [Cell(1, 0), Cell(1, 1), Cell(1, 2), Cell(1, 3), Cell(1, 4), Cell(1, 5), Cell(1, 6), Cell(1, 7), Cell(1, 8), Cell(1, 9)],
                     [Cell(2, 0), Cell(2, 1), Cell(2, 2), Cell(2, 3), Cell(2, 4), Cell(2, 5), Cell(2, 6), Cell(2, 7), Cell(2, 8), Cell(2, 9)],
                     [Cell(3, 0), Cell(3, 1), Cell(3, 2), Cell(3, 3), Cell(3, 4), Cell(3, 5), Cell(3, 6), Cell(3, 7), Cell(3, 8), Cell(3, 9)],
                     [Cell(4, 0), Cell(4, 1), Cell(4, 2), Cell(4, 3), Cell(4, 4), Cell(4, 5), Cell(4, 6), Cell(4, 7), Cell(4, 8), Cell(4, 9)],
                     [Cell(5, 0), Cell(5, 1), Cell(5, 2), Cell(5, 3), Cell(5, 4), Cell(5, 5), Cell(5, 6), Cell(5, 7), Cell(5, 8), Cell(5, 9)],
                     [Cell(6, 0), Cell(6, 1), Cell(6, 2), Cell(6, 3), Cell(6, 4), Cell(6, 5), Cell(6, 6), Cell(6, 7), Cell(6, 8), Cell(6, 9)],
                     [Cell(7, 0), Cell(7, 1), Cell(7, 2), Cell(7, 3), Cell(7, 4), Cell(7, 5), Cell(7, 6), Cell(7, 7), Cell(7, 8), Cell(7, 9)],
                     [Cell(8, 0), Cell(8, 1), Cell(8, 2), Cell(8, 3), Cell(8, 4), Cell(8, 5), Cell(8, 6), Cell(8, 7), Cell(8, 8), Cell(8, 9)],
                     [Cell(9, 0), Cell(9, 1), Cell(9, 2), Cell(9, 3), Cell(9, 4), Cell(9, 5), Cell(9, 6), Cell(9, 7), Cell(9, 8), Cell(9, 9)]]
        
        # Corners
        self.grid[0][0].setConnections([self.grid[0][1], self.grid[1][0]])
        self.grid[0][9].setConnections([self.grid[0][8], self.grid[1][9]])
        self.grid[9][0].setConnections([self.grid[8][0], self.grid[9][1]])
        self.grid[9][9].setConnections([self.grid[8][9], self.grid[9][8]])

        # Top row
        for i in range(1, 8+1):
            self.grid[0][i].setConnections([self.grid[0][i-1], self.grid[0][i+1], self.grid[1][i]])

        # Bottom row
        for i in range(1, 8+1):
            self.grid[9][i].setConnections([self.grid[9][i-1], self.grid[9][i+1], self.grid[8][i]])

        # Left column
        for i in range(1, 8+1):
            self.grid[i][0].setConnections([self.grid[i-1][0], self.grid[i+1][0], self.grid[i][1]])

        # Right column
        for i in range(1, 8+1):
            self.grid[i][9].setConnections([self.grid[i-1][9], self.grid[i+1][9], self.grid[i][9]])

        # Interior columns
        for i in range(1, 8+1):
            for j in range(1, 8+1):
                self.grid[i][j].setConnections([self.grid[i][j-1], self.grid[i][j+1], self.grid[i-1][j], self.grid[i+1][j]])

class MCTS():
    def __init__(self, board, linkPos, gannonPos):
        self.dest = [linkPos[0], linkPos[1]]
        self.src = [gannonPos[0], gannonPos[1]]

        self.root = MCTSNode(board.grid[gannonPos[0]][gannonPos[1]], None)
        self.root.makeChildren()

    def step(self):
        
        for i in range(0, 100+1):
            selected = self.root

            # Selection
            while len(selected.children) != 0:
                selected = self.selection(selected)
                print(selected.cell.name)

            # Expansion
            selected.makeChildren()

            # Simulation
            value = self.simulation(selected)

            # Backpropagation
            self.backpropagation(selected, value)

        selected = self.selection(self.root)
        return [int(selected.cell.name[0]), int(selected.cell.name[1])]

    def calcUCB(self, Vi, N, ni):
        # Vi = average reward/value of all nodes beneath this node
        # N = number of times the parent node has been visited
        # ni = number of times the child node i has been visited
        if N == 0 or ni == 0:
            return float('inf')
        else:
            return Vi + 2 * math.sqrt(math.log(N)/ni)

    def selection(self, node):  
        value = 0
        selected = node.children[0]

        for i in node.children:
            UCB = self.calcUCB(i.value, node.visits, i.visits)
            if UCB > value:
                value = i.value
                selected = i

        return selected

    def expansion(self):
        print()

    def moveLeft(self, pos):
        pos[1] -= 1
        if pos[1] < 0:
            pos[1] += 1

        return pos

    def moveRight(self, pos):
        pos[1] += 1
        if pos[1] > 9:
            pos[1] -= 1

        return pos

    def moveUp(self, pos):
        pos[0] -= 1
        if pos[0] < 0:
            pos[0] += 1
        
        return pos

    def moveDown(self, pos):
        pos[0] += 1
        if pos[0] > 9:
            pos[0] -= 1

        return pos

    def simulation(self, node):
        pos = [node.cell.row, node.cell.col]
        target = self.dest

        counter = 1

        while pos != target:
            move = random.randint(0, 3)

            counter += 1

            if (move == 0):
                pos = self.moveLeft(pos)
            elif (move == 1):
                pos = self.moveRight(pos)
            elif (move == 2):
                pos = self.moveUp(pos)
            else:
                pos = self.moveDown(pos)

            move = random.randint(0, 3)

            if (move == 0):
                target = self.moveLeft(target)
            elif (move == 1):
                target = self.moveRight(target)
            elif (move == 2):
                target = self.moveUp(target)
            else:
                target = self.moveDown(target)

        return 100.0 / counter

    def backpropagation(self, node, value):
        while node.parent != None:
            node.value += value
            node.visits += 1
            node = node.parent

        # Update root
        node.value += value
        node.visits += 1

class MCTSNode():
    def __init__(self, cell, parent):
        self.cell = cell
        self.parent = parent
        self.children = []
        self.value = 0
        self.visits = 0

    def makeChildren(self):
        for i in self.cell.connections:
            self.children.append(MCTSNode(i, self))

def detectGridPos(pos):
    row = 0
    col = 0

    if pos[0] > 200:
        if pos[0] > 320:
            if pos[0] > 360:
                col = 9
            else:
                col = 8
        else:
            if pos[0] > 280:
                col = 7
            elif pos[0] > 240:
                col = 6
            else:
                col = 5
    else:
        if pos[0] > 120:
            if pos[0] > 160:
                col = 4
            else:
                col = 3
        else:
            if pos[0] > 80:
                col = 2
            elif pos[0] > 40:
                col = 1
            else:
                col = 0

    if pos[1] > 200:
        if pos[1] > 320:
            if pos[1] > 360:
                row = 9
            else:
                row = 8
        else:
            if pos[1] > 280:
                row = 7
            elif pos[1] > 240:
                row = 6
            else:
                row = 5
    else:
        if pos[1] > 120:
            if pos[1] > 160:
                row = 4
            else:
                row = 3
        else:
            if pos[1] > 80:
                row = 2
            elif pos[1] > 40:
                row = 1
            else:
                row = 0

    return (row, col)

class Pathfinder():
    def __init__(self, grid):
        self.grid = grid
        self.currentPath = []

    def sortFrontier(self, frontier):
        return sorted(frontier, key=lambda x:x[1])
    
    def hCost(self, src, dest):
        pos = (int(src[0]), int(src[1]))

        x = dest.row - pos[0]
        y = dest.col - pos[1]

        x = abs(x)
        y = abs(y)

        return x + y
    
    def backtrack(self, dest, path):
        parent = dest.name

        while True:
            if parent == None:
                break
            
            self.currentPath.append(parent)
            
            try:
                parent = path[parent]
            except:
                print("No path available!")
                return

    def findPath(self, src, dest):
        frontier = []
        frontier.append([src.name, 0])
        frontier = self.sortFrontier(frontier)

        came_from = dict()
        cost_so_far = dict()
        came_from[src.name] = None
        cost_so_far[src.name] = 0

        while len(frontier) != 0:
            current = frontier[0]
            del frontier[0]

            if current[0] == dest.name:
                break

            pos = (int(current[0][0]), int(current[0][1]))

            for i in self.grid[pos[0]][pos[1]].connections:
                new_cost = cost_so_far[current[0]] + 1

                if i.blocked:
                    continue

                if i.name not in cost_so_far or new_cost < cost_so_far[i.name]:
                    cost_so_far[i.name] = new_cost
                    priority = new_cost + self.hCost(i.name, dest)
                    frontier.append([i.name, priority])
                    came_from[i.name] = current[0]

        self.backtrack(dest, came_from)

# -----------------------------------------------------------------------------

oldTime = time.time()

# Start display
pygame.init()
screen = pygame.display.set_mode((400, 400))

# Start audio
mixer.init()
mixer.music.load("bgmusic.mp3")
mixer.music.set_volume(0.3)
mixer.music.play()
mixer.music.pause()
mute = True

link = Link(0, 0, "link.jpg")
gannon = Gannon(9, 9, "enemy.jpg")

bgd = pygame.image.load("grid.jpg")
rock = pygame.image.load("rock.jpg")
rocks = []

running = True
doAStar = False
doMCTS = True

board = Board()
path = Pathfinder(board.grid)

# Main game loop
while running:

    step = False

    # Wait for user movement
    while step == False:

        if mute:
            mixer.music.pause()
        else:
            mixer.music.unpause()

        screen.blit(bgd, (0, 0))
        screen.blit(link.sprite, (link.pos[1] * 40, link.pos[0] * 40))
        screen.blit(gannon.sprite, (gannon.pos[1] * 40, gannon.pos[0] * 40))

        for i in rocks:
            screen.blit(rock, (i[1] * 40, i[0] * 40))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                pos = detectGridPos(pos)
                if pos not in rocks:
                    rocks.append(pos)
                    board.grid[pos[0]][pos[1]].blocked = True
                else:
                    rocks.remove(pos)
                    board.grid[pos[0]][pos[1]].blocked = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit(0)

                if event.key == pygame.K_w:
                    link.pos[0] -= 1

                    if link.pos[0] < 0:
                        link.pos[0] += 1

                    if board.grid[link.pos[0]][link.pos[1]].blocked:
                        link.pos[0] += 1
                    
                    step = True

                if event.key == pygame.K_s:
                    link.pos[0] += 1

                    if link.pos[0] > 9:
                        link.pos[0] -= 1

                    if board.grid[link.pos[0]][link.pos[1]].blocked:
                        link.pos[0] -= 1

                    step = True

                if event.key == pygame.K_d:
                    link.pos[1] += 1

                    if link.pos[1] > 9:
                        link.pos[1] -= 1
                    
                    if board.grid[link.pos[0]][link.pos[1]].blocked:
                        link.pos[1] -= 1

                    step = True

                if event.key == pygame.K_a:
                    link.pos[1] -= 1

                    if link.pos[1] < 0:
                        link.pos[1] += 1

                    if board.grid[link.pos[0]][link.pos[1]].blocked:
                        link.pos[1] += 1

                    step = True

                if event.key == pygame.K_m:
                    mute = not mute

                if event.key == pygame.K_f:
                    path.findPath()

                if event.key == pygame.K_SPACE:
                    step = True

                if event.key == pygame.K_1:
                    doAStar = True
                    doMCTS = False

                if event.key == pygame.K_2:
                    doAStar = False
                    doMCTS = True
    
    if doAStar:
        path.currentPath.clear()
        path.findPath(board.grid[gannon.pos[0]][gannon.pos[1]], board.grid[link.pos[0]][link.pos[1]])
        if len(path.currentPath) > 1:
            gannonMove = path.currentPath[len(path.currentPath)-2]
            gannon.pos = (int(gannonMove[0]), int(gannonMove[1]))

    if doMCTS:
        pos = MCTS(board, link.pos, gannon.pos).step()
        gannon.pos = pos