from machine import Pin, SPI
import time




class MAX6675:
    def __init__(self, spi_id=1, cs_pin=16, sck_pin=18, miso_pin=17, mosi_pin=23):
        # Initialisiere SPI
        self.spi = SPI(spi_id, baudrate=5000000, polarity=0, phase=0, bits=8, firstbit=SPI.MSB,
                       sck=Pin(sck_pin), mosi=Pin(mosi_pin), miso=Pin(miso_pin))
        # Chip-Select Pin
        self.cs = Pin(cs_pin, Pin.OUT)
        self.cs.value(1)  # CS auf High (inaktiv)

    def read_temperature(self):
        self.cs.value(0)  # CS aktivieren
        time.sleep_us(10)  # kleiner Delay (wichtig für Timing)
        raw = self.spi.read(2)
        self.cs.value(1)  # CS deaktivieren

        if raw is None:
            return None

        value = (raw[0] << 8) | raw[1]

        # Check auf offenen Thermocouple
        if value & 0x4:
            return None

        # Temperatur in °C berechnen
        temperature = (value >> 3) * 0.25
        return temperature

    def deinit(self):
        self.spi.deinit()


