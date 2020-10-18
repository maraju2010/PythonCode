import abc
import prop
import datetime
import six

@six.add_metaclass(abc.ABCMeta)
class Abstract():

    @abc.abstractmethod
    def _counter(self):
        pass


    @abc.abstractmethod
    def _analyse_counter(self):
        pass
