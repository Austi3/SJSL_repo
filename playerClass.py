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
          'weightedPercentileAvg' : self.weightedPercentileAvg
      }


class PlayerTourneyResults:
  def __init__(self, tourneyObj, placement, pts, placePercentile):
    self.tourneyName = tourneyObj.TName
    self.tourneyObj = tourneyObj
    """ self.headToHeadData = [] # TODO TODO TODO this later """
    self.tourneyPlacement = placement
    self.tourneyPtsEarned = pts
    self.tourneyPercentile = placePercentile
