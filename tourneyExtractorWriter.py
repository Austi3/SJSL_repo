import matplotlib.pyplot as plt
import numpy as np
import regex as re
import pysmashgg
import pandas as pd
from enum import Enum
import gspread
from gspread_dataframe import set_with_dataframe

from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import json


"""
This file should:
- Read in a google spreadsheet containing a list of tournament hyperlinks
- Use pysmashgg to get results of those tourneys, and write 
- Reference something containing all players alternate tags and fix those when it reads in OR use start.gg account directly
- Write to tournament sheet filling in columsn and information.
- Should dynamically be able to tell whether or not data exists in the sheet or not

"""

# Define your Google Sheets credentials
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

CREDENTIALS_FILE = r'C:\Users\acmaa\DocumentsACM\Local Projects\ImportantCoding\core-synthesis-384200-4101747176bd.json'

creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
client = gspread.authorize(creds)


# Smash.gg API key
KEY = '742fe712e6ebd8fc43700aa1b833d198'

smash = pysmashgg.SmashGG(KEY, True)

##########################################################################################################

def handleSpecialPlayers(tag):
  """
  TODO i might want a way to make this more robust or avoid this, but itll work for now
  """
  tag= tag.replace("~", "") # need this til i get rid of ~~~ formatting
  if tag.lower() in ['snogi', 'critz but retired', '<3 brisket']:
    tag = 'Snogi'
  elif tag.lower() in ['chanman', 'chan', 'poop87', 'funnymoments with ridley']:
    tag = 'Chanman'
  elif 'Poop' in tag:
    print("my name is", tag.lower())
  elif tag.lower() in ['sauce', 'hotsaucefuego','obmcbob', 'gravy']:
    tag = 'Sauce'
  elif tag in ['xavier', 'Xavier']:
    tag = 'Xavier'
  elif tag.lower() in ["vince", "sapphire"]:
    tag = "Vince"
  elif tag.lower() in ["hunter", "hunterwinthorpe"]:
    tag = "Hunter"
  elif tag.lower() in ["pee83", "treestain", "justin rodriguez"]:
    tag = "Treestain"
  elif tag.lower() in ["spiro", "tinder god"]:
    tag = "Spiro"
  elif tag.lower() in ["jacie", "jesty"]:
    tag = "Jesty"
  elif tag.lower() in ["grey", "badfish321"]:
    tag = "Grey"

  return tag



def updateTourneyDataSheet(docName, sheetName):
    # Will update the google sheet specified


    # Open the worksheet and get all the data as a list of lists
    sheet = client.open(docName).worksheet(sheetName)
    data = sheet.get_all_values()

    # Convert the data to a pandas DataFrame
    df = pd.DataFrame(data[1:], columns=data[0])


   # loop through each row of the DataFrame and extract the name from the hyperlink URL
   # store in a list to be added to the dataframe in order to match the links
    tournNamesList = []
    smashGGNameIDsList = []
    tournAttendanceList = []
    tournResults = []
    tournResultsDictsList=[]

    for index, row in df.iterrows():
        tournURL = row['Tourney URL']
        if df.loc[index, 'Tourney SmashGG ID'] != "":
           continue

        """TODO inset a check here to see hey if columns are empty extract"""
        print("url is", tournURL)
        smashGGTourneyName = tournURL.split('/')[-3]
        eventString = tournURL.split('/')[-1]

        tournament = smash.tournament_show(smashGGTourneyName)
        tournName = tournament['name']
        tournAttendance = tournament['entrants']
        

        # add a value to the "new_column" column of the row with index 0
        df.loc[index, 'Tourney SmashGG ID'] = smashGGTourneyName
        df.loc[index, 'Tourney Name'] = tournName
        df.loc[index, 'Attendence'] = tournAttendance
        

        tournResultsDict = {}

        resultsList = []
        i = 0
        pageNum = 1
        while i <= tournAttendance:
            resultsList += smash.tournament_show_entrants(smashGGTourneyName, eventString, pageNum)
            i+= 25
            pageNum+= 1

        for playerDataResult in resultsList:

            name = playerDataResult['tag'].split('| ')[-1]
            placement = playerDataResult['finalPlacement']

            # TODO i technically could get player info directly whyile im here. try this later?
            # entrant_sets = smash.tournament_show_entrant_sets(smashGGTourneyName, eventString, 'acorn')
            # print(entrant_sets)
            # seed = playerDataResult['seed']
        
            realTag = handleSpecialPlayers(name)
            tournResultsDict[realTag] = placement
    
        result_str = json.dumps(tournResultsDict)
        df.loc[index, 'Results'] = result_str

        
        # append all the info to the overall list
        # tournNamesList.append(tournName)
        # # smashGGNameIDsList.append(smashGGTourneyName)
        # tournAttendanceList.append(tournAttendance)
        # tournResultsDictsList.append(tournResultsDict)

    

    # df['Results'] = tournResultsDictsList
    # print(tournResultsDictsList)


    sheet.update([df.columns.values.tolist()] + df.values.tolist())

    return

############################################################
docName = "2023 SJ Smash Sheet"
sheetName = "testTourneysSheet"

updateTourneyDataSheet(docName, sheetName)
















# # replace the tournament_slug with the actual Smash.gg tournament slug
# tournament_slug = "hops-stocks-14-2-6-2023"
# tournament = smash.tournament_show(tournament_slug)

# # retrieve the entrants in the tournament
# entrants = smash.tournament_show_entrants(tournament_slug, )

# # print the tag of each entrant
# for e in entrants:
#     print(e["tag"])


# def formatTourneyName(name, tournEnum):    
#     splitName = name.split("-")

#     endNum = ""
#     for elt in splitName:
#       if re.search("[0-9]", elt):
#         endNum += "-" + elt

#     if tournEnum == TS.HOPS.value:
#       newName = "Hops N stocks"
#     elif tournEnum == TS.HYPR.value:
#       newName = "Hyperspace"
#     elif tournEnum == TS.PBJ.value:
#         newName = "Pop The Bubble"
#     elif tournEnum == TS.BOTB.value:
#       newName = "Battle Over The Bridge"
#     elif tournEnum == TS.ROWN.value:
#       newName = "RU Smashin"
#     elif tournEnum == TS.CAT.value:
#       newName = "Catastrophe"
#     else:
#       if "pbj-presents-road-to-apex" in name:
#         newName = "PBJ Road to Apex"
#       elif "palooza" in name:
#         newName = "PBJ Holiday Palooza"

#       newName = name.replace("-", " ")
#       newName = newName.title()
#       endNum = ""
    
#     return newName + endNum



def writeToResultsSheet(tourneyDF):
  """
  write to preliminary api sheet
  """


  googleSheet = client.open(seasonTourneyFileName)

  resultsSheet = googleSheet.worksheet('Results Sheet Test')

  resultsSheet.clear()
  set_with_dataframe(worksheet=resultsSheet, dataframe=tourneyDF, include_index=False,
  include_column_header=True, resize=True)