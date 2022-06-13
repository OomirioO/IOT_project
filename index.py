# 웹서버 프로그램 웹 브라우저에서 http://localhost:5000/로 접속하면 
# index.html을 실행하고 버튼을 이용하여 서보모터, 카메라를 작동시킴

from flask import Flask, request, render_template, url_for
import RPi.GPIO as GPIO
import time
import threading
import picamera
from PIL import Image

servo_pin=18 #서보모터를 이용해 사료 제어
app = Flask(__name__)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin,GPIO.OUT)

servo=GPIO.PWM(servo_pin,50)
servo.start(0)

@app.route("/")
def main():
    return render_template('index.html')
    

@app.route("/servo")                       # index.html에서 이 주소를 접속하여 해당 함수를 실행
def turn_servo():
    try:
        servo.ChangeDutyCycle(7.5)  # 90도 서보모터 작동 -> 사료 출구 open
        print("7.5")
        time.sleep(2)         
        servo.ChangeDutyCycle(2.5) # 0도 사료 출구 close
        print("2.5")
        time.sleep(2)
        return "ok"                         # 함수가 'ok'문자열을 반환함
    except :
        return "fail"

@app.route("/camera")
def turn_camera():
    try:
        with picamera.PiCamera() as camera:
            camera.resolution = (640, 480)
            camera.start_preview()
            time.sleep(1)
            camera.capture('photo.jpg')
            camera.stop_preview()

            im=Image.open('/home/pi/IOT_Python/photo.jpg') #이미지 불러오기
            im.show()
            return "ok"
    except :
        return "fail"

@app.route("/stream")
def turn_stream():
    try:
        return "ok"
    except :
        return "fail"


if __name__ == "__main__":
    app.run(host="0.0.0.0")