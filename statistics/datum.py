from math import frexp,ldexp,floor,log10

def rerror (x):
    """
    Gets the error made when rounding a real number
    to a 64 bits float point.

    :param x: The real number whose error is wanted.
    :return: The rounding error.
    """
    (m,e) = frexp(float(x))
    if x==0 or e<-1020:
        return ldexp(1.0,-1074)
    return ldexp(1.0,e-53)


def getDatum(x):
    """
    Converts a number or a tuple to a Datum object. For
    converting a tuple takes the value as the first element
    and the error as the second.

    :param x: Number, tuple or a Datum object to cast.
    :return: A Datum object.
    """
    if isinstance(x,Datum):
        return x
    elif isinstance(x,(list,tuple)):
        return Datum(x[0],x[1])
    return Datum(x)


class Datum(object):
    """
    Class that allows operate with objects as if them were
    numbers taking care of the error propagation.
    """

    def __init__(self, value=0, error=0, sign=1):
        """
        Constructor of Datum.

        :param value: The expected value of the datum.
        :param error: The error made in the measure of the
        datum (optional).
        :param sign: Number of significant ciphers the error
        is rounded to when converted to string.
        """
        self.value = float(value)
        self.error = rerror(self.value)
        error = abs(float(error))
        if self.error<error:
            self.error = error
        self.sign = sign

    def max(self):
        return self.value + self.error

    def min(self):
        return self.value - self.error

    def __eq__(self, other):
        if other==None:
            return False
        x = getDatum(other)
        return self.min()<=x.max() and self.max()>=x.min()

    def __ne__(self, other):
        if other==None:
            return True
        x = getDatum(other)
        return self.max()<x.min() or self.min()>x.max()

    def __lt__(self, other):
        if other==None:
            return False
        x = getDatum(other)
        return self.max()<x.min()

    def __gt__(self, other):
        if other==None:
            return False
        x = getDatum(other)
        return self.min()>x.max()

    def __le__(self, other):
        if other==None:
            return False
        x = getDatum(other)
        return self.min()<=x.max()

    def __ge__(self, other):
        if other==None:
            return False
        x = getDatum(other)
        return self.max()>=x.min()

    def __pos__(self):
        return self

    def __neg__(self):
        return Datum(-self.value,self.error)

    def __abs__(self):
        return Datum(abs(self.value),self.error)

    def __iadd__(self, other):
        x = getDatum(other)
        self.value += x.value
        self.error += x.error
        return self

    def __add__(self, other):
        x = getDatum(other)
        return Datum(self.value+x.value,self.error+x.error)

    def __radd__(self, other):
        x = getDatum(other)
        return Datum(self.value+x.value,self.error+x.error)

    def __isub__(self, other):
        x = getDatum(other)
        self.value -= x.value
        self.error += x.error
        return self

    def __sub__(self, other):
        x = getDatum(other)
        return Datum(self.value-x.value,self.error+x.error)

    def __rsub__(self, other):
        x = getDatum(other)
        return Datum(x.value-self.value,self.error+x.error)

    def __imul__(self, other):
        x = getDatum(other)
        self.error = abs(self.value*x.error)+abs(x.value*self.error)
        self.value *= x.value
        return self

    def __mul__(self, other):
        x = getDatum(other)
        return Datum(self.value*x.value,abs(self.value*x.error)+abs(x.value*self.error))

    def __rmul__(self, other):
        x = getDatum(other)
        return Datum(self.value*x.value,abs(self.value*x.error)+abs(x.value*self.error))

    def __idiv__(self, other):
        x = getDatum(other)
        self.error = (abs(self.value*x.error)+abs(x.value*self.error))/x.value/x.value
        self.value /= x.value
        return self

    def __div__(self, other):
        x = getDatum(other)
        return Datum(self.value/x.value,(abs(self.value*x.error)+abs(x.value*self.error))/x.value/x.value)

    def __truediv__(self, other):
        x = getDatum(other)
        return Datum(self.value/x.value,(abs(self.value*x.error)+abs(x.value*self.error))/x.value/x.value)

    def __rdiv__(self, other):
        x = getDatum(other)
        return Datum(x.value/self.value,(abs(self.value*x.error)+abs(x.value*self.error))/self.value/self.value)

    def __int__(self):
        return int(self.value)

    def __long__(self):
        return long(self.value)

    def __float__(self):
        return float(self.value)

    def __complex__(self):
        return complex(self.value)

    def __str__(self):
        eciph = self.sign
        if self.value==0:
            vorder = 0
        else:
            vorder = int(floor(log10(abs(self.value))))
        if self.error==0:
            eorder = 0
        else:
            eorder = int(floor(log10(abs(self.error))))
        if int(floor(self.error / 10.0**float(eorder-eciph+1)))==1:
            eciph += 1
        if vorder>=eorder-eciph+1:
            precission = eciph + vorder - eorder - 1
            value = self.value / 10.0**float(vorder)
            error = int(round(self.error / 10.0**float(eorder-eciph+1)))
            return ("{:."+str(precission)+"f}({:"+str(eciph)+"d})e{:d}").format(value,error,vorder)
        error = int(round(self.error,eciph-eorder-1))
        return "0({:d})e0".format(error)

    def to4sign(self):
        if self.value==0:
            vorder = 0
        else:
            vorder = int(floor(log10(abs(self.value))))
        if self.error==0:
            eorder = 0
        else:
            eorder = int(floor(log10(abs(self.error))))
        if vorder>=eorder-3:
            precission = 3 + vorder - eorder
            value = self.value / 10**float(vorder)
            error = int(round(self.error / 10**float(eorder-3)))
            return ("{:."+str(precission)+"f}({:4d})e{:d}").format(value,error,vorder)
        error = int(round(self.error,3-eorder))
        return "0({:d})e0".format(error)