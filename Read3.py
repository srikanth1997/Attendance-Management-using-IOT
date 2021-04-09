#!/usr/local/lib/python3.5/dist-packages/pymysql
import RPi.GPIO as GPIO
import MFRC522
import signal
import pymysql
import lcd
import pymysql.cursors
import time
  
continue_reading = True
GPIO.setwarnings(False)
LCD_LINE_1 = 0x80 
LCD_LINE_2 = 0xC0
LCD_CMD = False

def end_read(signal,frame):
    global continue_reading
    print ("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()

signal.signal(signal.SIGINT, end_read)

check = 0
MIFAREReader = MFRC522.MFRC522()

print "Welcome to the RFID Based Attendance System"
print "Press Ctrl-C to stop."
lcd.main()
while continue_reading:
    check = 0
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
    if status == MIFAREReader.MI_OK:
        print "Card detected"
    (status,uid) = MIFAREReader.MFRC522_Anticoll()
    if status == MIFAREReader.MI_OK:
        print "Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])
        s1=str(uid[0])+str(uid[1])+str(uid[2])+str(uid[3])
        key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        MIFAREReader.MFRC522_SelectTag(uid)
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)
        if status == MIFAREReader.MI_OK:
            MIFAREReader.MFRC522_Read(8)
            MIFAREReader.MFRC522_StopCrypto1()
        else:
            print "Authentication error"
        connection=pymysql.connect(host='localhost',user='root',password='major',db='students',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                sql="SELECT RFID,Attendance,Name from records"
                cursor.execute(sql)
                for row in cursor:
                    if row['RFID'] == s1:
                        temp=row['RFID']
                        temp2=row['Attendance']
                        temp3=row['Name']
                        print temp2
                        if temp2 == '0':
                            id1=int(row['Attendance'])+int('1')
                            cursor.execute("UPDATE records SET Attendance=%s where RFID=%s",(id1,temp))
                            connection.commit()
                            print "Updated"
                            lcd.lcd_byte(LCD_LINE_1, LCD_CMD)
                            lcd.lcd_string(temp3,1)
                            lcd.lcd_byte(LCD_LINE_2, LCD_CMD)
                            lcd.lcd_string('Attendance Marked',1)
                            check=1
                            lcd.crct_blink()
                            
                            break;
                        else:
                            print "Attendance Already Marked"
                            lcd.lcd_byte(LCD_LINE_1, LCD_CMD)
                            lcd.lcd_string(temp3,1)
                            lcd.lcd_byte(LCD_LINE_2, LCD_CMD)
                            lcd.lcd_string('Error',1)
                            check=1
                            lcd.err_blink()
                            break;
                        
                if check == 0:
                    print "Not Updated"
                    lcd.lcd_byte(LCD_LINE_1, LCD_CMD)
                    lcd.lcd_string('Not a Valid RFID',1)
                    lcd.lcd_byte(LCD_LINE_2, LCD_CMD)
                    lcd.lcd_string('Error',1)
                    lcd.err_blink()
                    
        
        finally:
            connection.close()
        
        
