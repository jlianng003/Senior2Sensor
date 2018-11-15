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
	for j in range (0,64):
		print ('[{:3.3f}]'.format(ir[j]), end=' ')
		if j%16==0: print ('')
		if ir[j] > 35.2:
			high_reading_count += 1
		if high_reading_count > 10:
			GPIO.output(11, True)
		else:
			GPIO.output(11, False)

	if high_reading_count > 10:
		time_count += 1
        else:
 	       time_count = 0
	print("\n count: ", high_reading_count)
	print(" || time: ", time_count)
	time.sleep(1)
