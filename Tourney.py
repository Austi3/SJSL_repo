
"""
TODO!!! rename a lot of these to make more sense
"""
from enum import Enum
import regex as re

class Tourney:
    def __init__(self, linkName, startgglink, TName, tseries, color, totalEntrants, resultsString):
      self.fullLink = linkName
      self.smashGGlink = startgglink
      self.TName = TName
      if "Battle Over The Bridge" in TName:
        self.TName = TName.replace("Battle Over The Bridge", "BOTB")
      self.tseries = tseries
      self.color = color
      self.totalEntrants = totalEntrants
      self.resultsString = resultsString

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
            'Hyperlink': self.fullLink,
            'SGGName': self.smashGGlink,
            'TName' : self.TName,
            'TSeries': self.tseries,
            'Color': self.color,
            'Total Entrants': self.totalEntrants,

            'resultsString' : self.resultsString,
            'notable entrants': self.notableEntrants,
            'otherEntrants': self.otherEntrants,
            'placementDict':self.placementDict,
            'attendanceScore' : self.attendanceScore, 
            'stackedScore': self.stackedScore,
            'totalScore': self.totalScore,
            'stackedRatio': self.stackedRatio
        }

