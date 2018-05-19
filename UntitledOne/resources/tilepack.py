#place to hold many rooms in the game
#hallway
class Hallway(MapTile):
	def intro_text(self):
		return """\nAn empty hallway. Musty and stained carpet greets the dull white walls at cracked trim\n"""

	def modify_player(self, the_player):
		pass #no effect

class NewCloset(GrabLootRoom):
	def __init__(self, x, y):
		super().__init__(x, y, items.Scalpel())

	def intro_text(self):
		return """\nYou find a small closet, a small scalpel lies on the floor\n"""

class Closet(LootRoom):
	def __init__(self, x, y):
		super().__init__(x, y, items.Syringe())

	def intro_text(self):
		return """\nYou enter a cramped room, a dim light illuminates empty shelves, bearing only a small empty syringe\n"""

  class GuardRoom(MobRoom):
	def __init__(self, x, y):
		super().__init__(x, y, enemies.Guard())

	def intro_text(self):
		if self.enemy.is_alive():
			return """\nA guard bars the way\n"""
		else:
			return """\nA guard lies on the ground, his blood splattered on the floor\n"""
