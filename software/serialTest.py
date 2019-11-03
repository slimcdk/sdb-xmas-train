import serial
import time
import struct
import ctypes

arduino = serial.Serial(
  port='/dev/ttyUSB0',
  baudrate=115200,
  parity=serial.PARITY_NONE,
  stopbits=serial.STOPBITS_ONE,
  bytesize=serial.EIGHTBITS,
  timeout=0
)
time.sleep(2)


train_is_running = False
pre_train_is_running = False


while True:

  pre_train_is_running = train_is_running

  # read Arduino output and parse it
  response = arduino.readline().decode('utf-8')
  values = response.split(",")

  print(values, end='\r')

  run_progress = values[0]
  train_speed = values[1]
  is_motor_running = values[2] == '1'


  train_is_running = int(train_speed) != int(0)

  if (pre_train_is_running != train_is_running):
    print('running?: {}'.format(train_is_running))


arduino.close()


