
from playerClass import *

def handleSpecialPlayers(tag):
  """
  TODO i might want a way to make this more robust or avoid this, but itll work for now
  """
  if tag.lower() in ['snogi', 'critz but retired', '<3 brisket']:
    tag = 'Snogi'
  elif tag.lower() in ['chanman', 'chan', 'poop87']:
    tag = 'Chanman'
  elif 'Poop' in tag:
    print("my name is", tag.lower())
  elif tag.lower() in ['sauce', 'hotsaucefuego','obmcbob']:
    tag = 'Sauce'
  elif tag in ['xavier', 'Xavier']:
    tag = 'Xavier'
  return tag

def calculatePlayerTourneyPts(placement, tourneyObj):
  """
  TODO!!!!!! so this calculation is inherently flawed and needs to be updated. what im noticing now is:
  players own worth is counted
  the percentage of points  might be too strong- like if 2nd gets 95% is that right? maybe a bonus is needed 
  for top 8??? 
  maybe thresholds are in order like 1st gets 100%. 2nd gets 95%. 3rd gets 90 etc. defined up to 33rd
  """
  
  if not placement:
    print("error: NO PLACEMENT FOUND for a player",tourneyObj.officialName, tourneyObj.placementDict)
    playerPts = 0
  else:
    """
    # NOTE this was my original percentage calculation- based off of total entrants and placement
    # perc = ((tourneyObj.totalEntrants - int(placement) + 1)/tourneyObj.totalEntrants)
    """
    placement = int(placement)
    # NOTE this is my fixed percentage model- may want to adjust
    perc = 0
    if placement == 1:
      perc = 1
    elif placement == 2:
      perc = .90
    elif placement == 3:
      perc = .80
    elif placement == 4:
      perc = .70
    
    # award pts to top 6 if more than 12 entrants
    if tourneyObj.totalEntrants > 12:
      if placement == 5:
        perc = .60
    
    # award pts to top 8 if more than 16 entrants
    if tourneyObj.totalEntrants > 16:
      if placement == 7:
        perc = .50

    # award pts to top 12 if more than 24 entrants
    if tourneyObj.totalEntrants > 24:
      if placement == 9:
        perc = .40

    
    playerPts = perc * tourneyObj.totalScore
  
  return playerPts


def getTourneyScores(tourneyObj, playerLvlsObj):
  """
  TODO i should make it so that any tourney below 8 entrants has a score of 0
  also i dont have a way to handle DQs yet

  This also should be modified but righ tnow the methodology is:
  - Each lvl player is worth a corresponding amount of points
  - The attendence score is half total entrants rounded down
  """
  
  tourneyObj.attendanceScore = tourneyObj.totalEntrants // 2

  for playerTag in tourneyObj.placementDict:
    lowerName = playerTag.lower()
    
    """
    TODO do i like 1.5 increments better??? 
    """
    if lowerName in playerLvlsObj.lvl5s:
      tourneyObj.stackedScore += 6
      tourneyObj.notableEntrants.append(lowerName)
    elif lowerName in playerLvlsObj.lvl4s:
      tourneyObj.stackedScore += 4.5
      tourneyObj.notableEntrants.append(lowerName)
    elif lowerName in playerLvlsObj.lvl3s:
      tourneyObj.stackedScore += 3
      tourneyObj.notableEntrants.append(lowerName)
    elif lowerName in playerLvlsObj.lvl2s:
      tourneyObj.stackedScore += 1.5
      tourneyObj.notableEntrants.append(lowerName)
    else:
      tourneyObj.otherEntrants.append(lowerName)

    tourneyObj.totalScore = tourneyObj.attendanceScore  + tourneyObj.stackedScore
    tourneyObj.stackedRatio = len(tourneyObj.notableEntrants)/ tourneyObj.totalEntrants


def makeTourneyPlacementDict(tourneyObj):

  # first build dictionary of all players by parsing the results string I jankily made
  # the dictionary has the key as the player's name and the value as the place they got at 
  # the particular tourney
  uglyPlayerString = tourneyObj.resultsString.split("$$")
  for playerStr in uglyPlayerString:
    if playerStr:
      try:
        tag = playerStr.split("~~~")[0]
        tag = handleSpecialPlayers(tag)
        place =  playerStr.split("~~~")[1]
      except:
        print("UH OH something went wrong getting player's name for ", tourneyObj.officialName)
        break
      tourneyObj.placementDict[tag] = place 


def updateAllPlayerScores(tourneyObj, playerObjDict):

    for playerTag in tourneyObj.placementDict:

      placement = tourneyObj.placementDict[playerTag]
      playerPts = calculatePlayerTourneyPts(placement, tourneyObj)

      if playerTag not in playerObjDict:
        playerObjDict[playerTag] = Player(playerTag)
      
      # TODO this is new test it
      playerObjDict[playerTag].tourneysEntered.append(tourneyObj.smashGGlink)
      playerObjDict[playerTag].numTourneysEntered += 1
      playerObjDict[playerTag].earnedTourneyPts += playerPts
      playerObjDict[playerTag].totalPossibleTourneyPts += tourneyObj.totalScore
      playerObjDict[playerTag].tourneyPtRatio = playerObjDict[playerTag].earnedTourneyPts/playerObjDict[playerTag].totalPossibleTourneyPts

 