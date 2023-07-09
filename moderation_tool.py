
# import subprocess
# import csv
# import time
# import json
# import random
# import string
import user_commands
import room_commands
import server_commands
import rdlist_commands
import hardcoded_variables

# check if homeserver url is hard coded, if not set it

if hardcoded_variables.homeserver_url == "matrix.example.org":
	homeserver_url = input("What is the URL of your server? Eg: matrix.example.org ")

# check if base url is hard coded, if not set it

if hardcoded_variables.base_url == "example.org":
	base_url = input("What is the URL of your server? Eg: example.org ")

# check if access token is hard coded, if not set it

length_access_token = len(hardcoded_variables.access_token)

if length_access_token == 0:
	access_token = input("Please enter access token for server admin account: ")

# loop menu for various moderation actions

pass_token = False
while pass_token == False:
	menu_input = input('\nPlease select one of the following options:\n#### User Account Commands ####\n1) Deactivate a user account.\n2) Deactivate multiple user accounts.\n3) Create a user account.\n4) Create multiple user accounts.\n5) Reset a users password.\n6) Whois user account.\n7) Whois multiple user accounts.\n8) List room memberships of user.\n9) Promote a user to server admin.\n10) List all user accounts.\n11) Quarantine all media a users uploaded.\n#### Room Commands ####\n12) List details of a room.\n13) Export the state events of a target room.\n14) List rooms in public directory.\n15) Remove a room from the public directory.\n16) Remove multiple rooms from the public directory.\n17) Redact a room event. (Like abusive avatars or display names.) \n18) List/Download all media in a room.\n19) Download media from multiple rooms.\n20) Quarantine all media in a room.\n21) Shutdown a room.\n22) Shutdown multiple rooms.\n23) Delete a room.\n24) Delete multiple rooms.\n25) Purge the event history of a room to a specific timestamp.\n26) Purge the event history of multiple rooms to a specific timestamp.\n#### Server Commands ####\n27) Delete and block a specific media. (Like an abusive avatar.) \n28) Purge remote media repository up to a certain date.\n29) Prepare database for copying events of multiple rooms.\n#### rdlist ####\n30) Block all rooms with specific rdlist tags.\n34) Block all rooms with recommended rdlist tags.\n(\'q\' or \'e\') Exit.\n\n')
	if menu_input == "1":
		user_commands.deactivate_account('')
	elif menu_input == "2":
		user_commands.deactivate_multiple_accounts()
	elif menu_input == "3":
		user_commands.create_account('','')
	elif menu_input == "4":
		user_commands.create_multiple_accounts()
	elif menu_input == "6":
		user_commands.reset_password('','')
	elif menu_input == "6":
		user_commands.whois_account('')
	elif menu_input == "7":
		user_commands.whois_multiple_accounts()
	elif menu_input == "8":
		user_commands.list_joined_rooms('')
	elif menu_input == "9":
		user_commands.set_user_server_admin('')
	elif menu_input == "10":
		user_commands.list_accounts()
	elif menu_input == "11":
		user_commands.quarantine_users_media()
	elif menu_input == "12":
		room_commands.list_room_details('')
	elif menu_input == "13":
		room_commands.export_room_state('')
	elif menu_input == "14":
		room_commands.list_directory_rooms()
	elif menu_input == "15":
		room_commands.remove_room_from_directory('')
	elif menu_input == "16":
		room_commands.remove_multiple_rooms_from_directory()
	elif menu_input == "17":
		room_commands.redact_room_event()
	elif menu_input == "18":
		room_commands.list_and_download_media_in_room('','','','./')
	elif menu_input == "19":
		room_commands.download_media_from_multiple_rooms()
	elif menu_input == "20":
		room_commands.quarantine_media_in_room()
	elif menu_input == "21":
		room_commands.shutdown_room('','','','','','')
	elif menu_input == "22":
		room_commands.shutdown_multiple_rooms()
	elif menu_input == "23":
		room_commands.delete_room('')
	elif menu_input == "24":
		room_commands.delete_multiple_rooms()
	elif menu_input == "25":
		room_commands.purge_room_to_timestamp('','')
	elif menu_input == "26":
		room_commands.purge_multiple_rooms_to_timestamp()
	elif menu_input == "27":
		server_commands.delete_block_media()
	elif menu_input == "28":
		server_commands.purge_remote_media_repo()
	elif menu_input == "29":
		server_commands.prepare_database_copy_of_multiple_rooms()
	elif menu_input == "30":
		rdlist_commands.block_all_rooms_with_rdlist_tags(False,'','','','','')
	elif menu_input == "34":
		rdlist_commands.block_recommended_rdlist_tags()
	elif menu_input == "q" or menu_input == "Q" or menu_input == "e" or menu_input == "E":
		print("\nExiting...\n")
		pass_token = True
	else:
		print("\nIncorrect input detected, please select a number from 1 to 34!\n")

