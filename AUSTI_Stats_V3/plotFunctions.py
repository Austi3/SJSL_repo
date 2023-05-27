"""
plot functions
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import scipy.stats as stats
import os

# these are the options for what can be plotted in the player graphs
playerGraphOptions = ["Total League Points", "Max Points Possible", "Earned Point Ratio", "Number of Tourneys Entered", 
        "Placement Percentile Average", "Weighted Placement Percentile Average", "Plot All"]

def get_user_choice():
    """
    Prompts the user to select an option from a list of playerGraphOptions and returns their choice as a number in a list.
    """

    while True:
        print("Please select an option:")
        for i, option in enumerate(playerGraphOptions):
            print(f"{i+1}: {option}")
        try:
            choiceIdx = int(input())
            if 1 <= choiceIdx < len(playerGraphOptions):
                return [playerGraphOptions[choiceIdx-1]], choiceIdx
            elif choiceIdx == len(playerGraphOptions):
                return playerGraphOptions[:-1], choiceIdx
            else:
                print(f"Invalid choice. Please enter a number between 1 and {len(playerGraphOptions)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def getAbbreviation(itemKey):
    """
    Returns the abbreviation of the metric I used
    """

    pos = playerGraphOptions.index(itemKey)
    abbreviations = ["ETP", "Max Points Possible", "EPR", "Tourneys Entered", "PPA", "WPPA"]
    return abbreviations [pos]


def plotPlayerData(playerDataFrame, itemKey, prSeason,  minReqTourneys=5, numPlayersPlotted=30, showPlot=False, customPlotName = ""):
    # filter out players who havent met attendance requirement
    playerDataFrame = playerDataFrame[playerDataFrame['Number of Tourneys Entered'] >= minReqTourneys]

    playerDataFrame = playerDataFrame.sort_values(by=[itemKey], ascending=False)[0:numPlayersPlotted]
    playerDataFrame = playerDataFrame.round(2)


    ax = playerDataFrame.plot.bar('Player',itemKey, figsize=(15, 7) , color = playerDataFrame['color'] )
    for container in ax.containers:
        ax.bar_label(container)

    # # add a text box with a note
    # plt.text(0.98, 0.98, f"*Min Tourneys Required: {minReqTourneys}", ha='right', va='top', transform=plt.gca().transAxes,
    #      bbox={'boxstyle': 'round,pad=0,rounding_size=0.2', 'facecolor': 'white', 'edgecolor': 'none'})

    
    ax.set_xticklabels([f'({i+1})  {name}' for i, name in enumerate(playerDataFrame['Player'])])
    plt.xticks(rotation=75)
    plt.ylabel(itemKey)

    abbr = getAbbreviation(itemKey)
    if customPlotName:
        plotTitle = customPlotName
    else:
        plotTitle = f"Top {numPlayersPlotted} Players Ranked by {abbr} ({prSeason})"
    plt.title(plotTitle)
    plt.tight_layout()
    ax.get_legend().remove()

    directory_name = '../plotsOutput/' + prSeason + '/'
    if not os.path.exists(directory_name):
        os.mkdir(directory_name)

    plt.savefig(directory_name + plotTitle.strip() + ".png" )

    if showPlot:
        plt.show()


        

def plotTourneyDataFrame(tourneyDF, plotItem, yAxisLabel, plotName, seasonStr):

  tourneyDF = tourneyDF.sort_values(by=[plotItem], ascending=False)

  tourneyDF= tourneyDF.round(2)
#   plt.bar(tourneyDF['TName'], tourneyDF[plotItem], color = tourneyDF['Color'])

  ax = tourneyDF.plot.bar('TName',plotItem, figsize=(13, 7) , color = tourneyDF['Color'] )
  for container in ax.containers:
    ax.bar_label(container)
  
  labels = [f"({tier}) {tournament}" for tier, tournament in zip(tourneyDF['Tier'], tourneyDF['TName'])]
  ax.set_xticklabels(labels)


  plt.xticks(rotation=75)

  botbPatch = mpatches.Patch(color='red', label='Battle Over The Bridge')
  catPatch = mpatches.Patch(color='blue', label='Catastrophe')
  hopsPatch = mpatches.Patch(color='orange', label='Hops N Stocks')
  rownPatch = mpatches.Patch(color='gold', label='RU Smashin')
  ptbPatch = mpatches.Patch(color='hotpink', label='Pop The Bubble')
  othrPatch = mpatches.Patch(color='lime', label='Other')

  plt.legend(handles=[botbPatch, catPatch, hopsPatch, ptbPatch, rownPatch, othrPatch])

  plt.ylabel(yAxisLabel)
  plt.title(plotName)

#   plt.grid( axis ='y')
  plt.tight_layout()

  directory_name = '../plotsOutput/' + seasonStr + '/'
  if not os.path.exists(directory_name):
      os.mkdir(directory_name)

  plt.savefig(directory_name +plotName.strip() + ".png" )

  plt.show()

