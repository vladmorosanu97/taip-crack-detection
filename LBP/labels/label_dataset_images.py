import os


def label_images(dataset_path):
    with open(os.path.abspath("new_training_labels_1.txt"), "wt") as label_file:
        for root, _, files in os.walk(dataset_path):
            for f in files:
                if "Negative" in dataset_path:
                    label_file.write("{} 0\n".format(f))
                else:
                    label_file.write("{} 2\n".format(f))


# label_images("/home/teodora/.facultate/taip/Concrete Crack Images for Classification/Negative")
label_images("/home/teodora/.facultate/taip/Concrete Crack Images for Classification/Positive")

