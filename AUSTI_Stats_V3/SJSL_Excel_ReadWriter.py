from sheetsReadWriteFunctions import *


from PlayerTags import *
# Define your Google Sheets credentials
scope = ['https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive']

CREDENTIALS_FILE = r'C:\Users\acmaa\DocumentsACM\Local Projects\ImportantCoding\core-synthesis-384200-4101747176bd.json'

creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
client = gspread.authorize(creds)
# Open the Google Sheet
SJSLDataDoc = 'SJSL Official Data'

def getRegisteredPlayers(playerObjDict):

    registeredSheet = "Registered Players"
    regList = []
    regPlayerData =  client.open(SJSLDataDoc).worksheet(registeredSheet).get_all_values()
    for row in regPlayerData:
        tag = handleSpecialPlayers(row[0]).lower()
        regList.append(tag)

        for tagKey in playerObjDict.keys():
            if tag == tagKey.lower():
                playerObjDict[tagKey].isRegistered = "YES"


def addBountyPoints(playerObjDict):

    bountySheetName = '(For TOs) Bounty Tracker'
    bountySheet = client.open(SJSLDataDoc).worksheet(bountySheetName)

    bountyData = bountySheet.get_all_values()

    # Iterate over the data and update player points
    for row in bountyData[1:]:
        if row[2] != "" and row[3] != "":
            bountyPoints = int(row[2]) # bounty points
            bountyClaimerPlayer = handleSpecialPlayers(row[3]) #player who claimed bounty
            playerObjDict[bountyClaimerPlayer].earnedBountyPoints += bountyPoints

def addDuelPoints(playerObjDict):

    duelSheetName = '(For TOs) Duel Tracker'
    duelSheet = client.open(SJSLDataDoc).worksheet(duelSheetName)

    duelData = duelSheet.get_all_values()

    # Iterate over the data and update player points
    for row in duelData[1:]:
        if row[1] != "":
            pointsWagered = int(row[1]) # Points Wagered
            duelWinner = handleSpecialPlayers(row[2]) #Duel Winner
            duelLoser = handleSpecialPlayers(row[3])#"Duel Loser"

            playerObjDict[duelWinner].earnedDuelPoints += pointsWagered
            playerObjDict[duelLoser].earnedDuelPoints -= pointsWagered



    # self.earnedTourneyPts = 0 # poitns earned just from tourneys
    # self.earnedDuelPoints = 0
    # self.earnedBountyPoints = 0
    # self.totalLeaguePoints = 0 # combined ETP + DP + BP


def getWriteLeagueLeaderboard(playerObjDict):
    addDuelPoints(playerObjDict)
    addBountyPoints(playerObjDict)
    getRegisteredPlayers(playerObjDict)
    registerBonus = 20

    for playerName in playerObjDict:
        playerObj = playerObjDict[playerName]
        playerObj.totalLeaguePoints = round(playerObj.earnedTourneyPts + playerObj.earnedDuelPoints + playerObj.earnedBountyPoints)
        if playerObj.isRegistered == "YES":
            playerObj.totalLeaguePoints += registerBonus
        
    leaguePlayerDF = pd.DataFrame.from_records([playerObjDict[playerTag].to_dict() for playerTag in playerObjDict])
    leaguePlayerDF = leaguePlayerDF.sort_values(by=['Total League Points'], ascending=False)


    playerLeaderboardSheet = "SJSL Leaderboard"
    leageDataSheet = "League Player Data"
    dropColumnsList = ["Max Points Possible", "Earned Point Ratio", "Weighted Placement Percentile Average", "color", "Tourneys Attended Object List", "tourneyResultsDict",
                       "Weighted Points"]
    writeDataFrame(SJSLDataDoc, leageDataSheet, leaguePlayerDF, dropColumnsList)

    dropColumnsList += ["Earned Tourney Points", "Earned Weighted Points", "Earned Placement Bonus Points", "Earned Duel Points", "Earned Bounty Points", 
                        "Weighted Placement Percentile Average", "Placement Percentile Average", "Number of Tourneys Entered", "Avg Points Per Tourney"]

    writeDataFrame(SJSLDataDoc, playerLeaderboardSheet, leaguePlayerDF, dropColumnsList)