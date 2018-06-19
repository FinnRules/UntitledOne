import world
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
		print("\nNot much for words\n")

class Guard(Enemy):
	def __init__(self):
		super().__init__(name='Guard', hp=10, damage=5)
		self.aggro = True

class LabTech(Enemy):
	def __init__(self):
		super().__init__(name='Lab Technician', hp=5, damage=2)
		self.aggro = True

class TunnelDweller(Enemy):
	def __init__(self):
		super().__init__(name='Tunnel Dweller', hp=5, damage=3)

	def talk(self):
		self.dialog = ["\nTunnel Dweller: Who are you? Do you mean to hurt us?\n", "\nTunnel Dweller: In that case you are welcome, but disturb nothing\n"]
		self.fightwords = ["\nTunnel Dweller: We will defend the tunnel at all costs!\n"]
		if self.aggro != True:
			print(self.dialog[0])
			response = input('y/n: ')
			if response != 'n':
				print(self.fightwords[0])
				self.aggro = True
				return
			print(self.dialog[1])
			return

class ComputerY34(Enemy):
	def __init__(self):
		super().__init__(name='Computer', hp=10, damage=3)

	def talk(self):
		command = input("admin@minni ~ $ ")
		
		if command == "sudo python3 opendoors.py":
			sudo = input("[sudo] password for admin: ")
			if sudo == "minniadmin":
				#code to make exit possible
				world.unlock(2, 5, False) #placeholder | see world.py for details
				print("<Process complete>\n")
			else:
				print("Sorry, try again\n")
		
		elif command == "python3 opendoors.py":
				print("Permission denied: requires root level access\n")
		
		elif command == "ls":
			print("\nopendoors.py	employeelist.txt	data_jan-june.txt	towhomitconcerns.txt\n")

		elif command == "ls -a":
			print("\nopendoors.py	employeelist.txt	data_jan-june.txt	towhomitconcerns.txt	.securityconcerns.txt\n")

		elif command == "cat emloyeelist.txt":
			print("\n<text>\n")

		elif command == "cat data_jan-june.txt":
			print("\n<text>\n")

		elif command == "cat towhomconcerns.txt":
			print("\n<text>\n")

		elif command == "cat .securityconcerns.txt":
			print("\n<text>\n")

		else:
			print("\n" + command + ": command not found\n")

class FactionGuardMob(Enemy):
	def __init__(self):
		super().__init__(name='Faction Guard', hp=25, damage=5)
		self.aggro = True

class FactionEnemyMob(Enemy):
	def __init__(self):
		super().__init__(name='Faction Enemy', hp=16, damage=3)
		self.aggro = True

