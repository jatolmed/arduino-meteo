#!/usr/bin/python3
#-*- coding: utf-8 -*-
import math
from statistics.datum import Datum


temp_filename = "datos/temperatura.dat"
pres_filename = "datos/presion.dat"

temp_out_filename = "datos/temperatura_proc.dat"
pres_out_filename = "datos/presion_proc.dat"
dens_out_filename = "datos/densidad_proc.dat"

R = Datum(8.314472,0.000001)
M = Datum(0.78084,0.00001) * Datum(14.007,0.001)*2 \
	+ Datum(0.20946,0.00001) * Datum(15.999,0.001)*2 \
	+ Datum(0.00934,0.00001) * Datum(39.948,0.001) \
	+ Datum(0.0004,0.0001) * (Datum(15.999,0.001)*2+Datum(12.011,0.001)) \
	+ Datum(0.00000524,0.00000001) * Datum(4.0026,0.0001)


time_width = 15 / 60 / 24

def is_valid(line):
	if line[-1:]=="\n":
		line = line[:-1]
	comp = line.split(" ")
	return len(comp)==4

def get_datum(line):
	if line[-1:]=="\n":
		line = line[:-1]
	comp = line.split(" ")
	time = Datum(comp[0],comp[2])
	data = Datum(comp[1],comp[3])
	return [time,data]


with open(temp_filename,"r") as temp_file, \
	open(pres_filename,"r") as pres_file, \
	open(temp_out_filename,"w") as temp_out, \
	open(pres_out_filename,"w") as pres_out, \
	open(dens_out_filename,"w") as dens_out:

	temp_data = map(get_datum,filter(is_valid,temp_file.readlines()))
	pres_data = map(get_datum,filter(is_valid,pres_file.readlines()))

	data = []
	for temp in temp_data:
		for pres in pres_data:
			if pres[0]==temp[0]:
				if pres[0]!=None \
					and pres[1]!=None \
					and temp[0]!=None \
					and temp[1]!=None:
					datum = [(pres[0]+temp[0])/2.0, \
						temp[1], \
						pres[1]]
					data += [datum]
					break

	print("Procesando " + str(len(data)) + " registros...")
	time = Datum(0.0,0.0)
	temp = Datum(0.0,0.0)
	pres = Datum(0.0,0.0)
	time1 = data[0][0].value
	count = 0
	for index,datum in enumerate(data):
		time2 = datum[0].value
		if time2-time1>time_width:
			time.error = math.sqrt((time.error - time.value*time.value/count)/(count-1))
			time.value /= count
			temp.value /= temp.error
			pres.value /= pres.error
			temp.error = 1.0/math.sqrt(temp.error)
			pres.error = 1.0/math.sqrt(pres.error)
			dens = pres/R/(temp+273.15)*M/1000.0
			temp_out.write(str(time.value) + " " + str(temp.value) + " " + str(time.error) + " " + str(temp.error) + "\n")
			pres_out.write(str(time.value) + " " + str(pres.value) + " " + str(time.error) + " " + str(pres.error) + "\n")
			dens_out.write(str(time.value) + " " + str(dens.value) + " " + str(time.error) + " " + str(dens.error) + "\n")
			time = Datum(0.0,0.0)
			temp = Datum(0.0,0.0)
			pres = Datum(0.0,0.0)
			time1 = time2
			count = 0
		time.value += datum[0].value
		time.error += datum[0].value*datum[0].value
		temp.value += datum[1].value/datum[1].error/datum[1].error
		pres.value += datum[2].value/datum[2].error/datum[2].error
		temp.error += 1.0/datum[1].error/datum[1].error
		pres.error += 1.0/datum[2].error/datum[2].error
		count += 1

	temp_file.close()
	pres_file.close()
	temp_out.close()
	pres_out.close()
	dens_out.close()