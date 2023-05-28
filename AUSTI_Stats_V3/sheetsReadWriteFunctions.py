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
import datetime
from Calculations import *
from Tourney import *


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

################################# Player Functions ####################################################################


def getPlayerLevels(docName, sheetName, ptValueIncrement):
    """
    Reads the clusters google sheet and returns a dictionary of player lists with values for each group
    """
    # Open the specified sheet
    playersheet = client.open(docName).worksheet(sheetName)

    # get all values from the sheet
    data = playersheet.get_all_values()

  # Convert the data to a pandas DataFrame
    df = pd.DataFrame(data[1:], columns=data[0])

    column_lists = []
    for col in df.columns:
      column_list = list(df[col].dropna())
      column_lists.append(column_list)

    clusterList = [[item for item in lst if item] for lst in column_lists]
    
    playerLevelsDict = {}
    pts = ptValueIncrement
    for playerCluster in clusterList:
      playerLevelsDict[pts] = playerCluster
      pts += ptValueIncrement


    return playerLevelsDict

################################# Tourney Functions ####################################################################


def getTourneyInfo(tourneyLink, smashGGName):
  """
  Returns the tournament series, a properly formatted and shortened tourney name, and color of tourney
  """
  splitName = smashGGName.split("-")
  endNum = ""
  for elt in splitName:
    if re.search("[0-9]", elt):
      endNum += "-" + elt

  if "hops" in tourneyLink:
    tSeries = "Hops N' Stocks"
    color = "orange"
  elif "ru" in tourneyLink and "smashin" in tourneyLink:
    tSeries = "RU' Smashin"
    color = "gold"
  elif "bubble" in tourneyLink:
    tSeries = "Pop The Bubble"
    color = "pink"
  elif "battle" in tourneyLink:
    tSeries = "BOTB"
    color = 'red'
  elif "catastrophe" in tourneyLink:
    tSeries = "Catastrophe"
    color = 'blue'
  else:
     tSeries = "Other"
     color = 'green'
     newTName = smashGGName.replace("-", " ").title()
     return tSeries, newTName, color

  newTName = tSeries + endNum
  newTName = newTName.replace("-", " ")
  return tSeries, newTName, color
  


def getTourneyObjDict(docName, sheetName):
    """
    Reads the google sheet specified and returns a toruney object dictionary
    """
    # Open the worksheet and get all the data as a list of lists
    sheet = client.open(docName).worksheet(sheetName)
    data = sheet.get_all_values()

    tourneyObjDict = {}

    # Convert the data to a pandas DataFrame
    df = pd.DataFrame(data[1:], columns=data[0])

    for row in df.iterrows():
        # row[0] is the index, row[1] is the dataframe 
        data = row[1]
        #tourney            Hyperlink                SGGName                         TName,                  TSeries,           Color,          TotalEntrants,                    Results Dict
        tourneyObj = Tourney(data['Tourney URL'],    data['Tourney SmashGG ID'],     data['Tourney Name'],   data['Tourney Series'],   data['Color'],  int(data['Attendance']),  json.loads(data['Results']))
        name = str(data['Tourney SmashGG ID'])  
        if int(data['Attendance'])>=8:
            tourneyObjDict[name] = tourneyObj

    return tourneyObjDict

def WriteUpdateTourneyDataSheet(docName, sheetName):
    """
    Will update the google sheet specified with initial smash.gg data read in. Sheet passed in must be formatted with proper headers
    to match the dataframe and contain URLs in the first column of the format:
    start.gg/tournament/<smashGGTourneyName>/event/<eventString>.
    """

    # Open the worksheet and get all the data as a list of lists
    sheet = client.open(docName).worksheet(sheetName)
    data = sheet.get_all_values()

    # Convert the data to a pandas DataFrame
    df = pd.DataFrame(data[1:], columns=data[0])


    for index, row in df.iterrows():
      
        # Iterate through the dataframe and skip the rows that are fully populated
        """
        NOTE: this will fail if i accidentally add an empty column dumb google sheets
        """

        isPopulated = True
        for column in row:
          if column == '':
            isPopulated = False        
        if isPopulated:
           continue

        tournURL = row['Tourney URL']
        print("Extracting: ", tournURL)
        smashGGTourneyName = tournURL.split('/')[-3] # used by smashgg to look up tourney
        eventString = tournURL.split('/')[-1] # figure out what smashgg event was used, set by TO
        # its usually ultimate-singles

        try:
            tournament = smash.tournament_show(smashGGTourneyName) # look up the tournament and get the dictionary object of data
        except:
           print("ERROR")
           break
        
        # tournName = tournament['name']
        tournAttendance = tournament['entrants']
        
        tournSeries, tournName, color = getTourneyInfo(tournURL, smashGGTourneyName)

        unixTime = tournament['startTimestamp']
        date = datetime.datetime.fromtimestamp(unixTime)
        tournDate = date.strftime("%Y-%m-%d") # print date in mm-dd-yyyy

        # add a value to the "new_column" column of the row with index 0
        df.loc[index, 'Tourney SmashGG ID'] = smashGGTourneyName
        df.loc[index, 'Tourney Name'] = tournName
        df.loc[index, 'Date'] = tournDate
        df.loc[index, 'Tourney Series'] = tournSeries
        df.loc[index, 'Color'] = color

        tournResultsDict = {}

        resultsList = []
        i = 0
        pageNum = 1
        while i <= tournAttendance:
            try:
              resultsList += smash.tournament_show_entrants(smashGGTourneyName, eventString, pageNum)
            except:
               print("ERROR WITH ENTRATNS")
               break
            i+= 25 # this is max number of entratns that appear on a startgg page
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
    
        df.loc[index, 'Attendance'] = len(resultsList)#NOTE: this prevents side bracket entrants

        result_str = json.dumps(tournResultsDict)
        df.loc[index, 'Results'] = result_str

    sheet.update([df.columns.values.tolist()] + df.values.tolist())



def getPlacementPercentileAverages(tourneyDF):
    results = tourneyDF['Results'].apply(lambda x: json.loads(x))
    player_dict = {}
    for tournament in results:
        for player, placement in tournament.items():
            percentile = calculatePercentile(placement, len(tournament))
            if player not in player_dict:
                player_dict[player] = {"percentile_sum": percentile, "tournaments_attended": 1}
            else:
                player_dict[player]["percentile_sum"] += percentile
                player_dict[player]["tournaments_attended"] += 1
    player_data = []
    for player, data in player_dict.items():
        avg_percentile = data["percentile_sum"] / data["tournaments_attended"]
        player_data.append({"player": player, "avg_placement_percentile": avg_percentile})
    
    playerDF = pd.DataFrame(player_data)
    
    return playerDF
    

#TODO defaulting cutoff to 50 cuz right now its plaeyr percentile placement avg based and i didnt want to deal with
# anyone who averaged below 50% of bracket
def writePlayerLevelClustersPPA(docName, tourneySheetName, clusterSheetName, cutoffThreshold=50, num_clusters=4):
    """
    This uses a kmeans algorithm to divide players into groups based on their PPA to be used as levels.
    It will write those results ot google sheet, overwriting anything currently there. 
    """
    from sklearn.cluster import KMeans
    from sklearn.preprocessing import StandardScaler

    sheet = client.open(docName).worksheet(clusterSheetName)
    sheet.clear()

    tourneySheet = client.open(docName).worksheet(tourneySheetName)

    data = tourneySheet.get_all_values()

    tourneyDF = pd.DataFrame(data[1:], columns=data[0])

    # Get the player ppa data to use for the clusters
    player_ppa = getPlacementPercentileAverages(tourneyDF)

    # Filter out players with placement percentiles below cutoffThreshold
    player_ppa = player_ppa[player_ppa['avg_placement_percentile'] >= cutoffThreshold]  

    # Create a matrix of placement percentile averages for each player
    ppa_matrix = player_ppa['avg_placement_percentile'].values.reshape(-1, 1)

    # Scale the matrix
    scaler = StandardScaler()
    ppa_matrix_scaled = scaler.fit_transform(ppa_matrix)

    # Cluster the players using K-Means
    kmeans = KMeans(n_clusters=num_clusters, n_init=5, random_state=0)
    kmeans.fit(ppa_matrix_scaled)

    # Get the cluster labels for each player
    player_ppa['Cluster'] = kmeans.labels_

    tierDict = {}
    # Analyze the results
    for i in range(num_clusters):
        # Get the players in the current cluster
        cluster_players = player_ppa[player_ppa['Cluster'] == i]
        
        # Determine the skill level for the current cluster
        cluster_ppa_mean = cluster_players['avg_placement_percentile'].mean()

        
        # tierDict[skill_level] = cluster_players['player']
        # print(f'Skill Level: {skill_level}')
        # print("Cluster Mean", cluster_ppa_mean)
        # print(cluster_players['player'])
        tierDict[cluster_ppa_mean] = cluster_players['player']
        
    players = dict(sorted(tierDict.items()))

    # Initialize column_data with empty lists for each column
    max_level = 5
    column_data = {'LEVEL {}'.format(i): [] for i in range(1, max_level + 1)}

    # Write each list of player names to a separate column
    for i, (team, names) in enumerate(players.items()):
        # Set the column header to the team name
        sheet.update_cell(1, i+1, team)
        # Write the player names to the column
        cell_list = sheet.range(2, i+1, len(names)+1, i+1)
        for cell, name in zip(cell_list, names):
            cell.value = name
        sheet.update_cells(cell_list)


def writeDataFrame(docName, sheetName, df, dropColumsList=[]):
  
  sheet = client.open(docName).worksheet(sheetName)
  sheet.clear()
  

  df = df.drop(columns=dropColumsList)

  for i, col in enumerate(df.columns):
      col_list = df[col].tolist()
      # convert non-serializable values to string before writing to sheet
      col_list = [json.dumps(x) if not isinstance(x, (int, float)) else x for x in col_list]
      # update cells
      cell_list = sheet.range(1, i+1, len(col_list), i+1)
      for cell, value in zip(cell_list, col_list):
          if isinstance(value, (int, float)):
            cell.value = round(value,2)
          elif isinstance(value, str):
            cell.value = value.strip('"')
          else:
             cell.value = value
      try:
        sheet.update_cells(cell_list)
      except TypeError:
            print(f"Column {col} contains non-serializable data and was skipped.")


  today = datetime.date.today().strftime('%Y-%m-%d')
  message = 'Last updated: ' + today

  header = list(df.columns) + ["", message]
  # insert the header as the first row in the worksheet
  sheet.insert_row(header, index=1)
