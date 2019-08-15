# Arduino Meteorological Station

This project runs in an Arduino with a BMP180 chip and retrieves and stores the air temperature and presure in a computer connected to it via the Arduino serial port. In order to achieve this it maintains a continuous comunication with the computer thanks to the [client.py](client.py) script.

The [procesar_datos.py](procesar_datos.py) script is prepared to proccess the raw data and get quantities like the air density.

## Third party libraries

The following third party libraries are used (and not included) in this project, and are needed to make it work:

* [Arduino-MemoryFree](https://github.com/mpflaga/Arduino-MemoryFree), by [Michael P. Flaga](https://github.com/mpflaga). Needed to monitor free memory.
* [BMP180](https://github.com/enjoyneering/BMP180), by [enjoyneering](https://github.com/enjoyneering). Needed to use the BMP180 chip.

Thanks to them for such invaluable work.