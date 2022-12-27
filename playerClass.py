class Player:
  def __init__(self, tag):
    self.tag = tag
    self.tourneysEntered = []
    self.numTourneysEntered = 0
    self.earnedTourneyPts = 0
    self.totalPossibleTourneyPts = 0
    self.tourneyPtRatio = 0


  def to_dict(self):
      return {
          'tag': self.tag,
          'tourneysEntered' : self.tourneysEntered,
          'earnedTourneyPts' : self.earnedTourneyPts,
          'totalPossibleTourneyPts' : self.totalPossibleTourneyPts,
          'tourneyPtRatio' : self.tourneyPtRatio,
          'numTourneysEntered' : self.numTourneysEntered
      }
