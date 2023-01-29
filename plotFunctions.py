"""
plot functions
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import scipy.stats as stats

def plotPlayerDataFrame(playerDataFrame,  playerObjDict, itemKey, yAxisLabel, plotTitle, min5Events= True, roundPlace = 2):

    """ TODO fix or move this but this is currently how i filter out players with less than 5 tourneys"""
    if min5Events:
        tempDict = {}
        for player in playerObjDict:
            if len(playerObjDict[player].tourneysEntered) >= 5:
                tempDict[player] = playerObjDict[player]

        playerObjDict = tempDict 

        #i redo the player dataframe here to filter by people with >= 5 tourneys. 
        playerDataFrame = pd.DataFrame.from_records([playerObjDict[playerTag].to_dict() for playerTag in playerObjDict])

    """
    TODO plot normal distribution
    df_mean = np.mean(playerDataFrame[plotItem])
    df_std = np.std(playerDataFrame[plotItem])
    
    # Calculating probability density function (PDF)
    pdf = stats.norm.pdf(playerDataFrame[plotItem].sort_values(), df_mean, df_std)
   

    plt.bar(playerDataFrame[plotItem].sort_values(), pdf)[0:30]
    plt.show()
     """

    playerDataFrame = playerDataFrame.sort_values(by=[itemKey], ascending=False)[0:30] # plot top 30
    playerDataFrame = playerDataFrame.round(roundPlace)

    # fig, ax = plt.figure(figsize=(10, 7))

    # plt.bar(playerDataFrame['tag'], playerDataFrame[plotItem])


    ax = playerDataFrame.plot.bar('tag',itemKey, figsize=(15, 7) , color = playerDataFrame['color'] )
    for container in ax.containers:
        ax.bar_label(container)

    plt.xticks(rotation=75)
    plt.xlabel("Player")
    plt.ylabel(yAxisLabel)
    plt.title(plotTitle)
    plt.tight_layout()
    ax.get_legend().remove()

    plt.savefig('./plotsOutput/newDir/' +plotTitle.strip() + ".png" )

    plt.show()


def plotPlayerPerformance(playerTag, playerObjDict, tourneyObjDict):
    player = playerObjDict[playerTag]

    placements = []
    tnames = []
    for tourney in player.tourneysEntered:
        placement = tourneyObjDict[tourney].placementDict[playerTag]
        tname =  tourneyObjDict[tourney].TName
        placements.append(placement)
        tnames.append(tname)
    
    plt.plot(tnames, placements)
    plt.show()

        

def plotDataFrame(tourneyDF, plotItem, plotName):

  tourneyDF = tourneyDF.sort_values(by=[plotItem], ascending=False)

#   plt.bar(tourneyDF['TName'], tourneyDF[plotItem], color = tourneyDF['Color'])


  ax = tourneyDF.plot.bar('TName',plotItem, figsize=(13, 7) , color = tourneyDF['Color'] )
  for container in ax.containers:
    ax.bar_label(container)

  plt.xticks(rotation=80)

  botbPatch = mpatches.Patch(color='red', label='Battle Over The Bridge')
  catPatch = mpatches.Patch(color='blue', label='Catastrophe')
#   hyprPatch = mpatches.Patch(color='gray', label='Hyperspace')
  hopsPatch = mpatches.Patch(color='orange', label='Hops N Stocks')
  rownPatch = mpatches.Patch(color='gold', label='RU Smashin')
  ptbPatch = mpatches.Patch(color='hotpink', label='Pop The Bubble')
  othrPatch = mpatches.Patch(color='lime', label='Other')

  plt.legend(handles=[botbPatch, catPatch, hopsPatch, ptbPatch, rownPatch, othrPatch])

  plt.ylabel(plotItem)
  plt.title(plotName)

#   plt.grid( axis ='y')
  plt.tight_layout()

  plt.savefig('./plotsOutput/newTournDir' +plotItem + ".png" )

  plt.show()

