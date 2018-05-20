class Enemy:
	def __init__(self, name, hp, damage):
		self.name = name
		self.hp = hp
		self.damage = damage

	def is_alive(self):
		return self.hp > 0
	
	def talk(self):
		pass

class Guard(Enemy):
	def __init__(self):
		super().__init__(name='Guard', hp=10, damage=5)


class LabTech(Enemy):
	def __init__(self):
		super().__init__(name='Lab Technician', hp=5, damage=2)

