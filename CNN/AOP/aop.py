from pythonrv import rv
# from cracks import cnn_classifier

from calculator import calculator
import time

start_time = None


@rv.monitor(call=calculator.initCalculator)
def spec_update(event):
    print "Log: init calculator is called"
    board = event.fn.call


@rv.monitor(call=calculator.initCalculator)
@rv.spec(when=rv.POST)
def spec_update(event):
    print "Log: init calculator was finished"
    board = event.fn.call


@rv.monitor(update=calculator.multiply)
# @rv.spec(when=rv.POST)
def spec_update(event):
    print "Log: multiply calculator is called"
    board = event.fn.update


@rv.monitor(update=calculator.multiply)
@rv.spec(when=rv.POST)
def spec_update(event):
    print "Log: multiply calculator was finished"
    board = event.fn.update


@rv.monitor(fibonacci=calculator.performFibonacci)
def spec_update(event):
    global start_time
    start_time = time.time()
    print start_time
    board = event.fn.fibonacci


@rv.monitor(fibonacci=calculator.performFibonacci)
@rv.spec(when=rv.POST)
def spec_update(event):
    global start_time
    print time.time() - start_time
    board = event.fn.fibonacci


calculator.multiply()
calculator.initCalculator(30, 20, 30)
calculator.performFibonacci()
