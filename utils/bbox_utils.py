# This function calculates the center point of a bounding box.
# The bounding box is defined by its corners (x1, y1) and (x2, y2).
# The center is found by averaging the x-coordinates and y-coordinates of the corners.
def get_center_of_bbox(bbox):
    x1, y1, x2, y2 = bbox
    return int((x1 + x2) / 2), int((y1 + y2) / 2)

# This function calculates the width of a bounding box.
# The width is determined by subtracting the x-coordinate of the left corner (x1) from the x-coordinate of 
# the right corner (x2).
def get_bbox_width(bbox):
    return bbox[2] - bbox[0]

# This function measures the Euclidean distance between two points p1 and p2.
# The distance is calculated using the Pythagorean theorem: 
# sqrt((x2 - x1)^2 + (y2 - y1)^2)
def measure_distance(p1, p2):
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5

# This function measures the distance between two points p1 and p2 separately along the x and y axes.
# It returns a tuple containing the differences in the x and y coordinates.
def measure_xy_distance(p1, p2):
    return p1[0] - p2[0], p1[1] - p2[1]

# This function calculates the foot position of an object within a bounding box.
# The foot position is considered to be the point at the bottom center of the bounding box.
# The x-coordinate of the foot position is the midpoint of the bottom edge,
# and the y-coordinate is the y-value of the bottom edge.
def get_foot_position(bbox):
    x1, y1, x2, y2 = bbox
    return int((x1 + x2) / 2), int(y2)
