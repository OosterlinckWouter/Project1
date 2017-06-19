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
p.start(0)
time.sleep(1/10)
p.stop()


while run== True:
    ldr_value = readadc(light_channel)
    if ldr_value <= waarde_toe:
        print("moet dicht")
        if toe == False:
            print("is open --> dicht doen")
            # p.ChangeDutyCycle(99)
            p.start(99.9)
            data_invoegen(ldr_value, toe)
            time.sleep(5)
            p.stop()
            # p.ChangeDutyCycle(0)

            toe=True
        else:
            print("is al toe")
            data_invoegen(ldr_value, toe)
            time.sleep(5)

    if ldr_value > waarde_toe :
        print("moet open")

        if toe== True:
            print("is toe --> open doen")
            # p.ChangeDutyCycle(2.5)

            p.start(2.5)
            data_invoegen(ldr_value, toe)
            time.sleep(5)
            p.stop()
            # p.ChangeDutyCycle(0)

            toe = False
        else:
            print("is al open")

            data_invoegen(ldr_value, toe)
            time.sleep(5)

    print(ldr_value)
    print(toe)

