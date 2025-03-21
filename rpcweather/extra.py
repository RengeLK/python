from dotenv import load_dotenv
import requests
from termcolor import cprint
import os, datetime

load_dotenv()
owm_key = os.getenv("OWM_KEY2")

cprint("DisWeather EXTRA --- By Renge. v1.1", "blue")
cprint("Please make sure you are connected to the internet and filled out the .env file correctly!", "yellow")
cprint("This script uses the OWM_KEY2 entry instead. Make sure you have filled it out before continuing.", "yellow")
city = input("Enter your city: ")
country = input("Enter your country (in ISO 3166 code): ")

print("Now attempting to look up your city..")
rg = requests.get(f'https://api.openweathermap.org/geo/1.0/direct?q={city},{country}&limit=1&appid={owm_key}')
while True:
    try:
        lat = rg.json()[0]['lat']
        lon = rg.json()[0]['lon']
        cprint("Found successfully! Now getting ready..", "green")
        break
    except IndexError:
        cprint("Failed with IndexError, meaning no city was found. Did you input everything correctly?", "red")
        input("Press Enter to exit.. ")
        exit()
    except KeyError:
        cprint("Failed with KeyError, meaning something went wrong with the API. Did you fill out the .env file correctly?", "red")
        input("Press Enter to exit.. ")
        exit()
    except KeyboardInterrupt:
        exit()
    except:
        cprint("Failed with an unknown error. Check your internet connection and try again.", "red")
        input("Press Enter to exit.. ")
        exit()

while True:
    try:
        rw = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&lang=en&appid={owm_key}')
        # rf = requests.get(f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&units=metric&lang=en&appid={owm_key}')
        rp = requests.get(f'https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={owm_key}')

        rw_city = rw.json()['name']
        rw_country = rw.json()['sys']['country']
        rw_main = rw.json()['weather'][0]['main']
        rw_weather = rw.json()['weather'][0]['description']
        rp_aqi =  "AQI " + str(rp.json()['list'][0]['main']['aqi'])
        rw_temp = str(rw.json()['main']['temp']) + "°C"
        rw_feels = str(rw.json()['main']['feels_like']) + "°C"
        rw_visibility = str(rw.json()['visibility']) + " m"
        rw_pressure = str(rw.json()['main']['pressure']) + " hPa"
        rw_humidity = str(rw.json()['main']['humidity']) + "%"
        rw_windsp = str(rw.json()['wind']['speed']) + " m/s"
        rw_clouds = str(rw.json()['clouds']['all']) + "%"
        rw_sunrise = datetime.datetime.fromtimestamp(rw.json()['sys']['sunrise'])
        rw_sunset = datetime.datetime.fromtimestamp(rw.json()['sys']['sunset'])
        rw_time = datetime.datetime.fromtimestamp(rw.json()['dt'])

        os.system('cls')

        cprint(f'Current weather in {rw_city}, {rw_country}', "green")
        print()
        print(f'{rw_main} - {rw_weather}')
        print(f'{rw_temp}, feels like {rw_feels} - {rp_aqi}')
        print(f'Visibility: {rw_visibility}, Pressure: {rw_pressure}, Humidity: {rw_humidity}, Clouds: {rw_clouds}')
        print(f'Wind -- Speed: {rw_windsp}')
        print()
        cprint("The following timestamps are in your local time!", "yellow")
        print()
        print(f'Sunrise: {rw_sunrise}')
        print(f'Sunset: {rw_sunset}')
        print(f'Query time: {rw_time}')
    except KeyError:
        cprint("Failed with KeyError, meaning something went wrong with the API. Did you fill out the .env file correctly?", "red")
        input("Press Enter to exit.. ")
        exit()
    except KeyboardInterrupt:
        exit()
    except:
        cprint("Failed with an unknown error. Check your internet connection and try again.", "red")
        input("Press Enter to exit.. ")
        exit()