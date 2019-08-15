#include <string.h>
#include <Wire.h>
#include <BMP180.h>
#include <MemoryFree.h>
#include <SerialIO.h>
#include <c_StringArray.h>

const char *COMMAND_CONNECT = "CONNECT";
const char *COMMAND_DISCONNECT = "DISCONNECT";
const char *COMMAND_BLINK = "BLINK";
const char *COMMAND_BMP180 = "BMP180";

const char *RESPONSE_CONNECT = "CONNECTED";
const char *RESPONSE_DISCONNECT = "DISCONNECTED";
const char *RESPONSE_BLINK = "BLINKING";
const char *RESPONSE_BMP180 = "BMP180";
const char *RESPONSE_NOT_FOUND = "COMMAND NOT FOUND";

const char *MESSAGE_INITIALIZING = "INITIALIZING ARDUINO";
const char *MESSAGE_BMP180_ERROR = "BMP180 INITIALIZATION ERROR";
const char *MESSAGE_MEMORY = "MEMORY";
const char *MESSAGE_WAITING = "WAITING";
const char *MESSAGE_RECEIVED = "RECEIVED";
const char SPACE = ' ';
const char NEW_LINE = '\n';
const char NULL_CHAR = '\x00';

const int BLINKING_PIN = 53;
BMP180 bmp(BMP180_ULTRAHIGHRES);

unsigned long loopCount;
SerialIO port(10);

void parseCommand(char *line)
{
  c_StringArray components = c_StringArray::split(SPACE,line);
  
  if(components.size()>0)
  {
    char *command = components.upper(0);
    char *full_command = components.join(SPACE);
    
    port.message(MESSAGE_RECEIVED,full_command);
    
    if(strcmp(command,COMMAND_CONNECT)==0)
    {
      Serial.println(RESPONSE_CONNECT);
    }
    else if(strcmp(command,COMMAND_DISCONNECT)==0)
    {
      Serial.println(RESPONSE_DISCONNECT);
    }
    else if(strcmp(command,COMMAND_BLINK)==0)
    {
      pinBlink(components);
    }
    else if(strcmp(command,COMMAND_BMP180)==0)
    {
      getBmp180(components);
    }
    else
    {
      Serial.println(RESPONSE_NOT_FOUND);
    }
    
    free(command);
    free(full_command);
    components.destroy();
  }
}

void setup()
{
  Serial.begin(9600);
  Serial.setTimeout(-1l);
  port.message(MESSAGE_INITIALIZING,ARDUINO);
  pinMode(BLINKING_PIN,OUTPUT);
  while(!bmp.begin())
  {
    Serial.println(MESSAGE_BMP180_ERROR);
    delay(5000);
  }
  loopCount = 0;
}

void loop()
{
  port.message(MESSAGE_MEMORY,freeMemory());
  port.message(MESSAGE_WAITING,++loopCount);
  char *command = port.readline();
  parseCommand(command);
  //Serial.println(command);
  free(command);
}
