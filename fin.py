# -*- coding:utf-8 -*-

from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.core import lib

from luma.oled.device import sh1106
from gpiozero import CPUTemperature
import RPi.GPIO as GPIO

import time
import subprocess
import requests
import json

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

#Time to get Wifi Connected
#time.sleep(90)

#a = requests.get('https://finnhub.io/api/v1/quote?symbol=WDC&token=bsqq90748v6p29vi9770')
#b = requests.get('https://finnhub.io/api/v1/quote?symbol=CTSH&token=bsqq90748v6p29vi9770')
#c = requests.get('https://finnhub.io/api/v1/quote?symbol=WBA&token=bsqq90748v6p29vi9770')
#d = requests.get('https://finnhub.io/api/v1/quote?symbol=INTC&token=bsqq90748v6p29vi9770')
#e = requests.get('https://finnhub.io/api/v1/quote?symbol=WFC&token=bsqq90748v6p29vi9770')
#print(a.json())
#ajson=a.json()
#bjson=b.json()
#cjson=c.json()
#djson=d.json()
#ejson=e.json()

#strvaluea=ajson["c"]
#print(strvaluea)
#val=ajson[""]
#print(val)
#print(ajson[0])
#for key, value in ajson.items():
#        print(key, ":", value)
#a_parsed=json.loads(a.json())
#b_parsed=json.loads(b.json())
#c_parsed=json.loads(c.json())
#d_parsed=json.loads(d.json())
#e_parsed=json.loads(e.json())
# Load default font.
font = ImageFont.load_default()

aval = 36.85
bval = 19.25
cval = 40.95
dval = 49.40
eval = 24.18

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = 128
height = 64
image = Image.new('1', (width, height))

# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

RST = 25
CS = 8		
DC = 24

USER_I2C = 0

if  USER_I2C == 1:
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(RST,GPIO.OUT)	
        print("I2C")
	GPIO.output(RST,GPIO.HIGH)
	
	serial = i2c(port=1, address=0x3c)
else:
	serial = spi(device=0, port=0, bus_speed_hz = 8000000, transfer_size = 4096, gpio_DC = 24, gpio_RST = 25)

device = sh1106(serial, rotate=2) #sh1106  

try:
	while True:
		curr_ex = requests.get('https://finnhub.io/api/v1/forex/rates?base=USD&token=bsqq90748v6p29vi9770')
		a = requests.get('https://finnhub.io/api/v1/quote?symbol=WDC&token=bsqq90748v6p29vi9770')
		b = requests.get('https://finnhub.io/api/v1/quote?symbol=KSS&token=bsqq90748v6p29vi9770')
		c = requests.get('https://finnhub.io/api/v1/quote?symbol=WBA&token=bsqq90748v6p29vi9770')
		d = requests.get('https://finnhub.io/api/v1/quote?symbol=INTC&token=bsqq90748v6p29vi9770')
		e = requests.get('https://finnhub.io/api/v1/quote?symbol=WFC&token=bsqq90748v6p29vi9770')
		ajson=a.json()
		bjson=b.json()
		cjson=c.json()
		djson=d.json()
		ejson=e.json()
		floatajson=float(ajson["c"])
		floatbjson=float(bjson["c"])
		floatcjson=float(cjson["c"])
		floatdjson=float(djson["c"])
		floatejson=float(ejson["c"])
		diffajson= floatajson - aval
		diffbjson= floatbjson - bval
		diffcjson= floatcjson - cval
		diffdjson= floatdjson - dval
		diffejson= floatejson - eval
		aprct= round(diffajson / aval * 100,1)
		bprct= round(diffbjson / bval * 100,1)
		cprct= round(diffcjson / cval * 100,1)
		dprct= round(diffdjson / dval * 100,1)
		eprct= round(diffejson / eval * 100,1)
		curr_exjson = curr_ex.json()
		floatcurr_ex = round(float(curr_exjson["quote"]["INR"]),2)
                time.sleep(3)
		with canvas(device) as draw:
			
			#draw.rectangle(device.bounding_box, outline="white", fill="black")
			#draw.text((30, 40), "Hello World", fill="white")
			# Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
			cmd = "hostname -I | cut -d\' \' -f1"
			IP = subprocess.check_output(cmd, shell = True )
			cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
			CPU = subprocess.check_output(cmd, shell = True )
			cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
			MemUsage = subprocess.check_output(cmd, shell = True )
			cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
			Disk = subprocess.check_output(cmd, shell = True )
			cpu = CPUTemperature()
			localtime = time.asctime( time.localtime(time.time()) )


			# Write two lines of text.

			#draw.text((x, top),       "IP: " + str(IP),  font=font, fill=255)
			#draw.text((x, top+8),     str(CPU), font=font, fill=255)
			#draw.text((x, top+16),    str(MemUsage),  font=font, fill=255)
			#draw.text((x, top+24),    str(Disk),  font=font, fill=255)

			draw.text((x, top),    "WDC:  " + str(ajson["c"]) + " "  + str(aprct),  font=font, fill=255)
			draw.text((x, top+8), "KSS:  " +  str(bjson["c"]) + " "  + str(bprct),  font=font, fill=255)
			draw.text((x, top+16), "WBA:  " +  str(cjson["c"]) + " "  + str(cprct),  font=font, fill=255)
			draw.text((x, top+24), "INTC: " +  str(djson["c"]) + " " + str(dprct),  font=font, fill=255)
			draw.text((x, top+32), "WFC:  " +  str(ejson["c"]) + " " + str(eprct),  font=font, fill=255)
			#draw.text((x, top+16), "WBA: " +  str(cjson["c"]) + "  40.95",  font=font, fill=255)
			#draw.text((x, top+24), "INTC: " +  str(djson["c"]) + "  49.40",  font=font, fill=255)
			#draw.text((x, top+32),  "WFC: " +  str(ejson["c"]) + "  24.18",  font=font, fill=255)
			draw.text((x, top+40),  "USD - INR: " +  str(floatcurr_ex),  font=font, fill=255)
			draw.text((x, top+48),  "CPU Temp: " +  str(cpu.temperature),  font=font, fill=255)
			draw.text((x, top+56),  str(localtime),  font=font, fill=255)
except:
	print("except")
	print(ajson["c"])
	print(bjson["c"])
	print(cjson["c"])
	print(djson["c"])
	print(ejson["c"])
	print(cpu)
	print(round(curr_exjson["quote"]["INR"],3))
GPIO.cleanup()
