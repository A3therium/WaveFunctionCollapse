# Imports
from common import *
import random as rn
import time

# CONSTANTS
NULL = '\x1b[0m0'
OFFSETS = [[0,1],[1,0],[0,-1],[-1,0]]

# Functions
class cell:
    def __init__(self, states):
        self.states = states
        self.state = NULL

    def collapse(self, neighbours):
        possibleStates = []
        for i in self.states:
            validState = True
            for j in neighbours:
                if j not in i[1]:
                    validState = False
                    break
            if validState: possibleStates.append(i[0])
        if len(possibleStates) != 0:
            self.state = rn.choice(possibleStates)

class grid:
    def __init__(self, states, dim):
        self.dim = dim
        self.grid = []
        for i in range(0,dim[1]):
            gridRow = []
            for j in range(0,dim[0]):
                gridRow.append(cell(states))
            self.grid.append(gridRow)
        self.propogationList = []

    def generate(self):
        areaPercentage = (self.dim[0] * self.dim[1]) / 100
        startX = rn.randint(0,self.dim[0]-1)
        startY = rn.randint(0,self.dim[1]-1)
        self.propogate([startX,startY])
        count = 0
        while len(self.propogationList) != 0:
            self.propogate(self.propogationList[-1])
            self.propogationList.pop()             
            if len(self.propogationList) == 0:
                for i in range(0,self.dim[1]):
                    for j in range(0,self.dim[0]):
                        if self.grid[i][j].state == NULL:
                            self.propogationList.append([j,i])

            count += 1
            self.print(count)
            time.sleep(0.001)

    def propogate(self,pos):
        if self.grid[pos[1]][pos[0]].state != NULL: return
        neighbours = []
        neighbourPos = posAdd(pos,OFFSETS)
        for i in neighbourPos:
            if i[0] < 0 or i[1] < 0:
                state = NULL
            else: 
                try:
                    state = self.grid[i[1]][i[0]].state
                except:
                    state = NULL
            if state != NULL:
                neighbours.append(state)
        rn.shuffle(neighbourPos)
        for i in neighbourPos:
            try:
                if self.grid[i[1]][i[0]].state == NULL and not (i[0] < 0 or i[1] < 0):
                    self.propogationList.append(i)
            except:
                pass
        self.grid[pos[1]][pos[0]].collapse(neighbours)

    def getGrid(self):
        returnGrid = []
        for i in self.grid:
            returnGridRow = []
            for j in i:
                if j.state == NULL: return False
                returnGridRow.append(j.state)
            returnGrid.append(returnGridRow)
        return returnGrid

    def print(self, count):
        percentageComplete = clamp(count / (self.dim[0] * self.dim[1]) * 50,0,100)
        output = ''
        for i in self.grid:
            for j in i:
                output += f'{j.state} '
            output += '\n'
        print('\x1b[H\x1b[0J',end='') # Clears console and moves cursor to 0,0
        for i in output.split('\n'):
            print(i)
        print(f'\x1b[0m{round(percentageComplete,2)}%')

def main():
    while True:
        print('Please enter desired dimensions: (max - 75 x 40) ')
        width = clamp(int(input('[width]: ')),0,75)
        height = clamp(int(input('[height]: ')),0,40)

        s1 = '\x1b[1;34m~\x1b[22m'
        s2 = '\x1b[33m='
        s3 = '\x1b[1;32m#\x1b[22m'
        s4 = '\x1b[32m|'
        s5 = '\x1b[37m^'
        states = [[s1,[s1,s2]],[s2,[s2,s1,s3]],[s3,[s3,s2,s1,s4,s5]],[s4,[s4,s3,s5]],[s5,[s4,s5]]]
        totals = [0] * len(states)
        map = grid(states, [width,height])
        map.generate()
        mapGrid = map.getGrid()
        for i in mapGrid:
            for j in i:
                for k in range(0,len(states)):
                    if j == states[k][0]:
                        totals[k] += 1
        for i in range(0,len(totals)): print(f'{states[i][0]}\x1b[0m: {round(totals[i] / (width * height) * 100,2)}%',end=' ')
        input('\n\x1b[38;5;1mDone generating. Press enter to run again.\x1b[0m')

# Driver
if __name__ == '__main__':
    main()
