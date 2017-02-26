from gpiozero import DistanceSensor
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
ultrasonic = DistanceSensor(echo=17, trigger=4, threshold_distance=0.3)
GPIO.setup(27,GPIO.OUT)
GPIO.setup(18,GPIO.OUT)
while True:
  dis = ultrasonic.distance
  print(dis)
  if dis<0.15:
          #no replenishment, green led
          GPIO.output(27,GPIO.LOW)
          GPIO.output(18,GPIO.HIGH)
  else:
          #replenish, red led
          GPIO.output(27,GPIO.HIGH)
          GPIO.output(18,GPIO.LOW)
