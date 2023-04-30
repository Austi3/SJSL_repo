# import gspread
# from oauth2client.service_account import ServiceAccountCredentials

# # Replace the variables below with your own values
# SPREADSHEET_NAME = "SJPlayerLevels"
# SHEET_NAME = "2023Q1"
# CREDS_FILE = r'C:\Users\acmaa\DocumentsACM\Local Projects\ImportantCoding\core-synthesis-384200-4101747176bd.json'
# # Authenticate with the Google Sheets API using OAuth2 credentials
# creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, ["https://www.googleapis.com/auth/spreadsheets"])
# client = gspread.authorize(creds)

# # Open the specified sheet
# sheet = client.open(SPREADSHEET_NAME).worksheet(SHEET_NAME)

# # Get all the values in the sheet as a list of lists
# data = sheet.get_all_values()

# # Print the data to the console
# print(data)

import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Define the scope that you need to access the API
SCOPE = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']


# Path to the credential JSON file
CREDENTIALS_FILE = r'C:\Users\acmaa\DocumentsACM\Local Projects\ImportantCoding\core-synthesis-384200-4101747176bd.json'

# Authenticate with the Google Sheets API using the JSON file
creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, SCOPE)
client = gspread.authorize(creds)

SPREADSHEET_NAME = "SJPlayerLevels"
SHEET_NAME = "2023Q1"

# # Open the specified sheet
sheet = client.open(SPREADSHEET_NAME).worksheet(SHEET_NAME)

# Get all the values in the sheet as a list of lists
data = sheet.get_all_values()

# Print the data to the console
print(data)