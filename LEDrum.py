__author__ = 'Chris'
__credits__ = ['Jeremy Blythe']

#Based on instructions on Jeremy's blog: http://jeremyblythe.blogspot.com.au/2013/03/raspberry-pi-midi-driven-solenoid-bell.html

import pigpio
import sys

pi = pigpio.pi()

#set default parameters
DEFAULT_BRIGHTNESS = 100

# define colors
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

# define color sets
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

# default color set is blue if no parameter provided
colorSet = instBlue
if int(sys.argv[1]) == 0:
    colorSet = instBlue
elif int(sys.argv[1]) ==1:
    colorSet = instRed
elif int(sys.argv[1]) ==2:
    colorSet = instColors1
elif int(sys.argv[1]) ==3:
    colorSet = instRed2

# define instrument, depends on midi device
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

#these will increase the brightness for a short time
boosters = {
    '\x26': 'snare',
    '\x24': 'kick',
    '\x39': 'kick2',
}

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

#open device, midi device specific
f = open('/dev/snd/midiC1D0')

note = False

# Initialize lights
RED_PIN = 22
GREEN_PIN = 23
BLUE_PIN = 24
current_color = 0x00FF000
bright = DEFAULT_BRIGHTNESS
gradiantBrightness = False
silence = 0 #factor of .3 seconds there has been silence

while True:
    b = f.read(1)
    if bright > 100 and not gradiantBrightness:
        #decrease brightness by 50 every .3 seconds
        bright = max(bright - 50 * silence, 100)
        hexOutputAndPrintCurrentColor()

    if b == '\xfe':
        #No input message received via midi every .3 seconds
        silence += 1
        print("Silence")

    else:
        silence = 0
        if b == '\x99':
            note = True
        elif note:
            if b in inst:
                print(inst[b])

                # boost light or change color
                if b in boosters:
                    bright = 250
                    hexOutputAndPrintCurrentColor()
                    if gradiantBrightness:
                        bright = DEFAULT_BRIGHTNESS

                elif b in colorSet:
                    current_color = colorSet[b]
            else:
                print(hex(ord(b)))

            note = False

    hexOutputAndPrintCurrentColor()
