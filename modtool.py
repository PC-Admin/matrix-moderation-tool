
# modtool.py
# an easy moderation tool for matrix/synapse
#
# created by @PC-Admin:perthchat.org
#
# This work is licensed under LGPLv3, for more information see: https://www.gnu.org/licenses/lgpl-3.0.txt
#
# To do:
# https://github.com/matrix-org/synapse/blob/master/docs/admin_api/delete_group.md
# https://github.com/matrix-org/synapse/blob/master/docs/admin_api/purge_room.md
# https://github.com/matrix-org/synapse/blob/master/docs/admin_api/purge_remote_media.rst
# https://github.com/matrix-org/synapse/blob/develop/docs/admin_api/media_admin_api.md#list-all-media-in-a-room

import subprocess
import csv
import time
import os

###########################################################################
# These values can be hard coded for easier usage:                        #
server_url = "example.org"
access_token = ""
federation_port = "8448"
###########################################################################

def parse_username(username):
	tail_end = ':' + server_url
	username = username.replace('@','')
	username = username.replace(tail_end,'')
	return username

def deactivate_account(preset_username):
	if len(preset_username) == 0:
		username = input("\nPlease enter the username to deactivate: ")
		username = parse_username(username)
	else:
		username = parse_username(preset_username)
	command_string = "curl -kX POST -H 'Content-Type: application/json' -d '{\"erase\": true}' https://" + server_url + ":" + str(federation_port) + "/_matrix/client/r0/admin/deactivate/@" + username + ":" + server_url + "?access_token=" + access_token
	print("\n" + command_string + "\n")
	process = subprocess.run([command_string], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
	output = process.stdout
	print(output)

# Example:
# $ curl -kX POST -H 'Content-Type: application/json' -d '{"erase": true}' https://perthchat.org/_matrix/client/r0/admin/deactivate/@billybob:perthchat.org?access_token=ACCESS_TOKEN

def reset_password():
	username = input("\nPlease enter the username for the password reset: ")
	password = input("Please enter the password to set: ")
	username = parse_username(username)
	command_string = "curl -kX POST -H 'Content-Type: application/json' -d '{\"new_password\": \"" + password + "\"}' https://" + server_url + ":" + str(federation_port) + "/_matrix/client/r0/admin/reset_password/@" + username + ":" + server_url + "?access_token=" + access_token
	print("\n" + command_string + "\n")
	process = subprocess.run([command_string], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
	output = process.stdout
	print(output)

# Example:
# $ curl -kX POST -H 'Content-Type: application/json' -d '{"new_password": "dogpoo"}' https://perthchat.org/_matrix/client/r0/admin/reset_password/@dogpoo:perthchat.org?access_token=ACCESS_TOKEN

def set_user_server_admin():
	# tried setting 'admin: false' here but it failed and promoted the user instead!
	print("\nBe aware that you need to set at least 1 user to server admin already by editing the database in order to use this command. See https://github.com/PC-Admin/PC-Admins-Synapse-Moderation-Tool/blob/master/README.md for details on how to do this.")
	username = input("\nPlease enter the username you want to promote to server admin: ")
	username = parse_username(username)
	passthrough = 0
	server_admin_result = "true"
	
	command_string = "curl -kX PUT -H 'Content-Type: application/json' -d '{\"admin\": \"" + server_admin_result + "\"}' https://" + server_url + ":" + str(federation_port) + "/_synapse/admin/v2/users/@" + username + ":" + server_url + "?access_token=" + access_token
	print("\n" + command_string + "\n")
	process = subprocess.run([command_string], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
	output = process.stdout
	print(output)

# Example:
# $ curl -kX POST -H 'Content-Type: application/json' -d '{"admin": "true"}' https://perthchat.org/_synapse/admin/v2/users/@dogpoo:perthchat.org?access_token=ACCESS_TOKEN

def query_account():
	username = input("\nPlease enter the username you wish to query: ")
	username = parse_username(username)
	command_string = "curl -kXGET https://" + server_url + ":" + str(federation_port) + "/_matrix/client/r0/admin/whois/@" + username + ":" + server_url + "?access_token=" + access_token
	print("\n" + command_string + "\n")
	process = subprocess.run([command_string], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
	output = process.stdout
	print(output)

# Example:
# $ curl -kXGET https://perthchat.org/_matrix/client/r0/admin/whois/@PC-Admin:perthchat.org?access_token=ACCESS_TOKEN

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

	command_string = "curl -kXGET \"https://" + server_url + ":" + str(federation_port) + "/_synapse/admin/v2/users?from=0&limit=1000000&" + guest_string + "&" + deactivated_string + "&access_token=" + access_token + "\""
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
# $ curl -kXGET "https://perthchat.org/_synapse/admin/v2/users?from=0&limit=10&guests=false&access_token=ACCESS_TOKEN"

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
	command_string = "curl -kX PUT -H 'Content-Type: application/json' -d '{\"password\": \"" + user_password + "\"}' https://" + server_url + ":" + str(federation_port) + "/_synapse/admin/v2/users/@" + username + ":" + server_url + "?access_token=" + access_token
	print("\n" + command_string + "\n")
	process = subprocess.run([command_string], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
	output = process.stdout
	print(output)

# Example:
# $ curl -kX PUT -H 'Content-Type: application/json' -d '{"password": "user_password","admin": false,"deactivated": false}' https://perthchat.org/_synapse/admin/v2/users/@billybob:perthchat.org?access_token=ACCESS_TOKEN

# needed to map /_synapse/ too!

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
	command_string = "curl -kX GET https://" + server_url + ":" + str(federation_port) + "/_matrix/client/r0/publicRooms?access_token=" + access_token
	print("\n" + command_string + "\n")
	process = subprocess.run([command_string], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
	output = process.stdout
	print(output)

# Example
# $ curl -kX GET https://perthchat.org/_matrix/client/r0/publicRooms?access_token=ACCESS_TOKEN

def remove_room_from_directory():
	internal_ID = input("\nEnter the internal id of the room you wish to remove from the directory (Example: !OLkDvaYjpNrvmwnwdj:matrix.org): ")
	command_string = "curl -kX PUT -H \'Content-Type: application/json\' -d \'{\"visibility\": \"private\"}\' \'https://" + server_url + ":" + str(federation_port) + "/_matrix/client/r0/directory/list/room/" + internal_ID + "?access_token=" + access_token + "\'"
	print("\n" + command_string + "\n")
	process = subprocess.run([command_string], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
	output = process.stdout
	print(output)

# Example
# $ curl -kX PUT -H 'Content-Type: application/json' -d '{"visibility": "private"}' 'https://perthchat.org/_matrix/client/r0/directory/list/room/!DwUPBvNapIVecNllgt:perthchat.org?access_token=ACCESS_TOKEN'

def list_media_in_room():
	internal_ID = input("\nEnter the internal id of the room you want to get a list of media for (Example: !OLkDvaYjpNrvmwnwdj:matrix.org): ")
	command_string = "curl -kX GET https://" + server_url + ":" + str(federation_port) + "/_synapse/admin/v1/room/" + internal_ID + "/media?access_token=" + access_token
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
				download_command = "wget https://" + server_url + "/_matrix/media/r0/download/" + cleaned_line
				print(download_command)
				download_process = subprocess.run([download_command], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
		os.chdir("../")

# Example
# $ curl -kX GET https://perthchat.org/_synapse/admin/v1/room/<room_id>/media?access_token=ACCESS_TOKEN

# To access via web:
# https://perthchat.org/_matrix/media/r0/download/ + server_name + "/" + media_id

def quarantine_media_in_room():
	internal_ID = input("\nEnter the internal id of the room you want to quarantine, this makes local and remote data inaccessible (Example: !OLkDvaYjpNrvmwnwdj:matrix.org): ")
	command_string = "curl -kX PUT \'https://" + server_url + ":" + str(federation_port) + "/_synapse/admin/v1/room/" + internal_ID + "/media/quarantine?access_token=" + access_token
	print("\n" + command_string + "\n")
	process = subprocess.run([command_string], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
	output = process.stdout
	print(output)

# UNTESTED

# Example
# $ curl -kX PUT 'https://perthchat.org/_synapse/admin/v1/room/!DwUPBvNapIVecNllgt:perthchat.org/media/quarantine?access_token=ACCESS_TOKEN'

def quarantine_users_media():
	username = input("\nPlease enter the username of the user who's media you want to quarantine: ")
	username = parse_username(username)
	command_string = "curl -kX PUT https://" + server_url + ":" + str(federation_port) + "/_synapse/admin/v1/user/@" + username + ":" + server_url + "/media/quarantine?access_token=" + access_token
	print("\n" + command_string + "\n")
	process = subprocess.run([command_string], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
	output = process.stdout
	print(output)

# UNTESTED

# Example:
# $ curl -kX PUT https://perthchat.org/_synapse/admin/v1/user/@PC-Admin:perthchat.org/media/quarantine?access_token=ACCESS_TOKEN


# check if url is hard coded, if not set it

if server_url == "example.org":
	server_url = input("What is the URL of your server? Eg: example.org ")

# check if access token is hard coded, if not set it

length_access_token = len(access_token)

if length_access_token == 0:
	access_token = input("Please enter access token for server admin account: ")

# check is federation port is hard coded, if not set it

if len(federation_port) == 0:
	federation_port = input("Please enter the federation port for the server (default is 8448): ")

# loop menu for various moderation actions

pass_token = False
while pass_token == False:
	menu_input = input('\nPlease select one of the following options:\n\n1) Deactivate a user account.\n2) Create a user account.\n3) Query user account.\n4) Reset a users password.\n5) Promote a user to server admin.\n6) List all user accounts.\n7) Create multiple user accounts.\n8) Deactivate multiple user accounts.\n9) List rooms in public directory.\n10) Remove a room from the public directory.\n11) List/Download all media in a room.\n12) Quarantine all media in a room.\n13) Quarantine all media a users uploaded.\n(\'q\' or \'e\') Exit.\n\n')
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
		create_multiple_accounts()
	elif menu_input == "8":
		deactivate_multiple_accounts()
	elif menu_input == "9":
		list_directory_rooms()
	elif menu_input == "10":
		remove_room_from_directory()
	elif menu_input == "11":
		list_media_in_room()
	elif menu_input == "12":
		quarantine_media_in_room()
	elif menu_input == "13":
		quarantine_users_media()
	elif menu_input == "q" or menu_input == "Q" or menu_input == "e" or menu_input == "E":
		print("\nExiting...\n")
		pass_token = True
	else:
		print("\nIncorrect input detected, please select a number from 1 to 11!\n")
