import items, enemies, actions, world

class MapTile:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.locked = False

	def intro_text(self):
		raise NotImplementedError()

	def modify_player(self, the_player):
		raise NotImplementedError()

	def adjacent_moves(self):
		moves = []
		if world.tile_exists(self.x + 1, self.y) and not world.is_locked(self.x + 1, self.y):
			moves.append(actions.MoveEast())
		if world.tile_exists(self.x - 1, self.y) and not world.is_locked(self.x - 1, self.y):
			moves.append(actions.MoveWest())
		if world.tile_exists(self.x, self.y - 1) and not world.is_locked(self.x, self.y - 1):
			moves.append(actions.MoveNorth())
		if world.tile_exists(self.x, self.y + 1) and not world.is_locked(self.x, self.y + 1):
			moves.append(actions.MoveSouth())
		return moves

	def available_actions(self):
		moves = self.adjacent_moves()
		moves.append(actions.ViewInventory())
		moves.append(actions.Use(tile=self))
		moves.append(actions.Quit())

		return moves

#Z/39
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
		moves.append(actions.Use(tile=self))
		moves.append(actions.Quit())
		if len(self.item) != 0:
			moves.append(actions.Grab(tile=self))

		return moves

class MobRoom(MapTile):
	def __init__(self, x, y, enemy, *args):
		self.enemy = enemy
		self.item = []
		for arg in args:
			self.item.append(arg)
		super().__init__(x, y)

	def modify_player(self, the_player):
		if self.enemy.is_alive() and self.enemy.aggro:
			the_player.hp = the_player.hp - self.enemy.damage
			print("\n{} does {} damage to you. You have {} HP remaining\n".format(self.enemy.name, self.enemy.damage, the_player.hp))

	def available_actions(self):
		if self.enemy.is_alive() and self.enemy.aggro:
			return [actions.Flee(tile=self), actions.Attack(enemy=self.enemy), actions.Talk(tile=self, enemy=self.enemy), actions.Quit()]
		elif self.enemy.is_alive() and not self.enemy.aggro:
			moves = self.adjacent_moves()
			moves.append(actions.ViewInventory())
			moves.append(actions.Use(tile=self))
			moves.append(actions.Quit())
			moves.append(actions.Attack(enemy=self.enemy))
			moves.append(actions.Talk(tile=self, enemy=self.enemy))
			return moves
		else:
			moves = self.adjacent_moves()
			moves.append(actions.ViewInventory())
			moves.append(actions.Use(tile=self))
			moves.append(actions.Quit())
			if len(self.item) != 0:
				moves.append(actions.Grab(tile=self))
			return moves

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

class StartingCloset(GrabLootRoom):
	def __init__(self, x, y):
		super().__init__(x, y, items.Syringe(), items.StartingClosetPaper())

	def intro_text(self):
		return """\nYou find a small closet, a small syringe lies on the floor. A cruppled paper is taped to the door\n"""

#Z/43, AD/49
class LabGuard(MobRoom):
	def __init__(self, x, y):
		super().__init__(x, y, enemies.Guard())

	def intro_text(self):
		if self.enemy.is_alive():
			return """\nA guard bars the way\n"""
		else:
			return """\nA guard lies on the ground, his blood splattered on the floor\n"""
#AB/39
class HallwayTunnel(MapTile):
	def intro_text(self):
		return """\nThe hallway stretches onward, with a small light flickering from a vent\n"""
	
	def modify_player(self, the_player):
		pass

#AB/40-41, etc
class Tunnel(MapTile):
	def __init__(self, x, y):
		super().__init__(x, y)
		self.locked = True

	def intro_text(self):
		return """\nThe walls, made only of compacked dirt, held up but wood posts and supports, stretch further onward\n"""
	
	def modify_player(self, the_player):
		pass
#AB/49
class TunnelSociety(MobRoom):
	def __init__(self, x, y):
		super().__init__(x, y, enemies.TunnelDweller(), items.Shovel())

	def intro_text(self):
		if self.enemy.is_alive():
			print("\nYou find yourself in a small clearing with several dirty people digging hurridly at a dirt wall")
			self.enemy.talk()
		else:
			print("\nThe bodies of the tunnelers lie at your feet, bathing the ground in crimson, their shovel still clutched in their hands\n")

class ComputerLab(MobRoom):
	def __init__(self, x, y):
		super().__init__(x, y, enemies.ComputerY34(), items.ComputerNote())

	def intro_text(self):
		return """\nThe door swings open to reveal a small computer lab, empty but for a moniter dimly flickering in a corner. A note is stuck to the upper left hand corner\n"""			
	
	def available_actions(self):
		moves = self.adjacent_moves()
		moves.append(actions.ViewInventory())
		moves.append(actions.Use(tile=self))
		moves.append(actions.Quit())
		moves.append(actions.Talk(tile=self, enemy=self.enemy))
		if len(self.item) != 0:
			moves.append(actions.Grab(tile=self))
		return moves
	
	
