import requests
from datetime import datetime
from flask import Flask, render_template, request

app = Flask(__name__)

def get_weather_data(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid=08d0b327e78ce1db068c63dfad2c79b3&units=metric'
    response = requests.get(url)
    data = response.json()
    weather = {
        'city': city,
        'temperature': round(data['main']['temp']),
        'description': data['weather'][0]['description'].capitalize(),
        'icon': data['weather'][0]['icon'],
        'humidity': data['main']['humidity'],
        'wind_speed': round(data['wind']['speed'] * 3.6), # Convert m/s to km/h
        'sunrise': datetime.fromtimestamp(data['sys']['sunrise']).strftime('%I:%M %p'),
        'sunset': datetime.fromtimestamp(data['sys']['sunset']).strftime('%I:%M %p'),
        'timezone': data['timezone']
    }
    return weather

def datetimeformat(value, format='%H:%M:%S'):
    return datetime.fromtimestamp(value).strftime(format)

@app.template_filter()
def datetimeformat(value, format='%H:%M:%S'):
    return datetime.fromtimestamp(value).strftime(format)

def get_icon_url(icon_name):
    return f"https://openweathermap.org/img/wn/{icon_name}@2x.png"



@app.route('/', methods=['POST', 'GET'])
def index():
    weather_data = None
    if request.method == 'POST':
        city = request.form['city']
        weather_data = get_weather_data(city)
    return render_template('index.html', weather_data=weather_data,icon_url=get_icon_url)

if __name__ == '__main__':
    app.run(debug=True)