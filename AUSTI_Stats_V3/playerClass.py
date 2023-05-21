import numpy as np
import math

class Player:
  def __init__(self, tag, color):
    self.tag = tag
    self.tourneysEntered = []
    self.tourneyResultsDict = {} 
    """ NOTE: key is tourneyname, value is an object of tournament information for the tourney entered by player"""
    self.numTourneysEntered = 0
    self.totalPossibleWeightedTourneyPts = 0

    self.bestTourneyResults = {} # will take top 7 or top 7+ and drop lowest 

    self.percentilePts = 0 # will be scaled by 100 cuz why not
    self.avgPercentile = 0
    self.weightedPercentileAvg = 0
    self.weightedPercentilePts = 0
    self.color = color

    self.tourneyPtRatio = 0 #TODO this is no longer a great metric since i made tourney poitns aharder to do- better metric is
    #placement ratio- what they got out of what was possible

    # LEAGUE DATA
    self.earnedTourneyPts = 0 # ETP: total points earned from tourneys (weighted + placementBonus)
    self.earnedWeightedPoints = 0
    self.placementBonusPoints = 0
    self.earnedDuelPoints = 0
    self.earnedBountyPoints = 0
    self.totalLeaguePoints = 0 # combined ETP + DP + BP


  def to_dict(self):
      return {
          'Player': self.tag,
          'Total League Points' : self.totalLeaguePoints,
          'Number of Tourneys Entered' : self.numTourneysEntered,

          'Earned Tourney Points' : self.earnedTourneyPts,
          'Earned Weighted Points': self.earnedWeightedPoints,
          'Earned Placement Bonus Points': self.placementBonusPoints,
          'Earned Duel Points' : self.earnedDuelPoints,
          'Earned Bounty Points' : self.earnedBountyPoints,


          'Tourneys Attended Object List' : self.tourneysEntered,
          'Max Points Possible' : self.totalPossibleWeightedTourneyPts,
          'Earned Point Ratio' : self.tourneyPtRatio,
          'Placement Percentile Average' : self.avgPercentile,
          'Weighted Points' : self.weightedPercentilePts,
          'Weighted Placement Percentile Average' : self.weightedPercentileAvg,
          'tourneyResultsDict': self.tourneyResultsDict,
          'color': self.color
      }


class PlayerTourneyResults:
  def __init__(self, tourneyObj, placement, pts, placePercentilePts, weightPercPoints):
    self.tourneyName = tourneyObj.TName
    self.tourneyObj = tourneyObj
    """ self.headToHeadData = [] # TODO TODO TODO this later """
    self.tourneyPlacement = placement
    self.tourneyPtsEarned = pts
    self.percentilePtsEarned = weightPercPoints
    self.tourneyPercentile = placePercentilePts

  def printInfo(self):
    print("==================================")
    print("tourney: ", self.tourneyName)
    print("placement: ", self.tourneyPlacement, "/",self.tourneyObj.totalEntrants)
    print("pts earned: ", self.tourneyPtsEarned)
    print("percentile poitns earned: ", self.percentilePtsEarned)
    print("max tourney pts: ",self.tourneyObj.totalScore)
    print("percentile: ", self.tourneyPercentile)