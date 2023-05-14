
from playerClass import *
import numpy as np



def getLeagueTourneyTier(tourneyObj):
  """
  This is to be dynamically set in accordance with Sector X tiers.

  ALSO you can change tourneyObj.stotalscore directly here!!! if u want fixed score or to add bonuses or what not idl 

  """
  
  if tourneyObj.totalScore >= 64:
    tier = "S"
  elif tourneyObj.totalScore >= 48:
    tier = "A+"
  elif tourneyObj.totalScore >= 36:
    tier = "A"
  elif tourneyObj.totalScore >= 24:
    tier = "B"
  elif tourneyObj.totalScore >= 16:
    tierPoints = 20
    tier = "C"
  elif tourneyObj.totalScore <= 16:
    tier = "D"

  # print("tier for", tourneyObj.TName, tier, tourneyObj.totalScore)
  return tier


def buildPointPlacementDictionary(pointIncrement):
  """
  If u want to dynamically assign points by placement u can use this
  """

  placements = [1,2,3,4,5,7,9,13]

  pointDict = {}
  maxPoints = len(placements) * pointIncrement

  value = maxPoints

  for place in placements:
    pointDict[place] = value
    value -= pointIncrement

  return pointDict


def getPlayerEarnedLeaguePoints(placement, tourneyObj, playerTag):
  """
  Returns the amount of points for the league the player earned at a given tourney. 
  NOTE: not sure how to use dueling points yet, would need a separate variable to track or soemthing and dont wnat it in this function.


  Currently formula is (Placement Percentile * Tourney Point Value * 0.5) + Place Bonus +? Bounty Bonus?

  ORRR it can just be the placement points since the tiers divides that up already
  """
  placement = int(placement)
  percentile = calculatePercentile(int(placement), tourneyObj.totalEntrants)


  earnedWeightedPoints = round((percentile/100) * tourneyObj.totalScore)

  myIncrement = 10 
  """THIS INCREMENT CAN BE CHANGED"""
  placementBonusDict = buildPointPlacementDictionary(myIncrement)
  """
  ZACK! this above is what u can award placement bonus poitns to. we can mess with this as needed as well as these 2 functions

  NOTE: including this means that max points possible drastically changes. every tourney u enter * 40
  """

  tourneyTier = tourneyObj.tier

  placementPoints = 0
  if tourneyTier in ["S"]:
    # award points to top 16
    if placement < 17:
      placementPoints = placementBonusDict[placement]
  elif tourneyTier in ["A", "A+"]:
    # award points bonus to top 12
    if placement < 13:
      placementPoints = placementBonusDict[placement]

  elif tourneyTier in ["B", "C"]:
    # top 8
    if placement < 9:
      placementPoints = placementBonusDict[placement]
  
  elif tourneyTier in ["D"]:
    if placement < 6:
      # top 6
      placementPoints = placementBonusDict[placement]
  
  # totalPointsForTourney = earnedWeightedPoints*.5 + placementPoints
  totalPointsForTourney = placementPoints


  # print(playerTag, placement, tourneyTier, earnedWeightedPoints, placementPoints, totalPointsForTourney)
  return totalPointsForTourney


                     




def calculatePlayerTourneyPts(placement, tourneyObj, playerTag):
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
        perc = .93
      elif placement == 3:
        perc = .86

      if tourneyObj.totalEntrants >= 12 or beatThreshold:
        if placement == 4:
          perc = .79
    
    # TODO i think awarding points to top 3rd of bracket might make most sense??? hmmm idk

    # award pts to top 6 if more than 18 entrants
    if tourneyObj.totalEntrants >= 18 or beatThreshold:
      if placement == 5:
        perc = .72
    
    # award pts to top 8 if more than 24 entrants
    if tourneyObj.totalEntrants >= 24 or beatThreshold:
      if placement == 7:
        perc = .65

    # award pts to top 12 if more than 32? or 36... entrants #TODO Decidison
    if tourneyObj.totalEntrants >= 36 or beatThreshold:
      if placement == 9:
        perc = .58

    # award pts to top 16 if more than 48?? entrants
    if tourneyObj.totalEntrants >= 48 or beatThreshold:
      if placement == 13:
        perc = .51

    # perc = percentile/100 
    # TODO TRY COMPARING PERC AS PERCENITLE VS WHTA I SET ALSO BEAT HRTREHSOLD!!!

    """
    WHAT I LEARNED- percentile only is no good, and no percentile 
    
    means people dont get enough pts?
    """
    playerPts = perc * tourneyObj.totalScore

    # playerPts = tourneyObj.totalScore/np.sqrt(placement)

  return playerPts


def get_player_points(player_name, point_dict):
    """
    gets points for notable entrants
    """
    for points, players in point_dict.items():
      if player_name in players:
        return float(points), True
        
    return 0, False


def getTourneyScores(tourneyObj, playerLvlsDict):
  """
  This parses through a tournyes attendants and keeps incrementing points for the tourneys score based on its entrants
  it can then get the tier of the tourney. beta phase rn

  This also should be modified but right now the methodology is:
  - Each lvl player is worth a corresponding amount of points
  - The attendence score is half total entrants rounded down
  """
  
  tourneyObj.attendanceScore = tourneyObj.totalEntrants // 2

  for playerTag in tourneyObj.placementDict:
    
    points, isNotable = get_player_points(playerTag, playerLvlsDict)
    if isNotable:
      tourneyObj.stackedScore += points
      tourneyObj.notableEntrants.append(playerTag)

    tourneyObj.totalScore = tourneyObj.attendanceScore  + tourneyObj.stackedScore
    # tourneyObj.stackedRatio = len(tourneyObj.notableEntrants)/ tourneyObj.totalEntrants
    tourneyObj.stackedRatio = tourneyObj.stackedScore/ (tourneyObj.totalEntrants* 4.5) #TODO this 4.5 number is for scaling i should make it the 
    # average or soemthing

  tourneyObj.tier = getLeagueTourneyTier(tourneyObj)
  print(tourneyObj.TName, tourneyObj.tier, " Tier")





def updateAllPlayerData(tourneyObj, playerObjDict):

    for playerTag in tourneyObj.placementDict:

      placement = tourneyObj.placementDict[playerTag]

      #playerPts = calculatePlayerTourneyPts(placement, tourneyObj, playerTag)
      """
      TODO LEAGUE FUNCTION CALL HERE
      """
      playerPts = getPlayerEarnedLeaguePoints(placement, tourneyObj, playerTag)


      if playerTag not in playerObjDict:
        color = getPlayerColor(playerTag)
        playerObjDict[playerTag] = Player(playerTag, color)
      
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


      #WHY DID I MAKE THIS CONFUSING AND THE SAME NAME??? IS IT RIGHT????
      placementPercentilePts = percentile 

      weightedPercentilePts = (percentile/100) * tourneyObj.totalScore
      # TODO TESTING !!!!! recompute avg each time

      playerObjDict[playerTag].weightedPercentilePts += weightedPercentilePts
      playerObjDict[playerTag].weightedPercentileAvg = (playerObjDict[playerTag].weightedPercentilePts /playerObjDict[playerTag].totalPossibleTourneyPts) * 100


      playerObjDict[playerTag].percentilePts += placementPercentilePts
      playerObjDict[playerTag].avgPercentile = (playerObjDict[playerTag].percentilePts) / (playerObjDict[playerTag].numTourneysEntered)
      

      playerObjDict[playerTag].tourneyResultsDict[tourneyObj.TName] = PlayerTourneyResults(tourneyObj, placement, playerPts, placementPercentilePts, weightedPercentilePts)

 
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

  percentile = (numStrictlyBetter/ numEntrants) * 100

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

calculatePercentile(3,40)

def getPlayerColor(player):
    if player.lower() in []:
        c = "lawngreen"
    elif player.lower() in ["spiro", "sauce", "hoodinii","charm", "grey"]:
      c = "limegreen"
    elif player.lower() in ["xavier", "vince", "secret",  "aryeh", "hunterwinthorpe"]:
        c = "red"
    elif player.lower() in ["noodl", "chanman", "austi", "spectro"]:
        c = "yellow"
    elif player.lower() in ["snogi", "consent is badass", "treestain", "a9", "azazel"]:
        c = "orange"
    elif player.lower() in ["boosk", "zeusie", "jesty", "ham burrito"]:
        c = "magenta"
    elif player.lower() in ["alo!", "wheezy", "sly", "blase"]:
        c = "darkviolet"
    elif player.lower() in ["critz", "chocolatejesus", "dyla", "crest", "kurama"]:
        c = "mediumblue"
    else:
        if len(player.lower()) % 3 == 0:
          c = "dodgerblue"
        elif len(player.lower()) % 3 == 1:
          c = "hotpink"
        elif len(player.lower()) % 3 == 2:
          c = "cyan"
    return c
