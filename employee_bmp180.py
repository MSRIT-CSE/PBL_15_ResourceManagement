#!/usr/bin/python

import time
import smbus
from ctypes import c_short
import time
import threading
import thread
import sqlite3
from datetime import datetime
import smtplib
import serial
#Import Serial Library
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# me == my email address
# you == recipient's email address
me = "dvrayz.dvrayz@gmail.com"
you = "vikas.hanumegowda@gmail.com"
you1 = "tejasdhasrali@gmail.com"
# temp=[];

# Create message container - the correct MIME type is multipart/alternative.
msg = MIMEMultipart('alternative')
msg['Subject'] = "TEST MESSAGE FROM PYTHON"
msg['From'] = me
msg['To'] = you

# Create the body of the message (a plain-text and an HTML version).
text = "working hours of employee with id 123 has exceeded the limit for this week"
# Record the MIME types of both parts - text/plain and text/html2
part = MIMEText(text, 'plain')

# Attach parts into message container.# According to RFC 2046, the last part of a multipart message, in this case
# the HTML message, is best and preferred.
msg.attach(part)
msg1 = MIMEMultipart('alternative')
msg1['Subject'] = "PBL"
msg1['From'] = me
msg1['To'] = you

# Create the body of the message (a plain-text and an HTML version).
text1 = "TEST TEXT"
# Record the MIME types of both parts - text/plain and text/html2
part1 = MIMEText(text1, 'plain')

# Attach parts into message container.# According to RFC 2046, the last part of a multipart message, in this case
# the HTML message, is best and preferred.
msg1.attach(part1)
# Send the message via local SMTP server.
mail = smtplib.SMTP_SSL('smtp.googlemail.com', 465)

mail.ehlo
mail.login('dvrayz.dvrayz@gmail.com', 'Welcome1234*')

 
DEVICE = 0x77 # Default device I2C address
elapsed_time=0.0
#bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
bus = smbus.SMBus(1) # Rev 2 Pi uses 1 
default_temp = 29
default_press= 915


def convertToString(data):
  # Simple function to convert binary data into
  # a string
  return str((data[1] + (256 * data[0])) / 1.2)

def getShort(data, index):
  # return two bytes from data as a signed 16-bit value
  return c_short((data[index] << 8) + data[index + 1]).value

def getUshort(data, index):
  # return two bytes from data as an unsigned 16-bit value
  return (data[index] << 8) + data[index + 1]

def readBmp180Id(addr=DEVICE):
  # Register Address
  REG_ID     = 0xD0

  (chip_id, chip_version) = bus.read_i2c_block_data(addr, REG_ID, 2)
  return (chip_id, chip_version)
  
def readBmp180(addr=DEVICE):
  # Register Addresses
  REG_CALIB  = 0xAA
  REG_MEAS   = 0xF4
  REG_MSB    = 0xF6
  REG_LSB    = 0xF7
  # Control Register Address
  CRV_TEMP   = 0x2E
  CRV_PRES   = 0x34 
  # Oversample setting
  OVERSAMPLE = 3    # 0 - 3
  
  # Read calibration data
  # Read calibration data from EEPROM
  cal = bus.read_i2c_block_data(addr, REG_CALIB, 22)

  # Convert byte data to word values
  AC1 = getShort(cal, 0)
  AC2 = getShort(cal, 2)
  AC3 = getShort(cal, 4)
  AC4 = getUshort(cal, 6)
  AC5 = getUshort(cal, 8)
  AC6 = getUshort(cal, 10)
  B1  = getShort(cal, 12)
  B2  = getShort(cal, 14)
  MB  = getShort(cal, 16)
  MC  = getShort(cal, 18)
  MD  = getShort(cal, 20)

  # Read temperature
  bus.write_byte_data(addr, REG_MEAS, CRV_TEMP)
  time.sleep(0.005)
  (msb, lsb) = bus.read_i2c_block_data(addr, REG_MSB, 2)
  UT = (msb << 8) + lsb

  # Read pressure
  bus.write_byte_data(addr, REG_MEAS, CRV_PRES + (OVERSAMPLE << 6))
  time.sleep(0.04)
  (msb, lsb, xsb) = bus.read_i2c_block_data(addr, REG_MSB, 3)
  UP = ((msb << 16) + (lsb << 8) + xsb) >> (8 - OVERSAMPLE)

  # Refine temperature
  X1 = ((UT - AC6) * AC5) >> 15
  X2 = (MC << 11) / (X1 + MD)
  B5 = X1 + X2
  temperature = (B5 + 8) >> 4

  # Refine pressure
  B6  = B5 - 4000
  B62 = B6 * B6 >> 12
  X1  = (B2 * B62) >> 11
  X2  = AC2 * B6 >> 11
  X3  = X1 + X2
  B3  = (((AC1 * 4 + X3) << OVERSAMPLE) + 2) >> 2

  X1 = AC3 * B6 >> 13
  X2 = (B1 * B62) >> 16
  X3 = ((X1 + X2) + 2) >> 2
  B4 = (AC4 * (X3 + 32768)) >> 15
  B7 = (UP - B3) * (50000 >> OVERSAMPLE)

  P = (B7 * 2) / B4

  X1 = (P >> 8) * (P >> 8)
  X1 = (X1 * 3038) >> 16
  X2 = (-7357 * P) >> 16
  pressure = P + ((X1 + X2 + 3791) >> 4)

  return (temperature/10.0,pressure/ 100.0)

def main():
  global elapsed_time
  elapsed_time=0.0
  #threading.Thread(target=dbentry1,args=()).start()
  start_time=0.0
  flag = False
  flag1=0
  while 1:    
    (chip_id, chip_version) = readBmp180Id()
    time_count=0
    (temperature,pressure)=readBmp180()
    if ((temperature-default_temp>2 or pressure-default_press>2) and (flag)== False):
      start_time=time.time()
      flag=True
      #while (temperature-default_temp>2 and pressure-default_press>2):
      print
      print "Temperature : ", temperature, "C"
      print "Pressure    : ", pressure, "mbar"
      #next_time=time.time()
      #time_elapsed=next_time-start_time
      print elapsed_time
    if (flag and (temperature<=default_temp or pressure<=default_press)):
      next_time=time.time()
      flag= False
      #print next_time
      if(start_time<next_time):
        elapsed_time+=(next_time-start_time)
        week=1
    mi=datetime.now().minute
    hr=datetime.now().hour
    da=str(datetime.now().year)+':'+str(datetime.now().month)+':'+str(datetime.now().day)
    if hr==2:
      if mi==0:
        if flag1==0:
          conn=sqlite3.connect('humanresource.db')
          curs=conn.cursor()
          curs.execute('insert into employee values("employee1",123,?,?)',(da,elapsed_time))
          flag1=1
          #print "inserted"
          conn.commit()
          conn.close()
          elapsed_time=0.0
          #time.sleep(23*60*60)
    if(elapsed_time>10):
      conn=sqlite3.connect('humanresource.db')
      curs=conn.cursor()
      curs.execute('insert into manage values(123,?,?)',(week,elapsed_time))
      #print "inserted"
      elapsed_time=0.0
      week+=1
      conn.commit()
      conn.close()
      mail.sendmail(me, you, msg.as_string())
      mail.sendmail(me, you1, msg.as_string())
      mail.quit()

if __name__=="__main__":
  main()
