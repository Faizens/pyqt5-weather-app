
import sys
import requests

from PyQt5.QtWidgets import (QApplication, QWidget, QLabel,
                             QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout)
from PyQt5.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Weather App 2.0 by Faizens")
        self.label1 = QLabel("BASIC WEATHER API APP", self)
        self.label2 = QLabel("Powered by OpenWeatherMap", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Click", self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()
        
        input_box = QHBoxLayout()
        self.city_input.setPlaceholderText("City name")
        input_box.addWidget(self.city_input)
        input_box.addWidget(self.get_weather_button)

        vbox.addWidget(self.label1)
        vbox.addWidget(self.label2)
        vbox.addLayout(input_box)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)
    
        self.label1.setAlignment(Qt.AlignCenter)
        self.label2.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.label1.setObjectName("label1")  
        self.label2.setObjectName("label2")        
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        self.get_weather_button.clicked.connect(self.get_weather)

        self.setStyleSheet("""
            QWidget {
             background-color: skyblue; 
            }               
            
            QLabel, QPushButton {
                font-family: arial;
            }
            QLabel#label1 {
                font-size: 40px;
                font-weight: bold;
                font-style: rhinos;
            }
            QLabel#label2 {
                font-size: 10px;
                font-weight: bold;
                font-style: rhinos;
            }      
            QLineEdit#city_input {
                font-size: 40px;
                background-color: white;
                color: black;
            }
            QPushButton#get_weather_button {
                font-size: 12px;
                font-weight: bold;
                background-color: red;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 20px;
            }
            QPushButton#get_weather_button:pressed {
                background-color: darkred; 
            }
            QLabel#temperature_label {
                font-size: 75px;
            }
            QLabel#emoji_label {
                font-size: 100px;
                font-family: Segoe UI Emoji;
            }
            QLabel#description_label {
                font-size: 50px;
            }
""")     
        
    def get_weather(self):
        api_key = "d6e5499adb3a3ab101d4db1a1ac9e6ec"      
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"


        try:   
            response = requests.get(url)
            response.raise_for_status()               
            data = response.json()                    
            if data["cod"] == 200:
                self.display_weather(data)

        except requests.exceptions.HTTPError as http_err:
            match response.status_code:
                case 400:
                    self.display_error("Bad request|\nPlease check your input")
                case 401:                                             
                    self.display_error("Unauthorized|\nInvalid API key")                   
                case 403:
                    self.display_error("Forbidden|\nAccess is denied")
                case 404:
                    self.display_error("Not found|\nCity not found")
                case 500:
                    self.display_error("Internal server error|\nPlease try again later")
                case 502:
                    self.display_error("Bad gatway|\nInvalid response from the server")
                case 503:
                    self.display_error("Service Unavaiable|\nServer is down")
                case 504:
                    self.display_error("Gatway timeout|\nNo response from the server")
                case _:
                    self.display_error(f"HTTP error occurred|\n{http_err}")

        except requests.exceptions.ConnectionError:  
            self.display_error("Connection error|\nCheck your internet connection")
        except requests.exceptions.Timeout:
            self.display_error("Request timed out|\nThe request timed out")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many redirects|\nCheck the URL")
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request error|\n{req_error}")


    def display_error(self, message):
        self.temperature_label.setStyleSheet("font-size: 30px; color: red;")
        
        self.temperature_label.setText(message)
        
        self.emoji_label.clear()
        self.description_label.clear()

    def display_weather(self, data):
        self.temperature_label.setStyleSheet("font-size: 75px;")
        
        temperature_k = data["main"]["temp"]  
        temperature_c = temperature_k - 273.15             
        self.temperature_label.setText(f"{temperature_c:.1f}°C")
        
        #
        weather_id = data["weather"][0]["id"]
        self.emoji_label.setText(self.get_weather_icon(weather_id))

        weather_description = data["weather"][0]["description"]
        self.description_label.setText(weather_description)

    @staticmethod
    def get_weather_icon(weather_id):
        """Return appropriate weather icon"""
        if 200 <= weather_id <= 232:
            return "⛈️"  # thunderstorm
        elif 300 <= weather_id <= 321:
            return "🌧️"  # drizzle
        elif 500 <= weather_id <= 531:
            return "🌧️"  # rain
        elif 600 <= weather_id <= 622:
            return "❄️"  # snow
        elif 701 <= weather_id <= 741:
            return "🌫️"  # fog
        elif weather_id == 762:
            return "🌋"  # volcanic ash
        elif weather_id == 771:
            return "💨"  # squalls
        elif weather_id == 781:
            return "🌪️"  # tornado
        elif weather_id == 800:
            return "☀️"  # clear
        elif 801 <= weather_id <= 804:
            return "☁️"  # clouds
        return "🌡️"  # default


if __name__ == "__main__":
    app = QApplication(sys.argv) 
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())