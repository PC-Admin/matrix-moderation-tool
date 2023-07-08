
import subprocess
import time
import csv
import hardcoded_variables

def parse_username(username):
	tail_end = ':' + hardcoded_variables.base_url
	username = username.replace('@','')
	username = username.replace(tail_end,'')
	return username

def deactivate_account(preset_username):
	if len(preset_username) == 0:
		username = input("\nPlease enter the username to deactivate: ")
		username = parse_username(username)
	else:
		username = parse_username(preset_username)
	command_string = "curl -X POST -H \"Authorization: Bearer " + hardcoded_variables.access_token + "\" 'https://" + hardcoded_variables.homeserver_url + "/_synapse/admin/v1/deactivate/@" + username + ":" + hardcoded_variables.base_url + "' --data '{\"erase\": true}'"
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
	command_string = "curl -X POST -H 'Content-Type: application/json' -d '{\"new_password\": \"" + password + "\", \"logout_devices\": true}' https://" + hardcoded_variables.homeserver_url + "/_synapse/admin/v1/reset_password/@" + username + ":" + hardcoded_variables.base_url + "?access_token=" + hardcoded_variables.access_token
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
	
	command_string = "curl -X PUT -H 'Content-Type: application/json' -d '{\"admin\": \"" + server_admin_result + "\"}' https://" + hardcoded_variables.homeserver_url + "/_synapse/admin/v1/users/@" + username + ":" + hardcoded_variables.base_url + "/admin?access_token=" + hardcoded_variables.access_token
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
	command_string = "curl -kXGET https://" + hardcoded_variables.homeserver_url + "/_matrix/client/r0/admin/whois/@" + username + ":" + hardcoded_variables.base_url + "?access_token=" + hardcoded_variables.access_token
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
	command_string = "curl -kXGET https://" + hardcoded_variables.homeserver_url + "/_synapse/admin/v1/users/@" + username + ":" + hardcoded_variables.base_url + "/joined_rooms?access_token=" + hardcoded_variables.access_token
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

	command_string = "curl -kXGET \"https://" + hardcoded_variables.homeserver_url + "/_synapse/admin/v2/users?from=0&limit=1000000&" + guest_string + "&" + deactivated_string + "&access_token=" + hardcoded_variables.access_token + "\""
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
	command_string = "curl -kX GET https://" + hardcoded_variables.homeserver_url + "/_synapse/admin/v2/users/@" + username + ":" + hardcoded_variables.base_url + "?access_token=" + hardcoded_variables.access_token
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
	command_string = "curl -kX PUT -H 'Content-Type: application/json' -d '{\"password\": \"" + user_password + "\"}' https://" + hardcoded_variables.homeserver_url + "/_synapse/admin/v2/users/@" + username + ":" + hardcoded_variables.base_url + "?access_token=" + hardcoded_variables.access_token
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

def quarantine_users_media():
	username = input("\nPlease enter the username of the user who's media you want to quarantine: ")
	username = parse_username(username)
	command_string = "curl -X POST \'https://" + hardcoded_variables.homeserver_url + "/_synapse/admin/v1/user/@" + username + ":" + hardcoded_variables.base_url + "/media/quarantine?access_token=" + hardcoded_variables.access_token + "\'"
	print("\n" + command_string + "\n")
	process = subprocess.run([command_string], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
	output = process.stdout
	print(output)

# Example:
# $ curl -X POST https://matrix.perthchat.org/_synapse/admin/v1/user/@PC-Admin:perthchat.org/media/quarantine?access_token=ACCESS_TOKEN