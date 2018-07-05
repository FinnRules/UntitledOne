import items, enemies, actions, world

class MapTile:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.locked = False
		self.key = None

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

	def devcommands(self, the_player): #houses all dev commands and extends the moves list if the player is in dev mode
		devcommandslist = []
		devcommandslist.append(actions.Teleport())
		devcommandslist.append(actions.MapInfo(tile=self))
		devcommandslist.append(actions.Invin())
		devcommandslist.append(actions.SetHp())
		devcommandslist.append(actions.NpcHp(tile=self))
		devcommandslist.append(actions.Settings())
		return devcommandslist

	def available_actions(self, the_player):
		moves = self.adjacent_moves()
		moves.append(actions.ViewInventory())
		moves.append(actions.Use(tile=self))
		moves.append(actions.Quit())
		if the_player.fsm:
			moves.extend(self.devcommands(the_player))

		return moves

#AB/39
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

	def available_actions(self, the_player):
		moves = self.adjacent_moves()
		moves.append(actions.ViewInventory())
		moves.append(actions.Use(tile=self))
		moves.append(actions.Quit())
		if len(self.item) != 0:
			moves.append(actions.Grab(tile=self))

		if the_player.fsm:
			moves.extend(self.devcommands(the_player))

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
			if not the_player.nv:
				the_player.hp = the_player.hp - self.enemy.damage
				print("\n{} does {} damage to you. You have {} HP remaining\n".format(self.enemy.name, self.enemy.damage, the_player.hp))
			elif the_player.nv:
				print("{} attempts to do {} damage [Prevented by Invincibility]\n".format(self.enemy.name, self.enemy.damage))

	def available_actions(self, the_player):
		if self.enemy.is_alive() and self.enemy.aggro:
			moves = []
			moves.append(actions.ViewInventory())
			moves.append(actions.Use(tile=self))
			moves.append(actions.Flee(tile=self))
			moves.append(actions.Attack(enemy=self.enemy))
			moves.append(actions.Talk(tile=self, enemy=self.enemy))
			moves.append(actions.Quit())
			if the_player.fsm:
				moves.extend(self.devcommands(the_player))

			return moves

		elif self.enemy.is_alive() and not self.enemy.aggro:
			moves = self.adjacent_moves()
			moves.append(actions.ViewInventory())
			moves.append(actions.Use(tile=self))
			moves.append(actions.Quit())
			moves.append(actions.Attack(enemy=self.enemy))
			moves.append(actions.Talk(tile=self, enemy=self.enemy))
			if the_player.fsm:
				moves.extend(self.devcommands(the_player))

			return moves
		else:
			moves = self.adjacent_moves()
			moves.append(actions.ViewInventory())
			moves.append(actions.Use(tile=self))
			moves.append(actions.Quit())
			if len(self.item) != 0:
				moves.append(actions.Grab(tile=self))

			if the_player.fsm:
				moves.extend(self.devcommands(the_player))

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


class LabGuard(MobRoom):
	def __init__(self, x, y):
		super().__init__(x, y, enemies.Guard())

	def intro_text(self):
		if self.enemy.is_alive():
			return """\nA guard bars the way\n"""
		else:
			return """\nA guard lies on the ground, his blood splattered on the floor\n"""

class Tunnel(MapTile):
	def __init__(self, x, y):
		super().__init__(x, y)

	def intro_text(self):
		return """\nThe walls, made only of compacked dirt, held up but wood posts and supports, stretch further onward\n"""
	
	def modify_player(self, the_player):
		pass

class TunnelSociety(MobRoom):
	def __init__(self, x, y):
		super().__init__(x, y, enemies.TunnelDweller(), items.Shovel())

	def intro_text(self):
		if self.enemy.is_alive():
			print("\nYou find yourself in a small clearing with several dirty people digging hurridly at a dirt wall")
			self.enemy.talk()
		else:
			print("\nThe bodies of the tunnelers lie at your feet, bathing the ground in crimson, their shovel still clutched in their hands\n")

class TunnelEntrance(MapTile):
	def __init__(self, x, y):
#		self.locked = True
		super().__init__(x, y)
		self.locked = True
		self.key = "screwdriver"

	def intro_text(self):
		return """\nLight seeps in from the vent, revealing a cramped tunnel twisting around the corner into darkness\n"""

	def modify_player(self, the_player):
		pass

class HallTunnel(MapTile):
	def __init__(self, x, y):
		super().__init__(x, y)

	def intro_text(self):
		if world.is_locked(self.x + 1, self.y):
			return """\nThe hallway stretches onward, passing a small vent glowing with light. The vent appears to be secured with hex screws\n"""
		else:
			return """\nThe vent lies removed and forgotten on the floor, the vent wide open\n"""

	def modify_player(self, the_player):
		pass

class ComputerLab(MobRoom):
	def __init__(self, x, y):
		super().__init__(x, y, enemies.ComputerY34(), items.ComputerNote())

	def intro_text(self):
		return """\nThe door swings open to reveal a small computer lab, empty but for a moniter dimly flickering in a corner. A note is stuck to the upper left hand corner\n"""

	def available_actions(self, the_player):
		moves = self.adjacent_moves()
		moves.append(actions.ViewInventory())
		moves.append(actions.Use(tile=self))
		moves.append(actions.Quit())
		moves.append(actions.Talk(tile=self, enemy=self.enemy))

		if len(self.item) != 0:
			moves.append(actions.Grab(tile=self))

		if the_player.fsm:
			moves.extend(self.devcommands(the_player))

		return moves
	
class Lab(MapTile):
	def __init__(self, x, y):
		super().__init__(x, y)

	def intro_text(self):
		return """\nThe floor crunches with broken glass under your feet. Strewn about are papers obscured and forgotten. This place was once bustling, but now there is nothing\n"""


class LabLoot1(GrabLootRoom):
	def __init__(self, x, y):
		super().__init__(x, y, items.Scalpel())

	def intro_text(self):
		if len(self.item) != 0:
			return """\nThe desolation continues, but it appears there is a small scapel on the ground\n"""

		else:
			return """\nThere doesn't appear to be anything useful here anymore\n"""

	def available_actions(self, the_player):
		moves = self.adjacent_moves()
		moves.append(actions.ViewInventory())
		moves.append(actions.Use(tile=self))
		moves.append(actions.Quit())

		if len(self.item) != 0:
			moves.append(actions.Grab(tile=self))

		if the_player.fsm:
			moves.extend(self.devcommands(the_player))

		return moves


class LabLoot2(GrabLootRoom):
	def __init__(self, x, y):
		super().__init__(x, y, items.HexDriver())

	def intro_text(self):
		if len(self.item) != 0:
			return """\nBuried under an upturned table is a small toolbox. Upon further examination there appears to be a small screwdriver in it\n"""

		else:
			return """\nThere doesn't appear to be anything useful here anymore\n"""

	def available_actions(self, the_player):
		moves = self.adjacent_moves()
		moves.append(actions.ViewInventory())
		moves.append(actions.Use(tile=self))
		moves.append(actions.Quit())

		if len(self.item) != 0:
			moves.append(actions.Grab(tile=self))

		if the_player.fsm:
			moves.extend(self.devcommands(the_player))

		return moves

class TunnelLoot(GrabLootRoom):
	def __init__(self, x, y):
		super().__init__(x, y, items.BrassKnuckles())

	def intro_text(self):
		if len(self.item) != 0:
			return """\nThere appears to be a pair of brass knuckles burried in the dirt. Nobody seems to be interesting in them\n"""

		else:
			return """\nThe tunnel appears the same as always, save for a bit of loose dirt on the ground\n"""

	def available_actions(self, the_player):
		moves = self.adjacent_moves()
		moves.append(actions.ViewInventory())
		moves.append(actions.Use(tile=self))
		moves.append(actions.Quit())

		if len(self.item) != 0:
			moves.append(actions.Grab(tile=self))

		if the_player.fsm:
			moves.extend(self.devcommands(the_player))

		return moves

class FinnAaronRoom(GrabLootRoom):
	#dev only room
	def __init__(self, x, y):
		super().__init__(x, y, items.HexDriver())

	def intro_text(self):
		return """\nEat pant\n"""
	def available_actions(self, the_player):
		moves = self.adjacent_moves()
		moves.append(actions.ViewInventory())
		moves.append(actions.Use(tile=self))
		moves.append(actions.Quit())

		if len(self.item) != 0:
			moves.append(actions.Grab(tile=self))

		if the_player.fsm:
			moves.extend(self.devcommands(the_player))

		return moves


class CaveEntrance(MapTile):
	def __init__(self, x, y):
		super().__init__(x, y)

	def intro_text(self):
		return """\nYou find yourself at the mouth of a cave\n"""

	def modify_player(self, the_player):
		pass

class Cave(MapTile):
	def __init__(self, x, y):
		super().__init__(x, y)

	def intro_text(self):
		return """\nThe walls of the cave drip and no end can be seen in the darkness\n"""

	def modify_player(self, the_player):
		pass


class ExitDoor(MapTile):
	def __init__(self, x, y):
		self.locked = True
		super().__init__(x, y)

	def intro_text(self):
		return """\nThe door lays open with a small elevator waiting patiantly\n"""

	def modify_player(self, the_player):
		pass

class Garden(MapTile):
	def __init__(self, x, y):
		super().__init__(x, y)

	def intro_text(self):
		return """\nFertile dirt lies around you, light water sprinkles from pipes above. Nothing to eat in here however\n"""

	def modify_player(self, the_player):
		pass

class Hospital(MapTile):
	def __init__(self, x, y):
		super().__init__(x, y)

	def intro_text(self):
		return """\nYou seem to have found yourself in a place of medicine. There might be something here to help heal you\n"""

	def modify_player(self, the_player):
		pass


class HospitalLoot(GrabLootRoom):
	def __init__(self, x, y):
		super().__init__(x, y, items.HealthPack())

	def intro_text(self):
		return """\nA small box with a red cross sit on the table, bearing the inscription "First Aid Kit" There is not much else here\n"""

	def available_actions(self, the_player):
		moves = self.adjacent_moves()
		moves.append(actions.ViewInventory())
		moves.append(actions.Use(tile=self))
		moves.append(actions.Quit())

		if len(self.item) != 0:
			moves.append(actions.Grab(tile=self))

		if the_player.fsm:
			moves.extend(self.devcommands(the_player))

		return moves

class CaveLoot(GrabLootRoom):
	def __init__(self, x, y):
		super().__init__(x, y, items.Diamond(), items.Pickaxe())

	def intro_text(self, x, y):
		return """\nA small glittering object sits in the corner, next to a hefty pickaxe\n"""

	def available_actions(self, the_player):
		moves = self.adjacent_moves()
		moves.append(actions.ViewInventory())
		moves.append(actions.Use(tile=self))
		moves.append(actions.Quit())

		if len(self.item) != 0:
			moves.append(actions.Grab(tile=self))

		if the_player.fsm:
			moves.extend(self.devcommands(the_player))

		return moves

class GardenLoot(GrabLootRoom):
	def __init__(self, x, y):
		super().__init__(x, y, items.Carrot(), items.Potato())

	def intro_text(self):
		return """\nA carrot and potato lie forgotten on a bench next to gardening equipment\n"""

	def available_actions(self, the_player):
		moves = self.adjacent_moves()
		moves.append(actions.ViewInventory())
		moves.append(actions.Use(tile=self))
		moves.append(actions.Quit())

		if len(self.item) != 0:
			moves.append(actions.Grab(tile=self))

		if the_player.fsm:
			moves.extend(self.devcommands(the_player))

		return moves


class FactionGuard(MobRoom):
        def __init__(self, x, y):
                super().__init__(x, y, enemies.FactionGuardMob())

        def intro_text(self):
                if self.enemy.is_alive():
                        return """\nA guard bars the way\n"""
                else:
                        return """\nA guard lies on the ground, his blood splattered on the floor\n"""


class FactionEnemy(MobRoom):
        def __init__(self, x, y):
                super().__init__(x, y, enemies.FactionEnemyMob())

        def intro_text(self):
                if self.enemy.is_alive():
                        return """\nA large guard  bars the way\n"""
                else:
                        return """\nA large guard lies on the ground, his blood splattered on the floor\n"""

class LabLoot(GrabLootRoom):
	def __init__(self, x, y):
		super().__init__(x, y, items.HexDriver())

	def intro_text(self):
		return """\nThere is a small screwdriver sitting on a bench\n"""

	def available_moves(self, the_player):
		moves = self.adjacent_moves()
		moves.append(actions.ViewInventory())
		moves.append(actions.Use(tile=self))
		moves.append(actions.Quit())

		if len(self.item) != 0:
			moves.append(actions.Grab(tile=self))

		if the_player.fsm:
			moves.extend(self.devcommands(the_player))

		return moves
