import requests

lat, lon = 48.1486, 17.1077
url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": lat,
    "longitude": lon,
    "current": "temperature_2m,apparent_temperature,wind_speed_10m",
    "hourly": "temperature_2m",
    "timezone": "Europe/Bratislava"
}

r = requests.get(url, params=params, timeout=10)
r.raise_for_status()
data = r.json()

current = data.get("current", {})
print(f"Aktuál: {current.get('temperature_2m')} °C, "
      f"pocitovo {current.get('apparent_temperature')} °C, "
      f"vietor {current.get('wind_speed_10m')} m/s")

print("\nNajbližších 6 hodín (°C):")
hours = data["hourly"]["time"][:6]
temps = data["hourly"]["temperature_2m"][:6]
for t, temp in zip(hours, temps):
    print(f"{t}: {temp} °C")
