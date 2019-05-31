import sensor, image, utime, sys, time
from pyb import UART
from machine import  I2C,Pin
from servo import Servos #importing a Servo class
import pca9685 #importing the servo driver class
import random
#Initial Setup
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False)
clock = time.clock()

#Defines pins that are connected to camera

#Define button pin
#buttonPin = 'P0'
#Define red, green, and blue pins for the multi color LED
#redPin = 'P1'
#greenPin = 'P2'
#bluePin = 'P3'

#Define variables based on pin
#button = Pin(buttonPin,Pin.IN,Pin.PULL_UP)
#redLED = Pin(redPin,Pin.OUT)
#greenLED = Pin(greenPin,Pin.OUT)
#blueLED = Pin(bluePin,Pin.OUT)
button = Pin('P0',Pin.IN,Pin.PULL_UP)
redLED = Pin('P1',Pin.OUT)
greenLED = Pin('P2',Pin.OUT)
blueLED = Pin('P3',Pin.OUT)

uart = UART(3, 9600, timeout_char=1000)
uart.init(9600, bits=8, parity=None, stop=1, timeout_char=1000)
i2c = I2C(sda=Pin('P8'), scl=Pin('P7'))
servo = Servos(i2c, address=0x41, freq=50, min_us=650, max_us=2800, degrees=180)
r_threshold = [75, 90, 5, 40, 20, 35]
g_threshold = [30, 50, -40,-10,-10,20]
b_threshold = [50, 70, -10, 0, -50, -30]
redCheck = [0,0,0,0,0,0]
greenCheck = [0,0,0,0,0,0]
blueCheck = [0,0,0,0,0,0]
colorCheck = ['none','none','none']

def learnThresholds():
  r = [(320//2)-(50//2), (240//2)-(50//2), 50, 50]
  for i in range(60):
    img = sensor.snapshot()
    img.draw_rectangle(r)
  print("Learning thresholds...")
  threshold = [50, 50, 0, 0, 0, 0]
  for i in range(60):
    img = sensor.snapshot()
    hist = img.get_histogram(roi=r)
    lo = hist.get_percentile(0.01)
    hi = hist.get_percentile(0.99)
    threshold[0] = (threshold[0] + lo.l_value()) // 2
    threshold[1] = (threshold[1] + hi.l_value()) // 2
    threshold[2] = (threshold[2] + lo.a_value()) // 2
    threshold[3] = (threshold[3] + hi.a_value()) // 2
    threshold[4] = (threshold[4] + lo.b_value()) // 2
    threshold[5] = (threshold[5] + hi.b_value()) // 2
    for blob in img.find_blobs([threshold], pixels_threshold=100, area_threshold=100, merge=True, margin=10):
        img.draw_rectangle(blob.rect())
        img.draw_cross(blob.cx(), blob.cy())
        img.draw_rectangle(r)
  print("Thresholds learned...")
  print(threshold)
  Color = determineColor(threshold)
  return Color

def determineColor(thresholdLearned):
  for i in range(6):
    redCheck[i] = abs(r_threshold[i]-thresholdLearned[i])
    greenCheck[i] = abs(g_threshold[i]-thresholdLearned[i])
    blueCheck[i] = abs(b_threshold[i]-thresholdLearned[i])
  check = [sum(redCheck), sum(greenCheck), sum(blueCheck)]
  #print(check)
  #print(min(check))
  indexColor = check.index(min(check))
  #print(indexColor)
  if indexColor == 0:
    color = 'Red'
  elif indexColor == 1:
    color = 'Green'
  elif indexColor == 2:
    color = 'Blue'
  return color

#def randomPosition():
#  positions = [0,30,60,90,120,150,180]
#  x = random.choice(positions)
#  return x

def turnRedLED():
  redLED.high()
  utime.sleep(3)
  redLED.low()
def turnGreenLED():
  greenLED.high()
  utime.sleep(3)
  greenLED.low()
def turnBlueLED():
  blueLED.high()
  utime.sleep(3)
  blueLED.low()
def valuesInList(list,color):
  list[0] = list[1]
  list[1] = list[2]
  list[2] = color
  return list

#pre_code = cloudGet("SafePassword")

def safeCode():
    initial_string = ''
    print('Resetting safe')
    servo.position(0,0)
    servo.position(1,0)
    servo.position(2,0)
    while(True):
       clock.tick()
       img = sensor.snapshot()
       img.lens_corr(1.8)
       #Once button is pressed
       if button.value() == 0:
        #this returns a color
        colorIdentified = learnThresholds()
        #this prints the color that was learned/seen
        print(colorIdentified)

    #this block changes LED Color based on the color seen
        if colorIdentified == 'Green':
          turnGreenLED()
          initial_string += 'G'
          print(initial_string)
        elif colorIdentified == 'Red':
          turnRedLED()
          initial_string += 'R'
          print(initial_string)
        elif colorIdentified == 'Blue':
          turnBlueLED()
          initial_string += 'B'
          print(initial_string)
        check = initial_string.find(code, 0, len(initial_string))
        if check == -1:
            continue
        elif check != -1:
            break
    servo.position(0,90) #this commands servos to move
    utime.sleep(0.5)
    servo.position(1,90)
    utime.sleep(0.5)
    servo.position(2,90)
    utime.sleep(1)
    input = '1' + '\n'
    print('sending over UART')
    while True:
        uart.write(input)
        utime.sleep(0.5)

code = 'RGB'

#print('Solenoid Test')
##input = '1'
#input += '\n'
#while True:
#    uart.write(input)
#    utime.sleep(0.5)
safeCode()

    #colorCheck = valuesInList(colorCheck,colorIdentified)
    #if colorCheck == ['Green','Blue','Red']:
    #  servo.position(0,90) #this commands servos to move
    #  servo.position(1,90)
    #  servo.position(2,90)
    #  turnBlueLED()
    #  turnRedLED()
    #  turnGreenLED()
    #  input = '1'
    #  input=input+'\n'
    #  while(True):
    #    uart.write(input)
    #    utime.sleep(0.5)
    #else:
    #  servo.position(0,randomPosition())
    #  servo.position(1,randomPosition())
    #  servo.position(2,randomPosition())

#   for code in img.find_qrcodes():
#       img.draw_rectangle(code.rect(), color = (255, 0, 0))
#       input = code.payload()
#       if input == 'Red':
#        turnRedLED()
#       elif input=='Green':
#        turnGreenLED()
#       elif input == 'Blue':
#        turnBlueLED()
#       print(input)
#       utime.sleep(1)
