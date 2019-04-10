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
        matcher = cv.BFMatcher(cv.NORM_HAMMING2, crossCheck=True)
        matches = matcher.match(image_1.descriptors, image_2.descriptors)
        # matches = sorted(matches, key=lambda x: x.distance)[:10]

        # match_image = image_1.image
        # match_image = cv.drawMatches(image_1.image, image_1.keypoints,
        #                              image_2.image, image_2.keypoints, matches,
        #                              match_image, flags=2)
        # plt.imshow(match_image), plt.show()

        return matches

    def flann(self, image_1, image_2):
        matcher = cv.DescriptorMatcher_create(cv.DescriptorMatcher_FLANNBASED)
        matches = matcher.knnMatch(image_1.descriptors, image_2.descriptors, 2)
        ratio_thresh = 0.5

        good_matches = []
        for m, n in matches:
            if m.distance < ratio_thresh * n.distance:
                good_matches.append(m)

        # match_image = image_1.image
        # match_image = cv.drawMatches(image_1.image, image_1.keypoints,
        #                              image_2.image, image_2.keypoints, good_matches,
        #                              match_image, flags=2)
        # plt.imshow(match_image), plt.show()

        return good_matches


class ImageMatcher:
    def __init__(self):
        self.features = FeaturesExtractor()
        self.matching = Matcher()
