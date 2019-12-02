import sys
import aspectlib
import os, shutil
from cracks import CnnClassifier
from aspectlib.debug import log

SAVE_MODEL_PATH = "C:\Master\Invalid_TAIP"


def remove_png_files_from_path(path):
    for r, d, f in os.walk(path):
        for file in f:
            if '.png' in file:
                print("Remove on file ", file)
                # os.remove(os.path.join(file_path, file))


def mop_for_crack_detection():
    @aspectlib.Aspect
    def load_files_aspect(*args):
        print("********** Load files aspect **********")
        m = args[0]
        path = m.TRAINING_PATH

        files_path = os.path.join(path, "Positive")
        remove_png_files_from_path(files_path)

        files_path = os.path.join(path, "Negative")
        remove_png_files_from_path(files_path)

        yield aspectlib.Proceed

    @aspectlib.Aspect
    def train_aspect(*args):
        print("********** Start training aspect **********")
        m = args[0]
        if m.train_datagen is None:
            print("Train datagen is null. Reload the files")
            m.load_training_dataset()
        if m.training_set is None:
            print("Train dataset is null. Reload the files")
            m.load_training_dataset()

        yield aspectlib.Proceed

    @aspectlib.Aspect
    def save_model_aspect(*args):
        print("********** Save model aspect **********")
        m = args[0]
        path = args[1]
        if not os.path.exists(path):
            print("The argument path is invalid. Save model to default path")
            default_path = "C:\Master\TAIP\MOP\models"
            m.save_model(default_path)
        yield aspectlib.Proceed

    with aspectlib.weave(CnnClassifier.load_training_dataset, load_files_aspect, subclasses=False):
        model = CnnClassifier()
        model.load_training_dataset()

    with aspectlib.weave(CnnClassifier.train, train_aspect, subclasses=False):
        model = CnnClassifier()
        # model.load_training_dataset()
        # model.train()

    with aspectlib.weave(CnnClassifier.save_model, save_model_aspect, subclasses=False):
        model = CnnClassifier()
        # model.load_training_dataset()
        model.save_model(SAVE_MODEL_PATH)


mop_for_crack_detection()
