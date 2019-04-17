import math
import cv2 as cv
import numpy as np


class PointCloudBuilder:
    def build_point_cloud_by_disparity(self, img_left, disparity_map):
        h, w = disparity_map.shape[:2]
        f = 0.8 * w
        Q = np.float32([[1, 0, 0, -0.5 * w],
                        [0, -1, 0, 0.5 * h],
                        [0, 0, 0, -f],
                        [0, 0, 1, 0]])
        points = cv.reprojectImageTo3D(disparity_map, Q)
        colors = cv.cvtColor(img_left, cv.COLOR_BGR2RGB)

        return points, colors

    def build_point_cloud_by_depth(self, img_left, depth_map):
        points = np.zeros((720, 1280, 3), np.float32)

        depth_map = depth_map / depth_map.max() * 1280

        cam_pos_x = depth_map.shape[1] / 2
        cam_pos_y = depth_map.shape[0] / 2
        for x in range(0, depth_map.shape[0]):
            for y in range(0, depth_map.shape[1]):
                dist = depth_map[x][y]
                z = 0 + math.sqrt(abs(dist**2 - (x - cam_pos_x)**2 - (y - cam_pos_y)**2))
                depth_map[x][y] = z
                points[x][y] = [x, y, z]

        points = points / points.max() * 255
        colors = cv.cvtColor(img_left, cv.COLOR_BGR2RGB)

        return points, colors
