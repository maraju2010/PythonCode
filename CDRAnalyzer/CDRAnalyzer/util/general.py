"""
    Basic utility functions

"""
def _strtranslate(astring):
    return str(astring).capitalize().strip("'{}'")

def _coltranslate(col):
        buffer=""
        for i in col.split(","):
            tempstr = i
            buffer+= "".join(tempstr + ",\n" if "))" not in tempstr else tempstr)
        return buffer
