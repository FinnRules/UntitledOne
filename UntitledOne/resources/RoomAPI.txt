#Guide on creating rooms

#tiles with no effects:
class <Name>(MapTile):
  def intro_text(self):
    return """Room intro text""" #triple quote supports multi line strings

  def modify_player(self, the_player):
    pass

#tiles with items, requires grab command
class <Name>(GrabLootRoom):
  def __init__(self, x, y):
    super().__init__(x, y, <item>) #<item> should be a plain object like items.Scalpel(), include param and format as a var
  
  def intro_text(self):
    return """Room text"""

#room that instantly gives an item (discouraged)
class <Name>(LootRoom):
   def __init__(self, x, y):
    super().__init__(x, y, <item>)

  def intro_text(self):
    return """Room text"""
