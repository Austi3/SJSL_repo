
"""
TODO!!! rename a lot of these to make more sense
"""
class Tourney:
    def __init__(self, linkName, startgglink, officialName, tseries, color, totalEntrants, resultsDFrame):
      self.fullLink = linkName
      self.smashGGlink = startgglink
      self.officialName = officialName
      self.tseries = tseries
      self.color = color
      self.totalEntrants = totalEntrants
      self.resultsDFrame = resultsDFrame

      """
      values to be calculated later
      """
      self.attendanceScore = 0
      self.stackedScore = 0
      self.totalScore = 0
      self.stackedRatio = 0
      self.notableEntrants = []
      self.otherEntrants = []
      self.allEntrants = []
      self.placementDict = {}


    def to_dict(self):
        return {
            'fullLink': self.fullLink,
            'smashGGlink': self.smashGGlink,
            'Tournament Name' : self.officialName,
            'tseries': self.tseries,
            'Color': self.color,
            'Total Entrants': self.totalEntrants,
            'resultsDFrame' : self.resultsDFrame,
            'notable entrants': self.notableEntrants,
            'otherEntrants': self.otherEntrants,
            'placementDict':self.placementDict,
            'attendanceScore' : self.attendanceScore, 
            'stackedScore': self.stackedScore,
            'totalScore': self.totalScore,
            'stackedRatio': self.stackedRatio
        }