import pulseio
import board
import adafruit_irremote

pulsein = pulseio.PulseIn(board.IR_RX, maxlen=120, idle_state=True)
decoder = adafruit_irremote.GenericDecode()

# Power button turned on
#>>> pulses
#[9014, 4416, 619, 510, 619, 508, 590, 1642, 616, 511, 598, 504, 625, 502, 585, 544, 595, 505, 624, 1633, 594, 1638, 590, 538, 590, 1640, 587, 1644, 624, 1633, 595, 1635, 611, 1619, 620, 508, 589, 539, 590, 511, 618, 511, 618, 511, 597, 504, 615, 1643, 595, 506, 623, 1634, 592, 1639, 588, 1642, 616, 1641, 597, 1633, 583, 1648, 621, 508, 590, 1640, 618]
#>>>

# What we should get back from decode but aren't
# IRMessage(pulses=(9014, 4416, 619, 510, 619, 508, 590, 1642, 616, 511, 598, 504, 625, 502, 585, 544, 595, 505, 624, 1633, 594, 1638, 590, 538, 590, 1640, 587, 1644, 624, 1633, 595, 1635, 611, 1619, 620, 508, 589, 539, 590, 511, 618, 511, 618, 511, 597, 504, 615, 1643, 595, 506, 623, 1634, 592, 1639, 588, 1642, 616, 1641, 597, 1633, 583, 1648, 621, 508, 590, 1640, 618), code=(223, 32, 253, 2))

while True:
    with open("codes.txt", "a") as output:
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
