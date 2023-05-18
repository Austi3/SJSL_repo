
from enum import Enum
import regex as re

class Tourney:
    def __init__(self, linkName, startgglink, TName, tseries, color, totalEntrants, resultsDict):
      self.fullLink = linkName
      self.smashGGlink = startgglink
      self.TName = TName
      if "Battle Over The Bridge" in TName:
        self.TName = TName.replace("Battle Over The Bridge", "BOTB")
      self.tseries = tseries
      self.color = color
      self.totalEntrants = totalEntrants
      self.placementDict = resultsDict

      """
      values to be calculated later
      """
      self.attendanceScore = 0
      self.tier = "None"
      self.stackedScore = 0
      self.totalScore = 0
      self.stackedRatio = 0
      self.notableEntrants = []
      self.allEntrants = []
      self.tier = "N/A"


    def to_dict(self):
        return {
            'Hyperlink': self.fullLink,
            'SGGName': self.smashGGlink,
            'TName' : self.TName,
            'totalScore': self.totalScore,
            'tier':self.tier,
            'attendanceScore' : self.attendanceScore, 
            'stackedScore': self.stackedScore,
            'Total Entrants': self.totalEntrants,
            'notable entrants': self.notableEntrants,
            'placementDict':self.placementDict,
            'TSeries': self.tseries,
            'Color': self.color,
            'stackedRatio': self.stackedRatio
        }

