from gpiozero import DistanceSensor
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
ultrasonic = DistanceSensor(echo=17, trigger=4, threshold_distance=0.2)
GPIO.setup(27,GPIO.OUT)
GPIO.setup(18,GPIO.OUT)

from flask import Flask, render_template, redirect

app = Flask(__name__)

dis = ultrasonic.distance
if dis<0.15:
    #no replenishment, green led
    GPIO.output(27,GPIO.LOW)
    GPIO.output(18,GPIO.HIGH)
    homepage = 'index.html'
else:
    #replenish, red led
    GPIO.output(27,GPIO.HIGH)
    GPIO.output(18,GPIO.LOW)
    homepage = 'replenish.html'

@app.route('/')
def index():
    return render_template(homepage)

@app.route('/authresponse')
def authresponse():
    return render_template('response.html')

@app.route('/accesstoken/<var>')
def accesstoken(var):
    import requests
    r = requests.post("https://api.amazon.com/auth/o2/token", data={'grant_type': 'authorization_code', 'code': var, 'client_id': 'amzn1.application-oa2-client.a0805eb8d8e4419b83cdb2afe0ef2d43', 'client_secret':'c35ff75f4e6ad14fee8b635e384ba61613a0a9825f9ddf2ed017f56ef870ea64','redirect_uri':'https://192.168.1.35:8100/authresponse'})
    data = r.json()
    accesstoken = data['access_token']
    token = 'Bearer ' + accesstoken
    x = requests.post("https://dash-replenishment-service-na.amazon.com/replenish/f76f5d12-1404-483a-97b1-f3fdc1dcf869", headers={'Authorization': token, 'x-amzn-accept-type': 'com.amazon.dash.replenishment.DrsReplenishResult@1.0', 'x-amzn-type-version': 'com.amazon.dash.replenishment.DrsReplenishInput@1.0'})
    return redirect("https://192.168.1.35:8100/sucess")

@app.route('/sucess')
def sucess():
    return render_template('sucess.html')

if __name__ == '__main__':
    context = ('/home/pi/web/server.crt','/home/pi/web/server.key')
    app.run(host='0.0.0.0', debug=True, port=8100, ssl_context=context)
