from PIL import Image, ImageDraw

class Map:
#creating a class for the map itself
    def __init__(self, filename):
        self.elevations = [] 
        #creating the empty list for elevations
        with open(filename) as file:
            for line in file:
                self.elevations.append([int(e) for e in line.split()])
 #inputting the elevation altitudes into the empty list
        self.maximum_elevation = max([max(row) for row in self.elevations])
        self.minimum_elevation = min([min(row) for row in self.elevations])
#finding the minimum and the maximum elevations 
    def elevation(self, x, y):
        return self.elevations[y][x]
#finding the x and y coordinates for the map
    def find_color(self, x, y): 
        return int((self.elevation(x, y) - self.minimum_elevation) / (self.maximum_elevation - self.minimum_elevation) * 255)
#finding the correct numerical value to assign them to colors
class DrawMap:
#creating a class for actually showing the colors and making the picture of the map
    def __init__(self, Map, point):
        self.Map = Map
        self.picture = Image.new('RGBA', (len(self.Map.elevations[0]), len(self.Map.elevations)))
        self.point = point
#using "point" in order to find the starting point to create the line in map
    def draw(self):
        for x in range(len(self.Map.elevations[0])):
            for y in range(len(self.Map.elevations)):
                self.picture.putpixel((x, y), (self.Map.find_color(x, y), self.Map.find_color(x, y), self.Map.color(x, y)))
        self.picture.save('map.png')

    def print_path(self, point):
        for item_point in point:
            self.picture.putpixel(item_point, (156, 226, 227))
        self.picture.save('aaronsmap.png')
        return self.picture

class Pathfinder:

    def __init__(self, Map):
        self.Map = Map

    def pathfinder_finalized(self):
        self.point = []
        cur_x = 0
        cur_y = 50
        while cur_x < len(self.Map.elevations[0]) - 1:
            possible_ys = [cur_y]
            if cur_y - 1 >= 0:
                possible_ys.append(cur_y - 1)
            if cur_y + 1 < len(self.Map.elevations):
                possible_ys.append(cur_y + 1)

            diffs = [
                abs(self.Map.elevations[poss_y][cur_x + 1] - self.Map.elevations[cur_y][cur_x])
                for poss_y in possible_ys
            ]

            min_diff = min(diffs)
            min_diff_index = diffs.index(min_diff)
            next_y = possible_ys[min_diff_index]

            cur_x += 1
            cur_y = next_y
            self.point.append((cur_x, cur_y))
        return self.point


if __name__ == '__main__':

    elevation_map = Map('elevation_small.txt')
    point = Pathfinder(elevation_map)
    draw_elevation_map = DrawMap(elevation_map, point.pathfinder_finalized())
    draw_elevation_map.draw()
    draw_elevation_map.print_path(point.pathfinder_finalized())
    pathfinder = Pathfinder(elevation_map)