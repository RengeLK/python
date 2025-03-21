from pypresence import Presence
from dotenv import load_dotenv
import requests
from termcolor import cprint
import os, time

load_dotenv()
client_id = os.getenv("CLIENT_ID")
owm_key = os.getenv("OWM_KEY")

cprint("DisWeather / rpcweather --- By Renge. v1.2", "blue")
cprint("Please make sure you are connected to the internet and filled out the .env file correctly!", "yellow")
city = input("Enter your city: ")
country = input("Enter your country (in ISO 3166 code): ")

print("Now attempting to look up your city..")
rg = requests.get(f'https://api.openweathermap.org/geo/1.0/direct?q={city},{country}&limit=1&appid={owm_key}')
while True:
    try:
        lat = rg.json()[0]['lat']
        lon = rg.json()[0]['lon']
        cprint("Found successfully! Now getting weather and starting up RPC..", "green")
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

RPC = Presence(client_id)
RPC.connect()

while True:
    try:
        rw = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&lang=en&appid={owm_key}')
        rp = requests.get(f'https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={owm_key}')

        rw_icon = rw.json()['weather'][0]['icon'] # icon to use
        rw_weather = rw.json()['weather'][0]['description'] # long weather
        rw_main = rw.json()['weather'][0]['main'] # short weather
        rp_aqi = rp.json()['list'][0]['main']['aqi'] # air pollution
        rw_temp = str(round(rw.json()['main']['temp'])) + "°C" # rounded float to str from json, temperature
        rw_tempf = str(rw.json()['main']['temp']) + "°C" # full float to str from json, temperature

        RPC.update(
            details=f"{rw_main}, {rw_temp}, AQI {rp_aqi}",
            state=f"{city}, {country}",
            large_image=rw_icon,
            large_text=rw_weather,
            small_image="temp",
            small_text=rw_tempf,
            buttons=[{"label": "Made by Renge", "url": "https://nelinka.neocities.org/projects/rpcweather"}, {"label": "Powered by OpenWeatherMap", "url": "https://openweathermap.org"}]
        )

        print("Still alive and working..")
        time.sleep(15)
    except KeyError:
        cprint("Failed with KeyError, meaning you probably ran out of API requests. Wait 1 minute, then try again.", "red")
        input("Press Enter to exit.. ")
        exit()
    except KeyboardInterrupt:
        exit()
    except:
        cprint("Failed with an unknown error. Check your internet connection and try again.", "red")
        input("Press Enter to exit.. ")
        exit()