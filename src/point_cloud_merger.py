import numpy as np


class PointCloudMerger:
    # FIXME
    def merge_clouds(self, cloud_left, cloud_right, matches):
        left_crop_min = np.min([m[0][0] for m in matches])
        # left_crop_max = np.max([m[0][0] for m in matches])

        # right_crop_min = np.min([m[1][0] for m in matches])
        right_crop_max = np.max([m[1][0] for m in matches])

        points_left = cloud_left['points'][:, :left_crop_min]
        colors_left = cloud_left['colors'][:, :left_crop_min]

        points_right = cloud_right['points'][:, right_crop_max:]
        colors_right = cloud_right['colors'][:, right_crop_max:]

        # angle = 30
        # sin = math.sin(angle)
        # cos = math.cos(angle)
        shift = points_left[0][left_crop_min - 1][1] - points_right[0][0][1]

        for k in range(0, points_right.shape[0]):
            for j in range(0, points_right.shape[1]):
                points_right[k][j][1] += shift

                # y = y * cos - x * sin
                # x = y * sin + x * cos

        # points_mid_1 = p[:, left_crop_min:left_crop_max]
        # colors_mid_1 = c[:, left_crop_min:left_crop_max]
        #
        # points_mid_2 = p[:, right_crop_min:right_crop_max]
        # colors_mid_2 = c[:, right_crop_min:right_crop_max]

        points = np.concatenate([points_left, points_right], axis=1)
        colors = np.concatenate([colors_left, colors_right], axis=1)

        return {
            'points': points,
            'colors': colors,
            'shift': points[0][points.shape[1] - 1][1]
        }
