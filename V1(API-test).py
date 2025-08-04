import requests

API_KEY = "815f8b9491b9b96c424f6844bf268d2b"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city_name):
    params = {
        "q": city_name,
        "appid": API_KEY,
        "lang": "tr",
        "units": "metric"
    }
    try:
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if response.status_code == 200:
            print(f"\n📍 {data['name']} - {data['sys']['country']}")
            print(f"🌡️ Sıcaklık: {data['main']['temp']}°C")
            print(f"🤒 Hissedilen: {data['main']['feels_like']}°C")
            print(f"💧 Nem: {data['main']['humidity']}%")
            print(f"🌬️ Rüzgar: {data['wind']['speed']} m/s")
            print(f"⛅ Açıklama: {data['weather'][0]['description']}")
        else:
            print("❌ Şehir bulunamadı veya API hatası!")
    except Exception as e:
        print("⚠️ Hata oluştu:", e)

while True:
    city = input("\nŞehir ismi gir (çıkmak için 'q'): ").strip().lower()
    if city.lower() == "q":
        print("Çıkılıyor...")
        break
    get_weather(city)