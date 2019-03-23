from PIL import Image, ImageDraw
import math
import numpy as np
import ray_test as rt


class Sphere():
    def __init__(self, center, radius, color):    # Position at center of sphere
        self.center = center
        self.radius = radius
        self.color = color
    
    def get_center(self):
        return self.center
    
    def get_radius(self):
        return self.radius

    def get_color(self):
        return self.color

    
#   Image plane location
# class Plane():
#     def __init__(self, position, normal_vector, color):
#         self.position = position
#         self.normal_vector = normal_vector

    
#   Create ray from camera through image plane
class Ray():
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction
    
    def get_origin(self):
        return self.origin
    
    def get_direction(self):
        return self.direction

    def get_vector(self):
        return list(np.asarray(self.direction) - np.asarray(self.origin))


#   Find if ray intersects with sphere and return distance along the ray
#   return 1st point on ray that is {radius} distance from sphere.position 
#   Computation Ref: https://www.scratchapixel.com/lessons/3d-basic-rendering/minimal-ray-tracer-rendering-simple-shapes/ray-sphere-intersection
def intersection(ray, obj):  # Ray is from camera origin to current pixel in render
    dist_origin_to_center = get_magnitude(ray.get_origin(), obj.get_center())   # |L|
    vect_origin_to_center = list(np.asarray(sphere.get_center()) - np.asarray(ray.get_origin()))    #  L (vector)
    ray_magnitude = get_magnitude(ray.get_origin(), ray.get_direction())   # Magnitude of ray from origin through current pixel
    ray_vector_normal = ray.get_vector() / np.linalg.norm(ray.get_vector()) # D

    # Projection of dist_origin_to_center onto normalized ray
    projection = np.dot(ray_vector_normal, vect_origin_to_center)   # t_ca

    dist_center_to_ray = math.sqrt(dist_origin_to_center**2 - projection**2)    # d

    if dist_center_to_ray > obj.get_radius():
        return (255,255,255) 

    side = math.sqrt(obj.radius**2 - dist_center_to_ray**2)    # t_hc. Needed to computate distance from origin to intersection


    dist_intersect = projection - side  # t_0

    # Verified format and calculation as correct using python interpreter (P)
    hit_point = list(np.asarray(ray.get_origin()) + list(np.asarray(ray_vector_normal) * dist_intersect))   # P
    hit_normal = rt.get_normal_v2(rt.get_vector(obj.get_center(), hit_point))   # N

    return get_color(hit_normal, hit_point, obj.get_color(), ray.get_origin())


def get_magnitude(origin, direction):
    #   Verified as correct calculation. Refer to ray_test.py
    magnitude = math.sqrt((direction[0] - origin[0])**2 + (direction[1] - origin[1])**2 + (direction[2] - origin[2])**2)
    return magnitude

def get_color(hit_normal, hit_point, color, origin):
    viewing_direction = rt.get_normal_v2(rt.get_vector(hit_point, origin))
    facing_ratio = np.dot(hit_normal, viewing_direction)
    # facing_ratio = hit_normal[0] * viewing_direction[0] + hit_normal[1] * viewing_direction[1] + hit_normal[2] * viewing_direction[2]
    print(facing_ratio)

    if facing_ratio < 0:
        return (0,0,0)

    pixel_color = list(np.asarray(color) * facing_ratio)

    for i, color in enumerate(pixel_color):
        pixel_color[i] = int(color)

    return tuple(pixel_color)

# Ref: http://www.scratchapixel.com/lessons/3d-basic-rendering/ray-tracing-generating-camera-rays/generating-camera-rays
def camera_stuff(pix_x, pix_y, width, height):
    pixel_ndc_x = (pix_x + 0.5) / width
    pixel_ndc_y = (pix_y + 0.5) / height 

    pix_screen_x = 2 * pixel_ndc_x - 1
    pix_screen_y = 1 - pixel_ndc_y * 2

    aspect_ratio = width / height
    fov = math.radians(90)

    pix_cam_x = (2 * pix_screen_x - 1) * aspect_ratio * math.tan(fov/2)
    pix_cam_y = 1 - 2 * pix_screen_y * math.tan(fov/2)

    return pix_cam_x, pix_cam_y 

#   Create scene (As constant? Ref:https://softwareengineering.stackexchange.com/questions/342374/should-i-really-use-all-uppercase-for-my-constants )
#       - Create two spheres. One for sphere, one for light. Creating a sphere object vs calling a get_sphere function?
#         Requires position, radius, and color to create
#       - Create plane. Use point-normal form? (Ref: https://en.wikipedia.org/wiki/Plane_(geometry)#Point-normal_form_and_general_form_of_the_equation_of_a_plane)

light = Sphere([0,0,11], 10, [255,255,0])     # Light (Yellow)
sphere = Sphere([0,0,3], 2, [0,0,255])       # Sphere (Blue)
# Plane([0,0,0,],[0,0,0], [0,255,9]),  # Ground (Green)


#   Render the image 
width = 800 
height = 600
render = Image.new('RGB', (width, height), color = 0)
pixels = render.load()
camera_coord = [0,0,0] # [width/2, height/2, 0]
image_plane_z = 1 
for i in range(width):
    for j in range(height):
        x, y = camera_stuff(i, j, width, height)
        ray = Ray(camera_coord, [x,y,image_plane_z])
        # intersection = intersection(ray, sphere)
        # if intersection is None:
        #     pixels[i,j] = (0,0,0)
        # else:
        pixels[i,j] = intersection(ray, sphere) 
        # if intersection(ray, light) is not None:
        #     pixels[i,j] = (255,255,0)
        #     print('light hit!')
render.show()


vect_origin_to_center = list(np.asarray(ray.get_origin()) - np.asarray(sphere.get_center()))  
dist_origin_to_center = get_magnitude(ray.get_origin(), sphere.get_center())    
ray_magnitude = get_magnitude(ray.get_origin(), ray.get_vector())   

ray_vector_normal = [ray.get_vector()[0]/ray_magnitude, ray.get_vector()[1]/ray_magnitude, ray.get_vector()[2]/ray_magnitude]

projection = np.dot(ray_vector_normal, dist_origin_to_center)

