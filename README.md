For day 98 of the 100 Days of Code course, The goal for the project was to create a program that can automate something. For my project, I chose to build on the custom API web app project (Day 96).

Similarly to the custom API based website project, the weatherdata.py file first compiles a list of relevent weather data using the Open Weather Map 5 Day 3 Hour API.

Where this project differs in that project, this project composes and sends an email fro mthe data that is pulled from the weatherdata.py file. Another difference is that the amount of data that is returned is cut back from the website project. Without reeducing the number of days and datapoints that are emailed, the email that is sent was easily hundreds of lines long which was not ideal to look at on a phone or easy on the eyes. After some tweaking, the emails body was knocked down to about 170 lines for data on six different ski and snow resorts. The length of the email can further be tweeked by adding or removing resorts to query or removing time stamps from the resorts that were queried. With where it sits now, the email sends three days of weather timestamps for six different ski resorts.

To get this program to send an email out daily, I passed it through a .ps1 file and ran it through Windows Task Scheduler. 

