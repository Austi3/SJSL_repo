import numpy as np
import regex as re
import pysmashgg
import pandas as pd

from Tourney import *

KEY = '742fe712e6ebd8fc43700aa1b833d198'
smash = pysmashgg.SmashGG(KEY, True)

def formatOtherTourneyNames(name):
    if "pbj-presents-road-to-apex" in name:
        newName = "PBJ Road to Apex"
    elif "palooza" in name:
        newName = "PBJ Holiday Palooza"  
    # elif "geek fest" in name:
    #     newName = "SJ Geek Fest"
      
    newName = name.replace("-", " ")
    newName = newName.title()
    
    return newName 

def getTourneyColor(tseries):
    if tseries == "Hops N Stocks":
        color = "orange"
    elif tseries == "Hyperspace":
        color = "gray"
    elif tseries == "Pop the Bubble":
        color = "pink"
    elif tseries == "Battle over the Bridge":
        color = 'red'
    elif tseries == "RU Smashin":
        color = "gold"
    elif tseries == "Catastrophe":
        color = 'blue'
    else:
        color = "green"

    return color

def makeTourneyObj(tseriesName, hyperlink):
    # this is where i want to make an object for a tourney and call smashgg api to get all the data for the tourney at once
    # and then ill add that to a pandas dataframe with the class function that converts it to a dictionary
    if not hyperlink.startswith('http'):
        print("ERROR! Invalid hyperlink")
    
    else:
        # need to get the tourney's exact name in smashgg. for example, we want to get tourneyName in:  'http/tourneyName/details
        smashGGName = hyperlink.split('/')[-2]
        splitName = smashGGName.split("-")
        endNum = ""
        for elt in splitName:
            if re.search("[0-9]", elt):
                endNum += "-" + elt

        officialTourneyName = tseriesName + endNum
        color = getTourneyColor(tseriesName)
        
        events = smash.tournament_show_events(smashGGName)

        try:
            eventString = 'ultimate-singles'
            """
            NOTE!!!! I believe this can only show top 48. I havent accounted for pagination addition when more than 48 attendees is involved, it crashes
            """
            results = smash.tournament_show_lightweight_results(smashGGName, eventString, 1)
        except:
            eventString = 'singles'
            results = smash.tournament_show_lightweight_results(smashGGName, eventString, 1)

        totalEntrants = len(results)

        """
        TODO this is the hackiest shit ive ever written because i was lazy and didnt wanna get pickle working in colab
        fix this cuz if anyone is named sno$$i for example, theyd mess this up later lmao
        """
        resultString = ""
        for entrant in results:
           name = entrant['name']
           place = entrant['placement']
           newString = name + '~~~' + str(place) + "$$"
           resultString += (newString)

        
        tournObj = Tourney(hyperlink, smashGGName, officialTourneyName, tseriesName, color, totalEntrants, resultString)

        return tournObj

def parseAllTourneys():


    masterExcelFile = "SJ Fall 2022 (Oct3- Dec23) Tournaments.xlsx"
    tourneyDF = pd.read_excel(masterExcelFile, sheet_name = 0)

    #lists of all urls of tourneys in a particular series
    hopsTrn = tourneyDF['Hops N Stocks'].unique()
    hyperTrn = tourneyDF['Hyperspace'].unique()
    pbjTrn = tourneyDF['Pop the Bubble'].unique()
    botbTrn = tourneyDF['Battle over the Bridge'].unique()
    rowanTrn = tourneyDF['RU Smashin'].unique()
    catTrn = tourneyDF['Catastrophe'].unique()
    othrTrn = tourneyDF['Other Tourneys'].unique()




    # allTourneyDict = {'Hops N Stocks': hopsTrn, 'Hyperspace': hyperTrn, 'Pop the Bubble': pbjTrn, 'Battle over the Bridge': botbTrn,
    #                   'RU Smashin': rowanTrn, 'Catastrophe': catTrn, 'Other Tourneys': othrTrn}

    # tournObjList = []

    # for 

    
    # for tourneyLink in hopsTrn:
    #     if isinstance(tourneyLink, str) :
    #         newTourneyObj = makeTourneyObj('Hops N Stocks', tourneyLink)
    #         tournObjList.append(newTourneyObj)

    # print(tournObjList)

def main():
    print("Provide the link to a tourney")
    tourneyLink=input()
    if "hops" in tourneyLink:
        tseriesName = "Hops N Stocks"
    
    if isinstance(tourneyLink, str) :
        newTourneyObj = makeTourneyObj('Hops N Stocks', tourneyLink)

        tourneyDF = pd.DataFrame.from_records([newTourneyObj.to_dict()])

        resultsExcelFile = "TourneyResultsFile.xlsx"



main()