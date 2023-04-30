import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import pysmashgg

# Define your Google Sheets credentials
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

CREDENTIALS_FILE = r'C:\Users\acmaa\DocumentsACM\Local Projects\ImportantCoding\core-synthesis-384200-4101747176bd.json'

    # TOURNEY_SHEET_NAME = "2023Q1 Tourneys"

creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
client = gspread.authorize(creds)

# Read the player skill level spreadsheet as a pandas DataFrame

sheet_name = "2023 SJ Smash Sheet"
worksheet_name = "2023Q1 Players"
player_skill_levels_worksheet = client.open(sheet_name).worksheet(worksheet_name)
player_skill_levels_data = player_skill_levels_worksheet.get_all_values()
player_skill_levels_df = pd.DataFrame(player_skill_levels_data[1:], columns=player_skill_levels_data[0])


# Define the Google Sheet name and worksheet name where the tournament hyperlinks are stored
tourneySheet = '2023 SJ Smash Sheet'
worksheet_name = 'testTourneys'

# # Open the worksheet and get all the data as a list of lists
# sheet = client.open(sheet_name).worksheet(worksheet_name)
# data = sheet.get_all_values()

# # Convert the data to a pandas DataFrame
# df = pd.DataFrame(data[1:], columns=data[0])


# Open the worksheet and get all the data as a list of lists
sheet = client.open(sheet_name).worksheet(worksheet_name)
data = sheet.get_all_values()

# Convert the data to a pandas DataFrame
df = pd.DataFrame(data[1:], columns=data[0])




# Calculate tournament weights based on player skill levels
weights = {'LEVEL1': 0.5,
           'LEVEL2': 1.0,
           'LEVEL3': 1.5,
           'LEVEL4': 2.0,
           'LEVEL5': 2.5}
player_skill_levels_df['weight'] = player_skill_levels_df['Skill Level'].map(weights)
player_skill_levels_df.set_index('Player Name', inplace=True)

# Loop through tournaments and calculate each player's average placement percentile
for tournament_name, tourneyObj in tourneyObjDict.items():
    num_entrants = len(tourneyObj.entrants)
    for entrant in tourneyObj.entrants:
        player_name = entrant.name
        player_placings = [match.entrant1Score if match.entrant1Id == entrant.id else match.entrant2Score
                           for match in entrant.matches]
        if len(player_placings) == 0:
            continue
        player_placings_sorted = sorted(player_placings)
        player_placings_percentile = [(num_entrants - player_placings_sorted.index(placing)) / num_entrants
                                      for placing in player_placings]
        player_avg_placing_percentile = sum(player_placings_percentile) / len(player_placings_percentile)
        # Update player's placement percentile average in the player_skill_levels DataFrame
        player_skill_levels_df.at[player_name, tournament_name] = player_avg_placing_percentile

# Multiply placement percentile averages by tournament weights and calculate final ranking
player_skill_levels_df = player_skill_levels_df.fillna(0)
weighted_placement_percentiles = player_skill_levels_df.drop(columns=['Skill Level', 'weight']).multiply(
    player_skill_levels_df['weight'], axis='index').sum(axis=1)
ranked_players = weighted_placement_percentiles.sort_values(ascending=True)


print(ranked_players)