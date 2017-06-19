import RPi.GPIO as IO
import spidev
import time
import mysql.connector as  connector


#CODE DATABASE

def data_invoegen(lichtsensor,opentoe):
    connection = connector.connect(host="localhost", user="wouter", passwd="wouter", db="dbproject1")
    cursor = connection.cursor()
    q= "INSERT INTO tblmetingen(Lichtsensor,Opentoe,Tijdstip,Gebruiksnaam) VALUES(" + str(lichtsensor) + ", " + str(opentoe) + ", now(),'Wouter')"
    cursor.execute(q)
    connection.commit()



# CODE LICHTSENSOR
light_channel = 0
spi = spidev.SpiDev()
spi.open(0, 0)

def readadc(adcnum):
    if adcnum > 7 or adcnum < 0:
        return -1
    r = spi.xfer2([1, 8 + adcnum << 4, 0])
    data = ((r[1] & 3) << 8) + r[2]
    print(data)
    return data

#CODE SERVOMOTOR

IO.setwarnings(False)
IO.setmode(IO.BCM)
IO.setup(23, IO.OUT)
p = IO.PWM(23, 50)
delay = 5000
waarde_toe = 350
toe = False
run = True

while run== True:
    ldr_value = readadc(light_channel)
    if ldr_value <= waarde_toe:
        if toe == False:
            p.start(12.5)
            data_invoegen(ldr_value, toe)
            time.sleep(5)
            p.stop()
            toe=True
        else:
            data_invoegen(ldr_value, toe)
            time.sleep(5)
    else:
        time.sleep(0.001)
    if ldr_value > waarde_toe :
        if toe== True:
            p.start(2.5)
            data_invoegen(ldr_value, toe)
            time.sleep(5)
            p.stop()
            toe = False
        else:
            data_invoegen(ldr_value, toe)
            time.sleep(5)
    else:
        time.sleep(0.001)
    print(ldr_value)
    print(toe)

