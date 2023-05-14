import numpy as np
import math

class Player:
  def __init__(self, tag, color):
    self.tag = tag
    self.tourneysEntered = []
    self.tourneyResultsDict = {} 
    """ NOTE: key is tourneyname, value is an object of tournament information for the tourney entered by player"""
    self.numTourneysEntered = 0
    self.earnedTourneyPts = 0
    self.totalPossibleTourneyPts = 0

    self.bestTourneyResults = {} # will take top 7 or top 7+ and drop lowest 

    self.percentilePts = 0 # will be scaled by 100 cuz why not
    self.avgPercentile = 0
    self.weightedPercentileAvg = 0
    self.weightedPercentilePts = 0
    self.color = color

    self.tourneyPtRatio = 0 #TODO this is no longer a great metric since i made tourney poitns aharder to do- better metric is
    #placement ratio- what they got out of what was possible

  def printPlayerInfo(self):
    print("****************************************")
    print("tag: ",self.tag )
    print("tourneys entered: ", len(self.tourneysEntered))
    print()
    print("total points earned by my tiers: ", self.earnedTourneyPts)
    print("total possible tourney pts: ", self.totalPossibleTourneyPts)
    print("tourney pt ratio: ", np.round(self.tourneyPtRatio,2))
    print()

    print("avg place percentile: ", np.round(self.avgPercentile,2))
    print("weighted percentile points: ", np.round(self.weightedPercentilePts,2))
    print("weighted percentile avg (which = pt ratio) ", np.round(self.weightedPercentileAvg,2))

  # TODO this doesnt work yet
  # def remove_bottom_20_percent(self, d: dict, attr_name: str) -> dict:
  #     n = len(d)
  #     if n <= 7:
  #         return d
  #     sorted_dict = sorted(d.items(), key=lambda x: getattr(x[1], attr_name))
  #     bottom_20_percent = math.ceil(n * 0.2)
  #     if bottom_20_percent == 0:
  #         return d
  #     else:
  #         bottom_keys = [key for key, value in sorted_dict[:bottom_20_percent]]
  #         for key in bottom_keys:
  #             del d[key]
  #         return d

  def to_dict(self):
      return {
          'tag': self.tag,
          'Tourneys Attended' : self.tourneysEntered,
          'Earned League Points' : self.earnedTourneyPts,
          'Max Points Possible' : self.totalPossibleTourneyPts,
          'Earned Point Ratio' : self.tourneyPtRatio,
          'Number of Tourneys Entered' : self.numTourneysEntered,
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