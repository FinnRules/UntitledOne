import random
import items, world

class Player():
	def __init__(self):
		self.inventory = [items.Cash(5), items.Syringe()] #creates array to store inv with starting items
		self.hp = 50
		self.location_x, self.location_y = world.starting_position
		self.victory = False

	def is_alive(self):
		return self.hp > 0 #returns true if the player is still alive

	def do_action(self, action, **kwargs):
		action_method = getattr(self, action.method.__name__)
		if action.method:
			action_method(**kwargs)

	def print_inventory(self):
		for item in self.inventory:
			print(item, '\n')

	def move(self, dx, dy):
		self.location_x += dx
		self.location_y += dy
		print(world.tile_exists(self.location_x, self.location_y).intro_text())

	def move_north(self):
		self.move(dx=0, dy=-1)

	def move_south(self):
		self.move(dx=0, dy=1)

	def move_east(self):
		self.move(dx=1, dy=0)

	def move_west(self):
		self.move(dx=-1, dy=0)

	def attack(self, enemy):
		best_weapon = None
		max_dmg = 0
		for i in self.inventory:
			if isinstance(i, items.Weapon):
				max_dmg = i.damage
				best_weapon = i

		print("You use {} against {}!".format(best_weapon.name, enemy.name))
		enemy.hp -= best_weapon.damage
		if not enemy.is_alive():
			print("You killed {}!".format(enemy.name))
		else:
			print("{} HP is {}.".format(enemy.name, enemy.hp))

	def flee(self, tile):
		available_moves = tile.adjacent_moves()
		r = random.randint(0, len(available_moves) - 1)
		self.do_action(available_moves[r])

	def grab(self, tile):
		if tile.item != None:
			self.inventory.append(tile.item)
			tile.item = None

	def use(self):
		check_item = input('Item to use? ')
		for i in range(len(self.inventory)):
			if check_item == self.inventory[i].name:
				self.inventory[i].use_item #add use item method to item
			
