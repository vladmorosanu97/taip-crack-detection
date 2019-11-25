from unittest import TestCase
from LBP.lbp_training_oop import TrainingModel
import os
from coverage import coverage, Coverage


class TestTraining(TestCase):
    def setUp(self):
        self.ttr = TrainingModel()


class TestInit(TestTraining):
    def test_initial_train_images(self):
        self.assertEqual(self.ttr.train_images, None)

    def test_initial_train_dict(self):
        self.assertEqual(self.ttr.train_dict, None)

    def test_initial_histograms(self):
        self.assertEqual(self.ttr.normalized_histograms, [])

    def test_initial_image_paths(self):
        self.assertEqual(self.ttr.image_paths, [])

    def test_initial_class_labels(self):
        self.assertEqual(self.ttr.class_labels, [])


cov = Coverage()


class Test(TestTraining):

    def test_set_train_images(self):
        cov.start()
        self.ttr.set_train_images("data/lbp_dataset/training")
        self.assertTrue(len(self.ttr.train_images) > 0)
        cov.stop()
        cov.exclude(regex='import ', which='exclude')
        cov.exclude(regex='def __init__(self) ', which='exclude')
        cov.exclude(regex='@property', which='exclude')
        cov.exclude(regex='def main()', which='exclude')
        cov.exclude(regex='def display_results', which='exclude')

        cov.html_report(directory='LBP/results')

    def test_if_is_image(self):
        cov.start()
        self.ttr.set_train_images("data/lbp_dataset/training")
        for img in self.ttr.train_images:
            self.assertTrue(os.path.exists(img))
            self.assertTrue(os.path.splitext(img)[1] in [".jpg", ".jpeg", ".png"])
        cov.stop()
        cov.html_report(directory='LBP/results')

    def test_if_is_not_image(self):
        cov.start()
        self.ttr.set_train_images("data/lbp_dataset/training")
        self.assertIsNone(self.ttr.train_images)
        cov.stop()
        cov.html_report(directory='LBP/results')

    def test_set_train_dict(self):
        cov.start()
        test_training_paths = ["data/lbp_dataset/train.txt", "data/lbp_dataset/training/", "data/lbp_dataset/training", "data/lbp_dataset/training.csv", "data/data/data"]
        for training_path in test_training_paths:
            if os.path.exists(training_path):
                if os.path.splitext(training_path)[1] == "txt":
                    try:
                        opened_files = open(training_path, 'rt')
                        self.ttr.set_train_dict(training_path)
                        try:
                            info = opened_files.readlines()
                            self.assertIsNotNone(info)
                            self.assertIsNotNone(self.ttr.train_dict)
                        except Exception as e:
                            print("Error: {}".format(e))
                        finally:
                            opened_files.close()
                    except IOError:
                        print("Could not open file")
                else:
                    if os.path.isdir(training_path):
                        self.assertIsNone(self.ttr.train_dict)
                    if os.path.isfile(training_path):
                        self.assertEqual(self.ttr.train_dict, None)
            else:
                self.assertIsNone(self.ttr.train_dict)
        cov.stop()
        cov.html_report(directory='LBP/results')

    def test_set_raw_results_exist(self):
        cov.start()
        self.ttr.set_train_images("data/lbp_dataset/training")
        self.ttr.set_train_dict("data/lbp_dataset/train.txt")
        if self.ttr.train_images:
            self.ttr.set_raw_results()
            self.assertTrue(len(self.ttr.normalized_histograms) > 0)
            self.assertTrue(len(self.ttr.image_paths) > 0)
            self.assertTrue(len(self.ttr.class_labels) > 0)
        cov.stop()
        cov.html_report(directory='LBP/results')

    def test_check_histograms_not_empty(self):
        cov.start()
        self.ttr.set_train_images("data/lbp_dataset/training")
        self.ttr.set_train_dict("data/lbp_dataset/train.txt")
        if self.ttr.train_images:
            self.ttr.set_raw_results()
            expected_count = len(self.ttr.train_images)
            self.assertEqual(expected_count, len(self.ttr.normalized_histograms))
        cov.stop()
        cov.html_report(directory='LBP/results')

    def test_check_image_paths_not_empty(self):
        cov.start()
        self.ttr.set_train_images("data/lbp_dataset/training")
        self.ttr.set_train_dict("data/lbp_dataset/train.txt")
        if self.ttr.train_images:
            self.ttr.set_raw_results()
            expected_count = len(self.ttr.train_images)
            self.assertEqual(expected_count, len(self.ttr.image_paths))
        cov.stop()
        cov.html_report(directory='LBP/results')

    def test_check_class_labels_not_empty(self):
        cov.start()
        self.ttr.set_train_images("data/lbp_dataset/training")
        self.ttr.set_train_dict("data/lbp_dataset/train.txt")
        if self.ttr.train_images:
            self.ttr.set_raw_results()
            expected_count = len(self.ttr.train_images)
            self.assertEqual(expected_count, len(self.ttr.class_labels))
        cov.stop()
        cov.html_report(directory='LBP/results')

    def test_serialization(self):
        cov.start()
        pickle_path = ["lbp_dataset.pkl", "lbp_dataset.txt", 12]
        for pkl in pickle_path:
            try:
                if os.path.splitext(pkl)[1] in [".pkl", ".txt"]:
                    self.assertTrue(os.path.exists(self.ttr.serialize_raw_results(pkl)))
                else:
                    self.assertEqual(self.ttr.serialize_raw_results(pkl), 0)
            except (TypeError, KeyError):
                print("Could not serialize data")
        cov.stop()
        cov.html_report(directory='LBP/results')
