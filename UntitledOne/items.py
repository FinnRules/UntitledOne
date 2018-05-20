
class Item():
	def __init__(self, name, description, value):
		self.name = name
		self.description = description
		self.value = value

	def __str__(self):
		return "{}\n=====\n{}\nValue: {}\n".format(self.name, self.description, self.value)

	def use_item(self):
		print("{} doesn't seem to do anything".format(self.name))

class Weapon(Item):
	def __init__(self, name, description, value, damage):
		self.damage = damage
		super().__init__(name, description, value)

	def __str__(self):
		return "{}\n====\n{}\nValue: {}\nDamage: {}".format(self.name, self.description, self.value, self.damage)

	
#Items:
class Syringe(Weapon):
	def __init__(self):
		super().__init__(name="Syringe", description="Empty, but still sharp", value=2, damage=1)

class Cash(Item):
	def __init__(self, amt):
		self.amt = amt
		super().__init__(name="Cash", description="A pile of {} bills".format(str(self.amt)), value=self.amt)

class Scalpel(Weapon):
	def __init__(self):
		super().__init__(name="Scalpel", description="Small, but sharp", value=3, damage=3)

#Appears in StartingCloset
class StartingClosetPaper(Item):
	def __init__(self):
		super().__init__(name="Paper", description="A notice of some sort", value=1)

	def use_item(self):
		print("""\nRed Sector Closet Borrowing Sheet:\n3/5: Harry Allen\n3/6: Harry Allen\n3/7: Harry Allen\n3/8: Harry Allen\n3/9: Harry Al\n3/10: Harry Alfred<The rest of the sheet is obscurred with heavy pen scribbles""")

