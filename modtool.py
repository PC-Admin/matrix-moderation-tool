
# modtool.py
# an easy moderation tool for matrix/synapse
#
# created by @PC-Admin:perthchat.org
#
# This work is licensed under AGPLv3, for more information see: https://www.gnu.org/licenses/agpl-3.0.txt
#
# To do:
# https://github.com/matrix-org/synapse/blob/master/docs/admin_api/delete_group.md
# Make the menu prettier!

import subprocess
import csv
import time
import os

###########################################################################
# These values can be hard coded for easier usage:                        #
homeserver_url = "matrix.example.org"
base_url = "example.org"
access_token = ""
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
	command_string = "curl -kX POST -H 'Content-Type: application/json' -d '{\"erase\": true}' https://" + homeserver_url + "/_matrix/client/r0/admin/deactivate/@" + username + ":" + base_url + "?access_token=" + access_token
	print("\n" + command_string + "\n")
	process = subprocess.run([command_string], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
	output = process.stdout
	print(output)

# Example:
# $ curl -kX POST -H 'Content-Type: application/json' -d '{"erase": true}' https://matrix.perthchat.org/_matrix/client/r0/admin/deactivate/@billybob:perthchat.org?access_token=ACCESS_TOKEN

def reset_password():
	username = input("\nPlease enter the username for the password reset: ")
	password = input("Please enter the password to set: ")
	username = parse_username(username)
	command_string = "curl -kX POST -H 'Content-Type: application/json' -d '{\"new_password\": \"" + password + "\"}' https://" + homeserver_url + "/_matrix/client/r0/admin/reset_password/@" + username + ":" + base_url + "?access_token=" + access_token
	print("\n" + command_string + "\n")
	process = subprocess.run([command_string], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
	output = process.stdout
	print(output)

# Example:
# $ curl -kX POST -H 'Content-Type: application/json' -d '{"new_password": "dogpoo"}' https://matrix.perthchat.org/_matrix/client/r0/admin/reset_password/@dogpoo:perthchat.org?access_token=ACCESS_TOKEN

def set_user_server_admin():
	# tried setting 'admin: false' here but it failed and promoted the user instead!
	print("\nBe aware that you need to set at least 1 user to server admin already by editing the database in order to use this command. See https://github.com/PC-Admin/PC-Admins-Synapse-Moderation-Tool/blob/master/README.md for details on how to do this.")
	username = input("\nPlease enter the username you want to promote to server admin: ")
	username = parse_username(username)
	passthrough = 0
	server_admin_result = "true"
	
	command_string = "curl -kX PUT -H 'Content-Type: application/json' -d '{\"admin\": \"" + server_admin_result + "\"}' https://" + homeserver_url + "/_synapse/admin/v2/users/@" + username + ":" + base_url + "?access_token=" + access_token
	print("\n" + command_string + "\n")
	process = subprocess.run([command_string], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
	output = process.stdout
	print(output)

# Example:
# $ curl -kX POST -H 'Content-Type: application/json' -d '{"admin": "true"}' https://matrix.perthchat.org/_synapse/admin/v2/users/@dogpoo:perthchat.org?access_token=ACCESS_TOKEN

def query_account():
	username = input("\nPlease enter the username you wish to query: ")
	username = parse_username(username)
	command_string = "curl -kXGET https://" + homeserver_url + "/_matrix/client/r0/admin/whois/@" + username + ":" + base_url + "?access_token=" + access_token
	print("\n" + command_string + "\n")
	process = subprocess.run([command_string], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
	output = process.stdout
	print(output)

# Example:
# $ curl -kXGET https://matrix.perthchat.org/_matrix/client/r0/admin/whois/@PC-Admin:perthchat.org?access_token=ACCESS_TOKEN

def list_joined_rooms():
	username = input("\nPlease enter the username you wish to query: ")
	username = parse_username(username)
	command_string = "curl -kXGET https://" + homeserver_url + "/_synapse/admin/v1/users/@" + username + ":" + base_url + "/joined_rooms?access_token=" + access_token
	print("\n" + command_string + "\n")
	process = subprocess.run([command_string], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
	output = process.stdout
	print(output)

# Example:
# $ curl -kXGET https://matrix.perthchat.org/_synapse/admin/v1/users/@PC-Admin:perthchat.org/joined_rooms?access_token=ACCESS_TOKEN

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

# Example:
# $ curl -kX PUT -H 'Content-Type: application/json' -d '{"password": "user_password","admin": false,"deactivated": false}' https://matrix.perthchat.org/_synapse/admin/v2/users/@billybob:perthchat.org?access_token=ACCESS_TOKEN

def create_multiple_accounts():
	print("Create multiple user accounts selected")
	user_list_location = input("\nPlease enter the path of the file containing a csv list of names: ")
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
			time.sleep(1)
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
		while x <= (len(data[0]) - 1):
			#print(data[0][x])
			deactivate_account(data[0][x])
			x += 1
			#print(x)
			time.sleep(1)
	if delete_confirmation == "n" or delete_confirmation == "N" or  delete_confirmation == "no" or  delete_confirmation == "No":
		print("\nExiting...\n")

def list_directory_rooms():
	command_string = "curl -kXGET https://" + homeserver_url + "/_matrix/client/r0/publicRooms?access_token=" + access_token
	print("\n" + command_string + "\n")
	process = subprocess.run([command_string], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
	output = process.stdout
	print(output)

# Example
# $ curl -kXGET https://matrix.perthchat.org/_matrix/client/r0/publicRooms?access_token=ACCESS_TOKEN

def remove_room_from_directory():
	internal_ID = input("\nEnter the internal id of the room you wish to remove from the directory (Example: !OLkDvaYjpNrvmwnwdj:matrix.org): ")
	command_string = "curl -kX PUT -H \'Content-Type: application/json\' -d \'{\"visibility\": \"private\"}\' \'https://" + homeserver_url + "/_matrix/client/r0/directory/list/room/" + internal_ID + "?access_token=" + access_token + "\'"
	print("\n" + command_string + "\n")
	process = subprocess.run([command_string], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
	output = process.stdout
	print(output)

# Example
# $ curl -kX PUT -H 'Content-Type: application/json' -d '{"visibility": "private"}' 'https://matrix.perthchat.org/_matrix/client/r0/directory/list/room/!DwUPBvNapIVecNllgt:perthchat.org?access_token=ACCESS_TOKEN'

def list_media_in_room():
	internal_ID = input("\nEnter the internal id of the room you want to get a list of media for (Example: !OLkDvaYjpNrvmwnwdj:matrix.org): ")
	command_string = "curl -kXGET https://" + homeserver_url + "/_synapse/admin/v1/room/" + internal_ID + "/media?access_token=" + access_token
	print("\n" + command_string + "\n")
	process = subprocess.run([command_string], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
	media_list_output = process.stdout
	print(media_list_output)
	print_file_list_choice = input("\n Do you want to write this list to a file? y/n? ")

	if print_file_list_choice == "y" or print_file_list_choice == "Y" or print_file_list_choice == "yes" or print_file_list_choice == "Yes":
		print_file_list_choice = "true"
	elif print_file_list_choice == "n" or print_file_list_choice == "N" or print_file_list_choice == "no" or print_file_list_choice == "No":
		print_file_list_choice = "false"
	else:
		print("Input invalid! Defaulting to 'No'.")
		print_file_list_choice = "false"

	if print_file_list_choice == "true":
		media_list_filename = open("media_list.txt","w+")
		media_list_filename.write(media_list_output)
		media_list_filename.close() 

	download_files_choice = input("\n Do you also want to download a copy of these media files? y/n? ")

	if download_files_choice == "y" or download_files_choice == "Y" or download_files_choice == "yes" or download_files_choice == "Yes":
		download_files_choice = "true"
	elif download_files_choice == "n" or download_files_choice == "N" or download_files_choice == "no" or download_files_choice == "No":
		download_files_choice = "false"
	else:
		print("Input invalid! Defaulting to 'No'.")
		download_files_choice = "false"

	if download_files_choice == "true":
		media_list_filename = open("media_list.txt", "r")
		media_list_filename_lines = media_list_filename.readlines()
		os.mkdir("./media-files")
		os.chdir("./media-files")
		count = 0
		# Strips the newline character 
		for line in media_list_filename_lines:
			if "mxc" in line:
				print(line)
				cleaned_line = line.replace('        "mxc://','')
				cleaned_line = cleaned_line.replace('",','')
				cleaned_line = cleaned_line.replace('"','')
				cleaned_line = cleaned_line.replace('\n','')
				print(cleaned_line)
				download_command = "wget https://" + homeserver_url + "/_matrix/media/r0/download/" + cleaned_line
				print(download_command)
				download_process = subprocess.run([download_command], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
		os.chdir("../")

# Example
# $ curl -kXGET https://matrix.perthchat.org/_synapse/admin/v1/room/<room_id>/media?access_token=ACCESS_TOKEN

# To access via web:
# https://matrix.perthchat.org/_matrix/media/r0/download/ + server_name + "/" + media_id

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

def purge_room():
	internal_ID = input("\nEnter the internal id of the room you want purge (Example: !OLkDvaYjpNrvmwnwdj:matrix.org): ")
	user_ID = input("\nPlease enter the local username that will create a 'muted violation room' for your users: ")
	new_room_name = input("\nPlease enter the room name of the muted violation room your users will be sent to: ")
	message = input("\nPlease enter the shutdown message that will be displayed to users: ")
	purge_choice = input("\n Do you want to purge the room? (This deletes all the room history from your database.) y/n? ")
	block_choice = input("\n Do you want to block the room? (This prevents your server users re-entering the room.) y/n? ")
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

	command_string = "curl -X POST -H 'Content-Type: application/json' -d '{\"new_room_user_id\": \"" + user_ID + "\",\"room_name\": \"" + new_room_name + "\",\"message\": \"" + message + "\",\"block\": " + block_choice + ",\"purge\": " + purge_choice + "}' \'https://" + homeserver_url + "/_synapse/admin/v1/rooms/" + internal_ID + "/delete?access_token=" + access_token + "\'"
	print("\n" + command_string + "\n")
	process = subprocess.run([command_string], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
	output = process.stdout
	print(output)

# Example:
# $ curl -X POST -H 'Content-Type: application/json' -d '{"new_room_user_id": "@PC-Admin:perthchat.org","room_name": "VIOLATION ROOM 2","message": "You have been very naughty!","block": true,"purge": true}' 'https://matrix.perthchat.org/_synapse/admin/v1/rooms/!mPfaFTrXqUJsgrldwu:perthchat.org/delete?access_token=ACCESS_TOKEN


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

# Exmaple:
# $ date --date '149 days ago' +%s
# 1589442217
# $ curl -X POST --header "Authorization: Bearer ACCESS_TOKEN" 'https://matrix.perthchat.org/_synapse/admin/v1/purge_media_cache?before_ts=1589439628000'


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

# loop menu for various moderation actions

pass_token = False
while pass_token == False:
	menu_input = input('\nPlease select one of the following options:\n#### User Account Commands ####\n1) Deactivate a user account.\n2) Create a user account.\n3) Query user account.\n4) Reset a users password.\n5) Promote a user to server admin.\n6) List all user accounts.\n7) List room memberships of user.\n8) Create multiple user accounts.\n9) Deactivate multiple user accounts.\n10) Quarantine all media a users uploaded\n#### Room Commands ####\n11) List rooms in public directory.\n12) Remove a room from the public directory.\n13) List/Download all media in a room.\n14) Quarantine all media in a room..\n15) Purge a room.\n#### Server Commands ####\n16) Purge Remote Media Repository up to a certain date.\n(\'q\' or \'e\') Exit.\n\n')
	if menu_input == "1":
		deactivate_account('')
	elif menu_input == "2":
		create_account('','')
	elif menu_input == "3":
		query_account()
	elif menu_input == "4":
		reset_password()
	elif menu_input == "5":
		set_user_server_admin()
	elif menu_input == "6":
		list_accounts()
	elif menu_input == "7":
		list_joined_rooms()
	elif menu_input == "8":
		create_multiple_accounts()
	elif menu_input == "9":
		deactivate_multiple_accounts()
	elif menu_input == "10":
		quarantine_users_media()
	elif menu_input == "11":
		list_directory_rooms()
	elif menu_input == "12":
		remove_room_from_directory()
	elif menu_input == "13":
		list_media_in_room()
	elif menu_input == "14":
		quarantine_media_in_room()
	elif menu_input == "15":
		purge_room()
	elif menu_input == "16":
		purge_remote_media_repo()
	elif menu_input == "q" or menu_input == "Q" or menu_input == "e" or menu_input == "E":
		print("\nExiting...\n")
		pass_token = True
	else:
		print("\nIncorrect input detected, please select a number from 1 to 14!\n")
