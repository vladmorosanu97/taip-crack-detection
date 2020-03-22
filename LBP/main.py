import os

from LBP.training_model import TrainingModel
from LBP.lbp_test import testing, display, record_results


NEGATIVE_IMG_PATH = "/home/teodora/.facultate/taip/Concrete Crack Images for Classification/Negative"
POSITIVE_IMG_PATH = "/home/teodora/.facultate/taip/Concrete Crack Images for Classification/Positive"

NEGATIVE_IMG_TEST_PATH = "/home/teodora/.facultate/taip/test-dataset/Negative"
POSITIVE_IMG_TEST_PATH = "/home/teodora/.facultate/taip/test-dataset/Positive"


def do_training(path_to_img_dir, path_to_serialized_data):
    """
    Train the model, both with negative images (no cracks) and positive ones (craks)

    """
    model = TrainingModel()
    model.set_train_images(path_to_img_dir)
    model.set_train_dict(os.path.abspath("labels/new_training_labels.txt"))
    model.set_raw_results()
    model.serialize_raw_results(path_to_serialized_data)
    # model.display_results()       # works for a few images


def do_testing(img_dir_path):
    negative_results = testing(
        img_dir_path, os.path.abspath("serialized_training_data/negative_images.pkl")
    )

    positive_results = testing(img_dir_path, os.path.abspath("serialized_training_data/positive_images.pkl"))

    results = {}

    for test_image, training_results in negative_results.items():
        maximum_negative_score = max(training_results, key=lambda item: item[1])[1]
        positive_training_results = positive_results[test_image]
        maximum_positive_score = max(positive_training_results, key=lambda item: item[1])[1]

        if maximum_negative_score > maximum_positive_score:
            results[test_image] = "negative"
        else:
            results[test_image] = "positive"

    return results


def main():

    # ----------------------------------------- TRAINING -------------------------------------------------

    # do_training(NEGATIVE_IMG_PATH, os.path.abspath("LBP/serialized_training_data/negative_images.pkl"))
    # do_training(POSITIVE_IMG_PATH, os.path.abspath("LBP/serialized_training_data/positive_images.pkl"))

    # ----------------------------------------- TESTING --------------------------------------------------

    results = dict()
    results.update(do_testing(NEGATIVE_IMG_TEST_PATH))
    results.update(do_testing(POSITIVE_IMG_TEST_PATH))

    for k, v in results.items():
        print("[RESULTS] Image {} was classified as {}".format(k, v))


main()
