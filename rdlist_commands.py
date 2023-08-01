
import os
import subprocess
import json
import time
import user_commands
import room_commands
import report_commands
import hardcoded_variables

def sync_rdlist():
	rdlist_dir = "./rdlist"
	os.makedirs(rdlist_dir, exist_ok=True)
	# Check if the rdlist repo has already been cloned
	if os.path.isdir("./rdlist/.git"):
		print("\nrdlist repo already cloned...")
		os.chdir("./rdlist/")
		# Update git remote references and get status
		subprocess.run(["git", "remote", "update"], check=True)
		status = subprocess.run(["git", "status", "-uno"], stdout=subprocess.PIPE, check=True)
		os.chdir("..")

		# If "Your branch is up to date" is not in the status, then there are changes to pull
		if "Your branch is up to date" not in status.stdout.decode():
			print("Pulling latest changes from rdlist repo...")
			os.chdir("./rdlist/")
			# Avoid pulling changes if testing mode is enabled
			if hardcoded_variables.testing_mode == False:
				subprocess.run(["git", "pull"], check=True)
			os.chdir("..")
		else:
			print("rdlist repo is up-to-date, no need to pull changes.")

	else:
		print("Cloning rdlist repo...")
		subprocess.run(["git", "clone", "ssh://gitea@code.glowers.club:1488/loj/rdlist.git"], check=True)

# A function to return the rdlist tags associated with a room
def get_rdlist_tags(preset_internal_ID):
	if preset_internal_ID == '':
		internal_ID = input("\nEnter the internal id of the room you wish to query (Example: !OLkDvaYjpNrvmwnwdj:matrix.org): ")
	elif preset_internal_ID != '':
		internal_ID = preset_internal_ID

	# Git clone the rdlist repo to ./rdlist/
	sync_rdlist()

	# Load the summaries JSON file
	summaries_path = os.path.join("rdlist", "dist", "summaries.json")
	with open(summaries_path, 'r') as file:
		data = json.load(file)

	# Find the room with the given id and return its tags
	for item in data:
		if 'room' in item and 'room_id' in item['room'] and item['room']['room_id'] == internal_ID:
			if 'report_info' in item and 'tags' in item['report_info']:
				return item['report_info']['tags']

	return None

def block_all_rooms_with_rdlist_tags(rdlist_use_recommended,preset_user_ID,preset_new_room_name,preset_message):
	# Git clone the rdlist repo to ./rdlist/
	sync_rdlist()

	if rdlist_use_recommended == True:
		# Use the hardcoded recommended tags
		blocked_tags = hardcoded_variables.rdlist_recommended_tags
		print(f"\nUsing recommended rdlist tags. Rooms matching the following tags will be purged and/or blocked:\n{hardcoded_variables.rdlist_recommended_tags}")

	elif rdlist_use_recommended == False:
		# After the git repo has been cloned/pulled, open the file and read it into a string
		with open(os.path.join("rdlist", "lib", "docs", "tags.md"), 'r') as file:
			data = file.readlines()

		# Print ./rdlist/lib/docs/tags.md README file for the user
		print("\nPrinting details about the current tags in rdlist:\n")
		for line in data:
			print(line, end='')  # Print the contents of the file

		# Take input from the user and convert it to a list
		print("\nPlease enter a space seperated list of tags you wish to block:\n")
		blocked_tags = input().split()
		print('')

	# Load the summaries JSON file
	summaries_path = os.path.join("rdlist", "dist", "summaries.json")
	with open(summaries_path, 'r') as file:
		data = json.load(file)

	# Create an empty dictionary to store all the room_ids for each user
	all_local_users = dict()
	all_remote_users = dict()

	# Create a set to store all room_ids
	all_room_ids = set()

	# Create a dictionary to store the tags for each room
	room_tags = dict()

	# Iterate over blocked_tags
	for tag in blocked_tags:
		# Filter the data to keep only the entries where the tag appears in the "tags" list
		filtered_data = [item for item in data if 'report_info' in item and 'tags' in item['report_info'] and tag in item['report_info']['tags']]

		# Store the tags for each room
		for item in filtered_data:
			if 'room' in item and 'room_id' in item['room']:
				room_id = item['room']['room_id']
				all_room_ids.add(room_id) # add the room_id to the set
				if room_id not in room_tags:
					room_tags[room_id] = set()
				room_tags[room_id].update(item['report_info']['tags'])

		# Extract the room_ids
		room_ids = [item['room']['room_id'] for item in filtered_data if 'room' in item and 'room_id' in item['room']]

		# Examine these room_ids for local and remote users
		for room_id in room_ids:
			joined_members = room_commands.get_room_members(room_id)

			# For each user, add the room_id and tags to the dictionary
			for user_id in joined_members:
				if user_id.endswith(hardcoded_variables.base_url):
					if user_id not in all_local_users:
						all_local_users[user_id] = dict()
					all_local_users[user_id][room_id] = list(room_tags.get(room_id, []))
				else:
					if user_id not in all_remote_users:
						all_remote_users[user_id] = dict()
					all_remote_users[user_id][room_id] = list(room_tags.get(room_id, []))

	all_room_ids = list(all_room_ids) # convert the set to a list

	#print(f"all_local_users: {all_local_users}")
	#print(f"all_remote_users: {all_remote_users}")
	#print(f"all_room_ids: {all_room_ids}")

	# If there's at least 1 local user detected, ask the admin if they want to generate a user report for every user found in rdlist rooms
	if len(all_local_users) > 0:
		print(f"\nWARNING! The following local users are current members of rooms tagged in rdlist: {list(all_local_users.keys())}")
		generate_user_report_confirmation = input("\nDo you want to generate a user report file for each of these users? y/n? ")
		if generate_user_report_confirmation.lower() in ['y', 'yes', 'Y', 'Yes']:
			for user_id in all_local_users:
				# Generate report_dict for each user
				report_content = report_commands.generate_rdlist_report_summary(all_local_users[user_id], user_id)
				report_commands.generate_user_report(user_id, report_content)
		elif generate_user_report_confirmation.lower() in ['n', 'no', 'N', 'No']:
			print("\nSkipping user report generation...\n")
	elif len(all_local_users) == 0:
		print(f"\nNo local users were found in rdlist rooms.")

	# Todo: Add Incident Report section

	# Ask the user if they wish to block and purge all these rooms, then collect shutdown parameters
	if preset_user_ID == '':
		user_ID = input("\nPlease enter the local username that will create a 'muted violation room' for your users (Example: michael): ")
	elif preset_user_ID != '':
		user_ID = preset_user_ID
	if preset_new_room_name == '':
		new_room_name = input("\nPlease enter the room name of the muted violation room your users will be sent to: ")
	elif preset_new_room_name != '':
		new_room_name = preset_new_room_name
	if preset_message == '':
		message = input("\nPlease enter the shutdown message that will be displayed to users: ")
	elif preset_message != '':
		message = preset_message

	# Ask the user if they wish to block and purge all these rooms
	shutdown_confirmation = input("\nNumber of rdlist rooms being shutdown: " + str(len(all_room_ids)) + "\n\nAre you sure you want to block/shutdown these rooms? y/n? ")

	total_list_kicked_users = []
	num_rooms_blocked = 0
	num_rooms_purged = 0

	if shutdown_confirmation.lower() in ['y', 'yes', 'Y', 'Yes']:
		# Ask the user if they wish to shadow ban all local users in these rooms
		shadow_ban_confirmation = input("\nDo you want to also shadow ban all your local users in these rooms before performing these shutdowns? (This is recommended as it prevents them from alerting others about these mass shutdown.) y/n? ")
		# Perform shadow bans if admin confirms
		if shadow_ban_confirmation in ['y', 'yes', 'Y', 'Yes']:
			for user in all_local_users:
				print(f"\nShadow banning user: {user}")
				user_commands.shadow_ban_account(user)
		for room_id in all_room_ids:
			blocked_status = room_commands.get_block_status(room_id)
			#print(f"\nroom_details_dict: {room_details_dict}")
			#print(f"\nblock_status: {blocked_status}")
			# If room is already blocked, skip it
			if blocked_status == False:
				# Examine if unblocked room is known, if not block it
				room_details_dict = room_commands.get_room_details(room_id)
				if "Room not found" in room_details_dict.get('error', ''):
					print(f"\n\nBlocking unknown room: {room_id}")
					room_commands.set_block_status(room_id, True)
					num_rooms_blocked += 1
				# If unblocked room is known, perform a shutdown of the room
				else:
					print(f"\n\nShutting down known room: {room_id}")
					list_kicked_users = room_commands.shutdown_room(room_id, user_ID, new_room_name, message, True, True)
					num_rooms_purged += 1
					total_list_kicked_users.extend(list_kicked_users)
				if hardcoded_variables.testing_mode == True:
					time.sleep(5)
			elif blocked_status == True:
				print(f"\n\nSkipping already blocked room: {room_id}")
				if hardcoded_variables.testing_mode == True:
					time.sleep(5)
	elif shutdown_confirmation.lower() in ['n', 'no', 'N', 'No']:
		print("\nSkipping blocking/shutdown of rooms...\n")
		return
	else:
		print("\nInvalid input, skipping these files...\n")
		return

	# Deduplicate the list of all kicked users
	total_list_kicked_users = list(set(total_list_kicked_users))
	
	# Return the list of all kicked users
	return num_rooms_blocked, num_rooms_purged, total_list_kicked_users

def block_recommended_rdlist_tags():
	# Print warning if testing mode is enabled
	if hardcoded_variables.testing_mode == True:
		print("\nWARNING! Testing mode is enabled, this will reduce the amount of data generated in reports and greatly slow down rdlist blocking!\n")

	# Check if user account already exists
	account_query = user_commands.query_account(hardcoded_variables.rdlist_bot_username)

	# If user is not found, create it
	if 'User not found' in account_query:
		# Create user account
		user_commands.create_account(hardcoded_variables.rdlist_bot_username, hardcoded_variables.rdlist_bot_password)
	else:
		print(f"@{hardcoded_variables.rdlist_bot_username}:{hardcoded_variables.base_url} account already exists. Resetting account password.\n")
		user_commands.reset_password(hardcoded_variables.rdlist_bot_username, hardcoded_variables.rdlist_bot_password)

	# Define default valies for shutdown_room()
	preset_new_room_name = 'POLICY VIOLATION'
	preset_message = 'THIS ROOM VIOLATES SERVER POLICIES'

	# Block all rooms with recommended tag set
	num_rooms_blocked, num_rooms_purged, total_list_kicked_users = block_all_rooms_with_rdlist_tags(True, hardcoded_variables.rdlist_bot_username, preset_new_room_name, preset_message)

	# Print user login details
	print("\n\nRoom shutdowns completed!\n\nUser login details for your moderator account:\n")
	print("Username: " + hardcoded_variables.rdlist_bot_username)
	print("Password: " + hardcoded_variables.rdlist_bot_password)

	# Print statistics for the admin
	print(f"\nPrint rdlist statistics:")
	print(f"\nNumber of rooms blocked: {num_rooms_blocked}")
	print(f"Number of rooms purged: {num_rooms_purged}")
	print(f"Number of local users located in rdlist rooms and kicked: {len(total_list_kicked_users)}")
	print(f"\nThe following users were current members of rooms tagged in rdlist: {total_list_kicked_users}")

	# Ask admin if they want to deactivate all the accounts that were kicked from rdlist rooms
	deactivate_confirmation = input("\nDo you want to also deactivate all these accounts that were kicked from rdlist rooms? y/n? ")
	if deactivate_confirmation.lower() in ['y', 'yes', 'Y', 'Yes']:
		for user_id in total_list_kicked_users:
			user_commands.deactivate_account(user_id)
		print(f"\nThese accounts have been deactivated.")
	elif deactivate_confirmation.lower() in ['n', 'no', 'N', 'No']:
		print("\nSkipping account deactivations...\n")
