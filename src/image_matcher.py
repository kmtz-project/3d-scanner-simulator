import cv2 as cv


class ImageData:
    def __init__(self, image, keypoints, descriptors):
        self.image = image
        self.keypoints = keypoints
        self.descriptors = descriptors


class FeaturesExtractor:
    def orb(self, images):
        result = []

        orb = cv.ORB_create()
        for idx in range(0, len(images)):
            image = images[idx]

            keypoints, descriptors = orb.detectAndCompute(image, None)
            result.append(ImageData(image, keypoints, descriptors))

        return result

    def surf(self, images):
        result = []

        min_hessian = 400
        surf = cv.xfeatures2d_SURF.create(hessianThreshold=min_hessian)
        for idx in range(0, len(images)):
            image = images[idx]

            keypoints, descriptors = surf.detectAndCompute(image, None)
            result.append(ImageData(image, keypoints, descriptors))

        return result


class Matcher:
    def bruteforce(self, images_data):
        result = []

        matcher = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)
        for idx in range(len(images_data) - 1):
            matches = matcher.match(images_data[idx].descriptors, images_data[idx + 1].descriptors)
            matches = sorted(matches, key=lambda x: x.distance)

            match_image = images_data[idx].image
            match_image = cv.drawMatches(images_data[idx].image, images_data[idx].keypoints,
                                         images_data[idx + 1].image, images_data[idx + 1].keypoints, matches[:20],
                                         match_image, flags=2)
            result.append(match_image)

        return match_image

    def flann(self, images_data):
        result = []

        matcher = cv.DescriptorMatcher_create(cv.DescriptorMatcher_FLANNBASED)
        for idx in range(len(images_data) - 1):
            matches = matcher.knnMatch(images_data[idx].descriptors, images_data[idx + 1].descriptors, 2)
            ratio_thresh = 0.7
            good_matches = []
            for m, n in matches:
                if m.distance < ratio_thresh * n.distance:
                    good_matches.append(m)

            match_image = images_data[idx].image
            match_image = cv.drawMatches(images_data[idx].image, images_data[idx].keypoints,
                                         images_data[idx + 1].image, images_data[idx + 1].keypoints, good_matches,
                                         match_image, flags=2)
            result.append(match_image)

        return match_image


class ImageMatcher:
    def __init__(self, filenames):
        self.images = self.__get_images__(filenames)
        self.features = FeaturesExtractor()
        self.matching = Matcher()

    def __get_images__(self, filenames):
        result = []

        for filename in filenames:
            img = cv.imread(filename, cv.IMREAD_GRAYSCALE)
            result.append(img)

        return result
