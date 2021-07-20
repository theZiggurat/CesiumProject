import math
from decimal import Decimal
from enum import Enum
from os import DirEntry

import matplotlib.pyplot as plt

HEIGHTMAP_WIDTH = 512
METERS_PER_PIXEL = 30
METERS_PER_HEIGHT = 11

def main():

    print("Reading data files...")
    pre = open("assets/pre.data", "rb").read()
    post = open("assets/post.data", "rb").read()

    while True:

        # initial error handling and argument parsing
        args1 = [x.strip() for x in input('Enter coordinates of first point (x, y): ').split(',')]
        if len(args1) != 2:
            print("Please enter two numbers seperated by comma")
            continue
        x1 = int(args1[0])
        y1 = int(args1[1])
        if x1 > HEIGHTMAP_WIDTH or y1 > HEIGHTMAP_WIDTH:
            print("X and Y values must be below {}".format(HEIGHTMAP_WIDTH))
            continue

        while True:
            args2 = [x.strip() for x in input('Enter coordinates of second point (x, y): ').split(',')]
            if len(args2) != 2:
                print("Please enter two numbers seperated by comma")
                continue
            x2 = int(args2[0])
            y2 = int(args2[1])
            if x2 > HEIGHTMAP_WIDTH or y2 > HEIGHTMAP_WIDTH:
                print("X and Y values must be below {}".format(HEIGHTMAP_WIDTH))
                continue
            break

        # actual computation

        # first step: gather all points where path intersects traingle boundaries
        # using normalized space where distance between vertices is 1 unit
        intersection_list = calc_intersection_points((x1, y1), (x2, y2))

        # second step: calculate actual distance with heightmap and given units
        

        # termination handle
        quit = input("Quit? (y, n): ").strip().lower()
        if quit == 'y':
            break


def calc_intersection_points(loc1, loc2):
        intersections = []
        x1, y1 = loc1
        x2, y2 = loc2

        # vertical intersections
        if x2 != x1:
            r = range(x1, x2)
            if x2 < x1:
                r = reversed(range(x2, x1))
            m = (y2 - y1)/(x2 - x1)
            for h in r:
                dist = h - x1
                
                if dist != 0:
                    y_offset = dist * m
                    intersections.append((h, y1 + y_offset))

        # horizontal intersections
        if y2 != y1:
            r = range(y1, y2)
            if y2 < y1:
                r = reversed(range(y2, y1))
            m = (x2 - x1)/(y2 - y1)
            for h in r:
                dist = h - y1
                if dist != 0:
                    x_offset = dist * m
                    intersections.append((x1 + x_offset, h))

        # diagonal intersections
        if y2 != y1 and x2 != x1:
            distx = x2 - x1
            disty = y2 - y1
            m = (y2 - y1)/(x2 - x1)
            if m != -1:
                if x1 < x2:
                    h = x1
                    lim = x2
                else:
                    h = x2
                    lim = x1
                while True:
                    h += 1
                    b = y1 + h
                    b_line = y1 - m * x1
                    x_intersect = (b - b_line) / (m + 1)
                    y_intersect = x_intersect * m + b_line
                    if x_intersect >= lim:
                        break
                    intersections.append((x_intersect, y_intersect))

        # quick and dirty duplicate removal
        intersections = list(set(intersections))

        #print(intersections)

        # lazy intersection sort
        ret = []
        ret.append(loc1)
        closest_loc = loc1
        while len(intersections) > 0:
            best_dist = 740
            for loc in intersections:
                dist = distance(loc[0], loc1[0], loc[1], loc1[1])
                if dist < best_dist:
                    closest_loc = loc
                    best_dist = dist
            intersections.remove(closest_loc)
            ret.append(closest_loc)

        ret.append(loc2)
        return ret


def distance(x1, x2, y1, y2):
    return ((((x2 - x1 ) **2) + ((y2 - y1) **2)) **0.5)

if __name__ == "__main__":
    main()