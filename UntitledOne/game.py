import world
from player import Player

def play():
	world.load_tiles()
	player = Player() #creates player as an object of the Player class
	room = world.tile_exists(player.location_x, player.location_y)
	print(room.intro_text())
	while player.is_alive() and not player.victory:
		room = world.tile_exists(player.location_x, player.location_y)
		room.modify_player(player) #modifies the player based on the room
		if player.is_alive() and not player.victory: #checks to see that player is not dead to room actions
			print("Choose an action:\n")
			available_actions = room.available_actions()
			for action in available_actions:
				print(action) #lists possible actions to player
			action_input = input('Action: ') #takes action input from player
			for action in available_actions:
				if action_input == action.hotkey:
					player.do_action(action, **action.kwargs)
					break

if __name__ == "__main__":
	play()

