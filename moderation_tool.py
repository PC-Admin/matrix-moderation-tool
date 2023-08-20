
#!/bin/env python3

import os
import json

# Check if ./hardcoded_variables.py file exists
if not os.path.exists("./hardcoded_variables.py"):
	print("ERROR: The file './hardcoded_variables.py' does not exist. It must be configured before using this script.")
	exit()

import user_commands
import room_commands
import server_commands
import ipinfo_commands
import rdlist_commands
import report_commands
import bot_commands

# Importing the module only after verifying its existence
import hardcoded_variables

# If it does exist... check if the variables are configured:

# check if homeserver url is the default

if hardcoded_variables.homeserver_url == "matrix.example.org":
	print("ERROR: homeserver_url not configured, please configure your './hardcoded_variables.py' file!")
	exit()

# check if base url is the default

if hardcoded_variables.base_url == "example.org":
	print("ERROR: base_url not configured, please configure your './hardcoded_variables.py' file!")
	exit()

# check if access token is the default

length_access_token = len(hardcoded_variables.access_token)

if length_access_token == 0:
	print("ERROR: access_token not configured, please configure your './hardcoded_variables.py' file!")
	exit()

# loop menu for various moderation actions

pass_token = False
while pass_token == False:
	print("\n##########################")
	print("# MATRIX MODERATION TOOL #")
	print("##########################")
	print("\nA tool for making common Synapse moderation tasks easier. Created by @PC-Admin.")
	print("\n----------------------------------------------")
	print("\n#### User Account Commands ####\t\t\t#### Room Commands ####")
	print("1) Deactivate a user account.\t\t\t50) List details of a room.")
	print("2) Deactivate multiple user accounts.\t\t51) List the members of a room.")
	print("3) Create a user account.\t\t\t52) Export the state events of a room.")
	print("4) Create multiple user accounts.\t\t53) Export the state events of multiple rooms.")
	print("5) Reset a users password.\t\t\t54) List rooms in public directory.")
	print("6) Whois user account.\t\t\t\t55) Remove a room from the public directory.")
	print("7) Whois multiple user accounts.\t\t56) Remove multiple rooms from the public directory.")
	print("8) Query user account.\t\t\t\t57) Redact a room event.")
	print("9) Query multiple user accounts.\t\t58) List/Download all media in a room.")
	print("10) List room memberships of user.\t\t59) Download media from multiple rooms.")
	print("11) Promote a user to server admin.\t\t60) Quarantine all media in a room.")
	print("12) List all user accounts.\t\t\t61) Shutdown a room.")
	print("13) Quarantine all media a users uploaded.\t62) Shutdown multiple rooms.")
	print("14) Collect account data.\t\t\t63) Delete a room.")
	print("15) List account pushers.\t\t\t64) Delete multiple rooms.")
	print("16) Get rate limit of a user account.\t\t65) Purge the event history of a room to a specific timestamp.")
	print("17) Set rate limit of a user account.\t\t66) Purge the event history of multiple rooms to a specific timestamp.")
	print("18) Delete rate limit of a user account.\t67) Get blocked status for room.")
	print("19) Check if user account exists.\t\t68) Block a room.")
	print("20) Shadow ban a user.\t\t\t\t69) Unblock a room.")
	print("21) Find a user by their 3PID.")
	print("\n#### Server Commands ####\t\t\t\t\t#### ipinfo.io ####")
	print("100) Delete and block a specific media.\t\t\t\t140) Analyse a users country of origin.")
	print("101) Purge remote media repository up to a certain date.\t141) Analyse multiple users country of origin.")
	print("102) Prepare database for copying events of multiple rooms.")
	print("103) Show last 10 reported events.\t\t\t\t#### Report Generation ####")
	print("104) Get all reported events.\t\t\t\t\t150) Generate user report.")
	print("105) Get details of a reported event.\t\t\t\t151) Lookup homeserver admin contact details.")
	print("\t\t\t\t\t\t\t\t152) Send a test email (to yourself).")
	print("#### rdlist - General ####\t\t\t\t\t153) Send a test Matrix message (to yourself).")
	print("120) Block all rooms with specific rdlist tags.\t\t\t154) Send test incident reports (to yourself).")
	print("121) Get rdlist tags for a room.")
	print("\n#### rdlist - Recommended Tags ####")
	print("For rdlist rooms with recommended tags, the following actions are available:")
	print("130) Collect User Reports on local accounts in rdlist rooms.")
	print("131) Send Incident Reports on remote accounts in rdlist rooms.")
	print("132) Block/Purge all rdlist rooms.")
	print("\nPlease enter a number from the above menu, or enter 'q' or 'e' to exit.\n")
	menu_input = input()
	if menu_input == "1":
		erase_data = input("Deactivating account. Do you want to also erase the user's data? (y/n) ")
		if erase_data in ["y", "Y", "yes", "Yes", "YES"]:
			user_commands.deactivate_account('',True)
		elif erase_data in ["n", "N", "no", "No", "NO"]:
			user_commands.deactivate_account('')
		else:
			print("\nIncorrect input detected, please select 'y' or 'n'!\n")
	elif menu_input == "2":
		user_commands.deactivate_multiple_accounts()
	elif menu_input == "3":
		user_commands.create_account('','')
	elif menu_input == "4":
		user_commands.create_multiple_accounts()
	elif menu_input == "5":
		user_commands.reset_password('','')
	elif menu_input == "6":
		whois_account_dict = user_commands.whois_account('')
		print(json.dumps(whois_account_dict, indent=4, sort_keys=True))
	elif menu_input == "7":
		user_commands.whois_multiple_accounts()
	elif menu_input == "8":
		query_account_dict = user_commands.query_account('')
		print(json.dumps(query_account_dict, indent=4, sort_keys=True))
	elif menu_input == "9":
		user_commands.query_multiple_accounts()
	elif menu_input == "10":
		joined_rooms_dict = user_commands.list_joined_rooms('')
		print(json.dumps(joined_rooms_dict, indent=4, sort_keys=True))
	elif menu_input == "11":
		set_user_server_admin_dict = user_commands.set_user_server_admin('')
		print(json.dumps(set_user_server_admin_dict, indent=4, sort_keys=True))
	elif menu_input == "12":
		user_commands.list_accounts()
	elif menu_input == "13":
		user_commands.quarantine_users_media()
	elif menu_input == "14":
		account_data_dict = user_commands.collect_account_data('')
		print(json.dumps(account_data_dict, indent=4, sort_keys=True))
	elif menu_input == "15":
		user_commands.list_account_pushers('')
	elif menu_input == "16":
		user_commands.get_rate_limit()
	elif menu_input == "17":
		user_commands.set_rate_limit()
	elif menu_input == "18":
		user_commands.delete_rate_limit()
	elif menu_input == "19":
		user_account_exists = user_commands.check_user_account_exists('')
		if user_account_exists == True:
			print("\nUser account exists.\n")
		elif user_account_exists == False:
			print("\nUser account does not exist.\n")
	elif menu_input == "20":
		shadow_ban_dict = user_commands.shadow_ban_account('')
		print(json.dumps(shadow_ban_dict, indent=4, sort_keys=True))
	elif menu_input == "21":
		user_dict = user_commands.find_account_with_threepid()
		print(f"\n{json.dumps(user_dict, indent=4, sort_keys=True)}")
	elif menu_input == "50":
		room_details_dict = room_commands.get_room_details('')
		print(json.dumps(room_details_dict, indent=4, sort_keys=True))
	elif menu_input == "51":
		room_members_dict = room_commands.get_room_members('',False)
		print(json.dumps(room_members_dict, indent=4, sort_keys=True))
	elif menu_input == "52":
		room_commands.export_room_state('','',True)
	elif menu_input == "53":
		room_commands.export_multiple_room_states()
	elif menu_input == "54":
		room_commands.public_directory_rooms()
	elif menu_input == "55":
		room_commands.remove_room_from_directory('')
	elif menu_input == "56":
		room_commands.remove_multiple_rooms_from_directory()
	elif menu_input == "57":
		room_commands.redact_room_event()
	elif menu_input == "58":
		room_commands.list_and_download_media_in_room('','','','./')
	elif menu_input == "59":
		room_commands.download_media_from_multiple_rooms()
	elif menu_input == "60":
		room_commands.quarantine_media_in_room()
	elif menu_input == "61":
		room_commands.shutdown_room('','','','','','')
	elif menu_input == "62":
		room_commands.shutdown_multiple_rooms()
	elif menu_input == "63":
		room_commands.delete_room('')
	elif menu_input == "64":
		room_commands.delete_multiple_rooms()
	elif menu_input == "65":
		room_commands.purge_room_to_timestamp('','')
	elif menu_input == "66":
		room_commands.purge_multiple_rooms_to_timestamp()
	elif menu_input == "67":
		blocked_status = room_commands.get_block_status('')
		if blocked_status == True:
			print("\nRoom is blocked.\n")
		elif blocked_status == False:
			print("\nRoom is not blocked.\n")
		print(json.dumps(blocked_status, indent=4, sort_keys=True))
	elif menu_input == "68":
		room_commands.set_block_status('', True)
	elif menu_input == "69":
		room_commands.set_block_status('', False)
	elif menu_input == "100":
		server_commands.delete_block_media()
	elif menu_input == "101":
		server_commands.purge_remote_media_repo()
	elif menu_input == "102":
		server_commands.prepare_database_copy_of_multiple_rooms()
	elif menu_input == "103":
		reported_events = server_commands.get_reported_events(10)
		print(json.dumps(reported_events, indent=4, sort_keys=True))
	elif menu_input == "104":
		all_reported_events = server_commands.paginate_reported_events()  # Again assuming default values are set
		print(json.dumps(all_reported_events, indent=4, sort_keys=True))
	elif menu_input == "105":
		report_details = server_commands.get_event_report_details()
		print(json.dumps(report_details, indent=4, sort_keys=True))
	elif menu_input == "120":
		rdlist_commands.block_all_rooms_with_rdlist_tags(False,'','','')
	elif menu_input == "121":
		rdlist_tags = rdlist_commands.get_rdlist_tags('')
		print(json.dumps(rdlist_tags, indent=4, sort_keys=True))
	elif menu_input == "130":
		rdlist_commands.collect_user_reports_on_rdlist_accounts()
	elif menu_input == "131":
		rdlist_commands.send_incident_reports_on_rdlist_accounts()
	elif menu_input == "132":
		rdlist_commands.block_recommended_rdlist_tags()
	elif menu_input == "140":
		ipinfo_commands.analyse_account_ip('')
	elif menu_input == "141":
		ipinfo_commands.analyse_multiple_account_ips()
	elif menu_input == "150":
		report_commands.generate_user_report('','')
	elif menu_input == "151":
		admin_contact_dict, is_whois = report_commands.lookup_homeserver_admin('')
		print(f"\nAdmin contacts: {json.dumps(admin_contact_dict, indent=4, sort_keys=True)}\nWhois: {str(is_whois)}")
	elif menu_input == "152":
		report_commands.test_send_email()
	elif menu_input == "153":
		bot_commands.test_matrix_message()
	elif menu_input == "154":
		report_commands.test_send_incident_reports()
	elif menu_input == "q" or menu_input == "Q" or menu_input == "e" or menu_input == "E":
		print("\nExiting...\n")
		pass_token = True
	else:
		print("\nIncorrect input detected, please select a number from 1 to 154!\n")

