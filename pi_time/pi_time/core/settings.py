 
METRIC = 'SI' # Report speed in km/h|m/s, distance in metres.
IMPERIAL = 'IM' # Report speed in m/h|y/s, distance in yards.
UNIT_OF_MEASUREMENT = (
    (METRIC, 'Metric'),
    (IMPERIAL, 'Imperial')
)

SENSOR_HW_RPI = 'RPI'
SENSOR_HW = (
    (SENSOR_HW_RPI, 'Raspberry Pi'),
)

# TODO: Not sure if neeeded?
#SENSOR_TYPE_INFRARED_ACTIVE = 'AIR' 
#SENSOR_TYPE_INFRARED_PASSIVE = 'PIR' 
#SENSOR_TYPE_RADIO = 'RAD' 
#SENSOR_TYPE = ( # Defines the hardware used by sensor TODO: i18n
#    (SENSOR_TYPE_INFRARED_ACTIVE, 'Active Infrared'),
#    (SENSOR_TYPE_INFRARED_PASSIVE, 'Passive Infrared'),    
#)

SENSOR_POS_START = 'ST' # Starting line
SENSOR_POS_FINISH = 'FIN' # Finishing line
SENSOR_POS_START_FINISH = 'SF' # Both start and finish line
SENSOR_POS_SECTOR = 'SEC' # Sector position (neither start nor finish)
SENSOR_POS = ( # Defines the sensor position on track TODO: i18n
    (SENSOR_POS_START, 'Start'),
    (SENSOR_POS_FINISH, 'Finish'),
    (SENSOR_POS_START_FINISH, 'Start and finish'),
    (SENSOR_POS_SECTOR, 'Sector checkpoint (split times)'),
)

RPI_GPIO_LAYOUT = ( # Raspberry Pi - http://pi.gadgetoid.com/pinout
    (3, '3 = GPIO 2'),
    (5, '5 = GPIO 3'),
    (7, '7 = GPIO 4 (GPCLK0)'),
    (8, '8 = GPIO 14 (UART0_TXD)'),
    (10, '10 = GPIO 15 (UART0_RXD)'),
    (11, '11 = GPIO 17'),
    (12, '12 = GPIO 18 (PCMCLK)'),
    (13, '13 = GPIO 27'),
    (15, '14 = GPIO 22'),
    (16, '15 = GPIO 23'),
    (18, '18 = GPIO 24'),
    (19, '19 = GPIO 10 (SPI0_MOSI)'),
    (21, '21 = GPIO 9 (SPI0_MISO '),
    (22, '22 = GPIO 25'),
    (23, '23 = GPIO 11 (SPI0_SCLK)'),
    (24, '24 = GPIO 8 (SPI0_CE0_N)'),
    (26, '26 = GPIO 7 (SPI0_CE1_N)')
)
