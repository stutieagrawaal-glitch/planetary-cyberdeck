import serial
import random
import pandas as pd
import joblib
import time

temp_model = joblib.load("models/temperature_model.pkl")
pressure_model = joblib.load("models/pressure_model.pkl")
windspeed_model = joblib.load("models/windspeed_model.pkl")
weather_model = joblib.load("models/weather_model.pkl")

arduino = serial.Serial("COM19", 9600, timeout=1)   
time.sleep(2)


terrain = {
    "Mercury": ["Crater", "Plain"],
    "Venus": ["Highland", "Plain"],
    "Earth": ["Mountain", "Forest", "Desert", "Ocean"],
    "Mars": ["Crater", "Plain", "Volcano"],
    "Jupiter": ["Belt", "Zone"],
    "Saturn": ["Belt", "Zone"],
    "Uranus": ["Cloud Layer"],
    "Neptune": ["Cloud Layer"]
}


irradiance = {
    "Mercury": 9126,
    "Venus": 2613,
    "Earth": 1361,
    "Mars": 586,
    "Jupiter": 50,
    "Saturn": 15,
    "Uranus": 3.7,
    "Neptune": 1.5
}

albedo = {
    "Mercury": (0.05,0.12),
    "Venus": (0.70,0.80),
    "Earth": (0.25,0.35),
    "Mars": (0.15,0.30),
    "Jupiter": (0.40,0.60),
    "Saturn": (0.45,0.65),
    "Uranus": (0.45,0.60),
    "Neptune": (0.35,0.50)
}



while True:

    if arduino.in_waiting:

        planet = arduino.readline().decode().strip()

        if planet == "":
            continue

        print(f"\nPlanet Selected : {planet}")

        row = pd.DataFrame([{

            "Planet": planet,

            "Latitude_deg": random.uniform(-90,90),

            "Longitude_deg": random.uniform(0,360),

            "Local_Solar_Time_hr": random.uniform(0,24),

            "Solar_Longitude_Ls_deg": random.uniform(0,360),

            "Elevation_m": random.uniform(-8000,21000),

            "Surface_Albedo": random.uniform(
                albedo[planet][0],
                albedo[planet][1]
            ),

            "Solar_Irradiance_Wm2": irradiance[planet],

            "Terrain_Type": random.choice(
                terrain[planet]
            ),

            "Atmospheric_Dust_Loading": random.uniform(0,1)

        }])

        temperature = temp_model.predict(row)[0]
        pressure = pressure_model.predict(row)[0]
        wind = windspeed_model.predict(row)[0]
        weather = weather_model.predict(row)[0]

        print("-----------------------------")
        print(f"Planet      : {planet}")
        print(f"Temperature : {temperature:.2f} °C")
        print(f"Pressure    : {pressure:.2f} Pa")
        print(f"Wind Speed  : {wind:.2f} m/s")
        print(f"Condition   : {weather}")
        print(f"coordinates : ")
        print("-----------------------------")