#!/usr/bin/python

import RPi.GPIO as GPIO
import time

    
LCD_RS = 37
LCD_E  = 35
LCD_D4 = 33
LCD_D5 = 31
LCD_D6 = 29
LCD_D7 = 11
LED=3
LCD_WIDTH = 16   
LCD_CHR = True
LCD_CMD = False

E_PULSE = 0.00005
E_DELAY = 0.00005

def lcd_init():

  GPIO.setmode(GPIO.BOARD)  
  GPIO.setup(LCD_E, GPIO.OUT) 
  GPIO.setup(LCD_RS, GPIO.OUT)
  GPIO.setup(LCD_D4, GPIO.OUT) 
  GPIO.setup(LCD_D5, GPIO.OUT) 
  GPIO.setup(LCD_D6, GPIO.OUT) 
  GPIO.setup(LCD_D7, GPIO.OUT) 
  GPIO.setup(LED,GPIO.OUT)
  lcd_byte(0x33,LCD_CMD)
  lcd_byte(0x32,LCD_CMD)
  lcd_byte(0x28,LCD_CMD)
  lcd_byte(0x0C,LCD_CMD)  
  lcd_byte(0x06,LCD_CMD)
  lcd_byte(0x01,LCD_CMD)
  
def crct_blink():
    GPIO.output(3,1)
    time.sleep(1)
    GPIO.output(3,0)

def err_blink():
    GPIO.output(3,1)
    time.sleep(2)
    GPIO.output(3,0)


def lcd_string(message,style):
  if style==1:
    message = message.ljust(LCD_WIDTH," ")  
  elif style==2:
    message = message.center(LCD_WIDTH," ")
  elif style==3:
    message = message.rjust(LCD_WIDTH," ")

  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)

def lcd_byte(bits, mode):
  GPIO.output(LCD_RS, mode) 
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x10==0x10:
    GPIO.output(LCD_D4, True)
  if bits&0x20==0x20:
    GPIO.output(LCD_D5, True)
  if bits&0x40==0x40:
    GPIO.output(LCD_D6, True)
  if bits&0x80==0x80:
    GPIO.output(LCD_D7, True)
  time.sleep(E_DELAY)    
  GPIO.output(LCD_E, True)  
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)  
  time.sleep(E_DELAY)      
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x01==0x01:
    GPIO.output(LCD_D4, True)
  if bits&0x02==0x02:
    GPIO.output(LCD_D5, True)
  if bits&0x04==0x04:
    GPIO.output(LCD_D6, True)
  if bits&0x08==0x08:
    GPIO.output(LCD_D7, True)
  time.sleep(E_DELAY)    
  GPIO.output(LCD_E, True)  
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)  
  time.sleep(E_DELAY)   



