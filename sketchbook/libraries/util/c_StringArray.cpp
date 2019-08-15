#include "Arduino.h"
#include "c_StringArray.h"
#include "string.h"

const char __c_string_array_NULL_CHAR = '\x00';

const int __c_string_array_CHARP_SIZE = sizeof(char*);
const int __c_string_array_CHAR_SIZE = sizeof(char);
const int __c_string_array_INT_SIZE = sizeof(int);

c_StringArray::c_StringArray()
{
	_size = 0;
}

c_StringArray::c_StringArray(int size)
{
	_size = size;
	_elements = (char **)malloc(size*__c_string_array_CHARP_SIZE);
	_lengths = (int *)malloc(size*__c_string_array_INT_SIZE);
}

char *c_StringArray::emptyString()
{
	char *result = (char *)malloc(__c_string_array_CHAR_SIZE);
	memcpy(result,&__c_string_array_NULL_CHAR,__c_string_array_CHAR_SIZE);
	return result;
}

char *c_StringArray::string(int index)
{
	if(index<0 || index>=_size)
	{
		return emptyString();
	}
	char *result = (char *)malloc((_lengths[index]+1)*__c_string_array_CHAR_SIZE);
	memcpy(result,_elements[index],(_lengths[index]+1)*__c_string_array_CHAR_SIZE);
	return result;
}

char *c_StringArray::upper(int index)
{
	if(index<0 || index>=_size)
	{
		return emptyString();
	}
	char *result = (char *)malloc((_lengths[index]+1)*__c_string_array_CHAR_SIZE);
	memcpy(result,_elements[index],(_lengths[index]+1)*__c_string_array_CHAR_SIZE);
	int i;
	for(i=0; i<_lengths[index]; i++)
	{
		if(result[i]>='a' && result[i]<='z')
		{
			result[i] -= 'a' - 'A';
		}
	}
	return result;
}

char *c_StringArray::lower(int index)
{
	if(index<0 || index>=_size)
	{
		return emptyString();
	}
	char *result = (char *)malloc((_lengths[index]+1)*__c_string_array_CHAR_SIZE);
	memcpy(result,_elements[index],(_lengths[index]+1)*__c_string_array_CHAR_SIZE);
	int i;
	for(i=0; i<_lengths[index]; i++)
	{
		if(result[i]>='A' && result[i]<='Z')
		{
			result[i] += 'a' - 'A';
		}
	}
	return result;
}

int c_StringArray::integer(int index)
{
	if(index<0 || index>=_size)
	{
		return 0;
	}
	return atoi(_elements[index]);
}

char **c_StringArray::strings()
{
	return _elements;
}

int c_StringArray::size()
{
	return _size;
}

int c_StringArray::length(int index)
{
	if(index<0 || index>=_size)
	{
		return 0;
	}
	return _lengths[index];
}

char *c_StringArray::join(char delimiter)
{
	int  i;
	int  len = 0;
	for(i=0; i<_size; i++)
	{
		len += _lengths[i];
	}
	
	char *result = (char *)malloc((len+_size+1)*__c_string_array_CHAR_SIZE);
	len = 0;
	for(i=0; i<_size; i++)
	{
		if(i>0)
		{
			memcpy(result+len,&delimiter,__c_string_array_CHAR_SIZE);
			len++;
		}
		memcpy(result+len,_elements[i],(_lengths[i]+1)*__c_string_array_CHAR_SIZE);
		len += _lengths[i];
	}
	return result;
}

void c_StringArray::putSubstring(int index, int start, int end, char *string)
{
	int length = end-start;
	_elements[index] = (char *)malloc((length+1)*__c_string_array_CHAR_SIZE);
	memcpy(_lengths+index,&length,__c_string_array_INT_SIZE);
	memcpy(_elements[index],string+start,length*__c_string_array_CHAR_SIZE);
	memcpy(_elements[index]+length,&__c_string_array_NULL_CHAR,__c_string_array_CHAR_SIZE);
}

c_StringArray c_StringArray::split(char delimiter, char *string)
{
	int  i;
	int  len = strlen(string);
	int  count = 0;
	bool ignoring = true;
	for(i=0; i<len; i++)
	{
		if(ignoring && string[i]!=delimiter)
		{
			count++;
			ignoring = false;
		}
		else if(!ignoring && string[i]==delimiter)
		{
			ignoring = true;
		}
	}

	c_StringArray result(count);

	ignoring = true;
	int   idx = 0;
	int   start = 0;
	for(i=0; i<len; i++)
	{
		if(ignoring && string[i]!=delimiter)
		{
			ignoring = false;
			start = i;
		}
		else if(!ignoring && string[i]==delimiter)
		{
			result.putSubstring(idx,start,i,string);
			ignoring = true;
			idx++;
		}
	}
	if(idx<count)
	{
		result.putSubstring(idx,start,len,string);
	}
	return result;
}

void c_StringArray::destroy()
{
	int i;
	for(i=0; i<_size; i++)
	{
		free(_elements[i]);
	}
	free(_elements);
	free(_lengths);
}