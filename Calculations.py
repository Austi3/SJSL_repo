
from playerClass import *
import numpy as np

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
  elif tag.lower() in ['sauce', 'hotsaucefuego','obmcbob', 'gravy']:
    tag = 'Sauce'
  elif tag in ['xavier', 'Xavier']:
    tag = 'Xavier'
  return tag

def calculatePlayerTourneyPts(placement, tourneyObj, playerTag):
  """
  TODO!!!!!! so this calculation is inherently flawed and needs to be updated. what im noticing now is:
  players own worth is counted
  the percentage of points  might be too strong- like if 2nd gets 95% is that right? maybe a bonus is needed 
  for top 8??? 
  maybe thresholds are in order like 1st gets 100%. 2nd gets 95%. 3rd gets 90 etc. defined up to 33rd
  """
  if playerTag == "A9":
    print()
  
  if not placement:
    print("error: NO PLACEMENT FOUND for a player",tourneyObj.officialName, tourneyObj.placementDict)
    playerPts = 0
  else:

    # NOTE this was my original percentage calculation- based off of total entrants and placement
    # perc = ((tourneyObj.totalEntrants - int(placement) + 1)/tourneyObj.totalEntrants)
    """
    """
    placement = int(placement)
    # NOTE this is my fixed percentage model- may want to adjust-- MY NEW PERCENTILE MODEL COULD DO IT!!!
    # its much less arbitrary and scales
    
    percentile = calculatePercentile(int(placement), tourneyObj.totalEntrants)

    percentileAbove = 100 - percentile
    
    stackedThreshold = tourneyObj.stackedRatio * 100

  
    beatThreshold = False
    if stackedThreshold > percentileAbove:
      beatThreshold = True
      #print(tourneyObj.TName, stackedThreshold, percentileAbove, placement)

    perc = 0
    if tourneyObj.totalEntrants >= 8:
      if placement == 1:
        perc = 1.00
      elif placement == 2:
        perc = .90
      elif placement == 3:
        perc = .80

      if tourneyObj.totalEntrants >= 12 or beatThreshold:
        if placement == 4:
          perc = .70
    
    # TODO i think awarding points to top 3rd of bracket might make most sense??? hmmm idk

    # award pts to top 6 if more than 18 entrants
    if tourneyObj.totalEntrants >= 18 or beatThreshold:
      if placement == 5:
        perc = .60
    
    # award pts to top 8 if more than 24 entrants
    if tourneyObj.totalEntrants >= 24 or beatThreshold:
      if placement == 7:
        perc = .50

    # award pts to top 12 if more than 32? or 36... entrants #TODO Decidison
    if tourneyObj.totalEntrants >= 36 or beatThreshold:
      if placement == 9:
        perc = .40

    # award pts to top 16 if more than 48?? entrants
    if tourneyObj.totalEntrants >= 48 or beatThreshold:
      if placement == 13:
        perc = .30

    # perc = percentile/100 
    # TODO TRY COMPARING PERC AS PERCENITLE VS WHTA I SET ALSO BEAT HRTREHSOLD!!!

    """
    WHAT I LEARNED- percentile only is no good, and no percentile 
    
    means people dont get enough pts?
    """
    playerPts = perc * tourneyObj.totalScore

    # playerPts = tourneyObj.totalScore/np.sqrt(placement)

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
    # tourneyObj.stackedRatio = len(tourneyObj.notableEntrants)/ tourneyObj.totalEntrants
    tourneyObj.stackedRatio = tourneyObj.stackedScore/ (tourneyObj.totalEntrants* 4.5)

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

      playerPts = calculatePlayerTourneyPts(placement, tourneyObj, playerTag)

      if playerTag not in playerObjDict:
        playerObjDict[playerTag] = Player(playerTag)
      
      # TODO this is new test it
      playerObjDict[playerTag].tourneysEntered.append(tourneyObj)
      playerObjDict[playerTag].numTourneysEntered += 1
      playerObjDict[playerTag].earnedTourneyPts += playerPts
      playerObjDict[playerTag].totalPossibleTourneyPts += tourneyObj.totalScore
      playerObjDict[playerTag].tourneyPtRatio = 100*(playerObjDict[playerTag].earnedTourneyPts/playerObjDict[playerTag].totalPossibleTourneyPts)
      

      percentile = calculatePercentile(int(placement), tourneyObj.totalEntrants)


      #THIS NEXT PART IS WRONG AND OUTDATED!!! ((tourneyObj.totalEntrants - int(placement) + 1)/tourneyObj.totalEntrants) 

      """
      todo todo TODO TODO
      NEED TO DOUBLE CHECK THIS???
      """
      placementPercentilePts = percentile 

      weightedPercentilePts = (percentile/100) * tourneyObj.totalScore
      # TODO TESTING !!!!! recompute avg each time

      playerObjDict[playerTag].weightedPercentilePts += weightedPercentilePts
      playerObjDict[playerTag].weightedPercentileAvg = playerObjDict[playerTag].weightedPercentilePts /playerObjDict[playerTag].totalPossibleTourneyPts


      playerObjDict[playerTag].percentilePts += placementPercentilePts
      playerObjDict[playerTag].avgPercentile = (playerObjDict[playerTag].percentilePts) / (playerObjDict[playerTag].numTourneysEntered)
      

      playerObjDict[playerTag].tourneyResultsDict[tourneyObj.TName] = PlayerTourneyResults(tourneyObj, placement, playerPts, placementPercentilePts)

 
def getPlayerTopResults(playerObjDict):
  for playerKey in playerObjDict:
    for tourneyKey in playerObjDict[playerKey].tourneyResultsDict:
      tourney = playerObjDict[playerKey].tourneyResultsDict[tourneyKey]
      if tourney.tourneyPts > 0:
        pass
        # print(tourney.tourneyName, tourney.tourneyPlacement, tourney.tourneyPts, playerKey)
      

def calculatePercentile(placement, numEntrants):
  # percentile formula is B/N * 100 where N is num Entrants and B is the number of players you did STRICTLY better than.
  # Meaning if you placed 9th its everyone who did worse than 9th, meaning we need to ignore the tie


  # hard part here is determining how many players placed the same as you becasue double elim makes that scale weirdly
  numPlayersTied = computePlayersTied(placement,numEntrants)

  numStrictlyBetter= numEntrants - (placement - 1) - numPlayersTied #TODO double chekc this later

  """
  #B = E - (P-1) - T
  #num players you did STRICTLY better than = numEntrants - (placement -1)
  """

  # TODO I  NEED TO CALCULATE NUM PLAYERS WORSE!!!! ITS NOT TIED!!!

  percentile = (numStrictlyBetter/ numEntrants) * 100

  # print("Placement/entrants", placement, "/", numEntrants, "PERCENTILE IS: ", percentile)
  
  """THIS RETURNS A WHOLE NUMBER OUT OF 100"""
  # print("percentile is ", percentile)
  return percentile 


def computePlayersTied(placement, numEntrants):  
  """
  compute the amount of OTHER players that tied with you

  so if u got 9th, 2 people get 7th but at most ONE OTHER PERSON tied with you. so answer is 1
  """

  # so its at maximum tied capacity if its not last place
  lastPlace = False

  if numEntrants <= 4:
    print("ERROR: tourney way too small lmao")
  
  elif 4 < numEntrants <= 6:
    last = 5
  elif 6 < numEntrants <= 8:
    last = 7
  elif 8 < numEntrants <= 12:
    last = 9
  elif 12 < numEntrants <= 16:
    last = 13
  elif 16 < numEntrants <= 24:
    last = 17
  elif 24 < numEntrants <= 32:
    last = 25
  elif 32 < numEntrants <= 48:
    last = 33
  elif 48 < numEntrants <= 64:
    last = 49
  elif 64 < numEntrants <= 96:
    last = 65
  elif numEntrants > 96:
    print("ERROR: Tourney too small lmao")
  
  if placement == last:
    numTied = numEntrants - (placement - 1)
    lastPlace = True
    return numTied
  
  if placement in [1,2,3,4]:
    numTied = 0 # nobody tied with you so return 0
    return numTied

  if not lastPlace:
    """aha the highest power of 2 tht fits/2?"""
    
    n = 0
    while 2**n <= placement:
      n +=1
  
    numTied = (2**(n-2)) #calculate the n value that gives you multiple of 2 thats needed and kinda weird
    

    return numTied #number of players tied for this placement. no longer doing the -1 thing

calculatePercentile(4,30)