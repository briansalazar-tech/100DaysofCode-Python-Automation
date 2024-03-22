import requests, os
from datetime import *

OWM_ENDPOINT = "https://api.openweathermap.org/data/2.5/forecast" # OpenWeather 5 Day 3 hour forecast endpoint
OWM_API_KEY = os.environ.get("OWM_API_KEY")
RESORT_NAMES = ["Mt. Rose Ski Tahoe", "Kirkwood Mountain Resort", "Northstar California Resort", "Palisades Tahoe", "Boreal Mountain Resort", "Heavenly Mountain Resort"]
RESORT_COORDINATES = [
    (39.31536205966153, -119.88242696290214), # Mt. Rose (Lat, Long)
    (38.685076025688694, -120.06518256903614), # Kirkwood (Lat, Long)
    (39.265070549674995, -120.13310469872255), # Northstar (Lat, Long)
    (39.19764404248699, -120.23275009165587), # Palisades (Lat, Long)
    (39.3363862980587, -120.35044481515166), # Boreal (Lat, Long)
    (38.935603234448905, -119.94488547556679), # Heavenly (Lat, Long)
                      ]
RESORT_LINKS = [
    "https://skirose.com/", # Mt. Rose
    "https://www.kirkwood.com/", # Kirkwood
    "https://www.northstarcalifornia.com/", # Northstar
    "https://www.palisadestahoe.com/", # Palisades
    "https://www.rideboreal.com/", # Boreal
    "https://www.skiheavenly.com/", # Heavenly
              ]


def pull_weather_data():
    """
    Function pulls information from OpenWeather using the 3 Hour / 5 Day API endpoint. 
    Function loops through each entry in RESORT_COORDINATES and creates a dictionary entry using the resort_template dictionary.
    Each dictionary is added to resort_list which is then returned.
    """
    resort_template = {
    "name": "",
    "link": "",
    "temp": [],
    "feels_like": [],
    "humidity": [],
    "weather_desc": [],
    "clouds": [],
    "wind_speed": [],
    "gusts": [],
    "date_time": [],
    }

    resorts_list = []

    for resort_index in range(len(RESORT_NAMES)):
        parameters = {
            "lat": RESORT_COORDINATES[resort_index][0],
            "lon": RESORT_COORDINATES[resort_index][1],
            "appid": OWM_API_KEY,
            "units": "imperial"

        }

        response = requests.get(url=OWM_ENDPOINT, params=parameters)
        weather_data = response.json()

        resort_template["name"] = RESORT_NAMES[resort_index]
        resort_template["link"] = RESORT_LINKS[resort_index]
        
        for time_stamp in range(40): # 8 Time stamps per day over 5 days
            resort_template["temp"].append(weather_data['list'][time_stamp]['main']['temp'])
            resort_template["feels_like"].append(weather_data['list'][time_stamp]['main']['feels_like'])
            resort_template["humidity"].append(weather_data['list'][time_stamp]['main']['humidity'])
            resort_template["weather_desc"].append(str(weather_data['list'][time_stamp]['weather'][0]['main']) + " - " + str(weather_data['list'][0]['weather'][0]['description']))
            resort_template["clouds"].append(weather_data['list'][time_stamp]['clouds']['all'])
            resort_template["wind_speed"].append(weather_data['list'][time_stamp]["wind"]["speed"])
            resort_template["gusts"].append(weather_data['list'][time_stamp]["wind"]["gust"])
            resort_template["date_time"].append(weather_data['list'][time_stamp]["dt_txt"])

        resorts_list.append(resort_template)
        
        resort_template = {
            "name": "",
            "link": "",
            "temp": [],
            "feels_like": [],
            "humidity": [],
            "weather_desc": [],
            "clouds": [],
            "wind_speed": [],
            "gusts": [],
            "date_time": [],
        }

    return resorts_list

def generate_tables():
    """
    Generate Tables takes the data from pull_weather_data and cleans up the information.
    First, the date_time inforamtion is cleaned up and formatted.
    Second, the information pull_weather_data is reformatted so that information can be displayed in rows when rendered.
    Invididual locations are added to the resort_data list which are then added to the all_resorts list.
    """
    raw_resort_list = pull_weather_data()
    all_resorts = []
    resort_data = []
    item_row = []

    # Convert time values
    for resort_index in range(len(raw_resort_list)):
    
        for datetime_pos in range(len(raw_resort_list[resort_index]['date_time'])):
            datetime_str = raw_resort_list[resort_index]['date_time'][datetime_pos]
            datetime_object = datetime.strptime( datetime_str, '%Y-%m-%d %H:%M:%S')
            formatted_time = datetime_object.strftime('%B %d, %Y @ %I:%M%p')
            raw_resort_list[resort_index]['date_time'][datetime_pos] = formatted_time
    
    # Create a new list for each resort. Rows will be list items appended from index of raw data for each key
    for resort_index in range(len(raw_resort_list)):
        resort_data.append(raw_resort_list[resort_index]["name"])
        resort_data.append(raw_resort_list[resort_index]["link"])

        for item in  range(len(raw_resort_list[0]['temp'])):
            item_row.append(raw_resort_list[0]['date_time'][item])
            item_row.append(raw_resort_list[0]['temp'][item])
            item_row.append(raw_resort_list[0]['feels_like'][item])
            item_row.append(raw_resort_list[0]['humidity'][item])
            item_row.append(raw_resort_list[0]['weather_desc'][item])
            item_row.append(raw_resort_list[0]['clouds'][item])
            item_row.append(raw_resort_list[0]['wind_speed'][item])
            item_row.append(raw_resort_list[0]['gusts'][item])
            resort_data.append(item_row)
            item_row = []
        all_resorts.append(resort_data)
        resort_data = []
    
    return all_resorts