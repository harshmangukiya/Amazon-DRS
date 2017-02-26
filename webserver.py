from flask import Flask, render_template, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/replenish')
def replenish():
    return render_template('replenish.html')

@app.route('/authresponse')
def authresponse():
    return render_template('response.html')

@app.route('/accesstoken/<var>')
def accesstoken(var):
    import requests
    r = requests.post("https://api.amazon.com/auth/o2/token", data={'grant_type': 'authorization_code', 'code': var, 'client_id': 'Client_ID', 'client_secret':'Client_Secret','redirect_uri':'https://192.168.1.35:8100/authresponse'})
    data = r.json()
    accesstoken = data['access_token']
    token = 'Bearer ' + accesstoken
    x = requests.post("https://dash-replenishment-service-na.amazon.com/replenish/Slot_id", headers={'Authorization': token, 'x-amzn-accept-type': 'com.amazon.dash.replenishment.DrsReplenishResult@1.0', 'x-amzn-type-version': 'com.amazon.dash.replenishment.DrsReplenishInput@1.0'})
    return redirect("https://192.168.1.35:8100/sucess")

@app.route('/sucess')
def sucess():
    return render_template('sucess.html')

if __name__ == '__main__':
    context = ('/home/pi/web/server.crt','/home/pi/web/server.key')
    app.run(host='0.0.0.0', debug=True, port=8100, ssl_context=context)
