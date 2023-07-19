class MCollector(object):

    def __init__(self):
        self.info = []
        # self.ct = 0

    def get_method(self, method_info):

        # self.ct += 1
        self.info.append(method_info)

#    def get_params(self, *args, **kwargs):
#        self.info['args'] = args
#        self.info['kwargs'] = kwargs

myservices = MCollector()

class ladonize(object):

    def __init__(self, *args, **kwargs):
        # print("Inside __init__()")
        self.args = args
        self.kwargs = kwargs

    def __call__(self, fun):
        # print(fun.__name__)
        myservices.get_method({'name': fun.__name__,
        'args': self.args, 'kwargs': self.kwargs, 'doc': fun.__doc__})

        # print("Inside __call__()")
        def wrapped(*args):
            # print("Inside wrapped_f()")
            fun(*args)
            # print("After f(*args)")

        return wrapped

#class mydecorator(object):
#
#    def __init__(self, arg1, arg2, arg3):
#        """
#        If there are decorator arguments, the function
#        to be decorated is not passed to the constructor!
#        """
#        print("Inside __init__()")
#        self.arg1 = arg1
#        self.arg2 = arg2
#        self.arg3 = arg3
#
#    def __call__(self, f):
#        """
#        If there are decorator arguments, __call__() is only called
#        once, as part of the decoration process! You can only give
#        it a single argument, which is the function object.
#        """
#        print("Inside __call__()")
#        def wrapped_f(*args):
#            print("Inside wrapped_f()")
#            print("Decorator arguments:", self.arg1, self.arg2, self.arg3)
#            f.info = [self.arg1, self.arg2, self.arg3]
#            f(*args)
#            print("After f(*args)")
#        return wrapped_f


