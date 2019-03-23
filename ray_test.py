import math
import numpy as np

def get_magnitude(direction, origin):
    mag = math.sqrt((direction[0] - origin[0])**2 + (direction[1] - origin[1])**2 + (direction[2] - origin[2])**2)
    return mag

def get_vector(origin, direction):
    vector = list(np.asarray(origin) - np.asarray(direction)) 
    # print(vector)
    return vector

def get_normal(magnitude, origin, direction):
    ray = get_vector(origin, direction)
    magnitude = get_magnitude(direction, origin)
    vector_normal = [ray[0]/magnitude, ray[1]/magnitude, ray[2]/magnitude]
    # print(vector_normal)

def get_normal_v2(ray):
    vector_normal = np.linalg.norm(ray)
    ray = ray / vector_normal
    # print(ray)
    return ray


origin = [0,0,0]
direction = [3,9,7]
magnitude = 2


# get_magnitude(direction, origin)
# get_vector(origin, direction)
get_normal(magnitude, origin, direction)
get_normal_v2(get_vector(origin, direction))
