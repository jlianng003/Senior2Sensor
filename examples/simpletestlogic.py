
# Very simple test to know if the thermomin service is running
# Uses numpy $>pip install numpy
# Thermomin (c) Rodo Lillo 2017
from __future__ import print_function #compatible with python 2.7
import sys, time, numpy
import RPi.GPIO as GPIO



fifo = open('/var/run/mlx9062x.sock', 'r')
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
time_count = 0

while 1:
	ir = numpy.frombuffer(fifo.read()[0:256], dtype=numpy.float32)
	sys.stderr.write("\x1b[2J\x1b[H") #clear the terminal
	high_reading_count = 0
	high_reading_temp = 0
	for j in range (0,64):
		print ('[{:3.3f}]'.format(ir[j]), end=' ')
		if j%4==0: print ('')
		if ir[j] > 29:
			high_reading_count += 1
		if ir[j] > high_reading_temp:
			high_reading_temp =ir[j]
	if high_reading_count > 4:
		time_count += 1
        else:
 	       time_count = 0
	if time_count >10:
		time_count = 0
	elif time_count > 7:
		GPIO.output(11, True)
	else:
		GPIO.output(11, False)

	print("\n || count: ", high_reading_count)
	print(" || time: ", time_count)
	print(" || High Temp: ", high_reading_temp)

 	time.sleep(1)
