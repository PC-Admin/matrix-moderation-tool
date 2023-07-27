
import os
import requests
import json
import csv
import time
import socket
import hardcoded_variables
import user_commands

# Should use: https://github.com/ipinfo/python

def is_valid_ipv4(ip):
	try:
		socket.inet_pton(socket.AF_INET, ip)
	except socket.error:  # not a valid address
		return False
	return True

def analyse_account_ip(preset_username):
	if not preset_username:
		preset_username = input("\nPlease enter a username to analyse their country of origin: ")
	data = user_commands.whois_account(preset_username=preset_username)

	user_id = data['user_id']
	device_data = data['devices']

	ip_info = {}
	for device_id, device_info in device_data.items():
		for session in device_info['sessions']:
			for connection in session['connections']:
				ip = connection['ip']
				if is_valid_ipv4(ip) and len(hardcoded_variables.ipinfo_token) > 0:
					res = requests.get(f"https://ipinfo.io/{ip}", 
								  headers={"Authorization": f"Bearer {hardcoded_variables.ipinfo_token}"})
					if res.status_code == 200:
						country = res.json().get('country')
						ip_info[ip] = country
			   
	if len(hardcoded_variables.ipinfo_token) == 0:
		return {"user_id": user_id, "ip_info": "IPINFO DISABLED"}
	else:
		return {"user_id": user_id, "ip_info": ip_info}

def analyse_multiple_account_ips():
	print("Analyse multiple user IPs selected")
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

	analyse_confirmation = input("\n\nAre you sure you want to analyse the IP of all of these users? y/n?\n")

	if analyse_confirmation.lower() in ("y", "yes"):  
		x = 0
		while x <= (len(data) - 1):
			output = analyse_account_ip(data[x][0])

			# if output file is specified, append to file
			if output_file:
				with open(output_file, 'a') as f:
					f.write(output + "\n")
			x += 1
			time.sleep(1)

	if analyse_confirmation.lower() in ("n", "no"):
		print("\nExiting...\n")

	if output_file and os.path.isfile(output_file):
		print(f"Output saved to {output_file}")
