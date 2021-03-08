import webbrowser, requests, smtplib, time
from datetime import datetime


MY_EMAIL = input('email address: ')
MY_PASSWORD = input('email password: ')

LAT = 40.712776
LNG = -74.005974


def is_iss_overhead():
    response = requests.get(url='http://api.open-notify.org/iss-now.json')
    response.raise_for_status()

    data = response.json()
    # print(data)

    iss_latitude = float(data['iss_position']['latitude'])
    iss_longitude = float(data['iss_position']['longitude'])
    zoom = 3

    iss_position = (latitude, longitude)
    print(iss_position)


    google_maps = f'https://www.google.com/maps/@{iss_latitude},{iss_longitude},{zoom}z'
    webbrowser.open(google_maps)
    print(f'ISS International Space Station location: latitude: {iss_latitude}, longitude: {iss_longitude}')


    if (LAT - 5 <= iss_latitude) <= LAT + 5 \
        and (LNG - 5 <= iss_longitude) <= LNG + 5:
        return True
        

def is_night():
    parameters = {
        'lat': LAT,
        'lng': LNG,
        'formatted': 0
    }

    response = requests.get('https://api.sunrise-sunset.org/json', params=parameters)
    response.raise_for_status()
    data = response.json()

    sunrise = int(data['results']['sunrise'].split('T')[1].split(':')[0])
    sunset = int(data['results']['sunset'].split('T')[1].split(':')[0])

    # print(sunrise)
    # print(sunset)


    time_now = datetime.now().hour
    print(time_now.hour)


    if time_now >= sunset or time_now <= sunrise:
        return True
    

while True:
    time.sleep(60)
    if is_iss_overhead() and is_night():
        connection = smtplib.SMTP('smtp.gmx.com') # change to your smtp
        connection.startls()
        connection.login(MY_EMAIL, MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg='Subject: The ISS is above you!'
        )