import adafruit_irremote
import board
import digitalio
import microcontroller
import pulseio
import time

# For most CircuitPython boards:
led = digitalio.DigitalInOut(board.LED)
# For QT Py M0:
# led = digitalio.DigitalInOut(board.SCK)
led.switch_to_output()

pulsein = pulseio.PulseIn(board.IR_RX, maxlen=120, idle_state=True)
decoder = adafruit_irremote.GenericDecode()

# Power button turned on
#>>> pulses
#[9014, 4416, 619, 510, 619, 508, 590, 1642, 616, 511, 598, 504, 625, 502, 585, 544, 595, 505, 624, 1633, 594, 1638, 590, 538, 590, 1640, 587, 1644, 624, 1633, 595, 1635, 611, 1619, 620, 508, 589, 539, 590, 511, 618, 511, 618, 511, 597, 504, 615, 1643, 595, 506, 623, 1634, 592, 1639, 588, 1642, 616, 1641, 597, 1633, 583, 1648, 621, 508, 590, 1640, 618]
#>>>

# What we should get back from decode but aren't
# IRMessage(pulses=(9014, 4416, 619, 510, 619, 508, 590, 1642, 616, 511, 598, 504, 625, 502, 585, 544, 595, 505, 624, 1633, 594, 1638, 590, 538, 590, 1640, 587, 1644, 624, 1633, 595, 1635, 611, 1619, 620, 508, 589, 539, 590, 511, 618, 511, 618, 511, 597, 504, 615, 1643, 595, 506, 623, 1634, 592, 1639, 588, 1642, 616, 1641, 597, 1633, 583, 1648, 621, 508, 590, 1640, 618), code=(223, 32, 253, 2))
try:
    with open("codes.txt", "a") as output:
        while True:
            pulses = decoder.read_pulses(pulsein)
            try:
                received_code = decoder.decode_bits(pulses)
                output.write(pulses)
            except adafruit_irremote.IRNECRepeatException:
                continue
            except adafruit_irremote.IRDecodeException as e:
                print("Failed to decode: ", e.args)
                continue

            output.write("NEC Infrared code received: ", received_code)
            output.flush()
except OSError as e:  # Typically when the filesystem isn't writeable...
    delay = 0.5  # ...blink the LED every half second.
    if e.args[0] == 28:  # If the file system is full...
        delay = 0.25  # ...blink the LED faster!
    while True:
        led.value = not led.value
        time.sleep(delay)
