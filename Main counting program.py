import time
import RPi.GPIO as GPIO
import subprocess as sp 
import threading
import time


time.sleep(1)
print "IMPORTING of Python Libraries DONE!!"
time.sleep(1)


GPIO.setmode(GPIO.BOARD)

GPIO.setup(37, GPIO.IN)
GPIO.setup(40, GPIO.IN)
GPIO.setup(13, GPIO.OUT)


#Defining Global variable to turn bulb on-off
Bulb = 0

def temp1():
 global Bulb
 a_cut = 0
 b_cut = 0
 inside = 0
 while True:
  if (GPIO.input(37) ==0 and GPIO.input(40) == 0 and b_cut == 0):
   a_cut = 1
#   print('a_cut=%d' %a_cut,'b_cut=%d' %b_cut) 
  elif (GPIO.input(37) ==1 and GPIO.input(40) ==1 and a_cut == 1):
   a_cut = 0
   inside = inside + 1
   Bulb  =  1 
   time.sleep(1) 
#   print('a_cut=%d' %a_cut,'b_cut=%d' %b_cut)
  elif (GPIO.input(37) ==1 and GPIO.input(40) == 1 and a_cut == 0):
   b_cut = 1
#   print('a_cut=%d' %a_cut,'b_cut=%d' %b_cut)
  elif (GPIO.input(37) ==0 and GPIO.input(40) == 0 and b_cut == 1): 
   b_cut = 0
   inside =  inside - 1
   if (inside ==0):
     Bulb = 0
   time.sleep(1)
  print('total_inside=%d' %inside, 'a_cut=%d' %a_cut, 'b_cut=%d' %b_cut)



def temp2():
 while True:
  if (Bulb == 0):
   time.sleep(5)
   GPIO.output(13,0)
  else:
   time.sleep(5)
   GPIO.output(13,1)
   

threading.Thread(target=temp1, args = ()).start()
threading.Thread(target=temp2, args = ()).start()
