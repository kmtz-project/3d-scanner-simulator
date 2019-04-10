import cv2 as cv
import math
import numpy as np
import os

from src import variables
from src.disparity_calculator import DisparityCalculator
from src.image_matcher import ImageMatcher
from src.point_cloud_builder import PointCloudBuilder


def __is_vertex_valid__(vertex):
    return math.inf not in vertex and (-math.inf) not in vertex and math.nan not in vertex


def __save_point_cloud_to_file__(vertices, colors, file_path):
    vertices = vertices.reshape(-1, 3)
    colors = colors.reshape(-1, 3)

    vertices = np.hstack([vertices, colors])
    vertices = [v for v in vertices if __is_vertex_valid__(v)]

    if len(vertices) != 0:
        with open(file_path, "wb") as f:
            f.write((variables.ply_header % dict(vert_num=len(vertices))).encode("utf-8"))
            np.savetxt(f, vertices, fmt="%f %f %f %d %d %d ")


disparity_calculator = DisparityCalculator()
cloud_builder = PointCloudBuilder()

data = []
file_names = os.listdir(variables.left_captures_path)
for file_name in file_names:
    left_path = "{}/{}".format(variables.left_captures_path, file_name)
    right_path = "{}/{}".format(variables.right_captures_path, file_name)

    file_name_without_extension = file_name.split(".")[0]

    disp_file_name = "disp_{}.png".format(file_name_without_extension)
    disp_path = "{}/{}".format(variables.disparity_path, disp_file_name)

    ply_file_name = file_name_without_extension + ".ply"
    ply_path = "{}/{}".format(variables.point_clouds_path, ply_file_name)

    img_left = cv.pyrDown(cv.imread(left_path))
    img_right = cv.pyrDown(cv.imread(right_path))

    disparity_map = disparity_calculator.get_disparity_map(img_left, img_right)
    print(disparity_map.shape)
    # cv.imwrite(disparity_map, disp_path)

    points, colors = cloud_builder.build_point_cloud(img_left, disparity_map)
    # __save_point_cloud_to_file__(points, colors, ply_path)
    data.append({
        'disp': disparity_map,
        'point_cloud': {
            'points': points,
            'colors': colors
        }
    })

points = np.empty(shape=[points.shape[0], len(file_names) * points.shape[1], points.shape[2]])
colors = np.empty(shape=points.shape)
# angle = 0
current_shift = 0

image_matcher = ImageMatcher()
images_data = [image_matcher.features.orb(x['disp']) for x in data]
for i in range(0, len(images_data) - 1):
    matches = image_matcher.matching.bruteforce(images_data[i], images_data[i + 1])
    distance = int(np.average([x.distance for x in matches]))

    img = data[i]['disp']

    points_local = data[i]['point_cloud']['points']
    colors_local = data[i]['point_cloud']['colors']

    for k in range(0, img.shape[0]):
        for j in range(0, distance):
            x, y, z = points_local[k][j]
            # x = x * math.cos(angle) - z * math.sin(angle)
            # z = x * math.sin(angle) + z * math.cos(angle)
            points[k][current_shift + j] = [x, y, z]
            colors[k][current_shift + j] = colors_local[k][j]
    current_shift += distance
    # angle += 5 * math.pi / 180

points.resize([points.shape[0], current_shift, points.shape[2]])
colors.resize(points.shape)
print(points.shape)
__save_point_cloud_to_file__(points, colors, "out.ply")
