import cv2 as cv
import math
import numpy as np
import os

from src import variables
from src.depth_parser import DepthParser
from src.disparity_calculator import DisparityCalculator
from src.image_matcher import ImageMatcher
from src.point_cloud_builder import PointCloudBuilder
from src.point_cloud_merger import PointCloudMerger


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
depth_parser = DepthParser()
cloud_builder = PointCloudBuilder()
cloud_merger = PointCloudMerger()

data = []
file_names = os.listdir(variables.left_captures_path)
for file_name in file_names:
    print(file_name)
    left_path = "{}/{}".format(variables.left_captures_path, file_name)
    right_path = "{}/{}".format(variables.right_captures_path, file_name)

    file_name_without_extension = file_name.split(".")[0]

    disp_file_name = "disp_{}.png".format(file_name_without_extension)
    disp_path = "{}/{}".format(variables.disparity_path, disp_file_name)

    ply_file_name = file_name_without_extension + ".ply"
    ply_path = "{}/{}".format(variables.point_clouds_path, ply_file_name)

    depth_map_file_name = file_name_without_extension + ".csv"
    depth_map_path = "{}/{}".format(variables.left_depth_maps_path, depth_map_file_name)

    img_left = cv.imread(left_path)
    img_right = cv.imread(right_path)

    # disparity_map = disparity_calculator.get_disparity_map(img_left, img_right)
    # cv.imwrite(disparity_map, disp_path)

    depth_map = depth_parser.get_depth_map_from_file(depth_map_path)

    # points, colors = cloud_builder.build_point_cloud(img_left, disparity_map)
    points, colors = cloud_builder.build_point_cloud_by_depth(img_left, depth_map)
    # __save_point_cloud_to_file__(points, colors, ply_path)

    data.append({
        'disp': depth_map,
        'point_cloud': {
            'points': points,
            'colors': colors
        }
    })

# angle = 0
image_matcher = ImageMatcher()

images_data = []
for x in data:
    images_data.append(image_matcher.features.orb(x['disp']))

points = np.empty(shape=(720, 0, 3))
colors = np.empty(shape=points.shape)

shift = 0

for i in range(0, len(images_data) - 1):
    matches = image_matcher.matching.bruteforce(images_data[i], images_data[i + 1])
    if len(matches) == 0:
        continue

    cloud = cloud_merger.merge_clouds(data[i]['point_cloud'], data[i+1]['point_cloud'], matches)
    for k in range(0, cloud['points'].shape[0]):
        for j in range(0, cloud['points'].shape[1]):
            cloud['points'][k][j][1] += shift

    points = np.concatenate([points, cloud['points']], axis=1)
    colors = np.concatenate([colors, cloud['colors']], axis=1)
    # __save_point_cloud_to_file__(cloud['points'], cloud['colors'], "out_{}.ply".format(i))

__save_point_cloud_to_file__(points, colors, "out.ply")


# TODO:
# points_1 = data[i]['point_cloud']['points'][:, :left_crop_max]
# colors_1 = data[i]['point_cloud']['colors'][:, :left_crop_max]
# __save_point_cloud_to_file__(points_1, colors_1, "out_{}_z.ply".format(i))
# __save_point_cloud_to_file__(points_1, colors_1, "out_{}_1.ply".format(i))
# points_2 = data[i+1]['point_cloud']['points'][:, right_crop_min:]
# colors_2 = data[i+1]['point_cloud']['colors'][:, right_crop_min:]
# __save_point_cloud_to_file__(points_2, colors_2, "out_{}_2.ply".format(i))
#
# for k in range(0, points_1.shape[0]):
#     for j in range(0, points_1.shape[1]):
#         y = points_1[k][j][1]
#         z = points_1[k][j][2]
#         points_1[k][j][1] = y * math.cos(angle) - z * math.sin(angle)
#         points_1[k][j][2] = y * math.sin(angle) + z * math.cos(angle)
#
# angle += (left_crop_max / 1280) * (-30 * math.pi / 180)
#
# points = np.concatenate([points, points_1], axis=1)
# colors = np.concatenate([colors, colors_1], axis=1)
