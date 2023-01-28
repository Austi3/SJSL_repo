import numpy as np

class Player:
  def __init__(self, tag):
    self.tag = tag
    self.tourneysEntered = []
    self.tourneyResultsDict = {} 
    """ TODO key is tourneyname, value is an object of tournament information for the tourney entered by player"""
    self.numTourneysEntered = 0
    self.earnedTourneyPts = 0
    self.totalPossibleTourneyPts = 0

    self.percentilePts = 0 # will be scaled by 100 cuz why not
    self.avgPercentile = 0
    self.weightedPercentileAvg = 0
    self.weightedPercentilePts = 0

    self.tourneyPtRatio = 0 #TODO this is no longer a great metric sinc ei made tourney poitns aharder to do- better metric is
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


  def to_dict(self):
      return {
          'tag': self.tag,
          'tourneysEntered' : self.tourneysEntered,
          'earnedTourneyPts' : self.earnedTourneyPts,
          'totalPossibleTourneyPts' : self.totalPossibleTourneyPts,
          'tourneyPtRatio' : self.tourneyPtRatio,
          'numTourneysEntered' : self.numTourneysEntered,
          'avgPercentile' : self.avgPercentile,
          'weightedPercentilePoints' : self.weightedPercentilePts,
          'weightedPercentileAvg' : self.weightedPercentileAvg,
          'tourneyResultsDict': self.tourneyResultsDict
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