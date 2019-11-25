from LBP.lbp_training import training
from LBP.lbp_test import testing, display, record_results


def main():

    training("data/lbp_dataset/training", "data/lbp_dataset/train.txt")
    results = testing("data/lbp_dataset/test", "data/lbp_dataset/test.txt")
    display(results)
    record_results(results)

main()