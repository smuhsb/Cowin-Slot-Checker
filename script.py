
import requests
from datetime import date, datetime

from requests.models import Response

import pandas as pd

# District ID for Gulbarga, Karnataka
districtId = "267"     

# Get Today's Date in DD-MM-YYYY format
today = date.today()
formattedDate = today.strftime('%d-%m-%Y')

# Intialize Data
data = []

# Build URL for getting Data from CoWIN
URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id="+districtId+"&date="+formattedDate

# HTTP Request
result = requests.get(URL)

if districtId == '267':
    print(URL)

if result.ok:
    ResponseJson = result.json()
    if ResponseJson["centers"]:
        for center in ResponseJson["centers"]:
            for session in center["sessions"]:
                if (session["min_age_limit"] == 18): #and session["available_capacity"] > 0 and session["available_capacity_dose1"] > 0):
                    sessionDate = session["date"]
                    sessionDose = session["available_capacity_dose1"]
                    data.append([sessionDate,sessionDose])

# Proceed if any slots found
if data:

# Create DataFrame
    df = pd.DataFrame(data, columns = ['Date', 'Slots'])
    df['Date'] = pd.to_datetime(df['Date'])
    df['Date'] = df['Date'].dt.strftime("%d-%m-%Y")
    df.sort_values(by=['Date'], inplace=True)
    df['Slots'] = pd.to_numeric(df['Slots'])
    df = df.groupby(['Date']).sum().reset_index()

print(df)