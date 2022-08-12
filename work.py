"""
TUTORIAL LINK FOR UPDATING SHEETS USING API:https://www.youtube.com/watch?v=4ssigWmExak
"""

import requests
from datetime import datetime
from googleapiclient.discovery import build
from google.oauth2 import service_account
from dotenv import load_dotenv
import os 
#///////////////////////////////////////////////////////////////////////////////////////////////////////
load_dotenv()
SHEET_ID=os.getenv("SHEET_I")
APP_ID=os.getenv("APP_I")
API_KEY=os.getenv("API_K")
ENDPOINT="https://trackapi.nutritionix.com/v2/natural/exercise"
SERVICE_ACCOUNT_FILE = 'keys.json'# this file contains the credentials of the goggle sheets api
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds=None
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
# The ID  of a sample spreadsheet.
service = build('sheets', 'v4', credentials=creds)
#///////////////////////////////////////////////////////////////////////////////////////////////////////

def upadte_sheet(inputs):
    sheet = service.spreadsheets()
    result2=sheet.values().append(spreadsheetId=SHEET_ID,range="work!a2",valueInputOption="USER_ENTERED",
                            insertDataOption="INSERT_ROWS",body={"values":inputs}).execute()
    print(result2)

#///////////////////////////////////////////////////////////////////////////////////////////////////////
header={
    "x-app-id":APP_ID,
    "x-app-key":API_KEY,
}
sport=input("What did you do to burn calories?\n")
parameters={
    "query":sport,
    "gender":"Male",
    "weight_kg":65,
    "height_cm":155.64,
    "age":23
}
response=requests.post(url=ENDPOINT,json=parameters,headers=header)
Exercises=response.json()["exercises"]
Date=datetime.now().strftime("%d/%m/%Y")
Time = datetime.now().strftime("%X")

#///////////////////////////////////////////////////////////////////////////////////////////////////////

for x in Exercises:
    Exercise=x["name"].title()
    Duration=x["duration_min"]
    Calories=x["nf_calories"]
    inputs=[[Date,Time,Duration,Exercise,Calories]]
    upadte_sheet(inputs)