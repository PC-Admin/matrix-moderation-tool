
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

import subprocess
import csv
import time

# These values can be hard coded for easier usage:
server_url = "example.org"
access_token = ""
federation_port = ""

def append_username(username):
	if username[0] == "@":
		return username
	elif username[0] != "@":
		username = "@" + username
		return username

def deactivate_account(preset_username):
	if len(preset_username) == 0:
		username = input("\nPlease enter the username to deactivate: ")
		username = append_username(username)
	else:
		username = append_username(preset_username)
	command_string = "curl -kX POST -H 'Content-Type: application/json' -d '{\"erase\": true}' https://" + server_url + ":" + str(federation_port) + "/_matrix/client/r0/admin/deactivate/" + username + ":" + server_url + "?access_token=" + access_token
	print("\n" + command_string + "\n")
	process = subprocess.run([command_string], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
	output = process.stdout
	print(output)

# Example:
# $ curl -kX POST -H 'Content-Type: application/json' -d '{"erase": true}' https://perthchat.org/_matrix/client/r0/admin/deactivate/@billybob:perthchat.org?access_token=ACCESS_TOKEN

def reset_password():
	username = input("\nPlease enter the username for the password reset: ")
	password = input("Please enter the password to set: ")
	username = append_username(username)
	command_string = "curl -kX POST -H 'Content-Type: application/json' -d '{\"new_password\": \"" + password + "\"}' https://" + server_url + ":" + str(federation_port) + "/_matrix/client/r0/admin/reset_password/" + username + ":" + server_url + "?access_token=" + access_token
	print("\n" + command_string + "\n")
	process = subprocess.run([command_string], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
	output = process.stdout
	print(output)

# Example:
# $ curl -kX POST -H 'Content-Type: application/json' -d '{"new_password": "dogpoo"}' https://perthchat.org/_matrix/client/r0/admin/reset_password/@dogpoo:perthchat.org?access_token=ACCESS_TOKEN

def query_account():
	username = input("\nPlease enter the username you wish to query: ")
	username = append_username(username)
	command_string = "curl -kXGET https://" + server_url + ":" + str(federation_port) + "/_matrix/client/r0/admin/whois/" + username + ":" + server_url + "?access_token=" + access_token
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
		username = append_username(username)
		user_password = input("Please enter the password for this account: ")
	elif len(preset_username) > 0 and len(preset_password) > 0:
		username = append_username(preset_username)
		user_password = preset_password
	else:
		print("\nError with user/pass file data, skipping...\n")
	command_string = "curl -kX PUT -H 'Content-Type: application/json' -d '{\"password\": \"" + user_password + "\"}' https://" + server_url + ":" + str(federation_port) + "/_synapse/admin/v2/users/" + username + ":" + server_url + "?access_token=" + access_token
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
	internal_ID = input("\nEnter the internal id of the room you wish to remove from the directory (Example: !rapAelwZkajRyeZIpm): ")
	command_string = "curl -kX PUT -H \'Content-Type: application/json\' -d \'{\"visibility\": \"private\"}\' \'https://" + server_url + ":" + str(federation_port) + "/_matrix/client/r0/directory/list/room/" + internal_ID + ":" + server_url + "?access_token=" + access_token + "\'"
	print("\n" + command_string + "\n")
	process = subprocess.run([command_string], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
	output = process.stdout
	print(output)

# Example
# $ curl -kX PUT -H 'Content-Type: application/json' -d '{"visibility": "private"}' 'https://perthchat.org/_matrix/client/r0/directory/list/room/!DwUPBvNapIVecNllgt:perthchat.org?access_token=ACCESS_TOKEN'


# check if url is hard coded, if not set it

if server_url == "example.org":
	server_url = input("What is the URL of your server? Eg: example.org ")

# check if access token is hard coded, if not set it

length_access_token = len(access_token)

if length_access_token == 0:
	access_token = input("Please enter access token for server admin account: ")

# check is federation port is hard coded, if not set it

if federation_port == 0:
	federation_port = input("Please enter the federation port for the server (default is 8448): ")

# loop menu for various moderation actions

pass_token = False
while pass_token == False:
	menu_input = input('\nPlease select one of the following options:\n\n1) Deactivate a user account.\n2) Create a user account.\n3) Query user account.\n4) Reset a users password.\n5) List all user accounts.\n6) Create multiple user accounts.\n7) Deactivate multiple user accounts.\n8) List rooms in public directory.\n9) Remove a room from the public directory.\n10) Exit.\n\n')
	if menu_input == "1":
		deactivate_account('')
	elif menu_input == "2":
		create_account('','')
	elif menu_input == "3":
		query_account()
	elif menu_input == "4":
		reset_password()
	elif menu_input == "5":
		list_accounts()
	elif menu_input == "6":
		create_multiple_accounts()
	elif menu_input == "7":
		deactivate_multiple_accounts()
	elif menu_input == "8":
		list_directory_rooms()
	elif menu_input == "9":
		remove_room_from_directory()
	elif menu_input == "10":
		print("\nExiting...\n")
		pass_token = True
	else:
		print("\nIncorrect input detected, please select a number from 1 to 4!\n")
