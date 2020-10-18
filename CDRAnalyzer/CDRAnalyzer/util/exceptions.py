"""
    general exception module

"""

class filenotready(IOError):
    pass

class keynotavailable(KeyError):
    pass

class generalerror(Exception):
    pass

class ImproperlyConfigured(Exception):
    pass

class SuspiciousOperation(Exception):
    pass
