
from flask import Flask, request, render_template, Response
import RPi.GPIO as GPIO
import time
from camera import Camera

app = Flask(__name__)

servo_pin=18 #서보모터를 이용해 사료 출구 제어
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin,GPIO.OUT)
servo=GPIO.PWM(servo_pin,50)

@app.route("/")
def main():
    return render_template('index.html')

control=True
@app.route("/servo")         # index.html에서 이 주소를 접속하여 해당 함수를 실행
def turn_servo():
    global control
    control=True
    try:
        while control==True:
            servo.start(0)
            servo.ChangeDutyCycle(9.5)  # 90도 서보모터 작동 -> 사료 출구 open
            print("9.5")
            time.sleep(1)         
           
            return "ok"                         # 함수가 'ok'문자열을 반환함
    except :
        return "fail"

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/turn_off")
def turn_off():
    global control
    try:
        control=False 
        servo.ChangeDutyCycle(2.5) # 0도 사료 출구 close
        print("2.5")
        time.sleep(1)
        # servo.stop()
        return "ok"
    except :
        return "fail"
        
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
