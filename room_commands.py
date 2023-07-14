
import subprocess
import json
import time
import os
import csv
import requests
import hardcoded_variables

def parse_username(username):
	tail_end = ':' + hardcoded_variables.base_url
	username = username.replace('@','')
	username = username.replace(tail_end,'')
	return username

def list_room_details(preset_internal_ID):
	if preset_internal_ID == '':
		internal_ID = input("\nEnter the internal id of the room you wish to query (Example: !OLkDvaYjpNrvmwnwdj:matrix.org): ")
	elif preset_internal_ID != '':
		internal_ID = preset_internal_ID
	url = f"https://{hardcoded_variables.homeserver_url}/_synapse/admin/v1/rooms/{internal_ID}"
	headers = {"Authorization": f"Bearer {hardcoded_variables.access_token}"}

	print("\n" + url + "\n")
	response = requests.get(url, headers=headers, verify=True)

	print(response.text)

# Example
# $ curl -kXGET 'https://matrix.perthchat.org/_synapse/admin/v1/rooms/!OeqILBxiHahidSQQoC:matrix.org?access_token=ACCESS_TOKEN'

def export_room_state(preset_internal_ID):
	# record the current directory location
	current_directory = os.getcwd()
	
	if preset_internal_ID == '':
		internal_ID = input("\nEnter the internal id of the room with which to export the 'state' of (Example: !OLkDvaYjpNrvmwnwdj:matrix.org): ")
	elif preset_internal_ID != '':
		internal_ID = preset_internal_ID
	
	room_dir = os.path.join(current_directory, "state_events")
	os.makedirs(room_dir, exist_ok=True)

	unix_time = int(time.time())
	url = f"https://{hardcoded_variables.homeserver_url}/_synapse/admin/v1/rooms/{internal_ID}/state"
	headers = {"Authorization": f"Bearer {hardcoded_variables.access_token}"}
	filename = os.path.join(room_dir, f"{internal_ID}_state_{unix_time}.json")

	print("\n" + url + "\n")
	response = requests.get(url, headers=headers, verify=True)

	with open(filename, 'w') as f:
		f.write(response.text)

	print(response.text)

# Example
# $ curl -kXGET 'https://matrix.perthchat.org/_synapse/admin/v1/rooms/!OeqILBxiHahidSQQoC:matrix.org/state?access_token=ACCESS_TOKEN'

# See
# https://matrix-org.github.io/synapse/latest/admin_api/rooms.html#room-state-api

def list_directory_rooms():
    url = f"https://{hardcoded_variables.homeserver_url}/_matrix/client/r0/publicRooms"
    headers = {"Authorization": f"Bearer {hardcoded_variables.access_token}"}

    print("\n" + url + "\n")
    response = requests.get(url, headers=headers, verify=True)
    output = response.text

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
	url = f"https://{hardcoded_variables.homeserver_url}/_matrix/client/r0/directory/list/room/{internal_ID}"
	headers = {"Authorization": f"Bearer {hardcoded_variables.access_token}"}
	data = {"visibility": "private"}

	print("\n" + url + "\n")
	response = requests.put(url, headers=headers, json=data, verify=True)

	print(response.text)

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

def list_and_download_media_in_room(preset_internal_ID, preset_print_file_list_choice, preset_download_files_choice, base_directory):
	headers = {
		'Authorization': f"Bearer {hardcoded_variables.access_token}"
	}

	if preset_internal_ID == '':
		internal_ID = input("\nEnter the internal id of the room you want to get a list of media for (Example: !OLkDvaYjpNrvmwnwdj:matrix.org): ")
	else:
		internal_ID = preset_internal_ID
    
	url = f"https://{hardcoded_variables.homeserver_url}/_synapse/admin/v1/room/{internal_ID}/media"
	print("\n" + url + "\n")

	response = requests.get(url, headers=headers, verify=True)
	media_list_output = response.text
	print("Full media list:\n" + media_list_output)

	if preset_print_file_list_choice == '':
		print_file_list_choice = input("\nDo you want to write this list to a file? y/n? ")
	else:
		print_file_list_choice = preset_print_file_list_choice

	if print_file_list_choice.lower() in ["y", "yes", "Y", "Yes"]:
		print_file_list_choice = "true"
	elif print_file_list_choice.lower() in ["n", "no", "N", "No"]:
		print_file_list_choice = "false"
	else:
		print("Input invalid! Defaulting to 'No'.")
		print_file_list_choice = "false"

	room_dir = os.path.join(base_directory, internal_ID.replace('!', '').replace(':', '-'))
	os.makedirs(room_dir, exist_ok=True)

	if print_file_list_choice == "true":
		media_list_filename_location = os.path.join(room_dir, "media_list.txt")
		with open(media_list_filename_location,"w+") as media_list_filename:
			media_list_filename.write(media_list_output)

	if preset_download_files_choice == '':
		download_files_choice = input("\nDo you also want to download a copy of these media files? y/n? ")
	else:
		download_files_choice = preset_download_files_choice

	if download_files_choice.lower() in ["y", "yes", "Y", "Yes"]:
		download_files_choice = "true"
	elif download_files_choice.lower() in ["n", "no", "N", "No"]:
		download_files_choice = "false"
	else:
		print("Input invalid! Defaulting to 'No'.")
		download_files_choice = "false"

	if download_files_choice == "true":
		media_files_dir = os.path.join(room_dir, "media-files")
		os.makedirs(media_files_dir, exist_ok=True)

		media_list_output = json.loads(media_list_output)
		for key in ['local', 'remote']:
			for media in media_list_output.get(key, []):
				media_url = media.replace('mxc://', f"https://{hardcoded_variables.homeserver_url}/_matrix/media/r0/download/")
				media_response = requests.get(media_url, stream=True, headers=headers, verify=True)

				if media_response.status_code == 200:
					media_file_path = os.path.join(media_files_dir, media.split('/')[-1])
					with open(media_file_path, 'wb') as media_file:
						media_file.write(media_response.content)
					print(f"Downloaded {media_url} to {media_file_path}")
				else:
					print(f"Failed to download {media_url}, status code: {media_response.status_code}")

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

def redact_room_event():
	internal_ID = input("\nEnter the internal id of the room the event is in (Example: !rapAelwZkajRyeZIpm:perthchat.org): ")
	event_ID = input("\nEnter the event id of the event you wish to redact (Example: $lQT7NYYyVvwoVpZWcj7wceYQqeOzsJg1N6aXIecys4s): ")
	redaction_reason = input("\nEnter the reason you're redacting this content: ")
	url = f"https://{hardcoded_variables.homeserver_url}/_matrix/client/v3/rooms/{internal_ID}/redact/{event_ID}"
	print(f"\nRequesting: {url}\n")
	output = requests.post(url, headers={'Authorization': f"Bearer {hardcoded_variables.access_token}"}, json={'reason': redaction_reason}, verify=True).text
	print(output)

# $ curl -X POST --header "Authorization: Bearer syt_..." --data-raw '{"reason": "Indecent material"}' 'https://matrix.perthchat.org/_matrix/client/v3/rooms/!fuYHAYyXqNLDxlKsWP:perthchat.org/redact/$nyjgZguQGadRRy8MdYtIgwbAeFcUAPqOPiaj_E60XZs'
# {"event_id":"$_m1gFtPg-5DiTyCvGfeveAX2xaA8gAv0BYLpjC8xe64"}

def quarantine_media_in_room():
	internal_ID = input("\nEnter the internal id of the room you want to quarantine, this makes local and remote data inaccessible (Example: !OLkDvaYjpNrvmwnwdj:matrix.org): ")
	url = f"https://{hardcoded_variables.homeserver_url}/_synapse/admin/v1/room/{internal_ID}/media/quarantine"
	print(f"\nRequesting: {url}\n")
	headers = {'Authorization': f'Bearer {hardcoded_variables.access_token}'}
	response = requests.post(url, headers=headers, verify=True)
	print(response.text)

# Example
# $ curl -X POST 'https://matrix.perthchat.org/_synapse/admin/v1/room/!DwUPBvNapIVecNllgt:perthchat.org/media/quarantine?access_token=ACCESS_TOKEN'

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

	command_string = 'curl -H "Authorization: Bearer ' + hardcoded_variables.access_token + "\" --data '{ \"new_room_user_id\": \"@" + username + ":" + hardcoded_variables.base_url + "\" , \"room_name\": \"" + new_room_name + "\", \"message\": \"" + message + "\", \"block\": " + block_choice + ", \"purge\": " + purge_choice + " }' -X DELETE 'https://" + hardcoded_variables.homeserver_url + "/_synapse/admin/v2/rooms/" + internal_ID + "'"
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
		command_string = 'curl -H "Authorization: Bearer ' + hardcoded_variables.access_token + "\" -kX GET 'https://" + hardcoded_variables.homeserver_url + '/_synapse/admin/v2/rooms/' + internal_ID + "/delete_status'"
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

	command_string = 'curl -H "Authorization: Bearer ' + hardcoded_variables.access_token + "\" --data '{ \"block\":  false, \"purge\": true }' -X DELETE 'https://" + hardcoded_variables.homeserver_url + "/_synapse/admin/v2/rooms/" + internal_ID + "'"
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
		command_string = 'curl -H "Authorization: Bearer ' + hardcoded_variables.access_token + "\" -kX GET 'https://" + hardcoded_variables.homeserver_url + '/_synapse/admin/v2/rooms/' + internal_ID + "/delete_status'"
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

	command_string = 'curl --header "Authorization: Bearer ' + hardcoded_variables.access_token + "\" -X POST -H \"Content-Type: application/json\" -d '{ \"delete_local_events\": false, \"purge_up_to_ts\": " + timestamp + " }' 'https://" + hardcoded_variables.homeserver_url + "/_synapse/admin/v1/purge_history/" + internal_ID + "'"
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
		command_string = 'curl -H "Authorization: Bearer ' + hardcoded_variables.access_token + "\" -kX GET 'https://" + hardcoded_variables.homeserver_url + '/_synapse/admin/v1/purge_history_status/' + purge_id + "'"
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
