def handleSpecialPlayers(tag):
  """
  TODO i might want a way to make this more robust or avoid this, but itll work for now

  This is my list of players who have changed their tags. Annoying but i must manually add each time i see new one.

  Returns a formatted player tag with their proper name
  """
  tag= tag.replace("~", "") # need this til i get rid of ~~~ formatting

  if tag.lower() in ['snogi', 'critz but retired', '<3 brisket']:
    tag = 'Snogi'
  elif tag.lower() in ['chanman', 'chan', "chan!", 'poop87', 'funnymoments with ridley']:
    tag = 'Chan'
  elif tag.lower() in ['sauce', 'hotsaucefuego','obmcbob', 'gravy', "brother zoinks"]:
    tag = 'Sauce'
  elif tag in ['xavier', 'Xavier']:
    tag = 'Xavier'
  elif tag.lower() in ['aryeh', 'boundy', 'unregistered hypercam 2']:
    tag = 'Aryeh'
  elif tag.lower() in ["vince", "sapphire"]:
    tag = "Vince"
  elif tag.lower() in ["hunter", "hunterwinthorpe"]:
    tag = "Hunter"
  elif tag.lower() in ["pee83", "treestain", "justin rodriguez"]:
    tag = "Treestain"
  elif tag.lower() in ["spiro", "tinder god", "ap"]:
    tag = "Spiro"
  elif tag.lower() in ["jacie", "jesty"]:
    tag = "Jesty"
  elif tag.lower() in ["grey", "badfish321"]:
    tag = "Grey"
  elif tag.lower() in ["waliu", "dak"]:
      tag = "dak"
  elif tag.lower() in ["torrent", "roommate", "harper"]:
    tag = "torrent"
  elif tag.lower() in ["blahaj fan", "organic"]:
     tag = "orGanic"

  return tag






def getPlayerColor(player):
    if player.lower() in []:
        c = "lawngreen"
    elif player.lower() in ["spiro", "sauce", "hoodinii","charm", "grey"]:
      c = "limegreen"
    elif player.lower() in ["xavier", "vince", "secret",  "aryeh", "hunterwinthorpe"]:
        c = "red"
    elif player.lower() in ["noodl", "chan", "austi", "spectro"]:
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