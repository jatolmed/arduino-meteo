#ifndef c_StringArray_h
#define c_StringArray_h

#include "Arduino.h"

class c_StringArray
{
	private:
		char **_elements;
		int    _size;
		int   *_lengths;
		void   putSubstring(int index, int start, int end, char *string);
		char  *emptyString();

	public:
		c_StringArray();
		c_StringArray(int size);
		void   destroy();
		char  *string(int index);
		char  *upper(int index);
		char  *lower(int index);
		int    integer(int index);
		char **strings();
		int    size();
		int    length(int index);
		char  *join(char delimiter);
		static c_StringArray split(char delimiter, char *string);
};

#endif