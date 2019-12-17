from setting import environment, constant
from util import path
from nn import nn


def main():
    dataset = "crackconcrete"
    train = False
    test = True
    environment.setup()
    exist = lambda x: len(x) > 0 and path.exist(path.data(x, mkdir=False))

    if dataset is not None and exist(dataset):
        if train:
            nn.train()
        elif test:
            nn.test()
    else:
        print("\n>> Dataset not found\n")


if __name__ == "__main__":
    main()

