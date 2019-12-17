import setting.constant as const
import importlib


def setup():
    const.fn_CHECKPOINT = ("%s_%s_%s" % (const.MODEL, const.DATASET, const.fn_CHECKPOINT))
    const.fn_LOGGER = ("%s_%s_%s" % (const.MODEL, const.DATASET, const.fn_LOGGER))
    arch = importlib.import_module("%s.%s.%s" % (const.dn_NN, const.dn_ARCH, const.MODEL))
    const.IMAGE_SIZE = arch.IMAGE_SIZE
    print("Dataset:", const.DATASET)
    print("DIP:\t", const.IMG_PROCESSING)
    print("Arch:\t", const.MODEL)
