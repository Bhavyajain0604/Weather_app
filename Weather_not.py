from tkinter import *
import tkinter as tk
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import datetime
import requests
import pytz
from PIL import Image, ImageTk
from tkinter import messagebox

# Function to fetch weather data
def getWeather():
    try:
        city = textfield.get().strip()
        if not city:
            messagebox.showerror("Weather App", "Please enter a city name.")
            return

        geolocator = Nominatim(user_agent="my_weather_app")  # Replace 'my_weather_app' with your user agent
        location = geolocator.geocode(city)
        if location:
            obj = TimezoneFinder()
            result = obj.timezone_at(lng=location.longitude, lat=location.latitude)
            home = pytz.timezone(result)
            local_time = datetime.now(home)
            current_time = local_time.strftime("%I:%M %p")
            clock.config(text=current_time)
            name.config(text="CURRENT TIME")

            # Fetch weather data from OpenWeatherMap API
            api = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=cf0833e315dc0fbec8baf38e4e8f36cf"
            response = requests.get(api)
            if response.status_code == 404:
                messagebox.showerror("Weather App", "City not found. Please check your spelling and try again.")
                return
            
            json_data = response.json()

            # Temperature
            temp = int(json_data['main']['temp'] - 273.15)
            t.config(text=f"{temp} °C")

            # Weather condition
            condition = json_data['weather'][0]['main']
            c.config(text=f"{condition} | FEELS LIKE {temp} °C")

            # Wind speed
            wind_speed = json_data['wind']['speed']
            wind.config(text=f"WIND: {wind_speed} m/s")

            # Humidity
            humidity_value = json_data['main']['humidity']
            humidity.config(text=f"HUMIDITY: {humidity_value}%")

            # Pressure
            pressure_value = json_data['main']['pressure']
            pressure.config(text=f"PRESSURE: {pressure_value} hPa")
        else:
            messagebox.showerror("Weather App", "Location not found. Please check your spelling and try again.")

    except requests.exceptions.RequestException as e:
        messagebox.showerror("Weather App", f"Error fetching data: {e}")
    except KeyError as e:
        messagebox.showerror("Weather App", f"Invalid response format: {e}")
    except Exception as e:
        messagebox.showerror("Weather App", f"An unexpected error occurred: {e}")

# Create main application window
root = Tk()
root.title("Weather App")
root.geometry("900x600+300+200")
root.resizable(False, False)

# Search Box
Search_image = PhotoImage(file="search_bar.png")
myimage = Label(image=Search_image)
myimage.place(x=20, y=20)

textfield = Entry(
    root,
    justify="center",
    width=17,
    font=("Times New Roman", 24, "bold"),
    bg="#404040",
    fg="white",
    border=0,
)
textfield.place(x=50, y=40)
textfield.focus()

# Search Icon
Search_icon = PhotoImage(file="search_icon.png")
myimage_icon = Button(
    image=Search_icon, borderwidth=0, cursor="hand2", bg="#404040", command=getWeather
)
myimage_icon.place(x=400, y=34)

# Logo
image = Image.open("logo.png")
resize_image = image.resize((250, 250))
Logo_image = ImageTk.PhotoImage(resize_image)
logo = Label(image=Logo_image)
logo.place(x=100, y=140)

# Time Display
name = Label(root, font=("Times New Roman", 33, "bold"))
name.place(x=480, y=150)
clock = Label(root, font=("Times New Roman", 30, "bold"))
clock.place(x=550, y=210)

# Labels for weather details
t = Label(root, font=("Times New Roman", 65, "bold"), fg="#ee666d")
t.place(x=550, y=300)

c = Label(root, font=("Times New Roman", 27, "bold"))
c.place(x=400, y=400)

# Labels for wind, humidity, pressure
wind = Label(text="WIND: ...", font=("Times New Roman", 18, "bold"), bg="#1ab5ef")
wind.place(x=180, y=540)

humidity = Label(text="HUMIDITY: ...", font=("Times New Roman", 18, "bold"), bg="#1ab5ef")
humidity.place(x=370, y=540)

pressure = Label(text="PRESSURE: ...", font=("Times New Roman", 18, "bold"), bg="#1ab5ef")
pressure.place(x=620, y=540)

root.mainloop()
