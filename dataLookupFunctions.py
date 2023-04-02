"""
helper after data functions

"""

from SJMainTTS import *

# def plotPlayerPerformance(playerTag, playerObjDict, tourneyObjDict):
#     player = playerObjDict[playerTag]

#     placements = []
#     tnames = []
#     for tourney in player.tourneysEntered:
#         placement = tourneyObjDict[tourney].placementDict[playerTag]
#         tname =  tourneyObjDict[tourney].TName
#         placements.append(placement)
#         tnames.append(tname)
    
#     plt.plot(tnames, placements)
#     plt.show()

def printPlayerResults(playerTag):
    playerTag = playerTag.lower()

    tourneyObjDict, playerObjDict = Main(False)

    playerObjDict = dict((k.lower(), v) for k, v in playerObjDict.items())

    try:
        player = playerObjDict[playerTag]
    except:
        print("Player not found, ")
    player.printPlayerInfo()

    percentileList = []
    pointsEarnedList = []
    tourneyPointsList = []
    tourneyNames = []
    for tournKey in player.tourneyResultsDict:

        player.tourneyResultsDict[tournKey].printInfo()
        percentileList.append(player.tourneyResultsDict[tournKey].tourneyPercentile)
        tourneyNames.append(player.tourneyResultsDict[tournKey].tourneyName)
    
    fig = plt.figure(figsize=(10, 7))
    """
    TODO i should organize by date!!!

    TODO!!! i should turn this entire page into awrapper class where u can just make calls and ask for info like on a player
    or a tourney or for playrs what info u want specifically! suepr cool- use enums lol

    i should try plottign side by side bar chart things

    like pairs of placement and percentile
    points earned and total pts possible
    points earned per place?''

    evem stacled omdex

    tjos would be really really useful in eval how good my alg is and if i missed anything

    sp,ething curiosu i just realized= if u do meh at 3 botb and still get points but u kick ass at a big tourney
    then algorithm favors u. and if u do real well at small tournyes but lose at big ones it doesnt favor u

    which i guess is more important and i stand by that logic

    spr tho is soemthing to keep in mind?? although seeding is still fairly arbitraru so idl???

    eventuayll i also use this wrapper i should to do head to heads
    """
    plt.bar(tourneyNames,percentileList)
    plt.xticks(rotation=80)
    plt.tight_layout()

    plt.show()


  

printPlayerResults("eo")