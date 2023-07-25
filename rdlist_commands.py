
import os
import subprocess
import json
import random
import string
import time
import user_commands
import room_commands
import report_commands
import hardcoded_variables

#rdlist_bot_username = hardcoded_variables.rdlist_bot_username

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
			subprocess.run(["git", "pull"], check=True)
			os.chdir("..")
		else:
			print("rdlist repo is up-to-date, no need to pull changes.")

	else:
		print("Cloning rdlist repo...")
		subprocess.run(["git", "clone", "ssh://gitea@code.glowers.club:1488/loj/rdlist.git"], check=True)

# def build_incident_report(users_list):
# 	# Git clone the rdlist repo to ./rdlist/
# 	sync_rdlist()

# 	# Load the summaries JSON file
# 	summaries_path = os.path.join("rdlist", "dist", "summaries.json")
# 	with open(summaries_path, 'r') as file:
# 		data = json.load(file)


# 	return incidents_dict

# 	# Example of the data structure we're trying to build/transform:
# 	# users_list = ["@billybob:matrix.org", "@johndoe:matrix.org", "@pedobear:perthchat.org", "@randomcreep:perthchat.org", "@fatweeb:grin.hu"]
# 	#
# 	# becomes:
# 	#
# 	# incidents_dict = {
# 	# 	f"@billybob:matrix.org": {
# 	# 		"!dummyid1:matrix.org": ["csam", "lolicon", "beastiality"],
# 	# 		"!dummyid2:matrix.org": ["csam", "anarchy"]
# 	# 	},
# 	# 	f"@johndoe:matrix.org": {
# 	# 		"!dummyid3:matrix.org": ["csam", "lolicon", "toddlercon"],
# 	# 		"!dummyid4:matrix.org": ["csam", "terrorism"]
# 	# 	},
# 	# 	f"@pedobear:perthchat.org": {
# 	# 		"!dummyid5:matrix.org": ["csam", "lolicon", "jailbait"],
# 	# 		"!dummyid6:matrix.org": ["csam", "hub_links"]
# 	# 	},
# 	# 	f"@randomcreep:perthchat.org": {
# 	# 		"!dummyid7:matrix.org": ["csam", "jailbait"],
# 	# 		"!dummyid8:matrix.org": ["csam", "pre_ban"]
# 	# 	},
# 	# 	f"@fatweeb:grin.hu": {
# 	# 		"!dummyid9:matrix.org": ["csam", "lolicon"],
# 	# 		"!dummyid10:matrix.org": ["csam", "degen"]
# 	# 	}
# 	# }

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

	# Create an empty list to store all the room_ids
	all_room_ids = []

	# Iterate over blocked_tags
	for tag in blocked_tags:
		# Filter the data to keep only the entries where the tag appears in the "tags" list
		filtered_data = [item for item in data if 'report_info' in item and 'tags' in item['report_info'] and tag in item['report_info']['tags']]
		# Extract the room_ids
		room_ids = [item['room']['room_id'] for item in filtered_data if 'room' in item and 'room_id' in item['room']]
		# Add the room_ids to the list of all room_ids
		all_room_ids.extend(room_ids)
		# If choosing specific tags, print the tag and corresponding room_ids
		if rdlist_use_recommended == False:
			# Print the tag and corresponding room_ids
			print(f"Tag: {tag}\nRoom IDs: {room_ids}\n")

	# Deduplicate the list of all room_ids
	all_room_ids = list(set(all_room_ids))

	# Examine these room_ids for local users
	all_local_users = []
	all_remote_users = []
	for room_id in all_room_ids:
		joined_local_members = room_commands.get_room_members(room_id, True)
		all_local_users.extend(joined_local_members)
		joined_remote_members = room_commands.get_room_members(room_id, False)
		all_remote_users.extend(joined_remote_members)

	# Deduplicate the list of all local users
	all_local_users = list(set(all_local_users))
	#print("all_local_users: " + str(all_local_users))

	# If there's at least 1 local user detected, ask the admin if they want to generate a user report for every user found in rdlist rooms
	if len(all_local_users) > 0:
		print(f"\nWARNING! The following local users are current members of rooms tagged in rdlist: {all_local_users}")
		generate_user_report_confirmation = input("\nDo you want to generate a user report file for each of these users? y/n? ")
		if generate_user_report_confirmation.lower() in ['y', 'yes', 'Y', 'Yes']:
			for user_id in all_local_users:
				report_commands.generate_user_report(user_id)
		elif generate_user_report_confirmation.lower() in ['n', 'no', 'N', 'No']:
			print("\nSkipping user report generation...\n")
	elif len(all_local_users) == 0:
		print(f"\nNo local users were found in rdlist rooms.")

	# Deduplicate the list of all remote users
	all_remote_users = list(set(all_remote_users))
	all_remote_users = [user for user in all_remote_users if user not in all_local_users]
	#print("all_remote_users: " + str(all_remote_users))

	# Ask the admin if they would like to mail off an incident report for every remote user found in rdlist rooms
	# if len(all_remote_users) > 0:
	# 	print(f"\nThe following remote users are current members of rooms tagged in rdlist: {all_remote_users}")
	# 	send_incident_report_confirmation = input("\nDo you want to send an incident report to the abuse email address for each of these users? y/n? ")
	# 	if send_incident_report_confirmation.lower() in ['y', 'yes', 'Y', 'Yes']:
	# 		build_incident_report(all_remote_users)
	# 		#for user_id in all_remote_users:
	# 		#	report_commands.send_incident_report(user_id)
	# 	elif send_incident_report_confirmation.lower() in ['n', 'no', 'N', 'No']:
	# 		print("\nSkipping incident report generation...\n")

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
	shutdown_confirmation = input("\nNumber of rdlist rooms being shutdown: " + str(len(all_room_ids)) + "\n\nAre you sure you want to shutdown these rooms? y/n? ")

	total_list_kicked_users = []
	num_rooms_blocked = 0

	#print(f"all_room_ids: {all_room_ids}")
	if shutdown_confirmation.lower() in ['y', 'yes', 'Y', 'Yes']:
		for room_id in all_room_ids:
			print(f"\n\nShutting down room: {room_id}")
			room_state_dict = room_commands.export_room_state(room_id, "", False)
			#print(f"\nroom_state_dict: {room_state_dict}")
			if "Room not found" in room_state_dict.get('error', ''):
				list_kicked_users = room_commands.shutdown_room(room_id, user_ID, new_room_name, message, False, True)
			else:
				list_kicked_users = room_commands.shutdown_room(room_id, user_ID, new_room_name, message, True, True)
			num_rooms_blocked += 1
			total_list_kicked_users.extend(list_kicked_users)
			time.sleep(5)
	elif shutdown_confirmation.lower() in ['n', 'no', 'N', 'No']:
		print("\nSkipping these files...\n")
		return
	else:
		print("\nInvalid input, skipping these files...\n")
		return

	# Deduplicate the list of all kicked users
	total_list_kicked_users = list(set(total_list_kicked_users))

	# Print the list of all kicked users
	print(f"\n\nList of all kicked users: {total_list_kicked_users}\n")
	
	# Return the list of all kicked users
	return num_rooms_blocked, total_list_kicked_users

def block_recommended_rdlist_tags():
	# Check if user account already exists
	account_query = user_commands.query_account(hardcoded_variables.rdlist_bot_username)

	# Generate random password
	preset_password = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(20))

	# If user is not found, create it
	if 'User not found' in account_query:
		# Create user account
		user_commands.create_account(hardcoded_variables.rdlist_bot_username, preset_password)
	else:
		print(f"\n@{hardcoded_variables.rdlist_bot_username}:{hardcoded_variables.base_url} account already exists. Resetting account password.")
		user_commands.reset_password(hardcoded_variables.rdlist_bot_username, preset_password)

	# Promote bot user to server admin
	print(f"\nEnsuring @{hardcoded_variables.rdlist_bot_username}:{hardcoded_variables.base_url} account is a server admin.")
	user_commands.set_user_server_admin(hardcoded_variables.rdlist_bot_username)

	# Define default valies for shutdown_room()
	preset_new_room_name = 'POLICY VIOLATION'
	preset_message = 'THIS ROOM VIOLATES SERVER POLICIES'

	# Block all rooms with recommended tag set
	num_rooms_blocked, total_list_kicked_users = block_all_rooms_with_rdlist_tags(True, hardcoded_variables.rdlist_bot_username, preset_new_room_name, preset_message)

	# Print user login details
	print("\n\nRoom shutdowns completed!\n\nUser login details for your moderator account:\n")
	print("Username: " + hardcoded_variables.rdlist_bot_username)
	print("Password: " + preset_password)

	# Print statistics for the admin
	print(f"\nPrint rdlist statistics:")
	print(f"\nNumber of rooms blocked/purged: {num_rooms_blocked}")
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