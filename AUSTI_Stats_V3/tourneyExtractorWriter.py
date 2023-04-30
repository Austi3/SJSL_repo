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


class playerLvls():
    def __init__(self, lvl2s, lvl3s, lvl4s, lvl5s):
        # Filter out empty strings
        self.lvl2s = list(filter(None, lvl2s))
        self.lvl3s = list(filter(None, lvl3s))
        self.lvl4s = list(filter(None, lvl4s))
        self.lvl5s = list(filter(None, lvl5s))

def getPlayerLevels(docName, sheetName):
    # Open the specified sheet
    playersheet = client.open(docName).worksheet(sheetName)

    # get all values from the sheet
    values = playersheet.get_all_values()

    # convert all values to lowercase
    for i in range(len(values)):
        for j in range(len(values[i])):
            values[i][j] = values[i][j].lower()

    lvl2s = [row[0] for row in values[1:]]
    lvl3s = [row[1] for row in values[1:]]
    lvl4s = [row[2] for row in values[1:]]
    lvl5s = [row[3] for row in values[1:]]

    """ TODO NEXT """
    # lvlList = [lvl2s, lvl3s, lvl4s, lvl5s]
    # for lvls in lvlList:
    #    lvls = [name.lower() for name in lvls]

    playerLvlsObj = playerLvls(lvl2s, lvl3s, lvl4s, lvl5s)

    return playerLvlsObj




def getTourneyInfo(tourneyLink, smashGGName):
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

def updateTourneyDataSheet(docName, sheetName):
    """
    Will update the google sheet specified. Sheet passed in must be formatted with proper headers
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
        
        # tournName = tournament['name']
        tournAttendance = tournament['entrants']
        
        tournSeries, tournName, color = getTourneyInfo(tournURL, smashGGTourneyName)

        unixTime = tournament['startTimestamp']
        date = datetime.datetime.fromtimestamp(unixTime)
        tournDate = date.strftime("%Y-%m-%d") # print date in mm-dd-yyyy

        # add a value to the "new_column" column of the row with index 0
        df.loc[index, 'Tourney SmashGG ID'] = smashGGTourneyName
        df.loc[index, 'Tourney Name'] = tournName
        df.loc[index, 'Attendance'] = tournAttendance
        df.loc[index, 'Date'] = tournDate
        df.loc[index, 'Tourney Series'] = tournSeries
        df.loc[index, 'Color'] = color

        tournResultsDict = {}

        resultsList = []
        i = 0
        pageNum = 1
        while i <= tournAttendance:
            resultsList += smash.tournament_show_entrants(smashGGTourneyName, eventString, pageNum)
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
    
        result_str = json.dumps(tournResultsDict)
        df.loc[index, 'Results'] = result_str

    sheet.update([df.columns.values.tolist()] + df.values.tolist())

############################################################

# def plotTopPlayers(playerDF, n=30, rotation=75):
#     # Get the top n players with the highest placement percentile averages
#     top_n = playerDF.groupby('player')['avg_placement_percentile'].mean().nlargest(n).reset_index()
    
#     # Create a bar plot of the top n players with their percentile averages
#     fig, ax = plt.subplots(figsize=(12, 6))
#     ax.bar(top_n['player'], top_n['avg_placement_percentile'])
#     ax.set_title(f'Top {n} Players by Placement Percentile Average')
#     ax.set_xlabel('Player Name')
#     ax.set_ylabel('Percentile Average')
#     ax.set_xticklabels(top_n['player'], rotation=rotation, fontsize=10)

#     # Add labels to the bar graph
#     labels = [f'{x:.2f}%' for x in top_n['avg_placement_percentile']]
#     ax.bar_label(ax.containers[0], labels=labels, label_type='edge')

#     plt.show()

def getPlacementPercentileAverages(df):
    results = df['Results'].apply(lambda x: json.loads(x))
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
def getPlayerSkillLevels(player_ppa, docName, sheetName, cutoffThreshold=50):
    from sklearn.cluster import KMeans
    from sklearn.preprocessing import StandardScaler

    sheet = client.open(docName).worksheet(sheetName)

    # Define the number of clusters
    num_clusters = 4


    # Filter out players with placement percentiles below cutoffThreshold
    player_ppa = player_ppa[player_ppa['avg_placement_percentile'] > cutoffThreshold]  

    # Create a matrix of placement percentile averages for each player
    ppa_matrix = player_ppa['avg_placement_percentile'].values.reshape(-1, 1)

    # Scale the matrix
    scaler = StandardScaler()
    ppa_matrix_scaled = scaler.fit_transform(ppa_matrix)

    # Cluster the players using K-Means
    kmeans = KMeans(n_clusters=num_clusters, random_state=0)
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
    print(players)
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
#     # Print the resulting DataFrame
    # print(tierDict)
    # # Create a DataFrame from the dictionary
    # df = pd.DataFrame.from_dict(tierDict, orient='index')

    # # Transpose the DataFrame to switch the rows and columns
    # df = df.transpose()

    # # Print the resulting DataFrame
    # print(df)

