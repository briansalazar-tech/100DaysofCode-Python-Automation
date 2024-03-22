import smtplib, os
from email.message import EmailMessage
from datetime import date
from weatherdata import generate_tables

EMAIL = os.environ.get("email")
APP_PW = os.environ.get("app_pw")
TO_ADDRESS = os.environ.get("email")
SMTP_SERVER = os.environ.get("smtp_server")
TODAY = str(date.today())

#### ------------------------------------------------- NOTES ----------------------------------------------------------- ####
# Weather data.py pulls the same data from the Day 96 project. Refer to fields values pulled in that file.                  #
# Ski Resort website (Day 96) lists complete data.                                                                          #
# This project omits two days of data along with the following entries from the resorts: feels_like, humidity, and clouds.  #
# Data omited to cut down on the length of the email that is sent. Currently sitting at about 170 lines of text.            #
# Feel free to modify data pulled as well as what data is emailed/nubmer of days looped through.                            #
#### ------------------------------------------------------------------------------------------------------------------- ####

# Try block first pulls the resort data using the weatherdata.py file. If data is successfuly pulled, body is composed and email is sent.
try:
    print("Pulling API data")
    resort_data = generate_tables()

    # Establish connection
    connection = smtplib.SMTP(SMTP_SERVER)
    connection.starttls()
    connection.login(user=EMAIL, password=APP_PW)

    print("Composing email body")
    body = "Weather data for local ski & snow resorts over the next three days!! See scripts notes to customize output!\n\n"
    # Loops through all resorts returned from the generate table function.
    for resort in range(len(resort_data)):
        # Resort Name & Website
        body +=  f"{resort_data[resort][0]}\nResort's website: {resort_data[resort][1]}\n------ Weather Data ------\n" 
        # Returns 3 days of data in 5 hour incriments. Would have been 5 days with additional columns, but decided to omit data so email would not be massive blocks of text.
        for index in range(2, len(resort_data[0]) - 16):
            # Date, time, and weather data
            body += f"{resort_data[0][index][0]} -- Temp: {str(resort_data[resort][index][1])}°F - Weather Conditions: {resort_data[resort][index][4]} - Wind/Gust Speeds: {str(resort_data[resort][index][6])} MPH/{str(resort_data[resort][index][7])} MPH\n"
        body += "------------------------\n"
    
    body += "\nHappy adventures!"

    print("Sending email")

    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = f"Ski & Snow data for {TODAY}"
    msg['from'] = EMAIL
    msg['to'] = TO_ADDRESS

    connection.send_message(msg)
    connection.close()
    print("SUCCESS: Email sent with weather data.")

# If API call is not successful or body fails to compose properly, except block is executed.
except:

    body = "ERROR: Data not retrieved properly from OpenWeather. Verify that body composed properly."
    
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = f"ERROR: Ski & Snow data for {TODAY}"
    msg['from'] = EMAIL
    msg['to'] = TO_ADDRESS

    connection.send_message(msg)
    connection.close()
    print("ERROR: Unable to properly compose body. Verify that body composed properly. Check that API data was pulled correctly.")