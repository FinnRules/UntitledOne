class Enemy:
	def __init__(self, name, hp, damage):
		self.name = name
		self.hp = hp
		self.damage = damage
		self.talknum = 0
		self.aggro = False

	def is_alive(self):
		return self.hp > 0
	
	def talk(self):
		print("Not much for words")

class Guard(Enemy):
	def __init__(self):
		super().__init__(name='Guard', hp=10, damage=5)


class LabTech(Enemy):
	def __init__(self):
		super().__init__(name='Lab Technician', hp=5, damage=2)

class TunnelDweller(Enemy):
	def __init__(self):
		super().__init__(name='Tunnel Dweller', hp=5, damage=3)

	def talk(self):
		self.dialog = ["\nWho are you? Do you mean to hurt us?\n", "\nIn that case you are welcome, but disturb nothing\n"]
		self.fightwords = ["\nWe will defend the tunnel at all costs!\n"]

		print(self.dialog[0])
		response = input('y/n: ')
		if response != 'n':
			print(self.fightwords)
			self.aggro = True
			return
		print(self.dialog[1])
