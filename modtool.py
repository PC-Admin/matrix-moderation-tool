
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
import requests
import json
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

#def deactivate_account(preset_username):
#	if len(preset_username) == 0:
#		username = input("\nPlease enter the username to deactivate: ")
#		username = parse_username(username)
#	else:
#		username = parse_username(preset_username)
#	command_string = "curl -X POST -H \"Authorization: Bearer " + access_token + "\" 'https://" + homeserver_url + "/_synapse/admin/v1/deactivate/@" + username + ":" + base_url + "' --data '{\"erase\": true}'"
#	print("\n" + command_string + "\n")
#	process = subprocess.run([command_string], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
#	output = process.stdout
#	print(output)


def deactivate_account(preset_username):
	if len(preset_username) == 0:
		username = input("\nPlease enter the username to deactivate: ")
		username = parse_username(username)
	else:
		username = parse_username(preset_username)
	deactivate_url = "https://" + homeserver_url + "/_synapse/admin/v1/deactivate/@" + username + ":" + base_url
	request_header = { "Authorization": 'Bearer ' + access_token }
	request_data = { "erase": True }
	deactivate = requests.post(deactivate_url, headers=request_header, json=request_data)
	print( '\nRequest .status_code: ' + str(deactivate.status_code) )
	print( 'Request .text: ' + deactivate.text )

# Example:
# $ curl -X POST -H "Authorization: Bearer ACCESS_TOKEN" "https://matrix.perthchat.org/_synapse/admin/v1/deactivate/@billybob:perthchat.org" --data '{"erase": true}'

#def reset_password():
#	username = input("\nPlease enter the username for the password reset: ")
#	password = input("Please enter the password to set: ")
#	username = parse_username(username)
#	command_string = "curl -X POST -H 'Content-Type: application/json' -d '{\"new_password\": \"" + password + "\", \"logout_devices\": true}' https://" + homeserver_url + "/_synapse/admin/v1/reset_password/@" + username + ":" + base_url + "?access_token=" + access_token
#	print("\n" + command_string + "\n")
#	process = subprocess.run([command_string], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
#	output = process.stdout
#	print(output)

def reset_password():
	username = input("\nPlease enter the username for the password reset: ")
	password = input("Please enter the password to set: ")
	username = parse_username(username)
	reset_url = "https://" + homeserver_url + "/_synapse/admin/v1/reset_password/@" + username + ":" + base_url
	request_header = { "Authorization": 'Bearer ' + access_token }
	request_data = { "new_password": password, "logout_devices": True }
	reset_password = requests.post(reset_url, headers=request_header, json=request_data)
	print( '\nRequest .status_code: ' + str(reset_password.status_code) )
	print( 'Request .text: ' + reset_password.text )

# Example:
# $ curl -X POST -H 'Content-Type: application/json' -d '{"new_password": "dogpoo", "logout_devices": true}' https://matrix.perthchat.org/_synapse/admin/v1/reset_password/@dogpoo:perthchat.org?access_token=ACCESS_TOKEN

#def set_user_server_admin():
	# tried setting 'admin: false' here but it failed and promoted the user instead!
#	print("\nBe aware that you need to set at least 1 user to server admin already by editing the database in order to use this command. See https://github.com/PC-Admin/PC-Admins-Synapse-Moderation-Tool/blob/master/README.md for details on how to do this.")
#	username = input("\nPlease enter the username you want to promote to server admin: ")
#	username = parse_username(username)
#	passthrough = 0
#	server_admin_result = "true"
	
#	command_string = "curl -X PUT -H 'Content-Type: application/json' -d '{\"admin\": \"" + server_admin_result + "\"}' https://" + homeserver_url + "/_synapse/admin/v1/users/@" + username + ":" + base_url + "/admin?access_token=" + access_token
#	print("\n" + command_string + "\n")
#	process = subprocess.run([command_string], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
#	output = process.stdout
#	print(output)

def set_user_server_admin():
	# tried setting 'admin: false' here but it failed and promoted the user instead!
	print("\nBe aware that you need to set at least 1 user to server admin already by editing the database in order to use this command. See https://github.com/PC-Admin/PC-Admins-Synapse-Moderation-Tool/blob/master/README.md for details on how to do this.")
	username = input("\nPlease enter the username you want to promote/demote to/from server admin: ")
	server_admin_result_raw = input("\nDo you want this user to be a server admin? yes/no? ")
	username = parse_username(username)
	if server_admin_result_raw == "y" or server_admin_result_raw == "yes" or server_admin_result_raw == "Y" or server_admin_result_raw == "Yes" or server_admin_result_raw == "YES":
		request_data = { "admin": "true" }
	elif server_admin_result_raw == "n" or server_admin_result_raw == "no" or server_admin_result_raw == "N" or server_admin_result_raw == "No" or server_admin_result_raw == "NO":
		request_data = { "admin": "false" }
	else:
		print("Input not recognised, aborting command.")
		return
	set_server_admin_url = "https://" + homeserver_url + "/_synapse/admin/v1/users/@" + username + ":" + base_url + "/admin"
	request_header = { "Authorization": 'Bearer ' + access_token }
	set_server_admin = requests.post(set_server_admin_url, headers=request_header, json=request_data)
	print( '\nRequest .status_code: ' + str(set_server_admin.status_code) )
	print( 'Request .text: ' + set_server_admin.text )
	
#### ^ THIS ISN'T WORKING ####

# Example:
# $ curl -kX POST -H 'Content-Type: application/json' -d '{"admin": "true"}' https://matrix.perthchat.org/_synapse/admin/v2/users/@dogpoo:perthchat.org?access_token=ACCESS_TOKEN

def query_account(preset_username):
	if preset_username == '':
		username = input("\nPlease enter the username you wish to query: ")
	elif preset_username != '':
		username = preset_username
	username = parse_username(username)
	query_account_url = "https://" + homeserver_url + "/_matrix/client/r0/admin/whois/@" + username + ":" + base_url
	request_header = { "Authorization": 'Bearer ' + access_token }
	query_account = requests.get(query_account_url, headers=request_header)
	print( '\nRequest .status_code: ' + str(query_account.status_code) )
	print( 'Request .text: ' + query_account.text )

#	command_string = "curl -kXGET https://" + homeserver_url + "/_matrix/client/r0/admin/whois/@" + username + ":" + base_url + "?access_token=" + access_token
	#print("\n" + command_string + "\n")
#	process = subprocess.run([command_string], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
#	output = process.stdout
#	print(output + "\n")

# Example:
# $ curl -kXGET https://matrix.perthchat.org/_matrix/client/r0/admin/whois/@PC-Admin:perthchat.org?access_token=ACCESS_TOKEN

def list_joined_rooms(preset_username):
	if preset_username == '':
		username = input("\nPlease enter the username you wish to query: ")
	elif preset_username != '':
		username = preset_username
	username = parse_username(username)
	list_joined_rooms_url = "https://" + homeserver_url + "/_synapse/admin/v1/users/@" + username + ":" + base_url + "/joined_rooms"
	request_header = { "Authorization": 'Bearer ' + access_token }
	list_joined_rooms = requests.get(list_joined_rooms_url, headers=request_header)
	print( '\nRequest .status_code: ' + str(list_joined_rooms.status_code) )
	print( 'Request .text: ' + list_joined_rooms.text )

#	command_string = "curl -kXGET https://" + homeserver_url + "/_synapse/admin/v1/users/@" + username + ":" + base_url + "/joined_rooms?access_token=" + access_token
	#print("\n" + command_string + "\n")
#	process = subprocess.run([command_string], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
#	output = process.stdout
#	print(output + "\n")

# Example:
# $ curl -kXGET https://matrix.perthchat.org/_synapse/admin/v1/users/@PC-Admin:perthchat.org/joined_rooms?access_token=ACCESS_TOKEN

def query_multiple_accounts():
	print("Query multiple user accounts selected")
	user_list_location = input("\nPlease enter the path of the file containing a newline seperated list of Matrix usernames: ")
	with open(user_list_location, newline='') as f:
		reader = csv.reader(f)
		data = list(reader)
		print(len(data))
	query_confirmation = input("\n" + str(data) + "\n\nAre you sure you want to query all of these users? y/n?\n")
	if query_confirmation == "y" or query_confirmation == "Y" or query_confirmation == "yes" or query_confirmation == "Yes":  
		x = 0
		while x <= (len(data) - 1):
			print(data[x][0])
			query_account(data[x][0])
			list_joined_rooms(data[x][0])
			x += 1
			#print(x)
			time.sleep(1)
	if query_confirmation == "n" or query_confirmation == "N" or query_confirmation == "no" or query_confirmation == "No":
		print("\nExiting...\n")

def list_accounts():
	deactivated_choice = input("Do you want to include deactivated accounts y/n? ")
	guest_choice = input("Do you want to include guest accounts y/n? ")

	if deactivated_choice == "y" or deactivated_choice == "Y" or deactivated_choice == "yes" or deactivated_choice == "Yes":
		deactivated_string = "&deactivated=true"
	elif deactivated_choice == "n" or deactivated_choice == "N" or deactivated_choice == "no" or deactivated_choice == "No":
		deactivated_string = "&deactivated=false"
	else:
		print("Input invalid! Defaulting to false.")
		deactivated_string = "&deactivated=false"

	if guest_choice == "y" or guest_choice == "Y" or guest_choice == "yes" or guest_choice == "Yes":
		guest_string = "&guests=true"
	elif guest_choice == "n" or guest_choice == "N" or guest_choice == "no" or guest_choice == "No":
		guest_string = "&guests=false"
	else:
		print("Input invalid! Defaulting to false.")
		guest_string = "&guests=false"

	list_accounts_url = "https://" + homeserver_url + "/_synapse/admin/v2/users?from=0" + guest_string + deactivated_string
	request_header = { "Authorization": 'Bearer ' + access_token }
	#request_data = { "guest": guest_string, "deactivate": deactivated_string }
	list_accounts = requests.get(list_accounts_url, headers=request_header)
	print( '\nRequest .status_code: ' + str(list_accounts.status_code) )
	print( 'Request .text: ' + list_accounts.text )

#	command_string = "curl -kXGET \"https://" + homeserver_url + "/_synapse/admin/v2/users?from=0&limit=1000000&" + guest_string + "&" + deactivated_string + "&access_token=" + access_token + "\""
#	print("\n" + command_string + "\n")
#	process = subprocess.run([command_string], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
#	output = process.stdout
	list_accounts_json = list_accounts.json()
	number_of_users = list_accounts_json['total']
	#
	print("\nTotal amount of users: " + str(number_of_users))
	if number_of_users < 100:	
		print(output)
	elif number_of_users >= 100:
		accounts_output_file = input("\nThere are too many users to list here, please specify a filename to print this data too: ")
		f = open(accounts_output_file, "a")
		for i in range(0, number_of_users, 100):
			list_accounts_url = "https://" + homeserver_url + "/_synapse/admin/v2/users?from=" + str(i) + guest_string + deactivated_string
			#request_data = { "guest": guest_string, "deactivate": deactivated_string }
			list_accounts = requests.get(list_accounts_url, headers=request_header)
			f.write("\n")
			f.write(list_accounts.text)
		f.close()
	print("Done!\n")

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
	
	create_account_url = "https://" + homeserver_url + "/_synapse/admin/v2/users/@" + username + ":" + base_url
	request_header = { "Authorization": 'Bearer ' + access_token }
	request_data = { "password": user_password ,"admin": False, "deactivated": False }
	create_account = requests.get(create_account_url, headers=request_header, data=request_data)
	print( '\nRequest .status_code: ' + str(create_account.status_code) )
	print( 'Request .text: ' + create_account.text )	
	#command_string = "curl -kX PUT -H 'Content-Type: application/json' -d '{\"password\": \"" + user_password + "\"}' https://" + homeserver_url + "/_synapse/admin/v2/users/@" + username + ":" + base_url + "?access_token=" + access_token
	#print("\n" + command_string + "\n")
	#process = subprocess.run([command_string], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
	#output = process.stdout
	#print(output)

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
	user_list_location = input("\nPlease enter the path of the file containing a newline seperated list of names: ")
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

def purge_room(preset_internal_ID,preset_user_ID,preset_new_room_name,preset_message,preset_purge_choice,preset_block_choice):
	if preset_internal_ID == '':
		internal_ID = input("\nEnter the internal id of the room you want purge (Example: !OLkDvaYjpNrvmwnwdj:matrix.org): ")
	elif preset_internal_ID != '':
		internal_ID = preset_internal_ID
	if preset_user_ID == '':
		user_ID = input("\nPlease enter the local username that will create a 'muted violation room' for your users: ")
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
		purge_choice = input("\n Do you want to purge the room? (This deletes all the room history from your database.) y/n? ")
	elif preset_purge_choice != '':
		purge_choice = preset_purge_choice
	if preset_block_choice == '':
		block_choice = input("\n Do you want to block the room? (This prevents your server users re-entering the room.) y/n? ")
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

	command_string = "curl -X POST -H 'user-agent: anything' -d '{\"new_room_user_id\": \"@" + username + ":" + base_url + "\",\"room_name\": \"" + new_room_name + "\",\"message\": \"" + message + "\",\"block\": " + block_choice + ",\"purge\": " + purge_choice + "}' \'https://" + homeserver_url + "/_synapse/admin/v1/rooms/" + internal_ID + "/delete?access_token=" + access_token + "\'"
	print("\n" + command_string + "\n")
	process = subprocess.run([command_string], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
	output = process.stdout
	print(output)

# Example:
# $ curl -X POST -H 'Content-Type: application/json' -d '{"new_room_user_id": "@PC-Admin:perthchat.org","room_name": "VIOLATION ROOM 2","message": "You have been very naughty!","block": true,"purge": true}' 'https://matrix.perthchat.org/_synapse/admin/v1/rooms/!mPfaFTrXqUJsgrldwu:perthchat.org/delete?access_token=ACCESS_TOKEN

def purge_multiple_rooms():
	print("Purge multiple rooms selected")
	purge_list_location = input("\nPlease enter the path of the file containing a newline seperated list of room ids: ")
	with open(purge_list_location, newline='') as f:
    		reader = csv.reader(f)
    		data = list(reader)
	preset_user_ID = input("\nPlease enter the local username that will create a 'muted violation room' for your users: ")
	preset_new_room_name = input("\nPlease enter the room name of the muted violation room your users will be sent to: ")
	preset_message = input("\nPlease enter the shutdown message that will be displayed to users: ")
	preset_purge_choice = input("\n Do you want to purge these rooms? (This deletes all the room history from your database.) y/n? ")
	preset_block_choice = input("\n Do you want to block these rooms? (This prevents your server users re-entering the room.) y/n? ")
	purge_confirmation = input("\n" + str(data) + "\n\nAre you sure you want to purge and block these rooms? y/n?\n")
	#print(len(data[0]))
	#print(data[0][0])
	if purge_confirmation == "y" or purge_confirmation == "Y" or  purge_confirmation == "yes" or  purge_confirmation == "Yes":  
		x = 0
		while x <= (len(data) - 1):
			print(data[x][0])
			purge_room(data[x][0],preset_user_ID,preset_new_room_name,preset_message,preset_purge_choice,preset_block_choice)
			x += 1
			#print(x)
			time.sleep(10)

	if purge_confirmation == "n" or purge_confirmation == "N" or  purge_confirmation == "no" or  purge_confirmation == "No":
		print("\nExiting...\n")

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
	menu_input = input('\nPlease select one of the following options:\n#### User Account Commands ####\n1) Deactivate a user account.\n2) Create a user account.\n3) Query user account.\n4) List room memberships of user.\n5) Query multiple user accounts.\n6) Reset a users password.\n7) Promote/Demote a user to/from server admin.\n8) List all user accounts.\n9) Create multiple user accounts.\n10) Deactivate multiple user accounts.\n11) Quarantine all media a users uploaded.\n#### Room Commands ####\n12) List details of a room.\n13) List rooms in public directory.\n14) Remove a room from the public directory.\n15) Remove multiple rooms from the public directory.\n16) List/Download all media in a room.\n17) Download media from multiple rooms.\n18) Quarantine all media in a room.\n19) Purge a room.\n20) Purge multiple rooms.\n#### Server Commands ####\n21) Purge remote media repository up to a certain date.\n22) Prepare database for copying events of multiple rooms.\n(\'q\' or \'e\') Exit.\n\n')
	if menu_input == "1":
		deactivate_account('')
	elif menu_input == "2":
		create_account('','')
	elif menu_input == "3":
		query_account('')
	elif menu_input == "4":
		list_joined_rooms('')
	elif menu_input == "5":
		query_multiple_accounts()
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
		list_directory_rooms()
	elif menu_input == "14":
		remove_room_from_directory('')
	elif menu_input == "15":
		remove_multiple_rooms_from_directory()
	elif menu_input == "16":
		list_and_download_media_in_room('','','','./')
	elif menu_input == "17":
		download_media_from_multiple_rooms()
	elif menu_input == "18":
		quarantine_media_in_room()
	elif menu_input == "19":
		purge_room('','','','','','')
	elif menu_input == "20":
		purge_multiple_rooms()
	elif menu_input == "21":
		purge_remote_media_repo()
	elif menu_input == "22":
		prepare_database_copy_of_multiple_rooms()
	elif menu_input == "q" or menu_input == "Q" or menu_input == "e" or menu_input == "E":
		print("\nExiting...\n")
		pass_token = True
	else:
		print("\nIncorrect input detected, please select a number from 1 to 22!\n")
