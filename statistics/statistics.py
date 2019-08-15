# -*- coding: utf-8 -*-
from math import sqrt,log10
from os.path import isfile
from .datum import Datum,getDatum


class Linear(object):

    def __init__(self, momenta):
        self.a = Datum()
        self.b = Datum()
        self.r = None
        if momenta.length>2:
            d = momenta.xx - momenta.x*momenta.x/float(momenta.length)
            self.a.value = (momenta.xy - momenta.x*momenta.y/float(momenta.length))/d
            self.b.value = (momenta.y*momenta.xx - momenta.x*momenta.xy)/d/float(momenta.length)
            sy2 = momenta.yy - 2.0*self.a.value*momenta.xy - 2.0*self.b.value*momenta.y + self.a.value*self.a.value*momenta.xx + 2.0*self.a.value*self.b.value*momenta.x + self.b.value*self.b.value*float(momenta.length)
            sy2 /= float(momenta.length - 2)
            self.a.error = sqrt(abs(sy2/d))
            self.b.error = self.a.error*sqrt(momenta.xx/float(momenta.length))
            self.r = (momenta.xy - momenta.x*momenta.y/float(momenta.length))/sqrt(d*(momenta.yy - momenta.y*momenta.y/float(momenta.length)))

    def echo(self):
        print("Coeficiente de correlación: " + str(self.r))
        print("Pendiente: " + str(self.a))
        print("Ordenada en el origen: " + str(self.b))


class Momenta(object):

    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.xx = 0.0
        self.xy = 0.0
        self.yy = 0.0
        self.length = 0


class DataBunch(object):

    def __init__(self, filename=''):
        self.points = []
        self.length = 0
        self.load(filename)

    def load(self, filename):
        if isfile(filename):
            file = open(filename,"r")
            for line in file:
                floats = []
                n = 0
                for field in line.split(";"):
                    try:
                        floats += [float(field)]
                        n += 1
                    except ValueError:
                        continue
                if n>1:
                    x = Datum(floats[0])
                    y = Datum(floats[1])
                    if n==3:
                        y.error = floats[2]
                    elif n>3:
                        x.error = floats[2]
                        y.error = floats[3]
                    self.add(x,y)
            file.close()

    def save(self, filename):
        file = open(filename,"w")
        for point in self.points:
            file.write(str(point[0].value) + ";" + str(point[1].value) + ";" + str(point[0].error) + ";" + str(point[1].error) + "\n")
        file.close()

    def add(self, x, y):
        self.points += [[getDatum(x),getDatum(y)]]
        self.length += 1

    def remove(self, start, end=None):
        if not end:
            end = start
        if end<start:
            c = end
            end = start
            start = c
        if start<0 or self.length<start+1:
            return
        if end<0 or self.length<end+1:
            return
        self.points = self.points[0:start] + self.points[end+1:]
        self.length -= end - start + 1

    def getLinear(self):
        momenta = Momenta()
        for point in self.points:
            momenta.x += point[0].value
            momenta.y += point[1].value
            momenta.xx += point[0].value*point[0].value
            momenta.xy += point[0].value*point[1].value
            momenta.yy += point[1].value*point[1].value
        momenta.length = self.length
        return Linear(momenta)

    def getLogarithmic(self):
        momenta = Momenta()
        for point in self.points:
            momenta.x += log10(point[0].value)
            momenta.y += log10(point[1].value)
            momenta.xx += log10(point[0].value)*log10(point[0].value)
            momenta.xy += log10(point[0].value)*log10(point[1].value)
            momenta.yy += log10(point[1].value)*log10(point[1].value)
        momenta.length = self.length
        return Linear(momenta)

    def echo(self):
        for i in range(self.length):
            print(str(i) + ":\t" + str(self.points[i][0]) + "\t" + str(self.points[i][1]))
