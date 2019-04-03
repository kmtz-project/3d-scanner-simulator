import math

import cv2 as cv
import numpy as np

# TODO: Move to JSON file
sgbm_config = {
    'num_disparities': 96,
    'window_size': 3,
    'p1_factor': 8,
    'p2_factor': 32,
    'uniqueness_ratio': 10,
    'speckle_window_size': 100,
    'speckle_range': 32,
    'disp12_max_diff': 1
}

ply_header = '''ply
format ascii 1.0
element vertex %(vert_num)d
property float x
property float y
property float z
property uchar red
property uchar green
property uchar blue
end_header
'''


class PointCloudBuilder:
    def build_point_cloud(self, img_left, img_right, output_path="out.point_clouds"):
        disparity_map = self.__get_disparity_map__(img_left, img_right)

        h, w = img_left.shape[:2]
        f = 0.8 * w  # guess for focal length
        Q = np.float32([[1,  0, 0, -0.5 * w],
                        [0, -1, 0,  0.5 * h],  # turn points 180 deg around x-axis,
                        [0,  0, 0, -f],        # so that y-axis looks up
                        [0,  0, 1,  0]])
        points = cv.reprojectImageTo3D(disparity_map, Q)
        colors = cv.cvtColor(img_left, cv.COLOR_BGR2RGB)
        mask = disparity_map > disparity_map.min()

        self.__save_point_cloud_to_file__(points[mask], colors[mask], output_path)


    def __get_disparity_map__(self, img_left, img_right):
        num_disparities = sgbm_config['num_disparities']
        num_disparities += 16 - (num_disparities % 16)

        sgbm_window_size = sgbm_config['window_size']

        stereo_sgbm = cv.StereoSGBM_create(blockSize=16,
                                           P1=sgbm_config['p1_factor'] * 3 * sgbm_window_size * sgbm_window_size,
                                           P2=sgbm_config['p2_factor'] * 3 * sgbm_window_size * sgbm_window_size,
                                           numDisparities=num_disparities,
                                           uniquenessRatio=sgbm_config['uniqueness_ratio'],
                                           speckleWindowSize=sgbm_config['speckle_window_size'],
                                           speckleRange=sgbm_config['speckle_range'],
                                           disp12MaxDiff=sgbm_config['disp12_max_diff']
                                           )

        disparity_map = stereo_sgbm.compute(img_left, img_right).astype(np.float32) / 16.0

        return disparity_map

    def __save_point_cloud_to_file__(self, vertices, colors, file_path):
        vertices = vertices.reshape(-1, 3)
        colors = colors.reshape(-1, 3)

        vertices = np.hstack([vertices, colors])
        vertices = [v for v in vertices if self.__is_vertex_valid__(v)]

        if len(vertices) != 0:
            with open(file_path, "wb") as f:
                f.write((ply_header % dict(vert_num=len(vertices))).encode("utf-8"))
                np.savetxt(f, vertices, fmt="%f %f %f %d %d %d ")

    def __is_vertex_valid__(self, vertex):
        return math.inf not in vertex and (-math.inf) not in vertex and math.nan not in vertex
