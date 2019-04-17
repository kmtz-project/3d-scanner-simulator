import cv2 as cv


class ImageData:
    def __init__(self, image, keypoints, descriptors):
        self.image = image
        self.keypoints = keypoints
        self.descriptors = descriptors


class FeaturesExtractor:
    def orb(self, image):
        orb = cv.ORB_create()
        keypoints, descriptors = orb.detectAndCompute(image, None)

        return ImageData(image, keypoints, descriptors)

    def surf(self, image):
        min_hessian = 400

        surf = cv.xfeatures2d_SURF.create(hessianThreshold=min_hessian)
        keypoints, descriptors = surf.detectAndCompute(image, None)

        return ImageData(image, keypoints, descriptors)


class Matcher:
    def bruteforce(self, image_1, image_2):
        result = []

        matcher = cv.BFMatcher(cv.NORM_HAMMING2, crossCheck=True)
        try:
            matches = matcher.match(image_1.descriptors, image_2.descriptors)
            matches = sorted(matches, key=lambda x: x.distance)[:5]

            for match in matches:
                keypoint_1 = tuple([int(x) for x in image_1.keypoints[match.queryIdx].pt])
                keypoint_2 = tuple([int(x) for x in image_2.keypoints[match.trainIdx].pt])

                result.append([keypoint_1, keypoint_2])
        except cv.error:
            pass

        return result

    def flann(self, image_1, image_2):
        matcher = cv.DescriptorMatcher_create(cv.DescriptorMatcher_FLANNBASED)
        matches = matcher.knnMatch(image_1.descriptors, image_2.descriptors, 2)
        ratio_thresh = 0.5

        good_matches = []
        for m, n in matches:
            if m.distance < ratio_thresh * n.distance:
                good_matches.append(m)
        good_matches = sorted(good_matches, key=lambda x: x.distance)[:10]

        result = []
        for match in good_matches:
            keypoint_1 = tuple([int(x) for x in image_1.keypoints[match.queryIdx].pt])
            keypoint_2 = tuple([int(x) for x in image_2.keypoints[match.trainIdx].pt])

            result.append([keypoint_1, keypoint_2])

        return result


class ImageMatcher:
    def __init__(self):
        self.features = FeaturesExtractor()
        self.matching = Matcher()
