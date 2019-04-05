from src.image_matcher import ImageMatcher


def test_feature_detection():
    args = [
        "../data/captures/left/360.png",
        "../data/captures/left/345.png"
    ]
    image_matcher = ImageMatcher(args)

    images_data = image_matcher.features.orb(image_matcher.images)
    # images_data = image_matcher.features.surf(image_matcher.images)

    # matches = image_matcher.matching.bruteforce(images_data)
    matches = image_matcher.matching.flann(images_data)


test_feature_detection()
