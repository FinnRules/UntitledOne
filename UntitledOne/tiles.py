import items, enemies, actions, world

class MapTile:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def intro_text(self):
		raise NotImplementedError()

	def modify_player(self, the_player):
		raise NotImplementedError()

	def adjacent_moves(self):
		moves = []
		if world.tile_exists(self.x + 1, self.y):
			moves.append(actions.MoveEast())
		if world.tile_exists(self.x - 1, self.y):
			moves.append(actions.MoveWest())
		if world.tile_exists(self.x, self.y - 1):
			moves.append(actions.MoveNorth())
		if world.tile_exists(self.x, self.y + 1):
			moves.append(actions.MoveSouth())
		return moves

	def available_actions(self):
		moves = self.adjacent_moves()
		moves.append(actions.ViewInventory())
		moves.append(actions.Use(tile=self))

		return moves

class StartingRoom(MapTile):
	def intro_text(self):
		return """\nYou wake up on the floor of a lab. You do not remember who you are or how you got here. In all four directions there lie doors\n"""

	def modify_player(self, the_player):
		pass #no effect

class LootRoom(MapTile):
	def __init__(self, x, y, item):
		self.item = item
		super().__init__(x, y)

	def add_loot(self, the_player):
		the_player.inventory.append(self.item)

	def modify_player(self, the_player):
		self.add_loot(the_player)

#room the waits for the player to specify that they want to grab an item, rather than giving it to them automatically
class GrabLootRoom(MapTile):
	def __init__(self, x, y, *args):
		self.item = []
		for arg in args:
			self.item.append(arg)
		super().__init__(x, y)


	def modify_player(self, the_player):
		pass

	def available_actions(self):
		moves = self.adjacent_moves()
		moves.append(actions.ViewInventory())
		if len(self.item) != 0:
			moves.append(actions.Grab(tile=self))

		return moves

class MobRoom(MapTile):
	def __init__(self, x, y, enemy):
		self.enemy = enemy
		super().__init__(x, y)

	def modify_player(self, the_player):
		if self.enemy.is_alive():
			the_player.hp = the_player.hp - self.enemy.damage
			print("\n{} does {} damage to you. You have {} HP remaining\n".format(self.enemy, self.enemy.damage, the_player.hp))

	def available_actions(self):
		if self.enemy.is_alive():
			return [actions.Flee(tile=self), actions.Attack(enemy=self.enemy)]
		else:
			return self.adjacent_moves()

class WinRoom(MapTile):
	def intro_text(self):
		return """\nYou feel the hot sun beat down on your face. Your eyes strain as its glow reaches you in what feels like a lifetime. You are free\n"""

	def modify_player(self, player):
		player.victory = True

#===========================================================================================================
#place to hold many rooms in the game
#hallway
class Hallway(MapTile):
	def intro_text(self):
		return """\nAn empty hallway. Musty and stained carpet greets the dull white walls at cracked trim\n"""

	def modify_player(self, the_player):
		pass #no effect

class NewCloset(GrabLootRoom):
	def __init__(self, x, y):
		super().__init__(x, y, items.Syringe(), items.Book())

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
