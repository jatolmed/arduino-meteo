#include "Arduino.h"
#include "SerialIO.h"

const char __serial_SPACE = ' ';
const char __serial_NEW_LINE = '\n';
const char __serial_NULL_CHAR = '\x00';
const int __serial_DEFAULT_BUFFER_SIZE = 10;

SerialIO::SerialIO()
{
	SerialIO(__serial_DEFAULT_BUFFER_SIZE);
}

SerialIO::SerialIO(int bufferSize)
{
	_bufferSize = bufferSize;
}

void SerialIO::message(const char *title, int value)
{
	Serial.print(title);
	Serial.print(__serial_SPACE);
	Serial.println(value);
}

void SerialIO::message(const char *title, char *value)
{
	Serial.print(title);
	Serial.print(__serial_SPACE);
	Serial.println(value);
}

void SerialIO::message(const char *title, int value, const char *unit)
{
	Serial.print(title);
	Serial.print(__serial_SPACE);
	Serial.print(value);
	Serial.print(__serial_SPACE);
	Serial.println(unit);
}

void SerialIO::message(const char *title, long value, const char *unit)
{
	Serial.print(title);
	Serial.print(__serial_SPACE);
	Serial.print(value);
	Serial.print(__serial_SPACE);
	Serial.println(unit);
}

void SerialIO::message(const char *title, const char *subtitle, int value, const char *unit)
{
	Serial.print(title);
	Serial.print(__serial_SPACE);
	Serial.print(subtitle);
	Serial.print(__serial_SPACE);
	Serial.print(value);
	Serial.print(__serial_SPACE);
	Serial.println(unit);
}

void SerialIO::message(const char *title, const char *subtitle, long value, const char *unit)
{
	Serial.print(title);
	Serial.print(__serial_SPACE);
	Serial.print(subtitle);
	Serial.print(__serial_SPACE);
	Serial.print(value);
	Serial.print(__serial_SPACE);
	Serial.println(unit);
}

void SerialIO::message(const char *title, const char *subtitle, float value, const char *unit)
{
	Serial.print(title);
	Serial.print(__serial_SPACE);
	Serial.print(subtitle);
	Serial.print(__serial_SPACE);
	Serial.print(value);
	Serial.print(__serial_SPACE);
	Serial.println(unit);
}

char *SerialIO::readline()
{
	int currentPosition = 0;

	char *buffer = (char *)malloc(_bufferSize*sizeof(char));
	int bytes = Serial.readBytesUntil(__serial_NEW_LINE,buffer,_bufferSize);

	int totalSize = bytes;
	char *result = (char *)malloc((totalSize+1)*sizeof(char));
	memcpy(result,buffer,totalSize);
	while(bytes==_bufferSize)
	{
		bytes = Serial.readBytesUntil(__serial_NEW_LINE,buffer,_bufferSize);

		currentPosition = totalSize;
		totalSize += bytes;

		result = (char *)realloc(result,(totalSize+1)*sizeof(char));
		memcpy(result+currentPosition,buffer,bytes);
	}
	result[totalSize] = __serial_NULL_CHAR;

	free(buffer);
	return result;
}