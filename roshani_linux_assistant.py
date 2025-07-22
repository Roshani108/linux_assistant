import os
import subprocess
import time
import platform
import shlex
import requests

# 🔑 Your OpenWeatherMap API Key
API_KEY = "c3c7089d0fe258c5850660b57abfc742"

def get_weather():
    city = input("🏙️ Enter city name: ").strip()

    if not city:
        print("❌ City name cannot be empty.")
        return

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()

        if data["cod"] != 200:
            print(f"❌ Error: {data.get('message', 'City not found')}")
            return

        weather = data["weather"][0]["description"].capitalize()
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]

        print(f"\n🌤️ Weather in {city}: {weather}")
        print(f"🌡️ Temperature: {temp}°C (Feels like {feels_like}°C)")
        print(f"💧 Humidity: {humidity}%\n")

    except Exception as e:
        print(f"❌ Failed to fetch weather: {e}\n")

def open_file_or_folder():
    raw_input = input("📂 Enter the full path of the file/folder to open: ").strip()

    try:
        path = shlex.split(raw_input)[0] if raw_input else ""
    except ValueError:
        print("❌ Invalid path format.")
        return

    if os.path.exists(path):
        try:
            system_type = platform.system()
            kernel = platform.release().lower()

            if system_type == "Linux" and "microsoft" in kernel:
                # ✅ WSL - use Windows Explorer
                drive = path.split("/")[2].upper()
                win_path = path.replace(f"/mnt/{drive.lower()}", f"{drive}:").replace("/", "\\")
                subprocess.run(["explorer.exe", win_path])
            elif system_type == "Windows":
                os.startfile(path)
            else:
                subprocess.call(["xdg-open", path])

            print("✅ Opened successfully.\n")
        except Exception as e:
            print(f"❌ Failed to open path: {e}\n")
    else:
        print("❌ Path not found.\n")

def set_reminder():
    reminder = input("⏰ What should I remind you of? ")
    try:
        delay = int(input("⏳ In how many seconds? "))
        print(f"🕒 Reminder set for {delay} seconds...")
        time.sleep(delay)
        print(f"🔔 Reminder: {reminder}")
    except ValueError:
        print("❌ Please enter a valid number.\n")

def log_daily_task():
    task = input("📝 Enter the task you completed: ")
    with open("daily_log.txt", "a") as file:
        file.write(f"{time.ctime()}: {task}\n")
    print("✅ Task logged!\n")

def main():
    while True:
        print("\n" + "=" * 50)
        print("🌟  Welcome to Roshani Assist - Cross-Platform CLI Tool  🌟")
        print("=" * 50)
        print("1. 🌤️ Get Weather")
        print("2. 📂 Open File/Folder")
        print("3. ⏰ Set Reminder")
        print("4. 📝 Log Daily Task")
        print("5. 🚪 Exit")
        print("=" * 50)

        choice = input("Choose an option [1-5]: ").strip()

        if choice == '1':
            get_weather()
        elif choice == '2':
            open_file_or_folder()
        elif choice == '3':
            set_reminder()
        elif choice == '4':
            log_daily_task()
        elif choice == '5':
            print("👋 Goodbye, Roshani!")
            break
        else:
            print("❌ Invalid choice. Please enter a number between 1 and 5.\n")

if __name__ == "__main__":
    main()
