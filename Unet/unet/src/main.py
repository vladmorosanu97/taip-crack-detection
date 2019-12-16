import argparse
from setting import environment, constant
from util import path, generator
from nn import nn


# python main.py
# python main.py --dataset=example
# python main.py --dataset=example --gpu --test
# python main.py --dataset=example --gpu --train

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", help="Dataset name", type=str, default=constant.DATASET)
    parser.add_argument("--train", help="Train", action="store_true", default=False)
    parser.add_argument("--test", help="Predict", action="store_true", default=True)
    parser.add_argument("--gpu", help="Enable GPU mode", action="store_true", default=True)
    parser.add_argument("--augmentation", help="Dataset augmentation (pass quantity)", type=int)
    args = parser.parse_args()

    environment.setup()
    exist = lambda x: len(x) > 0 and path.exist(path.data(x, mkdir=False))

    if args.dataset is not None and exist(args.dataset):
        if args.augmentation:
            generator.augmentation(args.augmentation)
        elif args.train:
            nn.train()
        elif args.test:
            nn.test()
    else:
        print("\n>> Dataset not found\n")


if __name__ == "__main__":
    main()

