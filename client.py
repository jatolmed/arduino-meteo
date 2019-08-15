#!/usr/bin/python3
#-*- coding: utf-8 -*-
import sys
import signal
import serial
import time
import datetime

DEVICE = "/dev/ttyACM0"
BAUD_RATE = 9600

temperature_output = "datos/temperatura.dat"
pressure_output = "datos/presion.dat"
log_output = "datos/requests.log"

COMMAND_CONNECT = "CONNECT"
COMMAND_DISCONNECT = "DISCONNECT"
COMMAND_BMP180 = "BMP180"

RESPONSE_CONNECT = "CONNECTED"
RESPONSE_WAITING = "WAITING"
RESPONSE_DISCONNECT = "DISCONNECTED"
RESPONSE_BMP180 = "BMP180"
BMP180_TEMPERATURE = "TEMPERATURE"
BMP180_PRESSURE = "PRESSURE"

BMP180_TEMPERATURE_ERROR = 1
BMP180_PRESSURE_ERROR = 100

UPDATE_TIME = 60

def get_next_command():
	time.sleep(UPDATE_TIME)
	return COMMAND_BMP180


def write_to_serial(port, command):
	if command[-1:]!="\n":
		command += "\n"
	port.write(command.encode("utf-8"))
	port.flush()

def read_from_serial(port):
	read = port.readline().decode("utf-8").strip()
	log(read)
	return read


def connect(port):
	if port and port.is_open:
		port.flushInput()
		write_to_serial(port,COMMAND_CONNECT)
		read = read_from_serial(port)
		while read!=RESPONSE_CONNECT:
			read = read_from_serial(port)

def disconnect(port):
	if port and port.is_open:
		write_to_serial(port,COMMAND_DISCONNECT)
		read = read_from_serial(port)
		while read!=RESPONSE_DISCONNECT:
			read = read_from_serial(port)

def close_and_exit(event,frame):
	if port and port.is_open:
		port.close()
	if not temp_file.closed:
		temp_file.close()
	if not pres_file.closed:
		pres_file.close();
	if not log_file.closed:
		log_file.close();
	exit()

signal.signal(signal.SIGINT,close_and_exit)


def write_value(file, value):
	if not file.closed:
		days = time.time() / 3600.0 / 24.0
		file.write(str(days) + " " + str(value) + "\n")
		file.flush()

def write_value_error(file, time, value, time_error, value_error):
	if not file.closed:
		file.write(str(float(time)/86400.0) + " " + str(value) + " " + str(float(time_error)/86400.0) + " " + str(value_error) + "\n")
		file.flush()


def log(text):
	if log_file and not log_file.closed:
		now = datetime.datetime.now()
		log_file.write(now.strftime("[%Y-%m-%dT%H:%M:%S%Z] ") + text + "\n")
		log_file.flush()


with serial.Serial(DEVICE,BAUD_RATE) as port, \
	open(temperature_output,"a+") as temp_file, \
	open(pressure_output,"a+") as pres_file, \
	open(log_output,"a+") as log_file:

	if not port.is_open:
		port.open()

	time.sleep(1)

	t1 = time.time()

	connect(port)
	read = read_from_serial(port)
	while read!=RESPONSE_DISCONNECT:
		components = read.split(" ")
		if len(components)>0:
			if components[0]==RESPONSE_WAITING:
				write = get_next_command()
				write_to_serial(port,write)
				t1 = time.time()
			if components[0]==RESPONSE_BMP180 and len(components)>2:
				if components[1]==BMP180_TEMPERATURE:
					t2 = time.time()
					write_value_error(temp_file,(t1+t2)/2.0,components[2],(t2-t1)/2.0,BMP180_TEMPERATURE_ERROR)
				if components[1]==BMP180_PRESSURE:
					t2 = time.time()
					write_value_error(pres_file,(t1+t2)/2.0,components[2],(t2-t1)/2.0,BMP180_PRESSURE_ERROR)
			if components[0]==RESPONSE_DISCONNECT:
				break
		read = read_from_serial(port)

	close_and_exit()