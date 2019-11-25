import os
import sys
import aspectlib
from aspectlib.debug import log


class Aspects:
    @aspectlib.Aspect
    def param_validator(*args, **kwargs):
        print(u"Got called with args: {} kwargs: {}".format(args, kwargs))
        yield aspectlib.Proceed

    @aspectlib.Aspect(bind=True)
    def exception_logger(cutpoint, *args):
        try:
            value = yield aspectlib.Proceed
        except Exception as e:
            print(u"Raised exception {} for function {} called with arguments: {}".format(cutpoint.__name__, e, args))
            raise
        else:
            print(u"Returned {} for {}".format(value, args))
            yield aspectlib.Return(value)

    @aspectlib.Aspect
    def result_logger(*args):
        result = yield aspectlib.Proceed
        print(u"[LOGGER] The return result is: {}".format(result, ))
        yield aspectlib.Return(result)

    @aspectlib.Aspect
    def path_exists(*args):
        with aspectlib.weave('os.path.exists', log(print_to=sys.stdout)):
            print(u"Checking if path exists: {}".format(args[1]))   # args[0] e instanta clasei
            yield aspectlib.Return(os.path.exists(args[1]))

    @aspectlib.Aspect
    def file_checker(*args):
        with aspectlib.weave('os.path.isfile', log(print_to=sys.stdout)):
            print(u"Checking if path given is a file: {}".format(args[1]))
            result = yield aspectlib.Proceed(os.path.isfile(args[1]))
            print("Result: {}".format(result))