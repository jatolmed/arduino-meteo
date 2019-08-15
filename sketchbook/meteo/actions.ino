/**
 * Blink a LED
 */
const char *BLINK_UNIT = "TIMES";

void pinBlink(c_StringArray args)
{
  int times = 6;
  if(args.size()>1)
  {
    times = args.integer(1);
  }
  port.message(RESPONSE_BLINK,times,BLINK_UNIT);
  int i;
  times *= 2;
  for(i=0; i<=times; i++)
  {
    if(i%2==0)
    {
      digitalWrite(BLINKING_PIN,LOW);
    }
    else
    {
      digitalWrite(BLINKING_PIN,HIGH);
    }
    delay(500);
  }
}

/**
 * Measure temperature and pressure
 */
const char *BMP180_TEMPERATURE = "TEMPERATURE";
const char *BMP180_PRESSURE = "PRESSURE";
const char *BMP180_ALL_SENSORS = "ALL";
const char *BPM180_TEMPERATURE_UNIT = "CELSIUS";
const char *BMP180_PRESSURE_UNIT = "PASCALS";

void getBmp180(c_StringArray args)
{
  digitalWrite(BLINKING_PIN,HIGH);
  char *datum = args.upper(1);
  if(args.size()<2
    || strcmp(datum,BMP180_ALL_SENSORS)==0
    || strcmp(datum,BMP180_TEMPERATURE)==0)
  {
    float celsius = bmp.getTemperature();
    port.message(RESPONSE_BMP180,BMP180_TEMPERATURE,celsius,BPM180_TEMPERATURE_UNIT);
  }
  if(args.size()<2
    || strcmp(datum,BMP180_ALL_SENSORS)==0
    || strcmp(datum,BMP180_PRESSURE)==0)
  {
    long pascals = bmp.getPressure();
    port.message(RESPONSE_BMP180,BMP180_PRESSURE,pascals,BMP180_PRESSURE_UNIT);
  }
  digitalWrite(BLINKING_PIN,LOW);
  free(datum);
}
