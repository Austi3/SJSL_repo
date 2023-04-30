
# import matplotlib.pyplot as plt
# import numpy as np
# import regex as re
# import pysmashgg
# import pandas as pd
# from enum import Enum

"""
OLD FILE USED IN MY OG GOOGLE COLLAB TO USE  API AND MAKE EXCEL SHEET
"""
      
# class Tourney:
#     def __init__(self, linkName, startgglink, officialName, tseries, color, totalEntrants, resultsDFrame):
#       self.fullLink = linkName
#       self.smashGGlink = startgglink
#       self.officialName = officialName
#       self.tseries = tseries
#       self.color = color
#       self.totalEntrants = totalEntrants
#       self.resultsDFrame = resultsDFrame

#       """
#       values to be calculated later
#       """
#       self.attendanceScore = 0
#       self.stackedScore = 0
#       self.totalScore = 0
#       self.stackedRatio = 0
#       self.notableEntrants = []
#       self.otherEntrants = []
#       self.allEntrants = []
#       self.placementDict = {}


#     def to_dict(self):
#         return {
#             'fullLink': self.fullLink,
#             'smashGGlink': self.smashGGlink,
#             'Tournament Name' : self.officialName,
#             'tseries': self.tseries,
#             'Color': self.color,
#             'Total Entrants': self.totalEntrants,
#             'resultsDFrame' : self.resultsDFrame,
#             'notable entrants': self.notableEntrants,
#             'otherEntrants': self.otherEntrants,
#             'placementDict':self.placementDict,
#             'attendanceScore' : self.attendanceScore, 
#             'stackedScore': self.stackedScore,
#             'totalScore': self.totalScore,
#             'stackedRatio': self.stackedRatio
#         }


# class TS(Enum):
#     HOPS = 0
#     HYPR = 1
#     PBJ = 2
#     BOTB = 3
#     ROWN = 4
#     CAT = 5
#     OTHR = 6

# """
# These formatting functions were used when i made the original API calls to populate a spreadsheet
# """

# def formatTourneyName(name, tournEnum):
    
#     splitName = name.split("-")

#     endNum = ""
#     for elt in splitName:
#       if re.search("[0-9]", elt):
#         endNum += "-" + elt

#     if tournEnum == TS.HOPS.value:
#       newName = "Hops N stocks"
#     elif tournEnum == TS.HYPR.value:
#       newName = "Hyperspace"
#     elif tournEnum == TS.PBJ.value:

#         newName = "Pop The Bubble"

#     elif tournEnum == TS.BOTB.value:
#       newName = "Battle Over The Bridge"
#     elif tournEnum == TS.ROWN.value:
#       newName = "RU Smashin"
#     elif tournEnum == TS.CAT.value:
#       newName = "Catastrophe"
#     else:
#       if "pbj-presents-road-to-apex" in name:
#         newName = "PBJ Road to Apex"
#       elif "palooza" in name:
#         newName = "PBJ Holiday Palooza"

#       newName = name.replace("-", " ")
#       newName = newName.title()
#       endNum = ""
    
#     return newName + endNum

# def getEnumInfo(enum):
#   if enum == TS.HOPS.value:
#     tseries = "Hops N Stocks"
#     color = "orange"
#   elif enum == TS.HYPR.value:
#     tseries = "Hyperspace"
#     color = "gray"
#   elif enum == TS.PBJ.value:
#     tseries = "Pop the Bubble"
#     color = "pink"
#   elif enum == TS.BOTB.value:
#     tseries = "Battle over the Bridge"
#     color = 'red'
#   elif enum == TS.ROWN.value:
#     tseries = "RU Smashin"
#     color = "gold"
#   elif enum == TS.CAT.value:
#       tseries = "Catastrophe"
#       color = 'blue'
#   else:
#     tseries = "Other"
#     color = "green"

#   return tseries, color

  

