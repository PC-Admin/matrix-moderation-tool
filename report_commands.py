
import os
import json
import random
import string
import datetime
import zipfile
import pyAesCrypt
import user_commands
import room_commands
import ipinfo_commands
import hardcoded_variables

# For testing the Report Generator, set this to True
testing_mode = False

def get_report_folder():
	# Get report_folder from hardcoded_variables
	report_folder = hardcoded_variables.report_folder

	# If report_folder ends with a slash, remove it
	if report_folder.endswith(os.sep):
		report_folder = report_folder[:-1]

	return report_folder

def encrypt_user_folder(user_report_folder, username):
	# Generate a strong random password
	strong_password = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(20))

	# Get parent directory of user_report_folder
	parent_directory = os.path.dirname(os.path.abspath(user_report_folder))

	# Create the name of the .zip file including timestamp
	zip_file_name = os.path.join(parent_directory, username + "_" + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".zip")

	# Create a .zip file of the specified folder
	with zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED) as zip_file:
		for root, dirs, files in os.walk(user_report_folder):
			for file in files:
				zip_file.write(os.path.join(root, file), arcname=os.path.relpath(os.path.join(root, file), user_report_folder))

	# Buffer size - 64K
	bufferSize = 64 * 1024

	# Encrypt the .zip file
	pyAesCrypt.encryptFile(zip_file_name, zip_file_name + ".aes", strong_password, bufferSize)

	# Delete the original zip file
	os.remove(zip_file_name)

	# You can return the password if you need to use it later, or you can directly print it here
	return strong_password, zip_file_name + ".aes"

def generate_user_report(preset_username):
	if len(preset_username) == 0:
		username = input("\nPlease enter the username to automatically generate a report: ")
		username = user_commands.parse_username(username)
	else:
		username = user_commands.parse_username(preset_username)

	# Check if user exists
	if user_commands.check_user_account_exists(username) == True:
		print("\nUser exists, continuing with report generation.")
		return

	# If report_folder ends in a slash, remove it
	report_folder = get_report_folder()

	# Create report folders
	user_report_folder = report_folder + "/" + username + "/"

	if os.path.exists(report_folder) == False:
		os.mkdir(report_folder)

	if os.path.exists(user_report_folder) == False:
		os.mkdir(user_report_folder)

	# Get user account data and write to ./report/username/account_data.json
	account_data = user_commands.collect_account_data(username)
	account_data_file = open(user_report_folder + "account_data.json", "w")
	account_data_file.write(json.dumps(account_data, indent=4, sort_keys=True))
	account_data_file.close()

	# Get user pushers and write to ./report/username/pushers.json
	pushers_data = user_commands.list_account_pushers(username)
	pushers_file = open(user_report_folder + "pushers.json", "w")
	pushers_file.write(json.dumps(pushers_data, indent=4, sort_keys=True))
	pushers_file.close()

	# Get whois data and write to ./report/username/whois.json
	whois_data = user_commands.whois_account(username)
	whois_file = open(user_report_folder + "whois.json", "w")
	whois_file.write(json.dumps(whois_data, indent=4, sort_keys=True))
	whois_file.close()

	# Get query data and write to ./report/username/query.json
	query_data = user_commands.query_account(username)
	query_file = open(user_report_folder + "query.json", "w")
	query_file.write(json.dumps(query_data, indent=4, sort_keys=True))
	query_file.close()

	# Get user joined rooms and write to ./report/username/joined_rooms.json
	joined_rooms_dict = user_commands.list_joined_rooms(username)
	joined_rooms_file = open(user_report_folder + "joined_rooms.json", "w")
	joined_rooms_file.write(json.dumps(joined_rooms_dict, indent=4, sort_keys=True))
	joined_rooms_file.close()

	# Get user ipinfo and write to ./report/username/ipinfo.json
	ipinfo = ipinfo_commands.analyse_account_ip(username)
	ipinfo_file = open(user_report_folder + "ipinfo.json", "w")
	ipinfo_file.write(json.dumps(ipinfo, indent=4, sort_keys=True))
	ipinfo_file.close()

	# For each room the user is in, get the room state and write to ./report/username/room_states/
	room_states_folder = user_report_folder + "room_states/"
	if os.path.exists(room_states_folder) == False:
		os.mkdir(room_states_folder)

	room_list = joined_rooms_dict.get('joined_rooms', [])

	count = 0
	for room in room_list:
		count += 1
		room = room.split(" ")[0]
		room_commands.export_room_state(room, room_states_folder)
		if count > 4 and testing_mode == True:
			break

	# For each room the user is in, get the room details and write to ./report/username/room_details/
	room_details_folder = user_report_folder + "room_details/"
	if os.path.exists(room_details_folder) == False:
		os.mkdir(room_details_folder)

	count = 0
	for room in room_list:
		count += 1
		room = room.split(" ")[0]
		room_details = room_commands.list_room_details(room)
		room_details_file = open(room_details_folder + room + ".json", "w")
		room_details_file.write(str(room_details))
		room_details_file.close()
		if count > 4 and testing_mode == True:
			break

	# Generate a random password, then encrypt the ./report/username/ folder to a timestamped .zip file
	strong_password, encrypted_zip_file_name = encrypt_user_folder(user_report_folder, username)

	# Measure the size of the encrypted .zip file in MB
	encrypted_zip_file_size = os.path.getsize(encrypted_zip_file_name) / 1000000

	# Print the password and the encrypted .zip file name
	print("\nReport generated successfully on user: \"" + username + "\"\n\nYou can send this .zip file and password when reporting a user to law enforcement.")
	print("\nPassword: " + strong_password)
	print("Encrypted .zip file location: " + encrypted_zip_file_name)
	print("Encrypted .zip file size: " + str(encrypted_zip_file_size) + " MB\n")

def decrypt_zip_file():
	# Ask user for the location of the encrypted .zip file
	encrypted_zip_file_name = input("\nPlease enter the location of the encrypted .zip file: ")
	# Ask user for the password
	strong_password = input("Please enter the password: ")
	# Decrypt the ZIP file into the same location as the encrypted ZIP file
	pyAesCrypt.decryptFile(encrypted_zip_file_name, encrypted_zip_file_name[:-4], strong_password, 64 * 1024)
	# Print the location of the decrypted ZIP file
	print("\nDecrypted .zip file location: " + encrypted_zip_file_name[:-4] + "\n")
