#ifndef SerialIO_h
#define SerialIO_h

#include "Arduino.h"

class SerialIO
{
	private:
		int    _bufferSize;

	public:
		SerialIO();
		SerialIO(int bufferSize);
		void  message(const char *title, int value);
		void  message(const char *title, char *value);
		void  message(const char *title, int value, const char *unit);
		void  message(const char *title, long value, const char *unit);
		void  message(const char *title, const char *subtitle, int value, const char *unit);
		void  message(const char *title, const char *subtitle, long value, const char *unit);
		void  message(const char *title, const char *subtitle, float value, const char *unit);
		char *readline();
};

#endif