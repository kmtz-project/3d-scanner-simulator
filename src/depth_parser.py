import numpy as np


class DepthParser:
    def get_depth_map_from_file(self, depth_file_path):
        depth_file = open(depth_file_path, "r")

        img = np.zeros((720, 1280), np.float32)

        num_lines = 0
        data_start_index = 24
        for line in depth_file:
            val_array = line.split(",")
            if num_lines >= data_start_index:
                idx = num_lines - data_start_index
                img[idx] = val_array[2:]
            num_lines += 1

        img = img / img.max() * 255
        img = np.uint8(img)

        return img
