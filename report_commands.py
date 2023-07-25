
import os
import json
import whois
import random
import string
import datetime
import zipfile
import pyAesCrypt
import smtplib
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE
from email import encoders
import user_commands
import room_commands
import ipinfo_commands
import hardcoded_variables

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

	# Write the password to a file
	password_file = open(zip_file_name + ".aes" + ".password", "w")
	password_file.write(strong_password)
	password_file.close()

	# You can return the password if you need to use it later, or you can directly print it here
	return strong_password, zip_file_name + ".aes"

def generate_user_report(preset_username):
	if len(preset_username) == 0:
		username = input("\nPlease enter the username to automatically generate a report: ")
		username = user_commands.parse_username(username)
	else:
		username = user_commands.parse_username(preset_username)

	# Check if user exists
	if user_commands.check_user_account_exists(username) == False:
		print("\nUser does not exist, exiting report generation.")
		return
	elif user_commands.check_user_account_exists(username) == True:
		print(f"\nGenerating user report for {username}...")
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

	# Prepare folder structures
	room_folder = user_report_folder + "rooms/"
	dm_folder = user_report_folder + "dms/"
	details_folder = "details/"
	states_folder = "states/"

	# For each room the user is in, get the room state and write to ./report/username/rooms/states/
	room_states_folder = room_folder + states_folder
	if not os.path.exists(room_states_folder):
		os.makedirs(room_states_folder, exist_ok=True)

	# For each room the user is in, get the room details and write to ./report/username/rooms/details/
	room_details_folder = room_folder + details_folder
	if not os.path.exists(room_details_folder):
		os.makedirs(room_details_folder, exist_ok=True)

	# For DM, get the state and write to ./report/username/dms/states/
	dm_states_folder = dm_folder + states_folder
	if not os.path.exists(dm_states_folder):
		os.makedirs(dm_states_folder, exist_ok=True)

	# For DM, get the details and write to ./report/username/dms/details/
	dm_details_folder = dm_folder + details_folder
	if not os.path.exists(dm_details_folder):
		os.makedirs(dm_details_folder, exist_ok=True)

	room_list = joined_rooms_dict.get('joined_rooms', [])

	count = 0
	for room in room_list:
		count += 1
		room = room.split(" ")[0]
		room_details = room_commands.list_room_details(room)

		# Check the room conditions to select the proper output folders
		if room_details['joined_members'] == 2 and room_details['public'] == False:
			room_details_file = open(dm_details_folder + room + ".json", "w")
			state_events = room_commands.export_room_state(room, dm_states_folder, True)
		else:
			room_details_file = open(room_details_folder + room + ".json", "w")
			state_events = room_commands.export_room_state(room, room_states_folder, True)

		room_details_file.write(json.dumps(room_details, indent=4, sort_keys=True))
		room_details_file.close()

		if count > 4 and hardcoded_variables.testing_mode == True:
			break

	# Generate a random password, then encrypt the ./report/username/ folder to a timestamped .zip file
	strong_password, encrypted_zip_file_name = encrypt_user_folder(user_report_folder, username)

	# Measure the size of the encrypted .zip file in MB
	encrypted_zip_file_size = os.path.getsize(encrypted_zip_file_name) / 1000000

	# Print the password and the encrypted .zip file name
	print("Report generated successfully on user: \"" + username + "\"\n\nYou can send this .zip file and password when reporting a user to law enforcement.")
	print("\nPassword: " + strong_password)
	print("Encrypted .zip file location: " + encrypted_zip_file_name)
	print("Encrypted .zip file size: " + str(encrypted_zip_file_size) + " MB\n")

	return encrypted_zip_file_name, strong_password

def decrypt_zip_file():
	# Ask user for the location of the encrypted .zip file
	encrypted_zip_file_name = input("\nPlease enter the location of the encrypted .zip file: ")
	# Ask user for the password
	strong_password = input("Please enter the password: ")
	# Decrypt the ZIP file into the same location as the encrypted ZIP file
	pyAesCrypt.decryptFile(encrypted_zip_file_name, encrypted_zip_file_name[:-4], strong_password, 64 * 1024)
	# Print the location of the decrypted ZIP file
	print("\nDecrypted .zip file location: " + encrypted_zip_file_name[:-4] + "\n")

def lookup_homeserver_admin_email(preset_baseurl):
	if preset_baseurl == '':
		baseurl = input("\nEnter the base URL to collect the admin contact details (Example: matrix.org): ")
	elif preset_baseurl != '':
		baseurl = preset_baseurl

	# If baseurl is matrix.org, return 'abuse@matrix.org' as a hardcoded response
	if baseurl == "matrix.org":
		print("\nAdmin contact email(s) for " + baseurl + " are: abuse@matrix.org")
		return {"matrix.org": ["abuse@matrix.org"]}, False

	# Check target homserver for MSC1929 support email
	url = f"https://{baseurl}/.well-known/matrix/support"
	try:
		response = requests.get(url)
	except requests.exceptions.RequestException as e:
		print(f"Error: Unable to connect to server {baseurl}. Trying WHOIS data...")
		response = None

	# If the request was successful, the status code will be 200
	if response and response.status_code == 200:
		# Parse the response as JSON
		data = json.loads(response.text)

		# Extract the emails from the admins field and remove duplicates
		admin_emails = list({admin['email_address'] for admin in data['admins']})

		print("\nAdmin contact emails for " + baseurl + " are: " + str(admin_emails))

		# Create a dictionary with baseurl as key and emails as value
		email_dict = {baseurl: admin_emails}

		return email_dict, False
	else:
		print(f"Error: Unable to collect admin email from server {baseurl}")
		print("Attempting to collect admin email from WHOIS data...")

		# Get WHOIS data
		try:
			w = whois.whois(baseurl)
			if w.emails:
				print("\nAdmin contact email(s) for " + baseurl + " are: " + str(w.emails))
				return {baseurl: list(w.emails)}, True
			else:
				print(f"Error: Unable to collect admin email from WHOIS data for {baseurl}")
				return None, False
		except:
			print(f"Error: Unable to collect WHOIS data for {baseurl}")
			return None, False

def send_email(email_address, email_subject, email_content, email_attachments):
	assert isinstance(email_attachments, list)

	msg = MIMEMultipart()  # Create a multipart message
	msg['From'] = hardcoded_variables.smtp_user
	msg['To'] = COMMASPACE.join([email_address])
	msg['Subject'] = email_subject

	msg.attach(MIMEText(email_content))  # Attach the email body

	# Attach files
	for file in email_attachments:
		part = MIMEBase('application', "octet-stream")
		with open(file, 'rb') as f:
			part.set_payload(f.read())
		encoders.encode_base64(part)
		part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
		msg.attach(part)

	try:
		# Send the email via SMTP server
		smtp = smtplib.SMTP(hardcoded_variables.smtp_server, hardcoded_variables.smtp_port)
		smtp.starttls()
		smtp.login(hardcoded_variables.smtp_user, hardcoded_variables.smtp_password)
		smtp.sendmail(hardcoded_variables.smtp_user, email_address, msg.as_string())
		smtp.close()
		return True
	except Exception as e:
		print(f"Failed to send email: {e}")
		return False

def test_send_email():
	# Ask the user for the destination email address
	email_address = input("\nPlease enter the destination email address to send this test email too: ")

	# Example email parameters
	email_subject = "Test Email"
	email_content = "This is a test email."
	email_attachments = ["./test_data/evil_clown.jpeg"]  # List of file paths. Adjust this to the actual files you want to attach.

	# Try to send the email
	if send_email(email_address, email_subject, email_content, email_attachments):
		print("\nEmail successfully sent.")
	else:
		print("\nFailed to send email.")

def prepare_email_content(user_dict, from_whois, baseurl):
	email_content = f"""Dear Administrator,

We regret to inform you that there have been incidents involving the following users in your homeserver:
	"""

	for full_username, room_dict in user_dict.items():
		email_content += f"\nUser: {full_username}\n"
		for room_id, rdlist_tags in room_dict.items():
			email_content += f"Is in the room {room_id}, this room has been flagged with the following rdlist tags:\n{', '.join(rdlist_tags)}\n"

	email_content += f"""

We request your immediate attention to this matter. It is recommended that you:
- Generate a report on these users' accounts and send it to law enforcement.
- Block and purge these rooms from your homeserver.
- Deactivate these users' accounts.

All of these actions can be done automatically using this moderation tool:
https://github.com/PC-Admin/matrix-moderation-tool

**********************************************************************
\tTHIS EMAIL IS UNMONITORED, PLEASE DO NOT REPLY TO IT
**********************************************************************

To contact us please email {hardcoded_variables.report_return_email}.

Thank you for helping us make Matrix safer.

Best regards,
Incident Report Team
https://{hardcoded_variables.base_url}
"""

	if from_whois:
		email_content += f"""\n\n**********************************************************************
\tATTENTION DOMAIN REGISTRAR, YOUR ACTION IS REQUIRED HERE
**********************************************************************
\nThis email is intended for the owner of the domain {baseurl}, but they have not published their email address.
\nAs the recipient of this email, you have a legal obligation to ensure that this email reaches them.
\nTo avoid receiving these emails in the future, please ask them to configure MSC1929 for their Matrix server:
https://github.com/matrix-org/matrix-spec-proposals/pull/1929
		"""

	confidentiality_warning = f"""\n\n**********************************************************************
\t\tATTENTION! CONFIDENTIALITY NOTICE!
\nThis electronic mail and any files linked to it may hold information
that is privileged, confidential, and intended exclusively for the use of
the designated recipient or entity. If you're not the expected recipient or
the individual tasked with delivering the electronic mail to the intended recipient,
be aware that you've received this mail in error. Any utilization, duplication,
distribution, forwarding, printing, or publicizing of this email or the attached files
is strictly prohibited, as is revealing the information contained within.
If you've received this email in error, please promptly inform the sender and
remove it from your electronic mailbox.
	\n**********************************************************************
	"""

	email_content += confidentiality_warning
	return email_content


def send_incident_report(incidents_dict):
	success = True
	homeserver_dict = {}

	# Aggregate incidents by homeserver.
	for full_username, room_dict in incidents_dict.items():
		baseurl = full_username.split(":")[1]

		if baseurl not in homeserver_dict:
			homeserver_dict[baseurl] = {}
		homeserver_dict[baseurl][full_username] = room_dict

	print("homeserver_dict: " + str(homeserver_dict))
	# Prepare and send one email per homeserver, including all users and rooms.
	for baseurl, user_dict in homeserver_dict.items():
		if hardcoded_variables.testing_mode == True:
			admin_email_dict = {baseurl: [hardcoded_variables.report_return_email]}
			print("admin_email_dict: " + str(admin_email_dict))
			from_whois = True
		elif hardcoded_variables.testing_mode == False:
			admin_email_dict, from_whois = lookup_homeserver_admin_email(baseurl)

		if not admin_email_dict or baseurl not in admin_email_dict:
			print(f"Unable to find any admin emails for {baseurl}")
			success = False
			continue

		# Prepare and send one email per homeserver, including all users and rooms.
		for email_address in admin_email_dict[baseurl]:
			email_subject = f"Incident Report for users from {baseurl}"
			email_content = prepare_email_content(user_dict, from_whois, baseurl)

			email_attachments = []
			if not send_email(email_address, email_subject, email_content, email_attachments):
				print(f"Failed to send email to {email_address}")
				success = False

	return success

def test_send_incident_reports():
	incidents_dict = {
		f"@billybob:matrix.org": {
			"!dummyid1:matrix.org": ["csam", "lolicon", "beastiality"],
			"!dummyid2:matrix.org": ["csam", "anarchy"]
		},
		f"@johndoe:matrix.org": {
			"!dummyid3:matrix.org": ["csam", "lolicon", "toddlercon"],
			"!dummyid4:matrix.org": ["csam", "terrorism"]
		},
		f"@pedobear:perthchat.org": {
			"!dummyid5:matrix.org": ["csam", "lolicon", "jailbait"],
			"!dummyid6:matrix.org": ["csam", "hub_links"]
		},
		f"@randomcreep:perthchat.org": {
			"!dummyid7:matrix.org": ["csam", "jailbait"],
			"!dummyid8:matrix.org": ["csam", "pre_ban"]
		},
		f"@fatweeb:grin.hu": {
			"!dummyid9:matrix.org": ["csam", "lolicon"],
			"!dummyid10:matrix.org": ["csam", "degen"]
		}
	}

	try:
		if hardcoded_variables.testing_mode == True:
			print("\nWARNING: TESTING MODE ENABLED, SENDING EMAIL TO: " + hardcoded_variables.report_return_email + "\n")
		if send_incident_report(incidents_dict):
			print("\nIncident reports successfully sent.")
		else:
			print("\nFailed to send the incident reports.")
	except Exception as e:
		print(f"\nFailed to send incident reports: {e}")
