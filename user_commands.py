
import os
import requests
import json
import time
import csv
import hardcoded_variables
import socket

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

	url = f"https://{hardcoded_variables.homeserver_url}/_synapse/admin/v1/deactivate/@{username}:{hardcoded_variables.base_url}"

	headers = {
		"Content-Type": "application/json",
		"Authorization": f"Bearer {hardcoded_variables.access_token}"
	}

	data = {
		"erase": True
	}

	print("\n" + url + "\n")
	response = requests.post(url, headers=headers, data=json.dumps(data), verify=True)

	if response.status_code in [200,201]:
		print("Successfully deactivated account.")
	else:
		print(f"Error deactivating account: {response.status_code}, {response.text}")

	return response.text

# Example:
# $ curl -X POST -H "Authorization: Bearer ACCESS_TOKEN" "https://matrix.perthchat.org/_synapse/admin/v1/deactivate/@billybob:perthchat.org" --data '{"erase": true}'

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

def create_account(preset_username, preset_password):
	if len(preset_username) == 0 and len(preset_password) == 0:
		username = input("\nPlease enter the username to create: ")
		username = parse_username(username)
		user_password = input("Please enter the password for this account: ")
	elif len(preset_username) > 0 and len(preset_password) > 0:
		username = parse_username(preset_username)
		user_password = preset_password
	else:
		print("\nError with user/pass file data, skipping...\n")
		return

	url = f"https://{hardcoded_variables.homeserver_url}/_synapse/admin/v2/users/@{username}:{hardcoded_variables.base_url}"
	url += f"?access_token={hardcoded_variables.access_token}"

	headers = {
		"Content-Type": "application/json"
	}

	data = {
		"password": user_password
	}

	#print("\n" + url + "\n")
	response = requests.put(url, headers=headers, data=json.dumps(data), verify=True)

	if response.status_code == 201:
		print("Successfully created account.")
	elif response.status_code == 200:
		print("Account already exists.")
	else:
		print(f"Error creating account: {response.status_code}, {response.text}")

	create_account_dict = json.loads(response.text)

	return create_account_dict

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

def reset_password(preset_username, preset_password):
	if len(preset_username) == 0 and len(preset_password) == 0:
		username = input("\nPlease enter the username for the password reset: ")
		password = input("Please enter the password to set: ")
	else:
		username = parse_username(preset_username)
		password = preset_password

	username = parse_username(username)

	url = f"https://{hardcoded_variables.homeserver_url}/_synapse/admin/v1/reset_password/@" + username + f":{hardcoded_variables.base_url}?access_token={hardcoded_variables.access_token}"

	headers = {'Content-Type': 'application/json'}
	data = {'new_password': password, 'logout_devices': True}

	#print("\n" + url + "\n")

	response = requests.post(url, headers=headers, data=json.dumps(data), verify=True)

	if response.status_code != 200:
		print(f"Error resetting password: {response.status_code}, {response.text}")

	reset_password_dict = json.loads(response.text)

	return reset_password_dict

# Example:
# $ curl -X POST -H 'Content-Type: application/json' -d '{"new_password": "dogpoo", "logout_devices": true}' https://matrix.perthchat.org/_synapse/admin/v1/reset_password/@dogpoo:perthchat.org?access_token=ACCESS_TOKEN

def set_user_server_admin(preset_username):
	if len(preset_username) == 0:
		print("\nBe aware that you need to set at least 1 user to server admin already by editing the database in order to use this command. See https://github.com/PC-Admin/PC-Admins-Synapse-Moderation-Tool/blob/master/README.md for details on how to do this.")
		username = input("\nPlease enter the username you want to promote to server admin: ")
		username = parse_username(username)
	elif len(preset_username) > 0:
		username = parse_username(preset_username)

	# tried setting 'admin: false' here but it failed and promoted the user instead!
	server_admin_result = "true"

	url = f"https://{hardcoded_variables.homeserver_url}/_synapse/admin/v1/users/@{username}:{hardcoded_variables.base_url}/admin"
	url += f"?access_token={hardcoded_variables.access_token}"

	headers = {
		"Content-Type": "application/json"
	}

	data = {
		"admin": server_admin_result
	}

	#print("\n" + url + "\n")
	response = requests.put(url, headers=headers, data=json.dumps(data), verify=True)

	if response.status_code != 200:
		print(f"Error setting user as server admin: {response.status_code}, {response.text}")

	set_user_server_admin_dict = json.loads(response.text)

	return set_user_server_admin_dict

# Example:
# $ curl -kX POST -H 'Content-Type: application/json' -d '{"admin": "true"}' https://matrix.perthchat.org/_synapse/admin/v2/users/@dogpoo:perthchat.org?access_token=ACCESS_TOKEN

def whois_account(preset_username):
	if preset_username == '':
		username = input("\nPlease enter the username you wish to whois: ")
	elif preset_username != '':
		username = preset_username
	username = parse_username(username)

	url = f"https://{hardcoded_variables.homeserver_url}/_matrix/client/r0/admin/whois/@{username}:{hardcoded_variables.base_url}"
	url += f"?access_token={hardcoded_variables.access_token}"

	#print("\n" + url + "\n")
	response = requests.get(url, verify=True)

	if response.status_code != 200:
		print(f"Error retrieving account info: {response.status_code}, {response.text}\n")

	whois_account_dict = json.loads(response.text)

	return whois_account_dict

# Example:
# $ curl -kXGET https://matrix.perthchat.org/_matrix/client/r0/admin/whois/@dogpoo:perthchat.org?access_token=ACCESS_TOKEN

def whois_multiple_accounts():
	print("Whois multiple user accounts selected")
	user_list_location = input("\nPlease enter the path of the file containing a newline seperated list of Matrix usernames: ")
	with open(user_list_location, newline='') as f:
		reader = csv.reader(f)
		data = list(reader)
		print(len(data))

	print("\n" + str(data))

	output_file = None
	if len(data) > 10:
		file_confirmation = input("\nThere are more than 10 users. Would you like to save the output to a file? y/n?\n")
		if file_confirmation.lower() in ("y", "yes"):
			output_file = input("\nPlease enter the desired output file path:\n")

	whois_confirmation = input("\n\nAre you sure you want to whois all of these users? y/n?\n")

	if whois_confirmation.lower() in ("y", "yes"):  
		x = 0
		while x <= (len(data) - 1):
			output = whois_account(data[x][0])

			# if output file is specified, append to file
			if output_file:
				with open(output_file, 'a') as f:
					f.write(output + "\n")
			x += 1
			time.sleep(1)

	if whois_confirmation.lower() in ("n", "no"):
		print("\nExiting...\n")

	if output_file and os.path.isfile(output_file):
		print(f"Output saved to {output_file}")

def list_joined_rooms(preset_username):
	if preset_username == '':
		username = input("\nPlease enter the username you wish to query: ")
	elif preset_username != '':
		username = preset_username

	username = parse_username(username)

	url = f"https://{hardcoded_variables.homeserver_url}/_synapse/admin/v1/users/@" + username + f":{hardcoded_variables.base_url}/joined_rooms?access_token={hardcoded_variables.access_token}"

	response = requests.get(url, verify=True)

	if response.status_code != 200:
		print(f"Error querying joined rooms: {response.status_code}, {response.text}")

	joined_rooms_dict = json.loads(response.text)

	return joined_rooms_dict

# Example:
# $ curl -kXGET https://matrix.perthchat.org/_synapse/admin/v1/users/@dogpoo:perthchat.org/joined_rooms?access_token=ACCESS_TOKEN

def list_accounts():
	deactivated_choice = input("Do you want to include deactivated accounts y/n? ")
	guest_choice = input("Do you want to include guest accounts y/n? ")

	deactivated_string = "deactivated=false" if deactivated_choice.lower() not in ["y", "yes"] else "deactivated=true"
	guest_string = "guest=false" if guest_choice.lower() not in ["y", "yes"] else "guest=true"

	url = f"https://{hardcoded_variables.homeserver_url}/_synapse/admin/v2/users?from=0&limit=1000000&{guest_string}&{deactivated_string}&access_token={hardcoded_variables.access_token}"

	print("\n" + url + "\n")
	response = requests.get(url, verify=True)

	if response.status_code == 200:
		users = response.json()
		number_of_users = len(users)
		print("\nTotal amount of users: " + str(number_of_users))

		if number_of_users < 100:
			print(users)
		else:
			accounts_output_file = input("\nThere are too many users to list here, please specify a filename to print this data too: ")
			with open(accounts_output_file, "w") as f:
				json.dump(users, f, indent=4)
	else:
		print(f"Error retrieving users list: {response.status_code}, {response.text}")

# Example:
# $ curl -kXGET "https://matrix.perthchat.org/_synapse/admin/v2/users?from=0&limit=10&guests=false&access_token=ACCESS_TOKEN"

# NEED A MENU OPTION FOR THIS:

def query_account(preset_username):
	if len(preset_username) == 0:
		username = input("\nPlease enter the username to query: ")
		username = parse_username(username)
	elif len(preset_username) > 0:
		username = parse_username(preset_username)

	url = f"https://{hardcoded_variables.homeserver_url}/_synapse/admin/v2/users/@{username}:{hardcoded_variables.base_url}?access_token={hardcoded_variables.access_token}"

	#print("\n" + url + "\n")
	response = requests.get(url, verify=True)

	if response.status_code != 200:
		print(f"Error querying account: {response.status_code}, {response.text}")

	query_account_dict = json.loads(response.text)

	return query_account_dict

# Example:
# $ curl -kX GET https://matrix.perthchat.org/_synapse/admin/v2/users/@billybob:perthchat.org?access_token=ACCESS_TOKEN

def query_multiple_accounts():
	print("Query multiple user accounts selected")
	user_list_location = input("\nPlease enter the path of the file containing a newline seperated list of Matrix usernames: ")
	with open(user_list_location, newline='') as f:
		reader = csv.reader(f)
		data = list(reader)
		print(len(data))

	print("\n" + str(data))

	output_file = None
	if len(data) > 10:
		file_confirmation = input("\nThere are more than 10 users. Would you like to save the output to a file? y/n?\n")
		if file_confirmation.lower() in ("y", "yes"):
			output_file = input("\nPlease enter the desired output file path:\n")

	query_confirmation = input("\n\nAre you sure you want to query all of these users? y/n?\n")

	if query_confirmation.lower() in ("y", "yes"):  
		x = 0
		while x <= (len(data) - 1):
			output = query_account(data[x][0])

			# if output file is specified, append to file
			if output_file:
				with open(output_file, 'a') as f:
					f.write(output + "\n")
			x += 1
			time.sleep(1)

	if query_confirmation.lower() in ("n", "no"):
		print("\nExiting...\n")

	if output_file and os.path.isfile(output_file):
		print(f"Output saved to {output_file}")

def quarantine_users_media():
	username = input("\nPlease enter the username of the user who's media you want to quarantine: ")
	username = parse_username(username)

	url = f"https://{hardcoded_variables.homeserver_url}/_synapse/admin/v1/user/@{username}:{hardcoded_variables.base_url}/media/quarantine?access_token={hardcoded_variables.access_token}"

	print("\n" + url + "\n")
	response = requests.post(url, verify=True)

	if response.status_code == 200:
		print(response.text)
	else:
		print(f"Error quarantining user's media: {response.status_code}, {response.text}")

# Example:
# $ curl -X POST https://matrix.perthchat.org/_synapse/admin/v1/user/@dogpoo:perthchat.org/media/quarantine?access_token=ACCESS_TOKEN

def collect_account_data(preset_username):
	if len(preset_username) == 0:
		username = input("\nPlease enter the username to collect account data: ")
		username = parse_username(username)
	elif len(preset_username) > 0:
		username = parse_username(preset_username)

	url = f"https://{hardcoded_variables.homeserver_url}/_synapse/admin/v1/users/@{username}:{hardcoded_variables.base_url}/accountdata?access_token={hardcoded_variables.access_token}"

	#print("\n" + url + "\n")
	response = requests.get(url, verify=True)

	if response.status_code != 200:
		print(f"Error querying account: {response.status_code}, {response.text}")

	account_data_dict = json.loads(response.text)

	return account_data_dict

# Example:
# $ curl -X GET https://matrix.perthchat.org/_synapse/admin/v1/users/@dogpoo:perthchat.org/accountdata?access_token=ACCESS_TOKEN

def list_account_pushers(preset_username):
	if len(preset_username) == 0:
		username = input("\nPlease enter the username to list all pushers: ")
		username = parse_username(username)
	elif len(preset_username) > 0:
		username = parse_username(preset_username)

	url = f"https://{hardcoded_variables.homeserver_url}/_synapse/admin/v1/users/@{username}:{hardcoded_variables.base_url}/pushers?access_token={hardcoded_variables.access_token}"

	#print("\n" + url + "\n")
	response = requests.get(url, verify=True)

	if response.status_code != 200:
		print(f"Error querying account: {response.status_code}, {response.text}")

	pusher_data_dict = json.loads(response.text)

	return pusher_data_dict

# Example:
# $ curl -X GET https://matrix.perthchat.org/_synapse/admin/v1/users/@dogpoo:perthchat.org/pushers

def get_rate_limit():
	username = input("\nPlease enter the username to get its ratelimiting: ")

	url = f"https://{hardcoded_variables.homeserver_url}/_synapse/admin/v1/users/@{username}:{hardcoded_variables.base_url}/override_ratelimit?access_token={hardcoded_variables.access_token}"

	#print("\n" + url + "\n")
	response = requests.get(url, verify=True)

	if response.status_code == 200:
		print(response.text)
	else:
		print(f"Error querying account: {response.status_code}, {response.text}")

	return response.text

# Example:
# $ curl -X GET https://matrix.perthchat.org/_synapse/admin/v1/users/@dogpoo:perthchat.org/override_ratelimit?access_token=ACCESS_TOKEN

def set_rate_limit():
	username = input("\nPlease enter the username to adjust its ratelimiting: ")

	messages_per_second = input("\nPlease enter the desired messages per second: ")
	burst_count = input("\nPlease enter the desired burst count: ")

	url = f"https://{hardcoded_variables.homeserver_url}/_synapse/admin/v1/users/@{username}:{hardcoded_variables.base_url}/override_ratelimit?access_token={hardcoded_variables.access_token}"

	headers = {'Content-Type': 'application/json'}
	data = {
		"messages_per_second": int(messages_per_second),
		"burst_count": int(burst_count)
	}

	#print("\n" + url + "\n")

	response = requests.post(url, headers=headers, data=json.dumps(data), verify=True)

	if response.status_code == 200:
		print(response.text)
	else:
		print(f"Error querying account: {response.status_code}, {response.text}")

	return response.text

# Example:
# $ curl -X POST -H "Content-Type: application/json" -d '{"messages_per_second": 0,"burst_count": 0}' https://matrix.perthchat.org/_synapse/admin/v1/users/@dogpoo:perthchat.org/override_ratelimit?access_token=ACCESS_TOKEN

def delete_rate_limit():
	username = input("\nPlease enter the username to delete its ratelimiting: ")

	url = f"https://{hardcoded_variables.homeserver_url}/_synapse/admin/v1/users/@{username}:{hardcoded_variables.base_url}/override_ratelimit?access_token={hardcoded_variables.access_token}"

	#print("\n" + url + "\n")
	response = requests.delete(url, verify=True)

	if response.status_code == 200:
		print(response.text)
	else:
		print(f"Error querying account: {response.status_code}, {response.text}")

	return response.text

# Example:
# $ curl -X DELETE https://matrix.perthchat.org/_synapse/admin/v1/users/@dogpoo:perthchat.org/override_ratelimit?access_token=ACCESS_TOKEN

def check_user_account_exists(preset_username):
	if len(preset_username) == 0:
		username = input("\nPlease enter the username to check if it exists: ")
		username = parse_username(username)
	elif len(preset_username) > 0:
		username = parse_username(preset_username)

	url = f"https://{hardcoded_variables.homeserver_url}/_synapse/admin/v1/username_available?username={username}&access_token={hardcoded_variables.access_token}"

	#print("\n" + url + "\n")
	response = requests.get(url, verify=True)

	if response.status_code == 200:
		#print("User ID is available.")
		return False
	elif response.status_code == 400:
		#print(f"User ID already exists.")
		return True
	else:
		print(f"Error querying account: {response.status_code}, {response.text}")

# Example:
# $ curl -X GET /_synapse/admin/v1/username_available?username=dogpoo&access_token=ACCESS_TOKEN
