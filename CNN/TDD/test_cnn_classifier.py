from unittest import TestCase
import os
# from cracks import  cnn_classifier

LOCAL_MODEL_FOLDER = r"C:\Master\TAIP\cracks\models\models.h5"
TRAIN_MODEL_FOLDER = r"C:\Master\TAIP\concrete-crack-images-for-classification\Concrete Crack Images for Classification"


class test_cnn_classifier(TestCase):
    def test_save_model(self):
        # arrange
        #model = cnn_classifier()
        file_path = LOCAL_MODEL_FOLDER

        # act
        # model.save_model(LOCAL_MODEL_FOLDER)
        is_file = os.path.exists(LOCAL_MODEL_FOLDER)

        # assert
        assert is_file == 1

    def test_train(self):
        # arrange
        file_path = TRAIN_MODEL_FOLDER

        # act
        is_folder = os.path.exists(LOCAL_MODEL_FOLDER)

        # assert
        assert is_folder == 1

