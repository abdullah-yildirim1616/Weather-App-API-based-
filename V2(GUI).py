import tkinter as tk
from tkinter import ttk
import requests
import json
import sys
import os

API_KEY = "815f8b9491b9b96c424f6844bf268d2b"

#CITY_FILE = "Projects\\Weather App(API-based)\\cities.json"

def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".") 
    return os.path.join(base_path, relative_path)

CITY_FILE = get_resource_path("cities.json")

def load_cities():
    with open(CITY_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)
        return [f"{c['name']}, {c['subcountry']}, {c['country']}" for c in data]

def get_weather(city_full_string):
    city_name = city_full_string.split(',')[0]
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&lang=tr&units=metric"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200:
            name = data["name"]
            temp = data["main"]["temp"]
            feels = data["main"]["feels_like"]
            humidity = data["main"]["humidity"]
            pressure = data["main"]["pressure"]
            wind = data["wind"]["speed"]
            visibility = data.get("visibility", 0) / 1000  # km
            lat = data["coord"]["lat"]
            lon = data["coord"]["lon"]
            desc = data["weather"][0]["description"]
            
            result = (
                f"Şehir: {name}\n"
                f"Durum: {desc.capitalize()}\n"
                f"Sıcaklık: {temp}°C\n"
                f"Hissedilen: {feels}°C\n"
                f"Nem: {humidity}%\n"
                f"Basınç: {pressure} hPa\n"
                f"Rüzgar: {wind} m/s\n"
                f"Görüş: {visibility:.1f} km\n"
                f"Koordinat: {lat}, {lon}"
            )
            return result
        else:
            return f"❌ Hata: {data.get('message', 'Bilinmeyen hata')}"
    except Exception as e:
        return f"⚠️ API Hatası: {str(e)}"

def on_key_release(event):
    typed = entry.get().lower()
    listbox.delete(0, tk.END)
    for city in all_cities:
        if typed in city.lower():
            listbox.insert(tk.END, city)

def on_city_select(event):
    if listbox.curselection():
        selected = listbox.get(listbox.curselection())
        entry.delete(0, tk.END)
        entry.insert(0, selected)
        listbox.delete(0, tk.END)
        result = get_weather(selected)
        output_label.config(text=result)

root = tk.Tk()
root.title("🌍 Gelişmiş Hava Durumu")
root.geometry("500x450")
root.configure(bg="#f0f0f5")

style = ttk.Style()
style.configure("TEntry", padding=6, font=("Segoe UI", 12))
style.configure("TListbox", font=("Segoe UI", 12))

entry = ttk.Entry(root, font=("Segoe UI", 12), width=50)
entry.pack(pady=10)
entry.bind("<KeyRelease>", on_key_release)

listbox = tk.Listbox(root, font=("Segoe UI", 12), height=6, width=50)
listbox.pack()
listbox.bind("<<ListboxSelect>>", on_city_select)

output_label = tk.Label(
    root,
    text="Şehir seçin ve hava durumunu görün",
    font=("Segoe UI", 12),
    wraplength=460,
    justify="left",
    bg="#f0f0f5",
    fg="#333"
)
output_label.pack(pady=20)

all_cities = load_cities()

root.mainloop()