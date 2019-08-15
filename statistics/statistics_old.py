# -*- coding: utf-8 -*-
from math import sqrt
from os.path import isfile
from .datum import Datum,getDatum


class Linear(object):

    def __init__(self):
        self.a = Datum()
        self.b = Datum()
        self.r = None

    def echo(self):
        print("Coeficiente de correlación: " + str(self.r))
        print("Pendiente: " + str(self.a))
        print("Ordenada en el origen: " + str(self.b))


class Momenta(object):

    def __init__(self):
        self.x = 0
        self.y = 0
        self.xx = 0
        self.xy = 0
        self.yy = 0


class DataBunch(object):

    def __init__(self, filename=''):
        self.points = []
        self.length = 0
        self.sums = Momenta()
        self.load(filename)

    def addPoint(self, x, y):
        dx = getDatum(x)
        dy = getDatum(y)
        self.points += [[dx,dy]]
        self.length += 1
        self.sums.x += dx.value
        self.sums.y += dy.value
        self.sums.xx += dx.value*dx.value
        self.sums.xy += dx.value*dy.value
        self.sums.yy += dy.value*dy.value

    def removePoints(self, start, end=None):
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
        for point in self.points[start:end+1]:
            self.sums.x -= point[0].value
            self.sums.y -= point[1].value
            self.sums.xx -= point[0].value*point[0].value
            self.sums.xy -= point[0].value*point[1].value
            self.sums.yy -= point[1].value*point[1].value
        self.points = self.points[0:start] + self.points[end+1:]
        self.length -= end - start + 1

    def echo(self):
        for i in range(self.length):
            print(str(i) + ":\t" + str(self.points[i][0]) + "\t" + str(self.points[i][1]))
        print("sum(x)   = " + str(self.sums.x))
        print("sum(y)   = " + str(self.sums.y))
        print("sum(x^2) = " + str(self.sums.xx))
        print("sum(xy)  = " + str(self.sums.xy))
        print("sum(y^2) = " + str(self.sums.yy))

    def save(self, filename):
        if isfile(filename):
            print("El archivo '" + filename + "' ya existe.")
        else:
            file = open(filename,"w")
            for point in self.points:
                file.write(str(point[0].value) + ";" + str(point[1].value) + ";" + str(point[0].error) + ";" + str(point[1].error) + "\n")
            file.close()

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
                    self.addPoint(x,y)
            file.close()

    def vOffset(self):
        if self.length<3:
            return None
        linear = Linear()
        d = self.sums.xx - self.sums.x*self.sums.x/self.length
        linear.a.value = (self.sums.xy - self.sums.x*self.sums.y/self.length)/d
        linear.b.value = (self.sums.y*self.sums.xx - self.sums.x*self.sums.xy)/d/self.length
        sy2 = self.sums.yy - 2*linear.a.value*self.sums.xy - 2*linear.b.value*self.sums.y + linear.a.value*linear.a.value*self.sums.xx + 2*linear.a.value*linear.b.value*self.sums.x + linear.b.value*linear.b.value*self.length
        sy2 /= self.length - 2
        linear.a.error = sqrt(sy2/d)
        linear.b.error = linear.a.error*sqrt(self.sums.xx/self.length);
        linear.r = (self.sums.xy - self.sums.x*self.sums.y/self.length)/sqrt(d*(self.sums.yy - self.sums.y*self.sums.y/self.length))
        return linear
