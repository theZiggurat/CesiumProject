import math

HEIGHTMAP_WIDTH = 512
METERS_PER_PIXEL = 30
METERS_PER_HEIGHT = 11

def main():

    pre_heightmap = open("assets/pre.data", "rb").read()
    post_heightmap = open("assets/post.data", "rb").read()

    while True:

        # initial error handling and argument parsing
        args1 = [x.strip() for x in input('Enter coordinates of first point (x, y): ').split(',')]
        if len(args1) != 2:
            print("Please enter two numbers seperated by comma")
            continue
        x1 = int(args1[0])
        y1 = int(args1[1])
        if x1 > HEIGHTMAP_WIDTH or y1 > HEIGHTMAP_WIDTH or x1 < 0 or y1 < 0:
            print("X and Y values must be between 0 and ", HEIGHTMAP_WIDTH)
            continue

        while True:
            args2 = [x.strip() for x in input('Enter coordinates of second point (x, y): ').split(',')]
            if len(args2) != 2:
                print("Please enter two numbers seperated by comma")
                continue
            x2 = int(args2[0])
            y2 = int(args2[1])
            if x2 > HEIGHTMAP_WIDTH or y2 > HEIGHTMAP_WIDTH or x2 < 0 or y2 < 0:
                print("X and Y values must be between 0 and ", HEIGHTMAP_WIDTH)
                continue
            break

        # actual computation

        # first step: gather all points where path intersects traingle boundaries
        # using normalized space where distance between vertices is 1 unit
        intersection_list = calc_intersection_points((x1, y1), (x2, y2))

        # second step: calculate actual distance using heightmap and given units
        pre_dist = compute_surface_distance(intersection_list, pre_heightmap)
        post_dist = compute_surface_distance(intersection_list, post_heightmap)


        # show results to user and allow them to enter another point pair or quit
        print("Distance between points in Mount St. Helens pre-eruption: ", pre_dist, " meters")
        print("Distance between points in Mount St. Helens post-eruption: ", post_dist, " meters")
        print("Difference between two distances: ", (post_dist - pre_dist), " meters")

        quit = input("Quit? (y, n): ").strip().lower()
        if quit == 'y':
            break


def calc_intersection_points(loc_start, loc_end):
    intersections = []
    x1, y1 = loc_start
    x2, y2 = loc_end

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

    # remove duplicates and sort intersections
    intersections = list(set(intersections))
    ret = []
    ret.append(loc_start)
    closest_loc = loc_start
    while len(intersections) > 0:
        best_dist = 740
        for curr_loc in intersections:
            dist = distance2(curr_loc, loc_start)
            if dist < best_dist:
                closest_loc = curr_loc
                best_dist = dist
        intersections.remove(closest_loc)
        ret.append(closest_loc)
    ret.append(loc_end)
    return ret

def compute_surface_distance(intersections, heightmap):

    distance_sum = 0
    for i in range(0, len(intersections) - 1):
        height1 = height_at(intersections[i], heightmap)
        height2 = height_at(intersections[i+1], heightmap)

        x1, y1 = intersections[i]
        x2, y2 = intersections[i+1]
        scaled_loc1 = mul3(x1, METERS_PER_PIXEL, y1, METERS_PER_PIXEL, height1, METERS_PER_HEIGHT)
        scaled_loc2 = mul3(x2, METERS_PER_PIXEL, y2, METERS_PER_PIXEL, height2, METERS_PER_HEIGHT)
        distance_sum += distance3(scaled_loc2, scaled_loc1)

    return distance_sum


def height_at(loc, heightmap):

    x, y = loc
    x_fract, x_int = math.modf(x)
    y_fract, y_int = math.modf(y)
    x_int = int(x_int)
    y_int = int(y_int)
    
    # on corner
    if x_fract == 0 and y_fract == 0:
        return heightmap[x_int + y_int * HEIGHTMAP_WIDTH]
    # on vertical line
    elif x_fract == 0:
        h1 = heightmap[x_int + y_int * HEIGHTMAP_WIDTH]
        h2 = heightmap[x_int + (y_int+1) * HEIGHTMAP_WIDTH]
        return (h1 * (1 - y_fract)) + (h2 * y_fract)
    # on horizontal line
    elif y_fract == 0:
        h1 = heightmap[x_int + y_int * HEIGHTMAP_WIDTH]
        h2 = heightmap[(x_int+1) + y_int * HEIGHTMAP_WIDTH]
        return (h1 * (1 - x_fract)) + (h2 * x_fract)
    # on diagonal line
    else:
        h1 = heightmap[(x_int+1) + y_int * HEIGHTMAP_WIDTH]
        h2 = heightmap[x_int + (y_int+1) * HEIGHTMAP_WIDTH]
        dist_top_right = distance2((1, 0), (x_fract, y_fract)) / math.sqrt(2)
        dist_bottom_left = distance2((0, 1), (x_fract, y_fract)) / math.sqrt(2)
        return (h1 * dist_top_right) + (h2 * dist_bottom_left)


def distance2(loc1, loc2):
    return ((((loc2[0] - loc1[0]) **2) + ((loc2[1] - loc1[1]) **2)) **0.5)

def distance3(loc1, loc2):
    return ((((loc2[0] - loc1[0]) **2) + ((loc2[1] - loc1[1]) **2) + ((loc2[2] - loc1[2]) **2)) **0.5)

def mul3(x1, x2, y1, y2, z1, z2):
    return (x1 * x2, y1 * y2, z1 * z2)

if __name__ == "__main__":
    main()