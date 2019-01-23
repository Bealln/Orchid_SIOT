import csv
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
import datetime
import time
import multiprocessing
import RPi.GPIO as GPIO
import time




def weather_info():

    # Create timeout- 7 days, 24 hours, 60 min, 60 seconds
    timeout = time.time() + 60 * 60 * 24 * 7
    #timeout = time.time() + 120

    JSON_FILENAME = 'data.json'

    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    # drive
    creds = ServiceAccountCredentials.from_json_keyfile_name(JSON_FILENAME, scope)
    client = gspread.authorize(creds)
    sheet = client.open("Weather_data")
    ws = sheet.get_worksheet(0)
    ws.append_row(["Date", "Time", "City", "Weather", "Wind speed", "humidity", "temperature"])

    # Print title on csv offline file for backup
    with open('weather.csv', 'w', newline='') as f:
        headers = ['Date', 'Time', 'City', 'Weather', 'Temperature', 'Wind speed', 'Humidity']
        w = csv.DictWriter(f, fieldnames=headers)
        w.writeheader()
        while True:
            if time.time() > timeout:
                break
            elif time.time() < timeout:
                city_id= '6360186'
                my_id = '877d9a23b9f8e7f5b3296c6ffa06e96a'
                r = requests.get('http://api.openweathermap.org/data/2.5/weather?id='+city_id+'&appid='+my_id+'')
                data = r.json()
                city = data['name']
                weather = data['weather'][0]['description']
                #wind = data['wind']
                wind_speed = data['wind']['speed']
                humidity = float(data['main']['humidity'])
                temp_k = float(data['main']['temp'])
                temp_c = (temp_k - 273.15)

                now = datetime.datetime.now()

                # json filename for credentials
                JSON_FILENAME = 'data.json'

                # Google sheet to save to
                # GSq'Weather_data'

                scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
                # drive
                creds = ServiceAccountCredentials.from_json_keyfile_name(JSON_FILENAME, scope)
                client = gspread.authorize(creds)
                sheet = client.open("Weather_data")
                ws = sheet.get_worksheet(0)
                ws.append_row([now.strftime("%d/%m/%Y"), now.strftime("%H:%M:%S"), city, weather,wind_speed, humidity, temp_c])

                #Print to offline csv file

                w.writerow({'Date': now.strftime("%d/%m/%Y"), "Time":now.strftime("%H:%M:%S"), 'City': city, 'Weather': weather, 'Temperature': temp_c, 'Wind speed': wind_speed, 'Humidity': humidity})


                #Wait for next,calculate every 15 minutes
                time.sleep(60 * 15)
                #time.sleep(5)

def sensor_info():
    # First drive, print titles
    #It misses out 3 seconds

    # Print titles for weather data

    # Create timeout
    #timeout = time.time() + 60 * 60 * 24 * 7
    GPIO.setmode(GPIO.BCM)
    GPIO_TRIGGER = 23
    GPIO_ECHO = 24

    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN)

    # Create timeout- 7 days, 24 hours, 60 min, 60 seconds
    timeout = time.time() + 60 * 60 * 24 * 7

    JSON_FILENAME = 'data.json'

    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    # drive
    creds = ServiceAccountCredentials.from_json_keyfile_name(JSON_FILENAME, scope)
    client = gspread.authorize(creds)
    sheet = client.open("Presence_data")
    ws = sheet.get_worksheet(0)
    ws.append_row(["Date", "Time", "Measurement", "Presence"])

    # Print title on csv offline file for backup
    with open('presence.csv', 'w', newline='') as f:
        headers = ["Date", "Time", "Measurement", "Presence"]
        w = csv.DictWriter(f, fieldnames=headers)
        w.writeheader()

        while True:
            if time.time() > timeout:
                break
            elif time.time() < timeout:
                GPIO.output(GPIO_TRIGGER, True)
                # set Trigger after 0.01ms to LOW
                time.sleep(0.00001)
                GPIO.output(GPIO_TRIGGER, False)
                StartTime = time.time()
                StopTime = time.time()

                while GPIO.input(GPIO_ECHO) == 0:
                    StartTime = time.time()
                # save time of arrival
                while GPIO.input(GPIO_ECHO) == 1:
                    StopTime = time.time()
                # time difference between start and arrival
                TimeElapsed = StopTime - StartTime
                # multiply with the sonic speed (34300 cm/s)
                # and divide by 2, because there and back
                distance = (TimeElapsed * 34300) / 2

                #The wall is around 90 (It gets around 94)
                if distance < 30 :
                    print("Measured Distance = %.1f cm" % distance)
                    presence = "Yes"
                    now = datetime.datetime.now()

                    # json filename for credentials
                    JSON_FILENAME = 'data.json'

                    # Google sheet to save to
                    # GSHEET_NAME = 'Weather_data'

                    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
                    # drive
                    creds = ServiceAccountCredentials.from_json_keyfile_name(JSON_FILENAME, scope)
                    client = gspread.authorize(creds)
                    sheet = client.open("Presence_data")
                    ws = sheet.get_worksheet(0)
                    ws.append_row([now.strftime("%d/%m/%Y"), now.strftime("%H:%M:%S"), distance, presence])

                    # Print to offline csv file

                    w.writerow(
                        {'Date': now.strftime("%d/%m/%Y"), "Time": now.strftime("%H:%M:%S"), 'Measurement': distance,
                         'Presence': presence})

                    # Wait for next
                    # time.sleep(60 * 15)
                    # time.sleep(2)
                    # return city, humidity, temp_c,now

               # else:
                 #   presence = "No"





if __name__ == '__main__':
    weather = multiprocessing.Process(name= "weather", target= weather_info)
    sensor = multiprocessing.Process(name="sensor", target=sensor_info)
    #weather_info()
    #sensor_info()

    weather.start()
    sensor.start()
