# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 15:16:11 2019

@author: dmlov
"""

import random
import matplotlib.pyplot as plot
import math
import sys, argparse
import time

side = 1.0
edge = math.sqrt(2)
corner = math.sqrt(3)
maxSize = 500
maxEnt = 5
tests = 10
totalEnt = 6

class map(object):
    def __init__(self, l, w, h):
        if h == -1:
            holderL = []
            for i in range(l):
                holderW = []
                for j in range(w):
                    holderW.append(mapSpot(i, j))
                holderL.append(holderW)
            self.map = holderL
        else:
            holderL = []
            for i in range(l):
                holderW = []
                for j in range(w):
                    holderH = []
                    for k in range(h):
                        holderH.append(mapSpot(i, j, k))
                    holderW.append(holderH)
                holderL.append(holderW)
            self.map = holderL
        self.l = l
        self.w = w
        self.h = h
        
    def verify(self):
        count = 1 
        for i in range(self.l):
            for j in range(self.w):
                for k in range(self.h):
                    m = self.map[i][j][k]
                    if m.end == True:
                        print(count)
                        count = count + 1
        
    def setEnd(self, l, w, h):
        if h == -1:
            end = self.map[l][w]
            end.setEnd()
            self.map[l][w] = end
        else:
            end = self.map[l][w][h]
            #print(l, w, h)
            end.setEnd()
            self.map[l][w][h] = end
    
    def printSize(self):
        print(self.l, self.w, self.h)
    
    def setEntity(self, dim, l, w, h = -1):
        if dim == False:
            spot = self.map[l][w]
            spot.entity = True
            self.map[l][w] = spot
        else:
            spot = self.map[l][w][h]
            spot.entity = True
            self.map[l][w][h] = spot
    
    def moveEntity(self, ent, dim, l, w, h = -1):
        if dim == False:
            spot = self.map[ent.locL][ent.locW]
            spot.entity = False
            spotL = spot
            self.map[ent.locL][ent.locW] = spot
            spot = self.map[l][w]
            spot.entity = True
            spot.last = spotL
            self.map[l][w] = spot
        else:
            spot = self.map[ent.locL][ent.locW][ent.locH]
            spot.entity = False
            spotL = spot
            self.map[ent.locL][ent.locW][ent.locH] = spot
            spot = self.map[l][w][h]
            spot.entity = True
            spot.last = spotL
            self.map[l][w][h] = spot
            
    def search(self, l, w, h, setDis = False):
        m = self.map
        #found = False
        searching = []
        if h != -1:
            cur = m[l][w][h]
            cur.search()
            m[l][w][h] = cur
            for i in range(l - 1, l + 2):
                if i < 0 or i >= self.l or i == l + 2:
                    continue
                for j in range(w - 1, w + 2):
                    if j < 0 or j >= self.w or j == w + 2:
                        continue
                    for k in range(h - 1, h + 2):
                        if k < 0 or k >= self.h or k == h + 2:
                            continue
                        hold = m[i][j][k]
                        if not hold.searching and not hold.searched and not hold.isEntity():
                            if i == l and j == w and k == h:
                                continue
                            #if hold.end:
                                #found = True
                            hold.find(m[l][w][h])
                            hold.findH()
                            if setDis:
                                hold.setDis()
                            searching.append(hold)
                            m[i][j][k] = hold
        else:
            cur = m[l][w]
            cur.search()
            m[l][w] = cur
            for i in range(l - 1, l + 2):
                if i < 0 or i >= self.l or i == l + 2:
                    continue
                for j in range(w - 1, w + 2):
                    if j < 0 or j >= self.w or j == w + 2:
                        continue
                    hold = m[i][j]
                    if not hold.searching and not hold.searched:
                        if i == l and j == w:
                            continue
                        #if hold.end:
                            #found = True
                        hold.find(m[l][w])
                        hold.findH()
                        if setDis:
                            hold.setDis()
                        searching.append(hold)
                        m[i][j]
        self.map = m
        return searching
        
    def reset(self):
        for i in range(self.l):
            for j in range(self.w):
                if self.h != -1:
                    for p in range(self.h):
                        spot = self.map[i][j][p]
                        spot.reset()
                        self.map[i][j][p] = spot
                else:
                    spot = self.map[i][j]
                    spot.reset()
                    self.map[i][j] = spot
                    
    def fullReset(self):
        for i in range(self.l):
            for j in range(self.w):
                if self.h != -1:
                    for p in range(self.h):
                        spot = self.map[i][j][p]
                        spot.fullReset()
                        self.map[i][j][p] = spot
                else:
                    spot = self.map[i][j]
                    spot.fullReset()
                    self.map[i][j] = spot
                    
    def findG(self, endL, endW, endH = -1):
        m = self.map
        if(endH != -1):
            for i in range(self.l):
                for j in range(self.w):
                    for k in range(self.h):
                        #print(i, j, k)
                        dis = [abs(endL - i), abs(endW - j), abs(endH - k)]
                        g = 0
                        small = 0
                        while small != maxSize * 2:
                            #print(small)
                            small = maxSize * 2
                            for x in dis:
                                if x < small and x > 0:
                                    small = x
                            dif = uniCount(dis)
                            if dif == 3:
                                g = g + (corner * small)
                            elif dif == 2:
                                g = g + (edge * small)
                            elif dif == 1:
                                g = g + (side * small)
                            dis = [x - small for x in dis]
                        hold = m[i][j][k]
                        #print(g)
                        hold.setHeurs(g, 0)
                        m[i][j][k] = hold
        self.map = m
    
    def setStart(self, x, y, z):
        m = self.map
        if z != -1:
            hold = m[x][y][z]
            hold.dis = 0
            m[x][y][z] = hold
        else:
            hold = m[x][y]
            hold.dis = 0
            m[x][y] = hold
        self.map = m
                                
def uniCount(list):
    unique = []
    for x in list:
        if x not in unique:
            unique.append(x)
    return len(unique)

class mapSpot(object):
    def __init__(self, l, w, h = -1):
        self.f = 0
        self.g = 0
        self.h = 0
        self.l = l
        self.w = w
        self.he = h
        self.dis = (maxSize * side) + (maxSize * edge) + (maxSize * corner)
        self.searching = False
        self.searched = False
        self.last = None
        self.entity = False
        self.end = False
        self.disEnd = 0
        
    def setHeurs(self, g, h):
        self.g = g
        #print(g)
        self.h = h
        #print(h)
        self.f = g + h
        #print(self.f)
        
    def reset(self):
        self.f = 0
        #self.g = 0
        self.h = 0
        self.searching = False
        self.searched = False
        self.last = None        
        self.dis = (maxSize * side) + (maxSize * edge) + (maxSize * corner)
        if self.end == True:
            self.entity = False
        
    def fullReset(self):
        self.f = 0
        #self.g = 0
        self.h = 0
        self.searching = False
        self.searched = False
        self.last = None
        self.dis = (maxSize * side) + (maxSize * edge) + (maxSize * corner)
        self.entity = False
        
    def find(self, last):
        self.searching = True
        self.last = last
        
    def setDis(self):
        last = self.last
        count = 0
        if last.l != self.l:
            count = count + 1
        if last.w != self.w:
            count = count + 1
        if last.he != self.he:
            count = count + 1
        if count == 3:
            self.dis = last.dis + corner
        if count == 2:
            self.dis = last.dis + edge
        if count == 1:
            self.dis = last.dis + side
        
    def findH(self):
        last = self.last
        same = 0
        dif = [self.l - last.l, self.w - last.w, self.he - last.he]
        for i in dif:
            if i == 0:
                same = same + 1
        if same == 0:
            self.setHeurs(self.g, last.h + corner)
        elif same == 1:
            self.setHeurs(self.g, last.h + edge)
        elif same == 2:
            self.setHeurs(self.g, last.h + side)
        else:
            print("Error in findH: ", same)
            sys.exit()
        
    def search(self):
        self.searched = True
        
    def setEnd(self):
        self.end = True
    
    def backTrack(self, num = 0):
        #print(self.l, self.w, self.he)
        #print(self.f)
        hold = self
        next = hold.last
        while next != None:
            hold = next
            next = hold.last
            num = num + 1
        """if self.last == None:
            return num
        hold = self.last
        num = num + 1"""
        return num
    
    def isEnd(self):
        return self.end
    
    def buildPath(self, path = []):
        hold = self.last
        print("Build", self.l, self.w, self.he)
        #print(len(path))
        path.append(self)
        #print(len(path))
        if self.entity == True and not hold == None:
            print("Is entity. Something went wrong")
            sys.exit()
        if hold == None:
            return path
        return hold.buildPath(path)
    
    def isEqual(self, second):
        return (self.l == second.l) and (self.w == second.w) and (self.he == second.he)
    
    def isEntity(self):
        return self.entity
    
class Dijkstra(object):
    def __init__(self, endL, endW, endH, startL, startW, startH, map):
        self.endL = endL
        self.endW = endW
        self.endH = endH
        self.locL = startL
        self.locW = startW
        self.locH = startH
        self.complete = False
        self.movable = False
        if endH == -1:
            self.dim = False
        else:
            self.dim = True
            
    def checkEnd(self):
        if self.endL == self.locL and self.endW == self.locW and self.endH == self.locH:
            print("Fin")
            self.complete = True
    
    def move(self, map):
        l = len(self.path)
        #print(l)
        x = self.path[l - 1]
        m = map.map
        if self.dim and m[x.l][x.w][x.he].entity == False:
            map.moveEntity(self, self.dim, x.l, x.w, x.he)
            self.locL = x.l
            self.locW = x.w
            self.locH = x.he
            self.checkEnd()
            path = self.path
            path.pop()
            self.path = path
            return self.complete
        elif not self.dim and m[x.l][x.w].entity == False:
            map.moveEntity(self, self.dim, x.l, x.w, x.he)
            self.locL = x.l
            self.locW = x.w
            self.locH = x.he
            self.checkEnd()
            path = self.path
            path.pop()
            self.path = path
            return self.complete
        else:
            self.movable = False
            return self.complete
        
    def simM(self, map):
        #start = time.time()
        map.setStart(self.locL, self.locW, self.locH)
        print("Dijkstra's Algorithm")
        x = None
        m = map.map
        found = False
        newSearching = []
        if self.endH != -1:
            searching = [m[self.locL][self.locW][self.locH]]
        else:
            searching = [m[self.locL][self.locW]]
        searched = []
        while not found:  
            count = 0
            smallest = (maxSize * side) + (maxSize * edge)
            if self.endH != -1:
                smallest = smallest + (maxSize * corner)
            if len(searching) == 1:
                spotLoc = 0
                smallest = searching[0].dis
            else:
                for i in searching:
                    if i.dis < smallest:
                        smallest = i.dis
                        spotLoc = count
                    count = count + 1
            x = searching[spotLoc]
            newSearching = map.search(x.l, x.w, x.he, True)
            k = 0
            while k != -1:
                k = -1
                for j in range(len(newSearching)):
                    if newSearching[j].isEntity():
                        k = j
                        newSearching.pop(j)
                        break
            m = map.map
            if self.endH != -1:
                x = m[x.l][x.w][x.he]
            else:
                x = m[x.l][x.w]
            searched.append(searching[spotLoc])
            searching.pop(spotLoc)
            count = 0
            counting = 0
            if len(searching) == 0:
                searching = newSearching
            else:
                for z in newSearching:
                    for y in searching:
                        if not z.isEqual(y):
                            count = count + 1
                            if y.l == z.l and y.w == z.w and y.he == z.he:
                                print("Something isn't working with equals: ", y.l, y.w, y.he, z.l, z.w, z.he)
                                sys.exit()
                        #print("RRTChecking equals", count, counting, len(searching), len(newSearching), len(searched), (map.l * map.w * map.h))
                    if count == len(searching) and not z.searched and not z.entity:
                        #print("Append: ", len(searching))
                        searching.append(z)
                    """if len(searching) + len(searched) > (map.l * map.w * map.h):
                        print("Error. Too many searching!")
                        sys.exit()"""
                    count = 0
                    counting = counting + 1
                newSearching = []
            found = x.end
        #print(spot.l, spot.w, spot.he, self.endL, self.endW, self.endH)
        m = map.map
        if self.endH != -1:
            x = m[x.l][x.w][x.he]
        else:
            x = m[x.l][x.w]
        print(x.l, x.w, x.he, self.endL, self.endW, self.endH)
        print(x.l, x.w, x.he, self.locL, self.locW, self.locH)
        #print(x.end)
        #print(m[self.endL][self.endW][self.endH].end)
        path = []
        #print(len(path))
        path = x.buildPath(path)
        #print(len(path))
        #for p in path:
        #    print(p.l, p.w, p.he)
        path.pop(-1)
        self.path = path
        self.movable = True
        
    def sim(self, map):
        start = time.time()
        map.setStart(self.locL, self.locW, self.locH)
        print("Dijkstra's Algorithm")
        x = None
        m = map.map
        found = False
        newSearching = []
        if self.endH != -1:
            searching = [m[self.locL][self.locW][self.locH]]
        else:
            searching = [m[self.locL][self.locW]]
        searched = []
        while not found:  
            count = 0
            smallest = (maxSize * side) + (maxSize * edge)
            if self.endH != -1:
                smallest = smallest + (maxSize * corner)
            if len(searching) == 1:
                spotLoc = 0
                smallest = searching[0].dis
            else:
                for i in searching:
                    if i.dis < smallest:
                        smallest = i.dis
                        spotLoc = count
                    count = count + 1
            x = searching[spotLoc]
            newSearching = map.search(x.l, x.w, x.he, True)
            m = map.map
            if self.endH != -1:
                x = m[x.l][x.w][x.he]
            else:
                x = m[x.l][x.w]
            searched.append(searching[spotLoc])
            searching.pop(spotLoc)
            count = 0
            counting = 0
            if len(searching) == 0:
                searching = newSearching
            else:
                for z in newSearching:
                    for y in searching:
                        if not z.isEqual(y):
                            count = count + 1
                            if y.l == z.l and y.w == z.w and y.he == z.he:
                                print("Something isn't working with equals: ", y.l, y.w, y.he, z.l, z.w, z.he)
                                sys.exit()
                        #print("RRTChecking equals", count, counting, len(searching), len(newSearching), len(searched), (map.l * map.w * map.h))
                    if count == len(searching) and not z.searched:
                        #print("Append: ", len(searching))
                        searching.append(z)
                    """if len(searching) + len(searched) > (map.l * map.w * map.h):
                        print("Error. Too many searching!")
                        sys.exit()"""
                    count = 0
                    counting = counting + 1
                newSearching = []
            if x.end:
                #print("End at: ", x.l, x.w, x.he)
                found = True
        #print(spot.l, spot.w, spot.he, self.endL, self.endW, self.endH)
        end = time.time()
        m = map.map
        if self.endH != -1:
            x = m[x.l][x.w][x.he]
        else:
            x = m[x.l][x.w]
        bt = x.backTrack()
        return (end - start), x, len(searching) + len(searched), len(searched), bt
    
class BestFS(object):
    def __init__(self, endL, endW, endH, startL, startW, startH):
        self.endL = endL
        self.endW = endW
        self.endH = endH
        self.locL = startL
        self.locW = startW
        self.locH = startH
        self.complete = False
        self.movable = False
        self.path = []
        if endH == -1:
            self.dim = False
        else:
            self.dim = True
            
    def simM(self, map):
        map.setStart(self.locL, self.locW, self.locH)
        print("Best First Search")
        x = None
        m = map.map
        found = False
        newSearching = []
        if self.endH != -1:
            searching = [m[self.locL][self.locW][self.locH]]
        else:
            searching = [m[self.locL][self.locW]]
        searched = []
        while not found:  
            count = 0
            spotLoc = 0
            smallest = (maxSize * side * 2) + (maxSize * edge * 2) + (maxSize * corner * 2)
            if len(searching) == 1:
                spotLoc = 0
                smallest = searching[0].dis
            else:
                for i in searching:
                    if i.g < smallest:
                        smallest = i.g
                        spotLoc = count
                    count = count + 1
            x = searching[spotLoc]
            newSearching = map.search(x.l, x.w, x.he, True)
            k = 0
            while k != -1:
                k = -1
                for j in range(len(newSearching)):
                    if newSearching[j].isEntity():
                        k = j
                        newSearching.pop(j)
                        break
            m = map.map
            if self.endH != -1:
                x = m[x.l][x.w][x.he]
            else:
                x = m[x.l][x.w]
            searched.append(searching[spotLoc])
            searching.pop(spotLoc)
            count = 0
            counting = 0
            if len(searching) == 0:
                searching = newSearching
            else:
                for z in newSearching:
                    for y in searching:
                        if not z.isEqual(y):
                            count = count + 1
                            if y.l == z.l and y.w == z.w and y.he == z.he:
                                print("Something isn't working with equals: ", y.l, y.w, y.he, z.l, z.w, z.he)
                                sys.exit()
                        #print("RRTChecking equals", count, counting, len(searching), len(newSearching), len(searched), (map.l * map.w * map.h))
                    if count == len(searching) and not z.searched and not z.isEntity():
                        #print("Append: ", len(searching))
                        searching.append(z)
                    """if len(searching) + len(searched) > (map.l * map.w * map.h):
                        print("Error. Too many searching!")
                        sys.exit()"""
                    count = 0
                    counting = counting + 1
                newSearching = []
            found = x.end
        #print(spot.l, spot.w, spot.he, self.endL, self.endW, self.endH)
        m = map.map
        if self.endH != -1:
            x = m[x.l][x.w][x.he]
        else:
            x = m[x.l][x.w]
        print(x.l, x.w, x.he, self.endL, self.endW, self.endH)
        print(x.l, x.w, x.he, self.locL, self.locW, self.locH)
        #print(x.end)
        #print(m[self.endL][self.endW][self.endH].end)
        path = []
        #print(len(path))
        path = x.buildPath(path)
        #print(len(path))
        #for p in path:
        #    print(p.l, p.w, p.he)
        path.pop(-1)
        self.path = path
        self.movable = True
    
    def move(self, map):
        l = len(self.path)
        #print(l)
        x = self.path[l - 1]
        m = map.map
        if self.dim and m[x.l][x.w][x.he].entity == False:
            map.moveEntity(self, self.dim, x.l, x.w, x.he)
            self.locL = x.l
            self.locW = x.w
            self.locH = x.he
            self.checkEnd()
            path = self.path
            path.pop()
            self.path = path
            return self.complete
        elif not self.dim and m[x.l][x.w].entity == False:
            map.moveEntity(self, self.dim, x.l, x.w, x.he)
            self.locL = x.l
            self.locW = x.w
            self.locH = x.he
            self.checkEnd()
            path = self.path
            path.pop()
            self.path = path
            print("Moving")
            return self.complete
        else:
            self.movable = False
            return self.complete
    
    def checkEnd(self):
        if self.endL == self.locL and self.endW == self.locW and self.endH == self.locH:
            print("Fin")
            self.complete = True
        
    def sim(self, map):
        start = time.time()
        map.setStart(self.locL, self.locW, self.locH)
        print("Best First Search")
        x = None
        m = map.map
        found = False
        newSearching = []
        if self.endH != -1:
            searching = [m[self.locL][self.locW][self.locH]]
        else:
            searching = [m[self.locL][self.locW]]
        searched = []
        while not found:  
            count = 0
            spotLoc = 0
            smallest = (maxSize * side) + (maxSize * edge) + (maxSize * corner)
            if len(searching) == 1:
                spotLoc = 0
                smallest = searching[0].dis
            else:
                for i in searching:
                    if i.g < smallest:
                        smallest = i.g
                        spotLoc = count
                    count = count + 1
            x = searching[spotLoc]
            newSearching = map.search(x.l, x.w, x.he, True)
            m = map.map
            if self.endH != -1:
                x = m[x.l][x.w][x.he]
            else:
                x = m[x.l][x.w]
            searched.append(searching[spotLoc])
            searching.pop(spotLoc)
            count = 0
            counting = 0
            if len(searching) == 0:
                searching = newSearching
            else:
                for z in newSearching:
                    for y in searching:
                        if not z.isEqual(y):
                            count = count + 1
                            if y.l == z.l and y.w == z.w and y.he == z.he:
                                print("Something isn't working with equals: ", y.l, y.w, y.he, z.l, z.w, z.he)
                                sys.exit()
                        #print("RRTChecking equals", count, counting, len(searching), len(newSearching), len(searched), (map.l * map.w * map.h))
                    if count == len(searching) and not z.searched:
                        #print("Append: ", len(searching))
                        searching.append(z)
                    """if len(searching) + len(searched) > (map.l * map.w * map.h):
                        print("Error. Too many searching!")
                        sys.exit()"""
                    count = 0
                    counting = counting + 1
                newSearching = []
            if x.end:
                #print("End at: ", x.l, x.w, x.he)
                found = True
        #print(spot.l, spot.w, spot.he, self.endL, self.endW, self.endH)
        end = time.time()
        m = map.map
        if self.endH != -1:
            x = m[x.l][x.w][x.he]
        else:
            x = m[x.l][x.w]
        bt = x.backTrack()
        return (end - start), x, len(searching) + len(searched), len(searched), bt
    
class BFS(object):
    def __init__(self, endL, endW, endH, startL, startW, startH):
        self.endL = endL
        self.endW = endW
        self.endH = endH
        self.locL = startL
        self.locW = startW
        self.locH = startH
        self.complete = False
        self.movable = False
        self.path = []
        if endH == -1:
            self.dim = False
        else:
            self.dim = True
        
    def simM(self, map):
        print("BFS")
        x = None
        m = map.map
        found = False
        newSearching = []
        if self.endH != -1:
            searching = [m[self.locL][self.locW][self.locH]]
        else:
            searching = [m[self.locL][self.locW]]
        searched = []
        while not found:
            if len(searching) == 1:
                spotLoc = 0
            else:
                spotLoc = random.randint(0, len(searching) - 1)
            x = searching[spotLoc]
            newSearching = map.search(x.l, x.w, x.he)
            k = 0
            while k != -1:
                k = -1
                for j in range(len(newSearching)):
                    if newSearching[j].isEntity():
                        k = j
                        newSearching.pop(j)
                        break
            m = map.map
            if self.endH != -1:
                x = m[x.l][x.w][x.he]
            else:
                x = m[x.l][x.w]
            searched.append(searching[spotLoc])
            searching.pop(spotLoc)
            count = 0
            counting = 0
            if len(searching) == 0:
                searching = newSearching
            else:
                for z in newSearching:
                    for y in searching:
                        if not z.isEqual(y):
                            count = count + 1
                            if y.l == z.l and y.w == z.w and y.he == z.he:
                                print("Something isn't working with equals: ", y.l, y.w, y.he, z.l, z.w, z.he)
                                sys.exit()
                        #print("RRTChecking equals", count, counting, len(searching), len(newSearching), len(searched), (map.l * map.w * map.h))
                    if count == len(searching) and not z.searched and not z.entity:
                        #print("Append: ", len(searching))
                        searching.append(z)
                    """if len(searching) + len(searched) > (map.l * map.w * map.h):
                        print("Error. Too many searching!")
                        sys.exit()"""
                    count = 0
                    counting = counting + 1
                newSearching = []
            found = x.end
        #print(spot.l, spot.w, spot.he, self.endL, self.endW, self.endH)
        m = map.map
        if self.endH != -1:
            x = m[x.l][x.w][x.he]
        else:
            x = m[x.l][x.w]
        print(x.l, x.w, x.he, self.endL, self.endW, self.endH)
        print(x.l, x.w, x.he, self.locL, self.locW, self.locH)
        #print(x.end)
        #print(m[self.endL][self.endW][self.endH].end)
        path = []
        #print(len(path))
        path = x.buildPath(path)
        #print(len(path))
        #for p in path:
        #    print(p.l, p.w, p.he)
        path.pop(-1)
        self.path = path
        self.movable = True
    
    def move(self, map):
        l = len(self.path)
        #print(l)
        x = self.path[l - 1]
        m = map.map
        if self.dim and m[x.l][x.w][x.he].entity == False:
            map.moveEntity(self, self.dim, x.l, x.w, x.he)
            self.locL = x.l
            self.locW = x.w
            self.locH = x.he
            self.checkEnd()
            path = self.path
            path.pop()
            self.path = path
            return self.complete
        elif not self.dim and m[x.l][x.w].entity == False:
            map.moveEntity(self, self.dim, x.l, x.w, x.he)
            self.locL = x.l
            self.locW = x.w
            self.locH = x.he
            self.checkEnd()
            path = self.path
            path.pop()
            self.path = path
            return self.complete
        else:
            self.movable = False
            return self.complete
    
    def checkEnd(self):
        if self.endL == self.locL and self.endW == self.locW and self.endH == self.locH:
            print("Fin")
            self.complete = True
        
    def sim(self, map):
        start = time.time()
        print("BFS")
        x = None
        m = map.map
        found = False
        newSearching = []
        if self.endH != -1:
            searching = [m[self.locL][self.locW][self.locH]]
        else:
            searching = [m[self.locL][self.locW]]
        searched = []
        while not found:
            spotLoc = 0
            x = searching[spotLoc]
            newSearching = map.search(x.l, x.w, x.he)
            m = map.map
            if self.endH != -1:
                x = m[x.l][x.w][x.he]
            else:
                x = m[x.l][x.w]
            searched.append(searching[spotLoc])
            searching.pop(spotLoc)
            count = 0
            counting = 0
            if len(searching) == 0:
                searching = newSearching
            else:
                for z in newSearching:
                    for y in searching:
                        if not z.isEqual(y):
                            count = count + 1
                            if y.l == z.l and y.w == z.w and y.he == z.he:
                                print("Something isn't working with equals: ", y.l, y.w, y.he, z.l, z.w, z.he)
                                sys.exit()
                        #print("RRTChecking equals", count, counting, len(searching), len(newSearching), len(searched), (map.l * map.w * map.h))
                    if count == len(searching) and not z.searched:
                        #print("Append: ", len(searching))
                        searching.append(z)
                    """if len(searching) + len(searched) > (map.l * map.w * map.h):
                        print("Error. Too many searching!")
                        sys.exit()"""
                    count = 0
                    counting = counting + 1
                newSearching = []
            if x.end:
                #print("End at: ", x.l, x.w, x.he)
                found = True
        #print(spot.l, spot.w, spot.he, self.endL, self.endW, self.endH)
        end = time.time()
        m = map.map
        if self.endH != -1:
            x = m[x.l][x.w][x.he]
        else:
            x = m[x.l][x.w]
        bt = x.backTrack()
        return (end - start), x, len(searching) + len(searched), len(searched), bt
    
class DFS(object):
    def __init__(self, endL, endW, endH, startL, startW, startH):
        self.endL = endL
        self.endW = endW
        self.endH = endH
        self.locL = startL
        self.locW = startW
        self.locH = startH
        self.complete = False
        self.movable = False
        self.path = []
        if endH == -1:
            self.dim = False
        else:
            self.dim = True
        
    def move(self, map):
        l = len(self.path)
        #print(l)
        x = self.path[l - 1]
        m = map.map
        if self.dim and m[x.l][x.w][x.he].entity == False:
            map.moveEntity(self, self.dim, x.l, x.w, x.he)
            self.locL = x.l
            self.locW = x.w
            self.locH = x.he
            self.checkEnd()
            path = self.path
            path.pop()
            self.path = path
            print("Moving")
            return self.complete
        elif not self.dim and m[x.l][x.w].entity == False:
            map.moveEntity(self, self.dim, x.l, x.w, x.he)
            self.locL = x.l
            self.locW = x.w
            self.locH = x.he
            self.checkEnd()
            path = self.path
            path.pop()
            self.path = path
            print("Moving")
            return self.complete
        else:
            self.movable = False
            return self.complete
    
    def checkEnd(self):
        if self.endL == self.locL and self.endW == self.locW and self.endH == self.locH:
            print("Fin")
            self.complete = True
            
    def simM(self, map):
        print("DFS")
        x = None
        m = map.map
        found = False
        newSearching = []
        if self.endH != -1:
            searching = [m[self.locL][self.locW][self.locH]]
        else:
            searching = [m[self.locL][self.locW]]
        searched = []
        while not found:
            spotLoc = len(searching) - 1
            #print(spotLoc)
            x = searching[spotLoc]
            newSearching = map.search(x.l, x.w, x.he)
            k = 0
            while k != -1:
                k = -1
                for j in range(len(newSearching)):
                    if newSearching[j].isEntity():
                        newSearching.pop(j)
                        k = j
                        break
            #print("new", len(newSearching))
            m = map.map
            if self.endH != -1:
                x = m[x.l][x.w][x.he]
            else:
                x = m[x.l][x.w]
            searched.append(searching[spotLoc])
            searching.pop(spotLoc)
            count = 0
            counting = 0
            if len(searching) == 0:
                searching = newSearching
            else:
                for z in newSearching:
                    for y in searching:
                        if not z.isEqual(y):
                            count = count + 1
                            m = map.map
                            if y.l == z.l and y.w == z.w and y.he == z.he:
                                print("Something isn't working with equals: ", y.l, y.w, y.he, z.l, z.w, z.he)
                                sys.exit()
                            if self.dim and m[z.l][z.w][z.he].entity == True:
                                count = count - 1
                            elif not self.dim and m[z.l][z.w].entity == True:
                                count = count - 1
                        #print("RRTChecking equals", count, counting, len(searching), len(newSearching), len(searched), (map.l * map.w * map.h))
                    if self.dim and count == len(searching) and not z.searched and (m[z.l][z.w][z.he].entity == False) and (z.entity == False):
                        #print("Append: ", len(searching))
                        #print(z.entity)
                        searching.append(z)
                    elif not self.dim and count == len(searching) and not z.searched and (m[z.l][z.w].entity == False) and (z.entity == False):
                        #print("Append: ", len(searching))
                        #print(z.entity)
                        searching.append(z)
                    count = 0
                    counting = counting + 1
                newSearching = []
            found = x.end
        #print(spot.l, spot.w, spot.he, self.endL, self.endW, self.endH)
        m = map.map
        if self.endH != -1:
            x = m[x.l][x.w][x.he]
        else:
            x = m[x.l][x.w]
        print(x.l, x.w, x.he, self.endL, self.endW, self.endH)
        print(x.l, x.w, x.he, self.locL, self.locW, self.locH)
        #print(x.end)
        #print(m[self.endL][self.endW][self.endH].end)
        path = []
        #print(len(path))
        path = x.buildPath(path)
        #print(len(path))
        #for p in path:
         #   print(p.l, p.w, p.he)
        path.pop(-1)
        self.path = path
        self.movable = True
        
    def sim(self, map):
        start = time.time()
        print("DFS")
        x = None
        m = map.map
        found = False
        newSearching = []
        if self.endH != -1:
            searching = [m[self.locL][self.locW][self.locH]]
        else:
            searching = [m[self.locL][self.locW]]
        searched = []
        while not found:
            spotLoc = len(searching) - 1
            #print(spotLoc)
            x = searching[spotLoc]
            newSearching = map.search(x.l, x.w, x.he)
            #print("new", len(newSearching))
            m = map.map
            if self.endH != -1:
                x = m[x.l][x.w][x.he]
            else:
                x = m[x.l][x.w]
            searched.append(searching[spotLoc])
            searching.pop(spotLoc)
            count = 0
            counting = 0
            if len(searching) == 0:
                searching = newSearching
            else:
                for z in newSearching:
                    for y in searching:
                        if not z.isEqual(y):
                            count = count + 1
                            if y.l == z.l and y.w == z.w and y.he == z.he:
                                print("Something isn't working with equals: ", y.l, y.w, y.he, z.l, z.w, z.he)
                                sys.exit()
                        #print("RRTChecking equals", count, counting, len(searching), len(newSearching), len(searched), (map.l * map.w * map.h))
                    if count == len(searching) and not z.searched and not z.entity:
                        #print("Append: ", len(searching))
                        searching.append(z)
                    """if len(searching) + len(searched) > (map.l * map.w * map.h):
                        print("Error. Too many searching!")
                        sys.exit()"""
                    count = 0
                    counting = counting + 1
                newSearching = []
            if x.end:
                #print("End at: ", x.l, x.w, x.he)
                found = True
        #print(spot.l, spot.w, spot.he, self.endL, self.endW, self.endH)
        end = time.time()
        m = map.map
        if self.endH != -1:
            x = m[x.l][x.w][x.he]
        else:
            x = m[x.l][x.w]
        bt = x.backTrack()
        return (end - start), x, len(searching) + len(searched), len(searched), bt
    
class RRT(object):
    def __init__(self, endL, endW, endH, startL, startW, startH):
        self.endL = endL
        self.endW = endW
        self.endH = endH
        self.locL = startL
        self.locW = startW
        self.locH = startH
        self.movable = False
        self.complete = False
        self.path = []
        if endH == -1:
            self.dim = False
        else:
            self.dim = True
        
    def simM(self, map):
        #start = time.time()
        print("RRT", self.locL, self.locW, self.locH)
        x = None
        m = map.map
        found = False
        newSearching = []
        if self.endH != -1:
            searching = [m[self.locL][self.locW][self.locH]]
        else:
            searching = [m[self.locL][self.locW]]
        searched = []
        while not found:
            if len(searching) == 1:
                spotLoc = 0
            else:
                spotLoc = random.randint(0, len(searching) - 1)
            x = searching[spotLoc]
            newSearching = map.search(x.l, x.w, x.he)
            k = 0
            while k != -1:
                k = -1
                for j in range(len(newSearching)):
                    if newSearching[j].isEntity():
                        newSearching.pop(j)
                        k = j
                        break
            m = map.map
            if self.endH != -1:
                x = m[x.l][x.w][x.he]
            else:
                x = m[x.l][x.w]
            searched.append(searching[spotLoc])
            searching.pop(spotLoc)
            count = 0
            counting = 0
            if len(searching) == 0:
                searching = newSearching
            else:
                for z in newSearching:
                    for y in searching:
                        if not z.isEqual(y):
                            count = count + 1
                            if y.l == z.l and y.w == z.w and y.he == z.he:
                                print("Something isn't working with equals: ", y.l, y.w, y.he, z.l, z.w, z.he)
                                sys.exit()
                        #print("RRTChecking equals", count, counting, len(searching), len(newSearching), len(searched), (map.l * map.w * map.h))
                    if count == len(searching) and not z.searched and not z.entity:
                        #print("Append: ", len(searching))
                        searching.append(z)
                    """if len(searching) + len(searched) > (map.l * map.w * map.h):
                        print("Error. Too many searching!")
                        sys.exit()"""
                    count = 0
                    counting = counting + 1
                newSearching = []
            found = x.end
        #print(spot.l, spot.w, spot.he, self.endL, self.endW, self.endH)
        m = map.map
        if self.endH != -1:
            x = m[x.l][x.w][x.he]
        else:
            x = m[x.l][x.w]
        print(x.l, x.w, x.he, self.endL, self.endW, self.endH)
        print(x.l, x.w, x.he, self.locL, self.locW, self.locH)
        #print(x.end)
        #print(m[self.endL][self.endW][self.endH].end)
        path = []
        #print(len(path))
        path = x.buildPath(path)
        #print(len(path))
        #for p in path:
        #    print(p.l, p.w, p.he)
        path.pop(-1)
        self.path = path
        self.movable = True
        
    def move(self, map):
        l = len(self.path)
        #print(l)
        x = self.path[l - 1]
        m = map.map
        if self.dim and m[x.l][x.w][x.he].entity == False:
            map.moveEntity(self, self.dim, x.l, x.w, x.he)
            self.locL = x.l
            self.locW = x.w
            self.locH = x.he
            self.checkEnd()
            path = self.path
            path.pop()
            self.path = path
            return self.complete
        elif not self.dim and m[x.l][x.w].entity == False:
            map.moveEntity(self, self.dim, x.l, x.w, x.he)
            self.locL = x.l
            self.locW = x.w
            self.locH = x.he
            self.checkEnd()
            path = self.path
            path.pop()
            self.path = path
            return self.complete
        else:
            self.movable = False
            return self.complete
    
    def checkEnd(self):
        if self.endL == self.locL and self.endW == self.locW and self.endH == self.locH:
            print("Fin")
            self.complete = True
        
    def sim(self, map):
        start = time.time()
        print("RRT")
        x = None
        m = map.map
        found = False
        newSearching = []
        if self.endH != -1:
            searching = [m[self.locL][self.locW][self.locH]]
        else:
            searching = [m[self.locL][self.locW]]
        searched = []
        while not found:
            if len(searching) == 1:
                spotLoc = 0
            else:
                spotLoc = random.randint(0, len(searching) - 1)
            x = searching[spotLoc]
            newSearching = map.search(x.l, x.w, x.he)
            m = map.map
            if self.endH != -1:
                x = m[x.l][x.w][x.he]
            else:
                x = m[x.l][x.w]
            searched.append(searching[spotLoc])
            searching.pop(spotLoc)
            count = 0
            counting = 0
            if len(searching) == 0:
                searching = newSearching
            else:
                for z in newSearching:
                    for y in searching:
                        if not z.isEqual(y):
                            count = count + 1
                            if y.l == z.l and y.w == z.w and y.he == z.he:
                                print("Something isn't working with equals: ", y.l, y.w, y.he, z.l, z.w, z.he)
                                sys.exit()
                        #print("RRTChecking equals", count, counting, len(searching), len(newSearching), len(searched), (map.l * map.w * map.h))
                    if count == len(searching) and not z.searched and not z.entity:
                        #print("Append: ", len(searching))
                        searching.append(z)
                    """if len(searching) + len(searched) > (map.l * map.w * map.h):
                        print("Error. Too many searching!")
                        sys.exit()"""
                    count = 0
                    counting = counting + 1
                newSearching = []
            if x.end:
                #print("End at: ", x.l, x.w, x.he)
                found = True
        #print(spot.l, spot.w, spot.he, self.endL, self.endW, self.endH)
        end = time.time()
        m = map.map
        if self.endH != -1:
            x = m[x.l][x.w][x.he]
        else:
            x = m[x.l][x.w]
        bt = x.backTrack()
        return (end - start), x, len(searching) + len(searched), len(searched), bt

class AStar(object):
    def __init__(self, endL, endW, endH, startL, startW, startH):
        self.endL = endL
        self.endW = endW
        self.endH = endH
        self.locL = startL
        self.locW = startW
        self.locH = startH
        self.complete = False
        self.path = []
        self.movable = False
        if endH == -1:
            self.dim = False
        else:
            self.dim = True
        
    def simM(self, map):
        #start = time.time()
        print("A Star", self.locL, self.locW, self.locH)
        m = map.map
        x = None
        found = False
        newSearching = []
        if self.endH != -1:
            searching = [m[self.locL][self.locW][self.locH]]
        else:
            searching = [m[self.locL][self.locW]]
        searched = []
        while not found:
            smallest = (maxSize * side * 2) + (maxSize * edge * 2)
            if self.endH != -1:
                smallest = smallest + (maxSize * corner * 2)
            i = 0
            spotLoc = 0
            for spot in searching:
                if spot.f < smallest:
                    smallest = spot.f
                    spotLoc = i
                i = i + 1
            #print(spotLoc, len(searching))
            x = searching[spotLoc]
            newSearching = map.search(x.l, x.w, x.he)
            k = 0
            while k != -1:
                k = -1
                for j in range(len(newSearching)):
                    if newSearching[j].isEntity():
                        newSearching.pop(j)
                        k = j
                        break
            searched.append(searching[spotLoc])
            searching.pop(spotLoc)
            count = 0
            if len(searching) == 0:
                searching = newSearching
            else:
                for z in newSearching:
                    for y in searching:
                        if not z.isEqual(y):
                            count = count + 1
                            #print("ASChecking equals", count, len(searching), len(newSearching), len(searched))
                    if count == len(searching) and not z.searched and not z.isEntity():
                        #print("Append: ", len(searching))
                        searching.append(z)
                    """if self.endH != -1 and (len(searching) + len(searched) > (map.l * map.w * map.h)):
                        print("Error. Too many searching!")
                        sys.exit()
                    elif len(searching) + len(searched) > (map.l * map.w):
                        print("Error. Too many searching!")
                        sys.exit()"""
                    count = 0
                newSearching = []
            found = x.end
        #print(spot.l, spot.w, spot.he, self.endL, self.endW, self.endH)
        m = map.map
        if self.endH != -1:
            x = m[x.l][x.w][x.he]
        else:
            x = m[x.l][x.w]
        print(x.l, x.w, x.he, self.endL, self.endW, self.endH)
        print(x.l, x.w, x.he, self.locL, self.locW, self.locH)
        #print(x.end)
        #print(m[self.endL][self.endW][self.endH].end)
        path = []
        #print(len(path))
        path = x.buildPath(path)
        #print(len(path))
        #for p in path:
        #    print(p.l, p.w, p.he)
        path.pop(-1)
        self.path = path
        self.movable = True
        
    def move(self, map):
        l = len(self.path)
        #print(l)
        x = self.path[l - 1]
        m = map.map
        if self.dim and m[x.l][x.w][x.he].entity == False:
            map.moveEntity(self, self.dim, x.l, x.w, x.he)
            self.locL = x.l
            self.locW = x.w
            self.locH = x.he
            self.checkEnd()
            path = self.path
            path.pop()
            self.path = path
            return self.complete
        elif not self.dim and m[x.l][x.w].entity == False:
            map.moveEntity(self, self.dim, x.l, x.w, x.he)
            self.locL = x.l
            self.locW = x.w
            self.locH = x.he
            self.checkEnd()
            path = self.path
            path.pop()
            self.path = path
            return self.complete
        else:
            self.movable = False
            return self.complete
    
    def checkEnd(self):
        if self.endL == self.locL and self.endW == self.locW and self.endH == self.locH:
            print("Fin")
            self.complete = True
        
    def sim(self, map):
        start = time.time()
        print("A Star")
        m = map.map
        x = None
        found = False
        newSearching = []
        if self.endH != -1:
            searching = [m[self.locL][self.locW][self.locH]]
        else:
            searching = [m[self.locL][self.locW]]
        searched = []
        while not found:
            smallest = (maxSize * side) + (maxSize * edge)
            if self.endH != -1:
                smallest = smallest + (maxSize * corner)
            i = 0
            spotLoc = 0
            for spot in searching:
                if spot.f < smallest:
                    smallest = spot.f
                    spotLoc = i
                i = i + 1
            x = searching[spotLoc]
            newSearching = map.search(x.l, x.w, x.he)
            searched.append(searching[spotLoc])
            searching.pop(spotLoc)
            count = 0
            if len(searching) == 0:
                searching = newSearching
            else:
                for z in newSearching:
                    for y in searching:
                        if not z.isEqual(y):
                            count = count + 1
                        #print("ASChecking equals", count, len(searching), len(newSearching), len(searched), (map.l * map.w * map.h))
                    if count == len(searching) and not z.searched:
                        #print("Append: ", len(searching))
                        searching.append(z)
                    """if self.endH != -1 and (len(searching) + len(searched) > (map.l * map.w * map.h)):
                        print("Error. Too many searching!")
                        sys.exit()
                    elif len(searching) + len(searched) > (map.l * map.w):
                        print("Error. Too many searching!")
                        sys.exit()"""
                    count = 0
                newSearching = []
            found = x.end
        #print(spot.l, spot.w, spot.he, self.endL, self.endW, self.endH)
        end = time.time()
        m = map.map
        if self.endH != -1:
            x = m[x.l][x.w][x.he]
        else:
            x = m[x.l][x.w]
        bt = x.backTrack()
        return (end - start), x, len(searching) + len(searched), len(searched), bt
        
    def getEnd(self):
        return self.endL, self.endW, self.endH
    
def obsAndSize(l, w, h):
    squares = l * w
    div = 3
    if h != -1:
        squares = squares * h
        div = 2
    obs = squares / div
    return obs, squares
    
def main(argv):
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", action="store_true")
    parser.add_argument("-e")
    parser.add_argument("-l")
    parser.add_argument("-w")
    parser.add_argument("-i")
    args = parser.parse_args()
    dim = bool(args.d)
    #dim = True
    entities = int(args.e)
    length = int(args.l)
    width = int(args.w)
    height = int(args.i)
    
    if entities < 1:
        print("Error. Please input at least 1 entity")
        sys.exit()
    if length < 2:
        print("Error: Please input a length of at least 2")
        sys.exit()
    if width < 2:
        print("Error: Please input a width of at least 2")
        sys.exit()
    if height < 2 and dim == True:
        print("Error: Please input a height of at least 2, or remove the 3D tag")
        sys.exit()
    if dim == False:
        height = -1
    obsMax, squares = obsAndSize(length, width, height)
    
    while squares > maxSize:
        if length > width:
            if height != -1 and height > length:
                height = height - 1
            else:
                length = length - 1
        else:
            if height != -1 and height > width:
                height = height - 1
            else:
                width = width - 1
        obsMax, squares = obsAndSize(length, width, height)
        
    if entities > maxEnt and entities != totalEnt:
        entities = maxEnt
        
    if entities == 1:
        oneEntity(length, width, height, dim)
    elif entities == 6:
        eachEnt(length, width, height, dim)
    else:
        multEntity(length, width, height, dim, entities)
        
def eachEnt(length, width, height, dim):
    
    maps = []
    starts = []
    ends = []
    
    for i in range(tests):
        mapPlot = map(length, width, height)
        endH = -1
        if dim == True:
            endH = random.randint(0, height - 1)
        endL = random.randint(0, length - 1)
        endW = random.randint(0, width - 1)
        startsX = []
        startsY = []
        startsZ = []
        for j in range(totalEnt):
            l = endL
            w = endW
            h = endH
            while l == endL and w == endW and h == endH:
                l = random.randint(0, length - 1)
                w = random.randint(0, width -  1)
                if dim == True:
                    h = random.randint(0, height - 1)
            startsX.append(l)
            startsY.append(w)
            startsZ.append(h)
            mapPlot.setEntity(dim, l, w, h)
        starts.append([startsX, startsY, startsZ])
        ends.append([endL, endW, endH])
        mapPlot.setEnd(endL, endW, endH)
        mapPlot.findG(endL, endW, endH)
        maps.append(mapPlot)
        
    timerArrAS = []
    movesAS = []
    
    timerArrRRT = []
    movesRRT = []
    
    timerArrDijk = []
    movesDijk = []
    
    timerArrBFS = []
    movesBFS = []
    
    timerArrDFS = []
    movesDFS = []
    
    timerArrBest = []
    movesBest = []
    
    for i in range(tests):
        moves = [0 for j in range(totalEnt)]
        timerEnt = [0 for j in range(totalEnt)]
        fullComplete = False
        indComplete = [False for j in range(totalEnt)]
        print("End: ", ends[i][0], ends[i][1], ends[i][2])
        for j in range(totalEnt):
            print("Start", j, ":", starts[i][0][j], starts[i][1][j], starts[i][2][j])
            
        A = AStar(ends[i][0], ends[i][1], ends[i][2], starts[i][0][0], starts[i][1][0], starts[i][2][0])
        
        R = RRT(ends[i][0], ends[i][1], ends[i][2], starts[i][0][1], starts[i][1][1], starts[i][2][1])
        
        D = Dijkstra(ends[i][0], ends[i][1], ends[i][2], starts[i][0][2], starts[i][1][2], starts[i][2][2], maps[i])
        
        B = BFS(ends[i][0], ends[i][1], ends[i][2], starts[i][0][3], starts[i][1][3], starts[i][2][3])
        
        DF = DFS(ends[i][0], ends[i][1], ends[i][2], starts[i][0][4], starts[i][1][4], starts[i][2][4])
        
        Be = BestFS(ends[i][0], ends[i][1], ends[i][2], starts[i][0][5], starts[i][1][5], starts[i][2][5])
        
        while not fullComplete:
            
            start = time.time()
            if not indComplete[0]:
                moves[0] = moves[0] + 1
                tf = False
                if A.movable == False:
                    A.simM(maps[i])
                else:
                    tf = A.move(maps[i])
                maps[i].reset()
                indComplete[0] = tf
                end = time.time()
                t = end - start
                timerEnt[0] = timerEnt[0] + t
                
            start = time.time()
            if not indComplete[1]:
                moves[1] = moves[1] + 1
                tf = False
                if R.movable == False:
                    R.simM(maps[i])
                else:
                    tf = R.move(maps[i])
                maps[i].reset()
                indComplete[1] = tf
                end = time.time()
                t = end - start
                timerEnt[1] = timerEnt[1] + t
                
            start = time.time()
            if not indComplete[2]:
                moves[2] = moves[2] + 1
                tf = False
                if D.movable == False:
                    D.simM(maps[i])
                else:
                    tf = D.move(maps[i])
                maps[i].reset()
                indComplete[2] = tf
                end = time.time()
                t = end - start
                timerEnt[2] = timerEnt[2] + t
                
            start = time.time()
            if not indComplete[3]:
                moves[3] = moves[3] + 1
                tf = False
                if B.movable == False:
                    B.simM(maps[i])
                else:
                    tf = B.move(maps[i])
                maps[i].reset()
                indComplete[3] = tf
                end = time.time()
                t = end - start
                timerEnt[3] = timerEnt[3] + t
                
            start = time.time()
            if not indComplete[4]:
                moves[4] = moves[4] + 1
                tf = False
                if DF.movable == False:
                    DF.simM(maps[i])
                else:
                    tf = DF.move(maps[i])
                maps[i].reset()
                indComplete[4] = tf
                end = time.time()
                t = end - start
                timerEnt[4] = timerEnt[4] + t
                
            start = time.time()
            if not indComplete[5]:
                moves[5] = moves[5] + 1
                tf = False
                if Be.movable == False:
                    Be.simM(maps[i])
                else:
                    tf = Be.move(maps[i])
                maps[i].reset()
                indComplete[5] = tf
                end = time.time()
                t = end - start
                timerEnt[5] = timerEnt[5] + t
                
            for j in range(totalEnt):
                if j == 0:
                    fullComplete = indComplete[j]
                else:
                    fullComplete = fullComplete and indComplete[j]
                
        timerArrAS.append(timerEnt[0])
        movesAS.append(moves[0])
        timerArrRRT.append(timerEnt[1])
        movesRRT.append(moves[1])
        timerArrDijk.append(timerEnt[2])
        movesDijk.append(moves[2])
        timerArrBFS.append(timerEnt[3])
        movesBFS.append(moves[3])
        timerArrDFS.append(timerEnt[4])
        movesDFS.append(moves[4])
        timerArrBest.append(timerEnt[5])
        movesBest.append(moves[5])
        
    names = ['AStar', 'RRT', 'Dijkstra', 'BFS', 'DSF', 'Best']
    timerAvg = [average(timerArrAS), average(timerArrRRT), average(timerArrDijk), average(timerArrBFS), average(timerArrDFS), average(timerArrBest)]
    movesAvg = [average(movesAS), average(movesRRT), average(movesDijk), average(movesBFS), average(movesDFS), average(movesBest)]

    plot.title('Time Averages')
    plot.bar(names, timerAvg)
    plot.show()
    plot.title('Moves Made')
    plot.bar(names, movesAvg)
    plot.show()
        
def multEntity(length, width, height, dim, ent):
    
    maps = []
    starts = []
    ends = []
    
    for i in range(tests):
        mapPlot = map(length, width, height)
        endH = -1
        if dim == True:
            endH = random.randint(0, height - 1)
        endL = random.randint(0, length - 1)
        endW = random.randint(0, width - 1)
        startsX = []
        startsY = []
        startsZ = []
        for j in range(ent):
            l = endL
            w = endW
            h = endH
            while l == endL and w == endW and h == endH:
                l = random.randint(0, length - 1)
                w = random.randint(0, width -  1)
                if dim == True:
                    h = random.randint(0, height - 1)
            startsX.append(l)
            startsY.append(w)
            startsZ.append(h)
            mapPlot.setEntity(dim, l, w, h)
        starts.append([startsX, startsY, startsZ])
        ends.append([endL, endW, endH])
        mapPlot.setEnd(endL, endW, endH)
        mapPlot.findG(endL, endW, endH)
        maps.append(mapPlot)
        
    timerArrAS = []
    movesAS = []
    
    timerArrRRT = []
    movesRRT = []
    
    timerArrDijk = []
    movesDijk = []
    
    timerArrBFS = []
    movesBFS = []
    
    timerArrDFS = []
    movesDFS = []
    
    timerArrBest = []
    movesBest = []
    
    for i in range(tests):
        ASEnt = []
        moves = 0
        timerEnt = [0 for j in range(ent)]
        fullComplete = False
        indComplete = [False for j in range(ent)]
        print("End:", ends[i][0], ends[i][1], ends[i][2])
        for j in range(ent):
            print("Start", j, ":", starts[i][0][j], starts[i][1][j], starts[i][2][j])
        for j in range(ent):
            ASEnt.append(AStar(ends[i][0], ends[i][1], ends[i][2], starts[i][0][j], starts[i][1][j], starts[i][2][j]))
            #print(ASEnt[j].endL, ASEnt[j].endW, ASEnt[j].endH)
        
        while fullComplete == False:
                
            for j in range(ent):
                start = time.time()
                if not indComplete[j]:
                    moves = moves + 1
                    tf = False
                    #print(moves)
                    if ASEnt[j].movable == False:
                        ASEnt[j].simM(maps[i])
                    else:
                        tf = ASEnt[j].move(maps[i])
                    maps[i].reset()
                    indComplete[j] = tf
                    end = time.time()
                    t = end - start
                    timerEnt[j] = timerEnt[j] + t
                
            for j in range(ent):
                if j == 0:
                    fullComplete = indComplete[j]
                else:
                    fullComplete = fullComplete and indComplete[j]
        
        timerArrAS.append(timerEnt)
        movesAS.append(moves)
        fullComplete = False
        indComplete = [False for j in range(ent)]
        maps[i].fullReset()
        for j in range(ent):
            maps[i].setEntity(dim, starts[i][0][j], starts[i][1][j], starts[i][2][j])
        
        RRTEnt = []
        moves = 0
        timerEnt = [0 for j in range(ent)]
        
        for j in range(ent):
            RRTEnt.append(RRT(ends[i][0], ends[i][1], ends[i][2], starts[i][0][j], starts[i][1][j], starts[i][2][j]))
        
        while fullComplete == False:
                
            for j in range(ent):
                start = time.time()
                if not indComplete[j]:
                    moves = moves + 1
                    tf = False
                    #print(moves)
                    if RRTEnt[j].movable == False:
                        RRTEnt[j].simM(maps[i])
                    else:
                        tf = RRTEnt[j].move(maps[i])
                    maps[i].reset()
                    indComplete[j] = tf
                    end = time.time()
                    t = end - start
                    timerEnt[j] = timerEnt[j] + t
                
            for j in range(ent):
                if j == 0:
                    fullComplete = indComplete[j]
                else:
                    fullComplete = fullComplete and indComplete[j]
        
        timerArrRRT.append(timerEnt)
        movesRRT.append(moves)
        
        fullComplete = False
        indComplete = [False for j in range(ent)]
        maps[i].fullReset()
        for j in range(ent):
            maps[i].setEntity(dim, starts[i][0][j], starts[i][1][j], starts[i][2][j])
            
        DijkEnt = []
        moves = 0
        timerEnt = [0 for j in range(ent)]
        
        for j in range(ent):
            DijkEnt.append(Dijkstra(ends[i][0], ends[i][1], ends[i][2], starts[i][0][j], starts[i][1][j], starts[i][2][j], maps[i]))
        
        while not fullComplete:
            
            for j in range(ent):
                start = time.time()
                if not indComplete[j]:
                    moves = moves + 1
                    tf = False
                    #print(moves)
                    if DijkEnt[j].movable == False:
                        DijkEnt[j].simM(maps[i])
                    else:
                        tf = DijkEnt[j].move(maps[i])
                    maps[i].reset()
                    indComplete[j] = tf
                    end = time.time()
                    t = end - start
                    timerEnt[j] = timerEnt[j] + t
                
            for j in range(ent):
                if j == 0:
                    fullComplete = indComplete[j]
                else:
                    fullComplete = fullComplete and indComplete[j]
                    
        timerArrDijk.append(timerEnt)
        movesDijk.append(moves)
        fullComplete = False
        indComplete = [False for j in range(ent)]
        maps[i].fullReset()
        for j in range(ent):
            maps[i].setEntity(dim, starts[i][0][j], starts[i][1][j], starts[i][2][j])
            
        BFSEnt = []
        moves = 0
        timerEnt = [0 for j in range(ent)]
        
        for j in range(ent):
            BFSEnt.append(BFS(ends[i][0], ends[i][1], ends[i][2], starts[i][0][j], starts[i][1][j], starts[i][2][j]))
        
        while not fullComplete:
        
            for j in range(ent):
                start = time.time()
                if not indComplete[j]:
                    moves = moves + 1
                    tf = False
                    #print(moves)
                    if BFSEnt[j].movable == False:
                        BFSEnt[j].simM(maps[i])
                    else:
                        tf = BFSEnt[j].move(maps[i])
                    maps[i].reset()
                    indComplete[j] = tf
                    end = time.time()
                    t = end - start
                    timerEnt[j] = timerEnt[j] + t
                
            for j in range(ent):
                if j == 0:
                    fullComplete = indComplete[j]
                else:
                    fullComplete = fullComplete and indComplete[j]
        
        timerArrBFS.append(timerEnt)
        movesBFS.append(moves)
        fullComplete = False
        indComplete = [False for j in range(ent)]
        maps[i].fullReset()
        for j in range(ent):
            maps[i].setEntity(dim, starts[i][0][j], starts[i][1][j], starts[i][2][j])
        
        DFSEnt = []
        moves = 0
        timerEnt = [0 for j in range(ent)]
        
        for j in range(ent):
            DFSEnt.append(DFS(ends[i][0], ends[i][1], ends[i][2], starts[i][0][j], starts[i][1][j], starts[i][2][j]))
        
        while not fullComplete:
            for j in range(ent):
                start = time.time()
                if not indComplete[j]:
                    moves = moves + 1
                    tf = False
                    #print(moves)
                    if DFSEnt[j].movable == False:
                        DFSEnt[j].simM(maps[i])
                    tf = DFSEnt[j].move(maps[i])
                    maps[i].reset()
                    indComplete[j] = tf
                    end = time.time()
                    t = end - start
                    timerEnt[j] = timerEnt[j] + t
                
            for j in range(ent):
                if j == 0:
                    fullComplete = indComplete[j]
                else:
                    fullComplete = fullComplete and indComplete[j]
        
        timerArrDFS.append(timerEnt)
        movesDFS.append(moves)
        fullComplete = False
        indComplete = [False for j in range(ent)]
        maps[i].fullReset()
        
        for j in range(ent):
            maps[i].setEntity(dim, starts[i][0][j], starts[i][1][j], starts[i][2][j])
            
        BestEnt = []
        moves = 0
        timerEnt =  [0 for j in range(ent)]
        
        for j in range(ent):
            BestEnt.append(BestFS(ends[i][0], ends[i][1], ends[i][2], starts[i][0][j], starts[i][1][j], starts[i][2][j]))
            
        while not fullComplete:
            for j in range(ent):
                start = time.time()
                if not indComplete[j]:
                    moves = moves + 1
                    tf = False
                    #print(moves)
                    if BestEnt[j].movable == False:
                        BestEnt[j].simM(maps[i])
                    else:
                        tf = BestEnt[j].move(maps[i])
                    maps[i].reset()
                    indComplete[j] = tf
                    end = time.time()
                    t = end - start
                    timerEnt[j] = timerEnt[j] + t
                
            for j in range(ent):
                if j == 0:
                    fullComplete = indComplete[j]
                else:
                    fullComplete = fullComplete and indComplete[j]
            
        timerArrBest.append(timerEnt)
        movesBest.append(moves)
        fullComplete = False
        indComplete = [False for j in range(ent)]
        maps[i].fullReset()
        
        for j in range(ent):
            maps[i].setEntity(dim, starts[i][0][j], starts[i][1][j], starts[i][2][j])
        
        print(i)
        
    names = ['AStar', 'RRT', 'Dijkstra', 'BFS', 'DSF', 'Best']
    timerAvgAS = [average(i) for i in timerArrAS]
    timerAvgRRT = [average(i) for i in timerArrRRT]
    timerAvgDijk = [average(i) for i in timerArrDijk]
    timerAvgBFS = [average(i) for i in timerArrBFS]
    timerAvgDFS = [average(i) for i in timerArrDFS]
    timerAvgBest = [average(i) for i in timerArrBest]
    
    movesAvg = [average(movesAS), average(movesRRT), average(movesDijk), average(movesBFS), average(movesDFS), average(movesBest)]
    timerAvg = [average(timerAvgAS), average(timerAvgRRT), average(timerAvgDijk), average(timerAvgBFS), average(timerAvgDFS), average(timerAvgBest)]
    
    plot.title('Time Averages')
    plot.bar(names, timerAvg)
    plot.show()
    plot.title('Average Moves Made')
    plot.bar(names, movesAvg)
    plot.show()
    
    tTime = 0
    for i in timerArrAS:
        for j in i:
            tTime = tTime + j
            
    for i in timerArrRRT:
        for j in i:
            tTime = tTime + j
            
    for i in timerArrDijk:
        for j in i:
            tTime = tTime + j
            
    for i in timerArrBFS:
        for j in i:
            tTime = tTime + j
            
    for i in timerArrDFS:
        for j in i:
            tTime = tTime + j
    
    for i in timerArrBest:
        for j in i:
            tTime = tTime + j
            
    print(tTime)
        
def oneEntity(length, width, height, dim):

    maps = []
    starts = []
    ends = []    

    for i in range(tests):
        mapPlot = map(length, width, height)
        el = random.randint(0, length - 1)
        ew = random.randint(0, width - 1)
        endH = -1
        eh = -1
        if dim == True:
            eh = random.randint(0, height - 1)
            endH = eh
        endL = el
        endW = ew
            
        while el == endL and ew == endW:
            if dim == True and endH == eh:
                endH = random.randint(0, height - 1)
            endL = random.randint(0, length - 1)
            endW = random.randint(0, width - 1)
        starts.append([el, ew, eh])
        ends.append ([endL, endW, endH])   
        mapPlot.setEnd(endL, endW, endH)
        mapPlot.findG(endL, endW, endH)
        maps.append(mapPlot)
    
    timerArrAS = []
    discoverAS = []
    searchAS = []
    pathAS = []
    
    timerArrRRT = []
    discoverRRT = []
    searchRRT = []
    pathRRT = []
    
    timerArrDijk = []
    discoverDijk = []
    searchDijk = []
    pathDijk = []
    
    timerArrBFS = []
    discoverBFS = []
    searchBFS = []
    pathBFS = []
    
    timerArrDFS = []
    discoverDFS = []
    searchDFS = []
    pathDFS = []
    
    timerArrBest = []
    discoverBest = []
    searchBest = []
    pathBest = []
    
    for i in range(tests):
        
        print(starts[i][0], starts[i][1], starts[i][2], ends[i][0], ends[i][1], ends[i][2])
        print()
        print()
        print()
    
        eAS = AStar(ends[i][0], ends[i][1], ends[i][2], starts[i][0], starts[i][1], starts[i][2])
        timerAS, endSquareAS, spotFoundAS, spotSearchedAS, btAS = eAS.sim(maps[i])
        print(endSquareAS.l, endSquareAS.w, endSquareAS.he)
        print(timerAS)
        print(spotFoundAS, spotSearchedAS, btAS)
        timerArrAS.append(timerAS)
        discoverAS.append(spotFoundAS)
        searchAS.append(spotSearchedAS)
        pathAS.append(btAS)
        maps[i].reset()
        print()
    
        rrt = RRT(ends[i][0], ends[i][1], ends[i][2], starts[i][0], starts[i][1], starts[i][2])
        timerRRT, endSquareRRT, spotFoundRRT, spotSearchedRRT, btRRT = rrt.sim(maps[i])
        print(timerRRT)
        print(spotFoundRRT, spotSearchedRRT, btRRT)
        timerArrRRT.append(timerRRT)
        discoverRRT.append(spotFoundRRT)
        searchRRT.append(spotSearchedRRT)
        pathRRT.append(btRRT)
        maps[i].reset()
        print()
        
        dijk = Dijkstra(ends[i][0], ends[i][1], ends[i][2], starts[i][0], starts[i][1], starts[i][2], maps[i])
        timerDijk, endSquareDijk, spotFoundDijk, spotSearchedDijk, btDijk = dijk.sim(maps[i])
        print(timerDijk)
        print(spotFoundDijk, spotSearchedDijk, btDijk)
        timerArrDijk.append(timerDijk)
        discoverDijk.append(spotFoundDijk)
        searchDijk.append(spotSearchedDijk)
        pathDijk.append(btDijk)
        maps[i].reset()
        print()
    
        bfs = BFS(ends[i][0], ends[i][1], ends[i][2], starts[i][0], starts[i][1], starts[i][2])
        timerBFS, endSquareBFS, spotFoundBFS, spotSearchedBFS, btBFS = bfs.sim(maps[i])
        print(timerBFS)
        print(spotFoundBFS, spotSearchedBFS, btBFS)
        timerArrBFS.append(timerBFS)
        discoverBFS.append(spotFoundBFS)
        searchBFS.append(spotSearchedBFS)
        pathBFS.append(btBFS)
        maps[i].reset()
        print()
    
        dfs = DFS(ends[i][0], ends[i][1], ends[i][2], starts[i][0], starts[i][1], starts[i][2])
        timerDFS, endSquareDFS, spotFoundDFS, spotSearchedDFS, btDFS = dfs.sim(maps[i])
        print(timerDFS)
        print(spotFoundDFS, spotSearchedDFS, btDFS)
        timerArrDFS.append(timerDFS)
        discoverDFS.append(spotFoundDFS)
        searchDFS.append(spotSearchedDFS)
        pathDFS.append(btDFS)
        maps[i].reset()
        print()
    
        maps[i].findG(ends[i][0], ends[i][1], ends[i][2])
        best = BestFS(ends[i][0], ends[i][1], ends[i][2], starts[i][0], starts[i][1], starts[i][2])
        timerBest, endSquareBest, spotFoundBest, spotSearchedBest, btBest = best.sim(maps[i])
        print(timerBest)
        print(spotFoundBest, spotSearchedBest, btBest)
        timerArrBest.append(timerBest)
        discoverBest.append(spotFoundBest)
        searchBest.append(spotSearchedBest)
        pathBest.append(btBest)
        print()
        
    names = ['AStar', 'RRT', 'Dijkstra', 'BFS', 'DSF', 'Best']
    timerAvg = [average(timerArrAS), average(timerArrRRT), average(timerArrDijk), average(timerArrBFS), average(timerArrDFS), average(timerArrBest)]
    discoverAvg = [average(discoverAS), average(discoverRRT), average(discoverDijk), average(discoverBFS), average(discoverDFS), average(discoverBest)]
    searchAvg = [average(searchAS), average(searchRRT), average(searchDijk), average(searchBFS), average(searchDFS), average(searchBest)]
    pathAvg = [average(pathAS), average(pathRRT), average(pathDijk), average(pathBFS), average(pathDFS), average(pathBest)]

    plot.title('Time Averages')
    plot.bar(names, timerAvg)
    plot.show()
    plot.title('Sectors Uncovered')
    plot.bar(names, discoverAvg)
    plot.show()
    plot.title('Sectors Searched')
    plot.bar(names, searchAvg)
    plot.show()
    plot.title('Path Length')
    plot.bar(names, pathAvg)
    plot.show()
    
    sim = []
    for i in range(tests):
        sim.append(i + 1)
    plot.title('Time Per Simulation')
    plot.plot(sim, timerArrAS, 'xkcd:cyan', sim, timerArrRRT, 'xkcd:lightgreen', sim, timerArrDijk, 'xkcd:azure', sim, timerArrBFS, 'xkcd:coral', sim, timerArrDFS, 'xkcd:fuchsia', sim, timerArrBest, 'xkcd:violet')
    plot.legend(names)
    plot.show()
    
    plot.title('Sectors Discovered Per Simulation')
    plot.plot(sim, discoverAS, 'xkcd:cyan', sim, discoverRRT, 'xkcd:lightgreen', sim, discoverDijk, 'xkcd:azure', sim, discoverBFS, 'xkcd:coral', sim, discoverDFS, 'xkcd:fuchsia', sim, discoverBest, 'xkcd:violet')
    plot.legend(names)
    plot.show()
    
    plot.title('Sectors Seached Per Simulation')
    plot.plot(sim, searchAS, 'xkcd:cyan', sim, searchRRT, 'xkcd:lightgreen', sim, searchDijk, 'xkcd:azure', sim, searchBFS, 'xkcd:coral', sim, searchDFS, 'xkcd:fuchsia', sim, searchBest, 'xkcd:violet')
    plot.legend(names)
    plot.show()
    
    plot.title('Path Length Per Simulation')
    plot.plot(sim, pathAS, 'xkcd:cyan', sim, pathRRT, 'xkcd:lightgreen', sim, pathDijk, 'xkcd:azure', sim, pathBFS, 'xkcd:coral', sim, pathDFS, 'xkcd:fuchsia', sim, pathBest, 'xkcd:violet')
    plot.legend(names)
    plot.show()
    
def average(list):
    holder = 0
    for x in list:
        holder = holder + x
    holder = holder / len(list)
    return holder
    
if __name__ == "__main__":
    main(sys.argv[1:])