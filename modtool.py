
# modtool.py
# an easy moderation tool for matrix/synapse
#
# created by @michael:perthchat.org
#
# This work is published under the MIT license, for more information on this license see here: https://opensource.org/license/mit/
#
# To do:
# 1) Add https://github.com/matrix-org/synapse/blob/master/docs/admin_api/delete_group.md
# 2) Make the menu prettier!
# 3) Add reporting functions for users
# 4) Add reporting functions for rooms
# 5) Add a function to extract a users email
# 6) Do room shutdowns in parallel?
# 7) Add more automated rdlist function with sane defaults - DONE

import subprocess
import csv
import time
import os
import json
import random
import string

###########################################################################
# These values can be hard coded for easier usage:                        #
homeserver_url = "matrix.example.org"
base_url = "example.org"
access_token = ""
# rdlist specific
rdlist_bot_username = "mod_team"
rdlist_recommended_tags = ['hub_room_links', 'preban', 'degen_misc', 'beastiality', 'degen_porn', 'gore', 'hub_room_trade', 'snuff', 'degen_larp', 'hub_room_sussy', 'bot_spam cfm', '3d_loli', 'jailbait', 'bot_porn', 'toddlercon', 'loli', 'csam', 'tfm', 'abandoned', 'degen_meet', 'stylized_3d_loli']
###########################################################################

def parse_username(username):
	tail_end = ':' + base_url
	username = username.replace('@','')
	username = username.replace(tail_end,'')
	return username

def deactivate_account(preset_username):
	if len(preset_username) == 0:
		username = input("\nPlease enter the username to deactivate: ")
		username = parse_username(username)
	else:
		username = parse_username(preset_username)
	command_string = "curl -X POST -H \"Authorization: Bearer " + access_token + "\" 'https://" + homeserver_url + "/_synapse/admin/v1/deactivate/@" + username + ":" + base_url + "' --data '{\"erase\": true}'"
	print("\n" + command_string + "\n")
	process = subprocess.run([command_string], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
	output = process.stdout
	print(output)

# Example:
# $ curl -X POST -H "Authorization: Bearer ACCESS_TOKEN" "https://matrix.perthchat.org/_synapse/admin/v1/deactivate/@billybob:perthchat.org" --data '{"erase": true}'

def reset_password(preset_username,preset_password):
	if len(preset_username) == 0 and len(preset_password) == 0:
		username = input("\nPlease enter the username for the password reset: ")
		password = input("Please enter the password to set: ")
	else:
		username = parse_username(preset_username)
		password = preset_password
	username = parse_username(username)
	command_string = "curl -X POST -H 'Content-Type: application/json' -d '{\"new_password\": \"" + password + "\", \"logout_devices\": true}' https://" + homeserver_url + "/_synapse/admin/v1/reset_password/@" + username + ":" + base_url + "?access_token=" + access_token
	print("\n" + command_string + "\n")
	process = subprocess.run([command_string], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
	output = process.stdout
	print(output)
	return output

# Example:
# $ curl -X POST -H 'Content-Type: application/json' -d '{"new_password": "dogpoo", "logout_devices": true}' https://matrix.perthchat.org/_synapse/admin/v1/reset_password/@dogpoo:perthchat.org?access_token=ACCESS_TOKEN

def set_user_server_admin(preset_username):
	if len(preset_username) == 0:
		# tried setting 'admin: false' here but it failed and promoted the user instead!
		print("\nBe aware that you need to set at least 1 user to server admin already by editing the database in order to use this command. See https://github.com/PC-Admin/PC-Admins-Synapse-Moderation-Tool/blob/master/README.md for details on how to do this.")
		username = input("\nPlease enter the username you want to promote to server admin: ")
		username = parse_username(username)
	elif len(preset_username) > 0:
		username = parse_username(preset_username)
	#passthrough = 0
	server_admin_result = "true"
	
	command_string = "curl -X PUT -H 'Content-Type: application/json' -d '{\"admin\": \"" + server_admin_result + "\"}' https://" + homeserver_url + "/_synapse/admin/v1/users/@" + username + ":" + base_url + "/admin?access_token=" + access_token
	print("\n" + command_string + "\n")
	process = subprocess.run([command_string], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
	output = process.stdout
	print(output)
	return output

# Example:
# $ curl -kX POST -H 'Content-Type: application/json' -d '{"admin": "true"}' https://matrix.perthchat.org/_synapse/admin/v2/users/@dogpoo:perthchat.org?access_token=ACCESS_TOKEN

def whois_account(preset_username):
	if preset_username == '':
		username = input("\nPlease enter the username you wish to whois: ")
	elif preset_username != '':
		username = preset_username
	username = parse_username(username)
	command_string = "curl -kXGET https://" + homeserver_url + "/_matrix/client/r0/admin/whois/@" + username + ":" + base_url + "?access_token=" + access_token
	#print("\n" + command_string + "\n")
	process = subprocess.run([command_string], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
	output = process.stdout
	print(output + "\n")
	return(output)

# Example:
# $ curl -kXGET https://matrix.perthchat.org/_matrix/client/r0/admin/whois/@PC-Admin:perthchat.org?access_token=ACCESS_TOKEN

def list_joined_rooms(preset_username):
	if preset_username == '':
		username = input("\nPlease enter the username you wish to query: ")
	elif preset_username != '':
		username = preset_username
	username = parse_username(username)
	command_string = "curl -kXGET https://" + homeserver_url + "/_synapse/admin/v1/users/@" + username + ":" + base_url + "/joined_rooms?access_token=" + access_token
	#print("\n" + command_string + "\n")
	process = subprocess.run([command_string], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
	output = process.stdout
	print(output + "\n")

# Example:
# $ curl -kXGET https://matrix.perthchat.org/_synapse/admin/v1/users/@PC-Admin:perthchat.org/joined_rooms?access_token=ACCESS_TOKEN

def whois_multiple_accounts():
	print("Whois multiple user accounts selected")
	user_list_location = input("\nPlease enter the path of the file containing a newline seperated list of Matrix usernames: ")
	with open(user_list_location, newline='') as f:
		reader = csv.reader(f)
		data = list(reader)
		print(len(data))
	whois_confirmation = input("\n" + str(data) + "\n\nAre you sure you want to whois all of these users? y/n?\n")
	if whois_confirmation == "y" or whois_confirmation == "Y" or whois_confirmation == "yes" or whois_confirmation == "Yes":  
		x = 0
		while x <= (len(data) - 1):
			print(data[x][0])
			query_account(data[x][0])
			list_joined_rooms(data[x][0])
			x += 1
			#print(x)
			time.sleep(1)
	if whois_confirmation == "n" or whois_confirmation == "N" or whois_confirmation == "no" or whois_confirmation == "No":
		print("\nExiting...\n")

def list_accounts():
	deactivated_choice = input("Do you want to include deactivated accounts y/n? ")
	guest_choice = input("Do you want to include guest accounts y/n? ")

	if deactivated_choice == "y" or deactivated_choice == "Y" or deactivated_choice == "yes" or deactivated_choice == "Yes":
		deactivated_string = "deactivated=true"
	elif deactivated_choice == "n" or deactivated_choice == "N" or deactivated_choice == "no" or deactivated_choice == "No":
		deactivated_string = "deactivated=false"
	else:
		print("Input invalid! Defaulting to false.")
		deactivated_string = "deactivated=false"

	if guest_choice == "y" or guest_choice == "Y" or guest_choice == "yes" or guest_choice == "Yes":
		guest_string = "guest=true"
	elif guest_choice == "n" or guest_choice == "N" or guest_choice == "no" or guest_choice == "No":
		guest_string = "guest=false"
	else:
		print("Input invalid! Defaulting to false.")
		guest_string = "guest=false"

	command_string = "curl -kXGET \"https://" + homeserver_url + "/_synapse/admin/v2/users?from=0&limit=1000000&" + guest_string + "&" + deactivated_string + "&access_token=" + access_token + "\""
	print("\n" + command_string + "\n")
	process = subprocess.run([command_string], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
	output = process.stdout
	number_of_users = output.count("name")
	#
	print("\nTotal amount of users: " + str(number_of_users))
	if number_of_users < 100:	
		print(output)
	elif number_of_users >= 100:
		accounts_output_file = input("\nThere are too many users to list here, please specify a filename to print this data too: ")
		f = open(accounts_output_file, "w")
		f.write(output)
		f.close()

# Example:
# $ curl -kXGET "https://matrix.perthchat.org/_synapse/admin/v2/users?from=0&limit=10&guests=false&access_token=ACCESS_TOKEN"

def query_account(preset_username):
	if len(preset_username) == 0:
		username = input("\nPlease enter the username to query: ")
		username = parse_username(username)
	elif len(preset_username) > 0:
		username = parse_username(preset_username)
	command_string = "curl -kX GET https://" + homeserver_url + "/_synapse/admin/v2/users/@" + username + ":" + base_url + "?access_token=" + access_token
	print("\n" + command_string + "\n")
	process = subprocess.run([command_string], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
	output = process.stdout
	print(output)
	return output

# Example:
# $ curl -kX GET https://matrix.perthchat.org/_synapse/admin/v2/users/@billybob:perthchat.org?access_token=ACCESS_TOKEN

def create_account(preset_username,preset_password):
	if len(preset_username) == 0 and len(preset_password) == 0:
		username = input("\nPlease enter the username to create: ")
		username = parse_username(username)
		user_password = input("Please enter the password for this account: ")
	elif len(preset_username) > 0 and len(preset_password) > 0:
		username = parse_username(preset_username)
		user_password = preset_password
	else:
		print("\nError with user/pass file data, skipping...\n")
	command_string = "curl -kX PUT -H 'Content-Type: application/json' -d '{\"password\": \"" + user_password + "\"}' https://" + homeserver_url + "/_synapse/admin/v2/users/@" + username + ":" + base_url + "?access_token=" + access_token
	print("\n" + command_string + "\n")
	process = subprocess.run([command_string], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
	output = process.stdout
	print(output)
	return output

# Example:
# $ curl -kX PUT -H 'Content-Type: application/json' -d '{"password": "user_password","admin": false,"deactivated": false}' https://matrix.perthchat.org/_synapse/admin/v2/users/@billybob:perthchat.org?access_token=ACCESS_TOKEN

def create_multiple_accounts():
	print("Create multiple user accounts selected")
	user_list_location = input("\nPlease enter the path of the file containing a newline seperated list of Matrix usernames: ")
	with open(user_list_location, newline='') as f:
		reader = csv.reader(f)
		data = list(reader)
		print(len(data))
	create_confirmation = input("\n" + str(data) + "\n\nAre you sure you want to create these users? y/n?\n")
	if create_confirmation == "y" or create_confirmation == "Y" or  create_confirmation == "yes" or  create_confirmation == "Yes":  
		x = 0
		while x <= (len(data) - 1):
			print(data[x][0])
			create_account(data[x][0],data[x][1])
			x += 1
			#print(x)
			time.sleep(10)
	if create_confirmation == "n" or create_confirmation == "N" or  create_confirmation == "no" or  create_confirmation == "No":
		print("\nExiting...\n")

def deactivate_multiple_accounts():
	print("Deactivate multiple user accounts selected")
	user_list_location = input("\nPlease enter the path of the file containing a csv list of names: ")
	with open(user_list_location, newline='') as f:
			reader = csv.reader(f)
			data = list(reader)
	delete_confirmation = input("\n" + str(data) + "\n\nAre you sure you want to deactivate these users? y/n?\n")
	#print(len(data[0]))
	#print(data[0][0])
	if delete_confirmation == "y" or delete_confirmation == "Y" or  delete_confirmation == "yes" or  delete_confirmation == "Yes":  
		x = 0
		while x <= (len(data) - 1):
			#print(data[0][x])
			deactivate_account(data[x][0])
			x += 1
			#print(x)
			time.sleep(10)
	if delete_confirmation == "n" or delete_confirmation == "N" or  delete_confirmation == "no" or  delete_confirmation == "No":
		print("\nExiting...\n")
		
def list_room_details(preset_internal_ID):
	if preset_internal_ID == '':
		internal_ID = input("\nEnter the internal id of the room you wish to query (Example: !OLkDvaYjpNrvmwnwdj:matrix.org): ")
	elif preset_internal_ID != '':
		internal_ID = preset_internal_ID
	command_string = "curl -kXGET 'https://" + homeserver_url + "/_synapse/admin/v1/rooms/" + internal_ID + "?access_token=" + access_token + "'"
	print("\n" + command_string + "\n")
	process = subprocess.run([command_string], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
	output = process.stdout
	print(output)

# Example
# $ curl -kXGET 'https://matrix.perthchat.org/_synapse/admin/v1/rooms/!OeqILBxiHahidSQQoC:matrix.org?access_token=ACCESS_TOKEN'

def export_room_state(preset_internal_ID):
	if preset_internal_ID == '':
		internal_ID = input("\nEnter the internal id of the room with with to export the 'state' of (Example: !OLkDvaYjpNrvmwnwdj:matrix.org): ")
	elif preset_internal_ID != '':
		internal_ID = preset_internal_ID

	os.chdir(current_directory)
	room_dir = current_directory + "/state_events"
	os.makedirs(room_dir, exist_ok=True)
	os.chdir(room_dir)

	unix_time = int(time.time())
	command_string = "curl -kXGET 'https://" + homeserver_url + "/_synapse/admin/v1/rooms/" + internal_ID + "/state?access_token=" + access_token + "' > ./" + internal_ID + "_state_" + str(unix_time) + ".json"
	print("\n" + command_string + "\n")
	process = subprocess.run([command_string], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
	output = process.stdout
	print(output)

# Example
# $ curl -kXGET 'https://matrix.perthchat.org/_synapse/admin/v1/rooms/!OeqILBxiHahidSQQoC:matrix.org/state?access_token=ACCESS_TOKEN'

# See
# https://matrix-org.github.io/synapse/latest/admin_api/rooms.html#room-state-api

def list_directory_rooms():
	command_string = "curl -kXGET https://" + homeserver_url + "/_matrix/client/r0/publicRooms?access_token=" + access_token
	print("\n" + command_string + "\n")
	process = subprocess.run([command_string], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
	output = process.stdout
	output = output.replace('\"room_id\":\"','\n')
	output = output.replace('\",\"name','\n\",\"name')
	print(output)

# Example
# $ curl -kXGET https://matrix.perthchat.org/_matrix/client/r0/publicRooms?access_token=ACCESS_TOKEN

def remove_room_from_directory(preset_internal_ID):
	if preset_internal_ID == '':
		internal_ID = input("\nEnter the internal id of the room you wish to remove from the directory (Example: !OLkDvaYjpNrvmwnwdj:matrix.org): ")
	elif preset_internal_ID != '':
		internal_ID = preset_internal_ID
	command_string = "curl -kX PUT -H \'Content-Type: application/json\' -d \'{\"visibility\": \"private\"}\' \'https://" + homeserver_url + "/_matrix/client/r0/directory/list/room/" + internal_ID + "?access_token=" + access_token + "\'"
	print("\n" + command_string + "\n")
	process = subprocess.run([command_string], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
	output = process.stdout
	print(output)

# Example
# $ curl -kX PUT -H 'Content-Type: application/json' -d '{"visibility": "private"}' 'https://matrix.perthchat.org/_matrix/client/r0/directory/list/room/!DwUPBvNapIVecNllgt:perthchat.org?access_token=ACCESS_TOKEN'

def remove_multiple_rooms_from_directory():
	print("Remove multiple rooms from directory selected")
	purge_list_location = input("\nPlease enter the path of the file containing a newline seperated list of room ids: ")
	with open(purge_list_location, newline='') as f:
			reader = csv.reader(f)
			data = list(reader)
	x = 0
	while x <= (len(data) - 1):
		print(data[x][0])
		remove_room_from_directory(data[x][0])
		x += 1
		#print(x)
		time.sleep(1)

def list_and_download_media_in_room(preset_internal_ID,preset_print_file_list_choice,preset_download_files_choice,base_directory):
	if preset_internal_ID == '':
		internal_ID = input("\nEnter the internal id of the room you want to get a list of media for (Example: !OLkDvaYjpNrvmwnwdj:matrix.org): ")
	elif preset_internal_ID != '':
		internal_ID = preset_internal_ID
	command_string = "curl -kXGET https://" + homeserver_url + "/_synapse/admin/v1/room/" + internal_ID + "/media?access_token=" + access_token
	print("\n" + command_string + "\n")
	process = subprocess.run([command_string], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
	media_list_output = process.stdout
	#print("Full media list:\n" + media_list_output)

	if preset_print_file_list_choice == '':
		print_file_list_choice = input("\n Do you want to write this list to a file? y/n? ")
	elif preset_print_file_list_choice != '':
		print_file_list_choice = preset_print_file_list_choice

	if print_file_list_choice == "y" or print_file_list_choice == "Y" or print_file_list_choice == "yes" or print_file_list_choice == "Yes":
		print_file_list_choice = "true"
	elif print_file_list_choice == "n" or print_file_list_choice == "N" or print_file_list_choice == "no" or print_file_list_choice == "No":
		print_file_list_choice = "false"
	else:
		print("Input invalid! Defaulting to 'No'.")
		print_file_list_choice = "false"

	room_dir = "./" + internal_ID
	room_dir = room_dir.replace('!', '')
	room_dir = room_dir.replace(':', '-')
	os.mkdir(room_dir)
	os.chdir(room_dir)

	if print_file_list_choice == "true":
		media_list_filename_location = "./media_list.txt"
		media_list_filename = open(media_list_filename_location,"w+")
		media_list_filename.write(media_list_output)
		media_list_filename.close()

	if preset_download_files_choice == '':
		download_files_choice = input("\n Do you also want to download a copy of these media files? y/n? ")
	if preset_download_files_choice != '':
		download_files_choice = preset_download_files_choice

	if download_files_choice == "y" or download_files_choice == "Y" or download_files_choice == "yes" or download_files_choice == "Yes":
		download_files_choice = "true"
	elif download_files_choice == "n" or download_files_choice == "N" or download_files_choice == "no" or download_files_choice == "No":
		download_files_choice = "false"
	else:
		print("Input invalid! Defaulting to 'No'.")
		download_files_choice = "false"

	if download_files_choice == "true":
		media_list_output = media_list_output.split('\"')
		#print("New media list:\n" + str(media_list_output))
		os.mkdir("./media-files")
		os.chdir("./media-files")
		count = 0
		# Strips the newline character 
		for line in media_list_output:
			if "mxc" in line:
				#print("Line is 1: \n\n" + line + "\n")
				line = line.replace('mxc://','')
				download_command = "wget https://" + homeserver_url + "/_matrix/media/r0/download/" + line
				print(download_command)
				download_process = subprocess.run([download_command], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
		os.chdir(base_directory)

# Example
# $ curl -kXGET https://matrix.perthchat.org/_synapse/admin/v1/room/<room_id>/media?access_token=ACCESS_TOKEN

# To access via web:
# https://matrix.perthchat.org/_matrix/media/r0/download/ + server_name + "/" + media_id

def redact_room_event():
	internal_ID = input("\nEnter the internal id of the room the event is in (Example: !rapAelwZkajRyeZIpm:perthchat.org): ")
	event_ID = input("\nEnter the event id of the event you wish to redact (Example: $lQT7NYYyVvwoVpZWcj7wceYQqeOzsJg1N6aXIecys4s): ")
	redaction_reason = input("\nEnter the reason you're redacting this content: ")
	command_string = "curl -X POST --header \"Authorization: Bearer " + access_token + "\" --data-raw '{\"reason\": \"" + redaction_reason + "\"}' 'https://matrix.perthchat.org/_matrix/client/v3/rooms/" + internal_ID + "/redact/" + event_ID + "'"
	print("\n" + command_string + "\n")
	process = subprocess.run([command_string], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
	output = process.stdout
	print(output)
# $ curl -X POST --header "Authorization: Bearer syt_..." --data-raw '{"reason": "Indecent material"}' 'https://matrix.perthchat.org/_matrix/client/v3/rooms/!fuYHAYyXqNLDxlKsWP:perthchat.org/redact/$nyjgZguQGadRRy8MdYtIgwbAeFcUAPqOPiaj_E60XZs'
# {"event_id":"$_m1gFtPg-5DiTyCvGfeveAX2xaA8gAv0BYLpjC8xe64"}

def download_media_from_multiple_rooms():
	print("Download media from multiple rooms selected")
	download_media_list_location = input("\nPlease enter the path of the file containing a newline seperated list of room ids: ")
	with open(download_media_list_location, newline='') as f:
			reader = csv.reader(f)
			data = list(reader)
	preset_print_file_list_choice = input("\n Do you want to print list files of all the media in these rooms? y/n? ")
	preset_download_files_choice = input("\n Do you want to download all the media in these rooms? y/n? ")

	os.mkdir("./media_download")
	os.chdir("./media_download")

	pwd_process = subprocess.run(["pwd"], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
	base_directory = pwd_process.stdout
	base_directory = base_directory.replace('\n','')
	print(base_directory)

	print("Beginning download of media from all rooms in list...")
	x = 0
	while x <= (len(data) - 1):
		print(data[x][0])
		list_and_download_media_in_room(data[x][0],preset_print_file_list_choice,preset_download_files_choice,base_directory)
		x += 1
		#print(x)
		time.sleep(1)

def quarantine_media_in_room():
	internal_ID = input("\nEnter the internal id of the room you want to quarantine, this makes local and remote data inaccessible (Example: !OLkDvaYjpNrvmwnwdj:matrix.org): ")
	command_string = "curl -X POST \'https://" + homeserver_url + "/_synapse/admin/v1/room/" + internal_ID + "/media/quarantine?access_token=" + access_token + "\'"
	print("\n" + command_string + "\n")
	process = subprocess.run([command_string], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
	output = process.stdout
	print(output)

# Example
# $ curl -X POST 'https://matrix.perthchat.org/_synapse/admin/v1/room/!DwUPBvNapIVecNllgt:perthchat.org/media/quarantine?access_token=ACCESS_TOKEN'

def quarantine_users_media():
	username = input("\nPlease enter the username of the user who's media you want to quarantine: ")
	username = parse_username(username)
	command_string = "curl -X POST \'https://" + homeserver_url + "/_synapse/admin/v1/user/@" + username + ":" + base_url + "/media/quarantine?access_token=" + access_token + "\'"
	print("\n" + command_string + "\n")
	process = subprocess.run([command_string], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
	output = process.stdout
	print(output)

# Example:
# $ curl -X POST https://matrix.perthchat.org/_synapse/admin/v1/user/@PC-Admin:perthchat.org/media/quarantine?access_token=ACCESS_TOKEN

def shutdown_room(preset_internal_ID,preset_user_ID,preset_new_room_name,preset_message,preset_purge_choice,preset_block_choice):
	if preset_internal_ID == '':
		internal_ID = input("\nEnter the internal id of the room you want shutdown (Example: !OLkDvaYjpNrvmwnwdj:matrix.org): ")
	elif preset_internal_ID != '':
		internal_ID = preset_internal_ID
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

	username = parse_username(user_ID)

	if purge_choice == "y" or purge_choice == "Y" or purge_choice == "yes" or purge_choice == "Yes":
		purge_choice = "true"
	elif purge_choice == "n" or purge_choice == "N" or purge_choice == "no" or purge_choice == "No":
		purge_choice = "false"
	else:
		print("Input invalid! exiting.")
		return

	if block_choice == "y" or block_choice == "Y" or block_choice == "yes" or block_choice == "Yes":
		block_choice = "true"
	elif block_choice == "n" or block_choice == "N" or block_choice == "no" or block_choice == "No":
		block_choice = "false"
	else:
		print("Input invalid! exiting.")
		return

    # First export the state events of the room to examine them later or import them to rdlist
	export_room_state(internal_ID)
	print ("Exported room state events to file, this data can be useful for profiling a room after you've blocked/purged it: ./state_events" + internal_ID + "_state.json")

	command_string = 'curl -H "Authorization: Bearer ' + access_token + "\" --data '{ \"new_room_user_id\": \"@" + username + ":" + base_url + "\" , \"room_name\": \"" + new_room_name + "\", \"message\": \"" + message + "\", \"block\": " + block_choice + ", \"purge\": " + purge_choice + " }' -X DELETE 'https://" + homeserver_url + "/_synapse/admin/v2/rooms/" + internal_ID + "'"
	#print("\n" + command_string + "\n")
	process = subprocess.run([command_string], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
	output = process.stdout
	#print(output)

	status = "null"
	count = 0
	sleep_time = 1

	while status != "complete" and count < 8:
		time.sleep(sleep_time)
		count = count + 1
		sleep_time = sleep_time * 2
		command_string = 'curl -H "Authorization: Bearer ' + access_token + "\" -kX GET 'https://" + homeserver_url + '/_synapse/admin/v2/rooms/' + internal_ID + "/delete_status'"
		#print("\n" + command_string + "\n")
		process = subprocess.run([command_string], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
		output_json = json.loads(process.stdout)
		#print(output_json)
		status = output_json["results"][0]["status"]
		print("status: " + status)
		#print("count: " + str(count))
		if status != "complete":
			print("Sleeping for " + str(sleep_time) + " seconds...")

	if status == "complete":
		print(internal_ID + " has been successfully shutdown!")
		if str(output_json["results"][0]["shutdown_room"]["kicked_users"]) != '[]':
			print("List of kicked users:")
			for entry in output_json["results"][0]["shutdown_room"]["kicked_users"]:
				print(entry)
		print("")

# Example:
#$ curl -H "Authorization: Bearer ACCESS_TOKEN" --data '{ "new_room_user_id": "@PC-Admin:perthchat.org", "room_name": "VIOLATION ROOM", "message": "YOU HAVE BEEN NAUGHTY!", "block": true, "purge": true }' -X DELETE 'https://matrix.perthchat.org/_synapse/admin/v2/rooms/!yUykDcYIEtrbSxOyPD:perthchat.org'
# {"delete_id":"efphJOtAxlBNtkGD"}

# Then check with:
# $ curl -H "Authorization: Bearer ACCESS_TOKEN" -kX GET 'https://matrix.perthchat.org/_synapse/admin/v2/rooms/!yUykDcYIEtrbSxOyPD:perthchat.org/delete_status'
# {"results":[{"delete_id":"yRjYjwoTOXOnRQPa","status":"complete","shutdown_room":{"kicked_users":["@michael:perthchat.org"],"failed_to_kick_users":[],"local_aliases":[],"new_room_id":"!AXTUBcSlehQuCidiZu:perthchat.org"}}]}

def shutdown_multiple_rooms():
	print("Shutdown multiple rooms selected")
	purge_list_location = input("\nPlease enter the path of the file or directory containing a newline seperated list of room ids: ")
	file_list = []
	# check if the input path is a directory or a file
	if os.path.isdir(purge_list_location):
		# iterate over all files in the directory
		for filename in os.listdir(purge_list_location):
			# construct full file path
			file_path = os.path.join(purge_list_location, filename)
			# add it to the list
			file_list.append(file_path)
	else:
		# it's a single file
		file_list.append(purge_list_location)
	preset_user_ID = input("\nPlease enter the local username that will create a 'muted violation room' for your users (Example: michael): ")
	preset_new_room_name = input("\nPlease enter the room name of the muted violation room your users will be sent to: ")
	preset_message = input("\nPlease enter the shutdown message that will be displayed to users: ")
	preset_purge_choice = input("\n Do you want to purge these rooms? (This deletes all the room history from your database.) y/n? ")
	preset_block_choice = input("\n Do you want to block these rooms? (This prevents your server users re-entering the room.) y/n? ")
	# Get the directory of the current script
	script_dir = os.path.dirname(os.path.realpath(__file__))
	room_list_data = []	
	for file in file_list:
		print("Processing file: " + file)
		# Change the current working directory
		os.chdir(script_dir)
		with open(file, newline='') as f:
			reader = csv.reader(f)
			data = list(reader)
			room_list_data = room_list_data + data
	# Deduplicate the room_list_data
	room_list_data = [list(item) for item in set(tuple(row) for row in room_list_data)]
	shutdown_confirmation = input("\n" + str(room_list_data) + "\n\nNumber of rooms being shutdown: " + str(len(room_list_data)) + "\n\nAre you sure you want to shutdown these rooms? y/n? ")
	if shutdown_confirmation.lower() in ["y", "yes"]:
		for room_id in room_list_data:
			shutdown_room(room_id[0], preset_user_ID, preset_new_room_name, preset_message, preset_purge_choice, preset_block_choice)
			time.sleep(10)
	elif shutdown_confirmation.lower() in ["n", "no"]:
		print("\nSkipping these files...\n")
	else:
		print("\nInvalid input, skipping these files...\n")

# Example:
# See shutdown_room()

def delete_room(preset_internal_ID):
	if preset_internal_ID == '':
		internal_ID = input("\nEnter the internal id of the room you want to delete (Example: !OLkDvaYjpNrvmwnwdj:matrix.org): ")
	elif preset_internal_ID != '':
		internal_ID = preset_internal_ID

	command_string = 'curl -H "Authorization: Bearer ' + access_token + "\" --data '{ \"block\":  false, \"purge\": true }' -X DELETE 'https://" + homeserver_url + "/_synapse/admin/v2/rooms/" + internal_ID + "'"
	print("\n" + command_string + "\n")
	process = subprocess.run([command_string], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
	output = process.stdout
	print(output)

	status = "null"
	count = 0
	sleep_time = 0.5

	while status != "complete" and count < 8:
		time.sleep(sleep_time)
		count = count + 1
		sleep_time = sleep_time * 2
		command_string = 'curl -H "Authorization: Bearer ' + access_token + "\" -kX GET 'https://" + homeserver_url + '/_synapse/admin/v2/rooms/' + internal_ID + "/delete_status'"
		#print("\n" + command_string + "\n")
		process = subprocess.run([command_string], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
		#print("\nOutput type: " + str(type(process.stdout)))
		#print("Output value: " + str(process.stdout) + "\n")
		output_json = json.loads(process.stdout)
		#print(output_json)
		status = output_json["results"][0]["status"]
		print("status: " + status)
		#print("count: " + str(count))
		if status != "complete":
			print("Sleeping for " + str(sleep_time) + " seconds...")

	if status == "complete":
		print(internal_ID + " has been successfully deleted!")
		if str(output_json["results"][0]["shutdown_room"]["kicked_users"]) != '[]':
			print("List of kicked users:")
			for entry in output_json["results"][0]["shutdown_room"]["kicked_users"]:
				print(entry)
		print("")

# Example:
#$ curl -H "Authorization: Bearer ACCESS_TOKEN" --data '{ "block": false, "purge": true }' -X DELETE 'https://matrix.perthchat.org/_synapse/admin/v2/rooms/!yUykDcYIEtrbSxOyPD:perthchat.org'
# {"delete_id":"efphJOtAxlBNtkGD"}

# Then check with:
# $ curl -H "Authorization: Bearer ACCESS_TOKEN" -kX GET 'https://matrix.perthchat.org/_synapse/admin/v2/rooms/!yUykDcYIEtrbSxOyPD:perthchat.org/delete_status'
# {"results":[{"delete_id":"efphJOtAxlBNtkGD","status":"complete","shutdown_room":{"kicked_users":[],"failed_to_kick_users":[],"local_aliases":[],"new_room_id":null}}]}

def delete_multiple_rooms():
	print("Delete multiple rooms selected")
	purge_list_location = input("\nPlease enter the path of the file containing a newline seperated list of room ids: ")
	with open(purge_list_location, newline='') as f:
		reader = csv.reader(f)
		data = list(reader)
	delete_confirmation = input("\n" + str(data) + "\n\nAre you sure you want to delete these rooms? y/n? ")
	#print("len(data[0]) - " + str(len(data[0])))
	#print("data[0][0] - " + data[0][0])
	if delete_confirmation == "y" or delete_confirmation == "Y" or delete_confirmation == "yes" or delete_confirmation == "Yes":
		x = 0
		while x <= (len(data) - 1):
			print("data[x][0] - " + data[x][0])
			delete_room(data[x][0])
			x += 1
			#print(x)
			#time.sleep(2) # deleting a room is quicker then a full shutdown

	if delete_confirmation == "n" or delete_confirmation == "N" or delete_confirmation == "no" or delete_confirmation == "No":
		print("\nExiting...\n")

# Example:
# See delete_room()

def purge_room_to_timestamp(preset_internal_ID, preset_timestamp):
	if preset_internal_ID == '':
		internal_ID = input("\nEnter the internal id of the room you want to delete (Example: !OLkDvaYjpNrvmwnwdj:matrix.org): ")
	elif preset_internal_ID != '':
		internal_ID = preset_internal_ID
	if preset_timestamp == '':
		timestamp = input("\nEnter the epoche timestamp in microseconds (Example: 1661058683000): ")
	elif preset_timestamp != '':
		timestamp = preset_timestamp

	command_string = 'curl --header "Authorization: Bearer ' + access_token + "\" -X POST -H \"Content-Type: application/json\" -d '{ \"delete_local_events\": false, \"purge_up_to_ts\": " + timestamp + " }' 'https://" + homeserver_url + "/_synapse/admin/v1/purge_history/" + internal_ID + "'"
	print("\n" + command_string + "\n")
	process = subprocess.run([command_string], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
	output = process.stdout
	print(output)
	output_json = json.loads(process.stdout)
	purge_id = output_json["purge_id"]

	status = "null"
	count = 0
	sleep_time = 0.5

	while status != "complete" and count < 8:
		time.sleep(sleep_time)
		count = count + 1
		sleep_time = sleep_time * 2
		command_string = 'curl -H "Authorization: Bearer ' + access_token + "\" -kX GET 'https://" + homeserver_url + '/_synapse/admin/v1/purge_history_status/' + purge_id + "'"
		print("\n" + command_string + "\n")
		process = subprocess.run([command_string], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
		#print("\nOutput type: " + str(type(process.stdout)))
		#print("Output value: " + str(process.stdout) + "\n")
		output_json = json.loads(process.stdout)
		#print(output_json)
		status = output_json["status"]
		print("status: " + status)
		#print("count: " + str(count))
		if status != "complete":
			print("Sleeping for " + str(sleep_time) + " seconds...")

	if status == "complete":
		print(internal_ID + " has successfully had its history purged!")
		print("")

# Example:
#$ curl --header "Authorization: Bearer syt_bW..." -X POST -H "Content-Type: application/json" -d '{ "delete_local_events": false, "purge_up_to_ts": 1661058683000 }' 'https://matrix.perthchat.org/_synapse/admin/v1/purge_history/!OnWgVbeuALuOEZowed:perthchat.org'
#{"purge_id":"rfWgHeCWWyDoOJZn"}

# Then check with:
#$ curl -H "Authorization: Bearer syt_bW..." -kX GET 'https://matrix.perthchat.org/_synapse/admin/v1/purge_history_status/rfWgHeCWWyDoOJZn'
#{"status":"complete"}

def purge_multiple_rooms_to_timestamp():
	print("Purge the event history of multiple rooms to a specific timestamp selected")
	purge_list_location = input("\nPlease enter the path of the file containing a newline seperated list of room ids: ")
	with open(purge_list_location, newline='') as f:
		reader = csv.reader(f)
		data = list(reader)
	preset_timestamp = input("\nPlease enter the epoche timestamp in milliseconds you wish to purge too (for example 1661058683000): ")
	purge_confirmation = input("\n" + str(data) + "\n\nAre you sure you want to purge the history of these rooms? y/n? ")
	print("len(data[0]) - " + str(len(data[0])))
	print("data[0][0] - " + data[0][0])
	if purge_confirmation == "y" or purge_confirmation == "Y" or purge_confirmation == "yes" or purge_confirmation == "Yes":
		x = 0
		while x <= (len(data) - 1):
			print("data[x][0] - " + data[x][0])
			purge_room_to_timestamp(data[x][0], preset_timestamp)
			x += 1
			#print(x)

	if purge_confirmation == "n" or purge_confirmation == "N" or purge_confirmation == "no" or purge_confirmation == "No":
		print("\nExiting...\n")

# Example:
# See purge_room_to_timestamp()

def delete_block_media():
	# Take media_id from user
	media_id = input("\nEnter the media_id of the media you would like to delete and block on your server. (Example: For this media https://matrix.perthchat.org/_matrix/media/r0/download/matrix.org/eDmjusOjnHyFPOYGxlrOsULJ the media_id is 'eDmjusOjnHyFPOYGxlrOsULJ'): ")
	remote_server = input("\nEnter the remote servers URL without the 'https://' (Example: matrix.org): ")
	# find filesystem_id from database
	command_collect_filesystem_id = "ssh " + homeserver_url + """ "/matrix/postgres/bin/cli-non-interactive --dbname=synapse -t -c 'SELECT DISTINCT filesystem_id FROM remote_media_cache WHERE media_id = '\\''""" + media_id + """'\\'" | xargs"""
	print(command_collect_filesystem_id)
	process_collect_filesystem_id = subprocess.run([command_collect_filesystem_id], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
	filesystem_id = process_collect_filesystem_id.stdout
	print(process_collect_filesystem_id.stdout)
	# list the target files on disk
	command_collect_thumbnails = "ssh " + homeserver_url + ' "find /matrix/synapse/storage/media-store/remote_thumbnail/' + remote_server + '/' + filesystem_id[:2] + "/" + filesystem_id[2:4] + "/" + filesystem_id[4:].rstrip() + """ -type f -printf '%p\\n'\""""
	print(command_collect_thumbnails)
	process_collect_thumbnails = subprocess.run([command_collect_thumbnails], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
	remote_thumbnails_list = process_collect_thumbnails.stdout
	print(remote_thumbnails_list)
	command_content_location = "ssh " + homeserver_url + ' "ls /matrix/synapse/storage/media-store/remote_content/' + remote_server + '/' + filesystem_id[:2] + "/" + filesystem_id[2:4] + "/" + filesystem_id[4:].rstrip() + '"'
	print(command_content_location)
	process_content_location = subprocess.run([command_content_location], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
	remote_content_location = process_content_location.stdout
	print(remote_content_location)
	# Zero the target files on disk then chattr +i them
	for line in remote_thumbnails_list.split('\n'):
		if line:
			command_zero_thumbnails = 'ssh ' + homeserver_url + ' "true > ' + line + '"'
			print(command_zero_thumbnails)
			process_zero_thumbnails = subprocess.run(command_zero_thumbnails, shell=True)
			print(process_zero_thumbnails.stdout)
			command_make_thumbnail_immutable = 'ssh ' + homeserver_url + ' "chattr +i ' + line + '"'
			print(command_make_thumbnail_immutable)
			process_make_thumbnail_immutable = subprocess.run(command_make_thumbnail_immutable, shell=True)
			print(process_make_thumbnail_immutable.stdout)
	command_zero_media = 'ssh ' + homeserver_url + ' "true > ' + remote_content_location.rstrip() + '"'
	print(command_zero_media)
	process_remove_media = subprocess.run(command_zero_media, shell=True)
	print(process_remove_media.stdout)
	command_make_content_immutable = 'ssh ' + homeserver_url + ' "chattr +i ' + remote_content_location.rstrip() + '"'
	print(command_make_content_immutable)
	process_make_content_immutable = subprocess.run(command_make_content_immutable, shell=True)
	print(process_make_content_immutable.stdout)

# Example, first use the media_id to find the filesystem_id:
# $ ssh matrix.perthchat.org "/matrix/postgres/bin/cli-non-interactive --dbname=synapse -t -c 'SELECT DISTINCT filesystem_id FROM remote_media_cache WHERE media_id = '\''eDmjusOjnHyFPOYGxlrOsULJ'\'" | xargs
# ehckzWWeUkDhhPfNFkcfCFNv

# Then use that filesystem_id to locate the remote file and all it's thumbnails:
# $ ssh matrix.perthchat.org "find /matrix/synapse/storage/media-store/remote_thumbnail/matrix.org/eh/ck/zWWeUkDhhPfNFkcfCFNv -type f -printf '%p\n'"
#/matrix/synapse/storage/media-store/remote_thumbnail/matrix.org/eh/ck/zWWeUkDhhPfNFkcfCFNv/32-32-image-jpeg-crop
#/matrix/synapse/storage/media-store/remote_thumbnail/matrix.org/eh/ck/zWWeUkDhhPfNFkcfCFNv/640-480-image-jpeg-scale
# ...
# $ ssh matrix.perthchat.org "ls /matrix/synapse/storage/media-store/remote_content/matrix.org/eh/ck/zWWeUkDhhPfNFkcfCFNv"
# /matrix/synapse/storage/media-store/remote_content/matrix.org/eh/ck/zWWeUkDhhPfNFkcfCFNv

# Then zero each file and make it immutable:
# $ ssh matrix.perthchat.org "true > /matrix/synapse/storage/media-store/remote_thumbnail/matrix.org/eh/ck/zWWeUkDhhPfNFkcfCFNv/32-32-image-jpeg-crop"
# $ ssh matrix.perthchat.org "chattr +i /matrix/synapse/storage/media-store/remote_thumbnail/matrix.org/eh/ck/zWWeUkDhhPfNFkcfCFNv/32-32-image-jpeg-crop"
# $ ssh matrix.perthchat.org "true > /matrix/synapse/storage/media-store/remote_thumbnail/matrix.org/eh/ck/zWWeUkDhhPfNFkcfCFNv/640-480-image-jpeg-scale"
# $ ssh matrix.perthchat.org "chattr +i /matrix/synapse/storage/media-store/remote_thumbnail/matrix.org/eh/ck/zWWeUkDhhPfNFkcfCFNv/640-480-image-jpeg-scale"
# ...
# $ ssh matrix.perthchat.org "true > /matrix/synapse/storage/media-store/remote_content/matrix.org/eh/ck/zWWeUkDhhPfNFkcfCFNv"
# $ ssh matrix.perthchat.org "chattr +i /matrix/synapse/storage/media-store/remote_content/matrix.org/eh/ck/zWWeUkDhhPfNFkcfCFNv"

def purge_remote_media_repo():
	purge_from = input("\nEnter the number of days to purge from: ")
	purge_too = input("\nEnter the number of days to purge too: ")

	while int(purge_from) >= int(purge_too):
		epoche_command = "date --date '" + str(purge_from) + " days ago' +%s"
		print(epoche_command)
		epoche_time_process  = subprocess.run([epoche_command], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
		print(epoche_time_process.stdout)
		epoche_time = epoche_time_process.stdout
		epoche_time_stripped = epoche_time.replace("\n", "")
		command_string = "curl -X POST --header \"Authorization: Bearer " + access_token + "\" 'https://" + homeserver_url + "/_synapse/admin/v1/purge_media_cache?before_ts=" + epoche_time_stripped + "000'"
		print(command_string)
		process = subprocess.run([command_string], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
		print(process.stdout)
		purge_from = int(purge_from) - 1
		time.sleep(2)

# This loop is quite slow, our server was having disk issues.
	print("Done! :)")

# Example:
# $ date --date '149 days ago' +%s
# 1589442217
# $ curl -X POST --header "Authorization: Bearer ACCESS_TOKEN" 'https://matrix.perthchat.org/_synapse/admin/v1/purge_media_cache?before_ts=1589439628000'

def prepare_database_copy_of_multiple_rooms():
	print("Preparing database copying of events from multiple rooms selected\n")
	print("This command needs to be run on the target server as root, it will setup postgres commands to download the join-leave events and all-events from a list of rooms.\n\nIt mounts a ramdisk beforehand at /matrix/postgres/data/ramdisk\n\nThis function is only compatible with Spantaleevs Matrix deploy script: https://github.com/spantaleev/matrix-docker-ansible-deploy\n")
	database_copy_list_location = input("Please enter the path of the file containing a newline seperated list of room ids: ")
	with open(database_copy_list_location, newline='') as f:
			reader = csv.reader(f)
			data = list(reader)

	make_ramdisk_command = "mkdir /matrix/postgres/data/ramdisk; mount -t ramfs -o size=512m ramfs /matrix/postgres/data/ramdisk; chown -R matrix:matrix /matrix/postgres/data/ramdisk"
	make_ramdisk_command_process = subprocess.run([make_ramdisk_command], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
	print(make_ramdisk_command_process.stdout)

	x = 0
	while x <= (len(data) - 1):
		print(data[x][0])
		roomid_trimmed = data[x][0]
		roomid_trimmed = roomid_trimmed.replace('!', '')
		roomid_trimmed = roomid_trimmed.replace(':', '-')
		os.mkdir("/matrix/postgres/data/ramdisk/" + roomid_trimmed)
		touch_command = "touch /matrix/postgres/data/ramdisk/" + roomid_trimmed + "/dump_room_data.sql"
		touch_command_process  = subprocess.run([touch_command], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
		print(touch_command_process.stdout)
		sql_file_contents = "\set ROOMID '" + data[x][0] + "'\nCOPY (SELECT * FROM current_state_events JOIN room_memberships ON room_memberships.event_id = current_state_events.event_id WHERE current_state_events.room_id = :'ROOMID') TO '/var/lib/postgresql/data/ramdisk/" + roomid_trimmed + "/user_join-leave.csv' WITH CSV HEADER;\nCOPY (SELECT * FROM event_json WHERE room_id=:'ROOMID') TO '/var/lib/postgresql/data/ramdisk/" + roomid_trimmed + "/room_events.csv' WITH CSV HEADER;"
		print(sql_file_contents)
		sql_file_location = "/matrix/postgres/data/ramdisk/" + roomid_trimmed + "/dump_room_data.sql"
		sql_file = open(sql_file_location,"w+")
		sql_file.write(sql_file_contents)
		sql_file.close()

		x += 1
		#print(x)
		time.sleep(1)

	chown_command = "chown -R matrix:matrix /matrix/postgres/data/ramdisk; docker restart matrix-postgres"
	chown_command_process = subprocess.run([chown_command], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
	print(chown_command_process.stdout)

	print("\nThe sql query files have been generated, as postgres user in container run:\n# docker exec -it matrix-postgres /bin/bash\nbash-5.0$  export PGPASSWORD=your-db-password\nbash-5.0$ for f in /var/lib/postgresql/data/ramdisk/*/dump_room_data.sql; do psql --host=127.0.0.1 --port=5432 --username=synapse -w -f $f; done\n\nAfter copying the data to a cloud location law enforcement can access, clean up the ramdisk like so:\n# rm -r /matrix/postgres/data/ramdisk/*\n# umount /matrix/postgres/data/ramdisk")

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
			shutdown_room(room_id, user_ID, new_room_name, message, purge_choice, block_choice)
			time.sleep(5)
	elif shutdown_confirmation.lower() in ['n', 'no', 'N', 'No']:
		print("\nSkipping these files...\n")
	else:
		print("\nInvalid input, skipping these files...\n")

def block_recommended_rdlist_tags():
	# Check if user account already exists
	account_query = query_account(rdlist_bot_username)
	# Generate random password
	preset_password = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(20))
	# If user is not found, create it
	if 'User not found' in account_query:
		# Create user account
		create_account(rdlist_bot_username, preset_password)
	else:
		print("Account already exists.")
		reset_password(rdlist_bot_username, preset_password)
	# Promote bot user to server admin
	set_user_server_admin(rdlist_bot_username)
	# Define default valies for shutdown_room()
	preset_new_room_name = 'POLICY VIOLATION'
	preset_message = 'THIS ROOM VIOLATES SERVER POLICIES'
	preset_purge_choice = 'y'
	preset_block_choice = 'y'
	# Block all rooms with recommended tag set
	block_all_rooms_with_rdlist_tags(True, rdlist_bot_username, preset_new_room_name, preset_message, preset_purge_choice, preset_block_choice)
	# Print user login details
	print("\nUser login details:\n")
	print("Username: " + rdlist_bot_username)
	print("Password: " + preset_password)

# check if homeserver url is hard coded, if not set it

if homeserver_url == "matrix.example.org":
	homeserver_url = input("What is the URL of your server? Eg: matrix.example.org ")

# check if base url is hard coded, if not set it

if base_url == "example.org":
	base_url = input("What is the URL of your server? Eg: example.org ")

# check if access token is hard coded, if not set it

length_access_token = len(access_token)

if length_access_token == 0:
	access_token = input("Please enter access token for server admin account: ")

# record the current directory location

current_directory = os.getcwd()

# loop menu for various moderation actions

pass_token = False
while pass_token == False:
	menu_input = input('\nPlease select one of the following options:\n#### User Account Commands ####\n1) Deactivate a user account.\n2) Create a user account.\n3) Query user account.\n4) List room memberships of user.\n5) Query multiple user accounts.\n6) Reset a users password.\n7) Promote a user to server admin.\n8) List all user accounts.\n9) Create multiple user accounts.\n10) Deactivate multiple user accounts.\n11) Quarantine all media a users uploaded.\n#### Room Commands ####\n12) List details of a room.\n13) Export the state events of a target room.\n14) List rooms in public directory.\n15) Remove a room from the public directory.\n16) Remove multiple rooms from the public directory.\n17) Redact a room event. (Like abusive avatars or display names.) \n18) List/Download all media in a room.\n19) Download media from multiple rooms.\n20) Quarantine all media in a room.\n21) Shutdown a room.\n22) Shutdown multiple rooms.\n23) Delete a room.\n24) Delete multiple rooms.\n25) Purge the event history of a room to a specific timestamp.\n26) Purge the event history of multiple rooms to a specific timestamp.\n#### Server Commands ####\n27) Delete and block a specific media. (Like an abusive avatar.) \n28) Purge remote media repository up to a certain date.\n29) Prepare database for copying events of multiple rooms.\n#### rdlist ####\n30) Block all rooms with specific rdlist tags.\n34) Block all rooms with recommended rdlist tags.\n(\'q\' or \'e\') Exit.\n\n')
	if menu_input == "1":
		deactivate_account('')
	elif menu_input == "2":
		create_account('','')
	elif menu_input == "3":
		whois_account('')
	elif menu_input == "4":
		list_joined_rooms('')
	elif menu_input == "5":
		whois_multiple_accounts()
	elif menu_input == "6":
		reset_password()
	elif menu_input == "7":
		set_user_server_admin()
	elif menu_input == "8":
		list_accounts()
	elif menu_input == "9":
		create_multiple_accounts()
	elif menu_input == "10":
		deactivate_multiple_accounts()
	elif menu_input == "11":
		quarantine_users_media()
	elif menu_input == "12":
		list_room_details('')
	elif menu_input == "13":
		export_room_state('')
	elif menu_input == "14":
		list_directory_rooms()
	elif menu_input == "15":
		remove_room_from_directory('')
	elif menu_input == "16":
		remove_multiple_rooms_from_directory()
	elif menu_input == "17":
		redact_room_event()
	elif menu_input == "18":
		list_and_download_media_in_room('','','','./')
	elif menu_input == "19":
		download_media_from_multiple_rooms()
	elif menu_input == "20":
		quarantine_media_in_room()
	elif menu_input == "21":
		shutdown_room('','','','','','')
	elif menu_input == "22":
		shutdown_multiple_rooms()
	elif menu_input == "23":
		delete_room('')
	elif menu_input == "24":
		delete_multiple_rooms()
	elif menu_input == "25":
		purge_room_to_timestamp('','')
	elif menu_input == "26":
		purge_multiple_rooms_to_timestamp()
	elif menu_input == "27":
		delete_block_media()
	elif menu_input == "28":
		purge_remote_media_repo()
	elif menu_input == "29":
		prepare_database_copy_of_multiple_rooms()
	elif menu_input == "30":
		block_all_rooms_with_rdlist_tags(False,'','','','','')
	elif menu_input == "34":
		block_recommended_rdlist_tags()
	elif menu_input == "q" or menu_input == "Q" or menu_input == "e" or menu_input == "E":
		print("\nExiting...\n")
		pass_token = True
	else:
		print("\nIncorrect input detected, please select a number from 1 to 34!\n")

