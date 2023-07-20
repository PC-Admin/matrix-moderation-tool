
import os
import subprocess
import json
import random
import string
import time
import user_commands
import room_commands
import hardcoded_variables

#rdlist_bot_username = hardcoded_variables.rdlist_bot_username

def sync_rdlist():
    rdlist_dir = "./rdlist"
    os.makedirs(rdlist_dir, exist_ok=True)
    # Check if the rdlist repo has already been cloned
    if os.path.isdir("./rdlist/.git"):
        print("rdlist repo already cloned...")
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

def block_all_rooms_with_rdlist_tags(rdlist_use_recommended,preset_user_ID,preset_new_room_name,preset_message,preset_purge_choice,preset_block_choice):
	# Git clone the rdlist repo to ./rdlist/
	sync_rdlist()
	if rdlist_use_recommended == True:
		# Take input from the user and convert it to a list
		blocked_tags = rdlist_recommended_tags
		print("\nUsing recommended rdlist tags.\n")
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
	if preset_purge_choice == '':
		purge_choice = input("\nDo you want to purge the room? (This deletes all the room history from your database.) y/n? ")
	elif preset_purge_choice != '':
		purge_choice = preset_purge_choice
	if preset_block_choice == '':
		block_choice = input("\nDo you want to block the room? (This prevents your server users re-entering the room.) y/n? ")
	elif preset_block_choice != '':
		block_choice = preset_block_choice
	# Ask the user if they wish to block and purge all these rooms
	shutdown_confirmation = input("\nNumber of rooms being shutdown: " + str(len(all_room_ids)) + "\n\nAre you sure you want to shutdown these rooms? y/n? ")
	if shutdown_confirmation.lower() in ['y', 'yes', 'Y', 'Yes']:
		for room_id in all_room_ids:
			room_commands.shutdown_room(room_id, user_ID, new_room_name, message, purge_choice, block_choice)
			time.sleep(5)
	elif shutdown_confirmation.lower() in ['n', 'no', 'N', 'No']:
		print("\nSkipping these files...\n")
	else:
		print("\nInvalid input, skipping these files...\n")

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
		print("Account already exists.")
		user_commands.reset_password(hardcoded_variables.rdlist_bot_username, preset_password)
	# Promote bot user to server admin
	user_commands.set_user_server_admin(hardcoded_variables.rdlist_bot_username)
	# Define default valies for shutdown_room()
	preset_new_room_name = 'POLICY VIOLATION'
	preset_message = 'THIS ROOM VIOLATES SERVER POLICIES'
	preset_purge_choice = 'y'
	preset_block_choice = 'y'
	# Block all rooms with recommended tag set
	block_all_rooms_with_rdlist_tags(True, hardcoded_variables.rdlist_bot_username, preset_new_room_name, preset_message, preset_purge_choice, preset_block_choice)
	# Print user login details
	print("\nUser login details:\n")
	print("Username: " + hardcoded_variables.rdlist_bot_username)
	print("Password: " + preset_password)
