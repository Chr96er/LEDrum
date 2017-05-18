__author__ = 'Chris'
#import RPi.GPIO as GPIO
import pigpio
import sys

pi = pigpio.pi()

# Colors
GREEN = 0x00FF00
DARKGREEN = 0x009900
RED = 0xFF0000
DARKRED = 0xCC0000
BLUE = 0x0000FF
LIGHTRED = 0xFF0066
LIGHTBLUE = 0x0099FF
DARKBLUE = 0x000099
PURPLE = 0xCC00FF
ORANGE1 = 0xFFCC99
ORANGE2 = 0xFFCC00
ORANGE3 = 0xFF9900
YELLOW = 0xFFFF00

instColors1 = {
    '\x30':ORANGE1, #'tom1',
    '\x2d':ORANGE2, #'tom2',
    '\x2b':ORANGE3, #'tom3',
    '\x1a':LIGHTBLUE, #'hi-hat rim open',
    '\x2e':LIGHTBLUE, #'hi-hat head open',
    '\x16':BLUE, #'hi-hat rim close',
    '\x2a':BLUE, #'hi-hat head close',
    '\x31':RED, #'crash head',
    '\x37':DARKRED, #'crash rim',
    '\x33':DARKGREEN, #'ride head',
    '\x3b':GREEN, #'ride rim',
}

instRed2 = {
    '\x16':0xED4506, #'hi-hat rim close',
    '\x2a':0xED4506, #'hi-hat head close',
    '\x1a':0xF72506, #'hi-hat rim open',
    '\x2e':0xF72506, #'hi-hat head open',
    '\x30':0xE92525, #'tom1',
    '\x2d':0xFF4C4C, #'tom2',
    '\x2b':0xFF6B6B, #'tom3',
    '\x31':0xE00613, #'crash head',
    '\x37':0xE00613, #'crash rim',
    '\x3b':0xED7206, #'ride rim',
    '\x33':0xF72506, #'ride head',
}

instBlue = {
    '\x16':0x0099FF, #'hi-hat rim close',
    '\x2a':0x0099FF, #'hi-hat head close',
    '\x1a':0x0066FF, #'hi-hat rim open',
    '\x2e':0x0066FF, #'hi-hat head open',
    '\x30':0x6633FF, #'tom1',
    '\x2d':0x3333FF, #'tom2',
    '\x2b':0x0033FF, #'tom3',
    '\x31':0x0066FF, #'crash head',
    '\x37':0x6600FF, #'crash rim',
    '\x3b':0x3300FF, #'ride rim',
    '\x33':0x0000FF, #'ride head',
}

instRed = {
    '\x16':0xD30000, #'hi-hat rim close',
    '\x2a':0xD30000, #'hi-hat head close',
    '\x1a':0x9B0000, #'hi-hat rim open',
    '\x2e':0x9B0000, #'hi-hat head open',
    '\x30':0xE92525, #'tom1',
    '\x2d':0xFF4C4C, #'tom2',
    '\x2b':0xFF6B6B, #'tom3',
    '\x31':0xA80000, #'crash head',
    '\x37':0xA80000, #'crash rim',
    '\x3b':0x730000, #'ride rim',
    '\x33':0x360000, #'ride head',
}

colorSet = instBlue
if int(sys.argv[1]) == 0:
    colorSet = instBlue
elif int(sys.argv[1]) ==1:
    colorSet = instRed
elif int(sys.argv[1]) ==2:
    colorSet = instColors1
elif int(sys.argv[1]) ==3:
    colorSet = instRed2

inst = {
    '\x26':'snare',
    '\x28':'snare rim',
    '\x30':'tom1',
    '\x32':'tom1 rim',
    '\x2d':'tom2',
    '\x2f':'tom2 rim',
    '\x2b':'tom3',
    '\x3a':'tom3 rim',
    '\x24':'kick',
    '\x1a':'hi-hat rim open',
    '\x2e':'hi-hat head open',
    '\x16':'hi-hat rim close',
    '\x2a':'hi-hat head close',
    '\x2c':'hi-hat foot close',
    '\x31':'crash head',
    '\x37':'crash rim',
    '\x33':'ride head',
    '\x3b':'ride rim',
    '\x35':'ride bell',
    '\x39':'kick2',
}

bluedrums = {
    '\x16': 'hi-hat rim close',
    '\x2a': 'hi-hat head close',
    '\x33': 'ride head',
}

reddrums = {
    '\x31': 'crash head',
    '\x37': 'crash rim',
}

greendrums = {
    '\x3b': 'ride rim',
}

purpledrums = {
    '\x1a': 'hi-hat rim open',
    '\x2e': 'hi-hat head open',
}

boosters = {
    '\x26': 'snare',
    '\x24': 'kick',
    '\x39': 'kick2',
}

def resetAll():
    pi.set_PWM_dutycycle(RED_PIN, 0)
    pi.set_PWM_dutycycle(GREEN_PIN, 0)
    pi.set_PWM_dutycycle(BLUE_PIN, 0)


def colorGpioOutputAndPrint(pin, brightness):
    resetAll()
    pi.set_PWM_dutycycle(pin, brightness)
    print("Pin: " + str(pin) + ", brightness: " + str(brightness))

def hexOutputAndPrintCurrentColor():

    hex = current_color

    r = int(int(( hex >> 16 ) & 0xFF) * (float(bright) / 255.0))
    g = int(int(( hex >> 8 ) & 0xFF) * (float(bright) / 255.0))
    b = int(int(( hex & 0xFF) * (float(bright) / 255.0)))

    pi.set_PWM_dutycycle(RED_PIN, r)
    print("Red, brightness: " + str(r))

    pi.set_PWM_dutycycle(GREEN_PIN, g)
    print("Green, brightness: " + str(g))

    pi.set_PWM_dutycycle(BLUE_PIN, b)
    print("Blue, brightness: " + str(b))

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


f = open('/dev/snd/midiC1D0')

note = False


# Initialize lights
RED_PIN = 22
GREEN_PIN = 23
BLUE_PIN = 24
current_color = 0x00FF000
previous_color = current_color
bright = 100
silence = 0 #amount of 300ms there has been silence
BRIGHTNESS_INCREASEMENT = 3
BRIGHTNESS_DECREASEMENT = 3

while True:
    b = f.read(1)
    if bright <> 100:
        bright = max(bright - 50 * silence, 100)
        hexOutputAndPrintCurrentColor()

    # if backup_color <> current_color:
    #     backup_color = current_color
    #     hexOutputAndPrintCurrentColor()

    if b == '\xfe':
        #No input message received via midi every .3 seconds
        silence += 1
        print("Silence")

    # GPIO.output(GPIO_NUM, False)
    else:
        #               if b == '\x40':
        #                       print hex(ord(b))
        #               else:
        #                       print hex(ord(b)),
        silence = 0
        if b == '\x99':
            note = True
        elif note:
            if b in inst:
                print inst[b]

                # Main functionality here!
                if b in boosters:
                    bright = 250
                    hexOutputAndPrintCurrentColor()
                    bright = 100

                elif b in colorSet:
                    current_color = colorSet[b]
            else:
                print hex(ord(b))

            note = False


    hexOutputAndPrintCurrentColor()
    previous_color = current_color