import tkinter as tk
from tkinter import messagebox
import requests

API_KEY = "9fcb8c11ab69447111bdbf27c13b47b2"  # put your real key

# ---------------- WEATHER FETCH ----------------
def get_weather():
    city = city_entry.get().strip()

    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name")
        return

    url = (
        f"https://api.openweathermap.org/data/2.5/weather?"
        f"q={city}&appid={API_KEY}&units=metric"
    )

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        if data.get("cod") != 200:
            messagebox.showerror("Error", "City not found or API issue")
            return

        temp = data["main"]["temp"]
        feels = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]
        condition = data["weather"][0]["description"].title()
        city_name = data["name"]

        result_label.config(
            text=(
                f"📍 City: {city_name}\n\n"
                f"🌡 Temperature: {temp} °C\n"
                f"🤗 Feels Like: {feels} °C\n"
                f"☁ Condition: {condition}\n"
                f"💧 Humidity: {humidity}%\n"
                f"🌬 Wind Speed: {wind} m/s"
            )
        )

    except Exception as e:
        messagebox.showerror("Error", str(e))


# ---------------- GUI ----------------
root = tk.Tk()
root.title("Advanced Weather App")
root.geometry("420x450")
root.configure(bg="#1e1e2f")
root.resizable(False, False)

tk.Label(
    root,
    text="🌦 Weather Application",
    font=("Segoe UI", 18, "bold"),
    bg="#1e1e2f",
    fg="white"
).pack(pady=15)

frame = tk.Frame(root, bg="#2a2a40")
frame.pack(padx=20, pady=10, fill="both", expand=True)

tk.Label(
    frame,
    text="Enter City Name",
    font=("Segoe UI", 11),
    bg="#2a2a40",
    fg="white"
).pack(pady=(20, 5))

city_entry = tk.Entry(frame, font=("Segoe UI", 11), width=25, justify="center")
city_entry.pack(pady=5)
city_entry.focus()

tk.Button(
    frame,
    text="Get Weather",
    font=("Segoe UI", 11),
    bg="#4CAF50",
    fg="white",
    command=get_weather
).pack(pady=15)

result_label = tk.Label(
    frame,
    text="",
    font=("Segoe UI", 12),
    bg="#2a2a40",
    fg="white",
    justify="left"
)
result_label.pack(pady=10)

root.mainloop()
