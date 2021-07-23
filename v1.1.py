# Copyright (c) 2017 Adafruit Industries
# Author: Tony DiCola & James DeVito
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
from gpiozero import Button
import time
import os
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess

# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

btnUP = Button(26)
btnDOWN = Button(19)
btnLEFT = Button(13)
btnRIGHT = Button(6)
btnRESET = Button(5)
btnSET = Button(0)
btnMID = Button(1)

# Beaglebone Black pin configuration:
# RST = 'P9_12'
# Note the following are only used with SPI:
# DC = 'P9_15'
# SPI_PORT = 1
# SPI_DEVICE = 0

# 128x32 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

# 128x64 display with hardware I2C:
# disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

# Note you can change the I2C address by passing an i2c_address parameter like:
# disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_address=0x3C)

# Alternatively you can specify an explicit I2C bus number, for example
# with the 128x32 display you would use:
# disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, i2c_bus=2)

# 128x32 display with hardware SPI:
# disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

# 128x64 display with hardware SPI:
# disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

# Alternatively you can specify a software SPI implementation by providing
# digital GPIO pin numbers for all the required display pins.  For example
# on a Raspberry Pi with the 128x32 display you might use:
# disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, dc=DC, sclk=18, din=25, cs=22)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

options = ["Mount partitions", "Connectivity", "NAS Info", "Battery Info", "Screen off", "Reboot", "Shutdown"]
heights = [0,8,16,25]
hindex= 0
# Load default font.
font = ImageFont.load_default()
index = 0
r_index=0
confirm = 0
selectedopt = 0
# Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
# font = ImageFont.truetype('Minecraftia.ttf', 8)

while True:

    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    draw.text((x+8, top),       options[index], font=font, fill=255)
    draw.text((x+8, top+8),     options[index+1], font=font, fill=255)
    draw.text((x+8, top+16),    options[index+2], font=font, fill=255)
    draw.text((x+8, top+25),    options[index+3], font=font, fill=255)
    draw.text((x, top+heights[hindex]), ">", font=font, fill=255)
    selectedopt = index+hindex
    # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    # Write two lines of text.
    if btnDOWN.is_pressed:
       if (index!=len(options)-4 and hindex==len(heights)-1):
         index += 1
         print("Index " + str(index))
       if hindex != len(heights)-1:
        hindex += 1
    elif btnUP.is_pressed:
        if hindex != 0:
         hindex -= 1
        if (index>0 and hindex==0):
         index -= 1
         print("Index " + str(index))

    elif btnMID.is_pressed:
        if (options[selectedopt]=="Screen off"):
            while not btnLEFT.is_pressed:
                draw.rectangle((0,0,width,height), outline=0, fill=0)
                disp.image(image)
                disp.display()
        if (options[selectedopt]=="Shutdown"):
            r_index=0
            confirm= 0
            while confirm == 0:
             draw.rectangle((0,0,width,height), outline=0, fill=0)
             draw.text((x+8, top),       "No", font=font, fill=255)
             draw.text((x+8, top+8),     "Yes", font=font, fill=255)
             draw.text((x, top+heights[r_index]), ">", font=font, fill=255)
             if btnDOWN.is_pressed:
                r_index = 1
             elif btnUP.is_pressed:
                r_index = 0
             elif (btnMID.is_pressed and r_index == 0 ):
              confirm = 1
             elif (btnMID.is_pressed and r_index == 1 ):
                draw.rectangle((0,0,width,height), outline=0, fill=0)
                draw.text((x+12, top+12), "Shutting down...", font=font, fill=255)
                disp.image(image)
                disp.display()
                time.sleep(3)
                draw.rectangle((0,0,width,height), outline=0, fill=0)
                disp.image(image)
                disp.display()
                os.system('sudo shutdown now')
                quit()
        if (options[selectedopt]=="Reboot"):
            r_index=0
            confirm = 0
            while confirm == 0:
             draw.rectangle((0,0,width,height), outline=0, fill=0)
             draw.text((x+8, top),       "No", font=font, fill=255)
             draw.text((x+8, top+8),     "Yes", font=font, fill=255)
             draw.text((x, top+heights[r_index]), ">", font=font, fill=255)
             if btnDOWN.is_pressed:
                r_index = 1
             elif btnUP.is_pressed:
                r_index = 0
             elif (btnMID.is_pressed and r_index == 0 ):
              cofnirm  = 1
             elif (btnMID.is_pressed and r_index == 1 ):
                draw.rectangle((0,0,width,height), outline=0, fill=0)
                draw.text((x+12, top+12), "Rebooting...", font=font, fill=255)
                disp.image(image)
                disp.display()
                time.sleep(3)
                draw.rectangle((0,0,width,height), outline=0, fill=0)
                disp.image(image)
                disp.display()
                os.system('sudo reboot now')
                quit()

    # Display image.
    disp.image(image)
    disp.display()
    time.sleep(.1)