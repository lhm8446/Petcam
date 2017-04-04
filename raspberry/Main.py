import RPi.GPIO as GPIO
import socket, time, requests, json, os, MySQLdb, threading, argparse, vlc
from Sensor_lib import dht11, mcp_3002

# Start tinc
# os.system("sudo gnome-terminal -e 'sudo tincd -n hotdog -D -d3' ")

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-info", required=True, help="path to the JSON configuration file")
args = vars(ap.parse_args())
info = json.load(open(args["info"]))

# socket
deviceNum = str(info["ip"])
PORT = 8000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    sock.bind((deviceNum, PORT))
except socket.error as e:
    print(str(e))

# DB connect
infoDB = tuple(info["datebase"])
db = MySQLdb.connect(infoDB[0], infoDB[1], infoDB[2], infoDB[3])
cursor = db.cursor()

cursor.execute("select token from raspberrypi where device_num = '" + deviceNum + "'")
token = cursor.fetchone()

cursor.execute(
    "select u.users_no, u.nickname, u.sec_pass_word from users u, (select * from raspberrypi ri where ri.device_num='" + deviceNum + "') r where r.users_no= u.users_no")
userInfo = cursor.fetchone()

userNo = str(userInfo[0])
nickName = str(userInfo[1])
secPass = str(userInfo[2])

# GPIO Setting
pinMotor = 12
pinSound = 11
pinTemp = 13
tempFlag = 0

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pinMotor, GPIO.OUT)
GPIO.setup(pinSound, GPIO.IN)
readTemperature = dht11.DHT11(pinTemp)

# Servo Motor frequency Setting ,Start
motor = GPIO.PWM(pinMotor, 50)
motor.start(0)


# method for remote motor
def remoteMotorLeft():
    motor.ChangeDutyCycle(1)

def remoteMotorCenter():
    motor.ChangeDutyCycle(5)

def remoteMotorRight():
    motor.ChangeDutyCycle(8)

# sound detect notification
def notificationForSound(a):
    url2 = info["sendMessageURL"]

    headers = {'Content-Type': 'application/json', 'Authorization': info["sendMessageKey"]}

    payload = {'notification': {'title': 'Sound Detect', 'body': ' Watch your dog !! '},
               'to': 'f56tDnhgF6c:APA91bHxGoX1sslAkcAAHhKwa3v7MLk0SyKmnwKdMPg4mYRcE-emTvkGDVokdTlP8R18SriqHRt1AAC0ZXtMl-nn7qZozSB-iCO7f4ciwOBCYpGGkhe4wLeYK9jOdYAzQE8yiNgxR54-'}

    requests.post(url2, headers=headers, data=json.dumps(payload))

    print "Detected"


# sound detect notification
def notificationForGas():
    url2 = info["sendMessageURL"]

    headers = {'Content-Type': 'application/json', 'Authorization': info["sendMessageKey"]}

    payload = {'notification': {'title': 'Gas Detect', 'body': ' Watch your Home !! '},
               'to': 'f56tDnhgF6c:APA91bHxGoX1sslAkcAAHhKwa3v7MLk0SyKmnwKdMPg4mYRcE-emTvkGDVokdTlP8R18SriqHRt1AAC0ZXtMl-nn7qZozSB-iCO7f4ciwOBCYpGGkhe4wLeYK9jOdYAzQE8yiNgxR54-'}

    requests.post(url2, headers=headers, data=json.dumps(payload))

    print "Detected"


# TemperatureSensor
def detectTemperature():
    instanceTemp = readTemperature.read()

    temperature = instanceTemp.temperature
    humidity = instanceTemp.humidity

    print temperature

    global tempFlag

    if (temperature != 0 and temperature != tempFlag):
        tempFlag = temperature
        cursor.execute("update raspberrypi set temperature = " + str(temperature) + ", humidity = " + str(
            humidity) + " where device_num = '" + deviceNum + "'")
        db.commit()
        print 'insert'

    threadTemp = threading.Timer(300, detectTemperature)
    threadTemp.start()


# GasSensor
def detectGas():
    smokeLevel = mcp_3002.readAnalog()
    print smokeLevel

    if (smokeLevel > 800):
        notificationForGas()

    treadGas = threading.Timer(300, detectGas)
    treadGas.start()

# Sound  detect
GPIO.add_event_detect(pinSound, GPIO.RISING, callback=notificationForSound, bouncetime=5000)

# Thread temperature, gas detect
detectTemperature()
detectGas()

while True:

    data, addr = sock.recvfrom(2048)

    print data

    if (data == 'left'):
        remoteMotorLeft()
    elif (data == 'center'):
        remoteMotorCenter()
    elif (data == 'right'):
        remoteMotorRight()

    elif (data == 'stream'):
        os.system("sudo gnome-terminal -e 'sudo sh streaming.sh " + nickName + " " + secPass + "'")
        time.sleep(1.5)
        os.system("sudo gnome-terminal -e 'sudo sh picam.sh' ")

    elif (data == 'streamstop'):
        os.system("sudo pkill -9 -ef 'sh streaming.sh' ")
        os.system("sudo pkill -9 -ef 'sh picam.sh' ")

    elif (data == 'audio'):
        # p = vlc.MediaPlayer('http://150.95.141.66/hotdog/hotdog/image/user/18/myrecord.mp3')
        # p.play()
        os.system("gnome-terminal --window -e 'cvlc http://150.95.141.66/hotdog/hotdog/image/user/18/myrecord.mp3'")

    elif (data == 'audiostop'):
        os.system("sudo pkill -9 -ef 'sudo sh audio.sh' ")

    elif (data == 'break'):
        break

db.close()
sock.close()
GPIO.cleanup()