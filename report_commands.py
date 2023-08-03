
import os
import json
import whois
import datetime
import zipfile
import smtplib
import requests
import asyncio
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE
from email import encoders
import user_commands
import room_commands
import ipinfo_commands
import bot_commands
import hardcoded_variables

rdlist_tag_descriptions = {
    "csam": "Child Sexual Abuse Material",
    "cfm": "An abundance of content which would directly appeal to those seeking csam.",
    "jailbait": "Photos which contain underage individuals in questionable or suggestive situations.",
    "tfm": "An abundance of content which would directly appeal to those seeking jailbait.",
    "beastiality": "Self explanatory.",
    "3d_loli": "Pornography which depicts photorealistic underage characters.",
    "stylized_3d_loli": "Pornography which depicts underage characters that are not depicted in a realistic style.",
    "gore": "Self explanatory.",
    "snuff": "Self explanatory.",
    "degen_misc": "Other types of coomers rooms.",
    "degen_larp": "Coomer larp rooms.",
    "degen_meet": "Coomer socializing rooms.",
    "degen_porn": "Rooms dedicated to pornography, excluding types which have dedicated tags.",
    "bot_porn": "Rooms which contain bots that spam pornographic content.",
    "bot_spam": "Rooms which contain bots that spam content. Primarily for malvertising and cryptospam",
    "preban": "Rooms which may not contain tagged content, however have clear intent. i.e: Rooms with names like 'CP Room', 'Child Porn', etc",
    "hub_room_trade": "Rooms which exist solely to trade illegal or questionable content. i.e: csam, jailbait",
    "hub_room_sussy": "A room which is sussy. This tag does not have a solid definition, see existing tagged rooms",
    "abandoned": "Similar to 'anarchy', primarily for rooms which have automated spam bots.",
    "anarchy": "Unmoderated rooms.",
    "hub_room_underage": "Rooms which contain a disproportionate amount of underage users.",
    "hub_room_links": "Rooms which exist to share links to other rooms.",
    "toddlercon": "Lolicon but younger.",
    "loli": "Rooms which exist to host lolicon.",
}

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

def get_report_folder():
	# Get report_folder from hardcoded_variables
	report_folder = hardcoded_variables.report_folder

	# If report_folder ends with a slash, remove it
	if report_folder.endswith(os.sep):
		report_folder = report_folder[:-1]

	return report_folder

def zip_report_folder(user_report_folder, username):
	# Get parent directory of user_report_folder
	parent_directory = os.path.dirname(os.path.abspath(user_report_folder))

	# Create the name of the .zip file including timestamp
	zip_file_name = os.path.join(parent_directory, username + "_" + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".zip")

	# Create a .zip file of the specified folder
	with zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED) as zip_file:
		for root, dirs, files in os.walk(user_report_folder):
			for file in files:
				zip_file.write(os.path.join(root, file), arcname=os.path.relpath(os.path.join(root, file), user_report_folder))

	return zip_file_name

def generate_user_report(preset_username, report_details):
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

	# Collect and write the report details to ./report/username/report_details.txt
	if report_details == '':
		report_details = input("\nPlease enter the details for this report. Include as much detail as possible, including:\n- A description of what happened.\n- Timestamps of events.\n- Whether this user was a repeat offender, if so include details about previous incidents.\n- Other user or rooms involved.\n- Other evidence you've collected against this user.\n- Whether the offending users were deactivated.\n- Whether the offending rooms were shut down.\n\n")
	report_details_file = open(user_report_folder + "report_details.txt", "w")
	report_details_file.write(report_details)
	report_details_file.close()

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
	forgotten_folder = user_report_folder + "forgotten/"
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

	# For forgotten rooms, get the state and write to ./report/username/forgotten/states/
	forgotten_states_folder = forgotten_folder + states_folder
	if not os.path.exists(forgotten_states_folder):
		os.makedirs(forgotten_states_folder, exist_ok=True)

	# For forgotten rooms, get the details and write to ./report/username/forgotten/details/
	forgotten_details_folder = forgotten_folder + details_folder
	if not os.path.exists(forgotten_details_folder):
		os.makedirs(forgotten_details_folder, exist_ok=True)

	room_list = list(account_data['account_data']['rooms'].keys())

	count = 0
	for room in room_list:
		count += 1
		room = room.split(" ")[0]
		room_details = room_commands.get_room_details(room)

		# Check the room conditions to select the proper output folders
		if room_details['forgotten'] == True:
			room_details_file = open(forgotten_details_folder + room + ".json", "w")
			room_commands.export_room_state(room, forgotten_states_folder, True)
		elif room_details['joined_members'] == 2 and room_details['public'] == False:
			room_details_file = open(dm_details_folder + room + ".json", "w")
			room_commands.export_room_state(room, dm_states_folder, True)
		else:
			room_details_file = open(room_details_folder + room + ".json", "w")
			room_commands.export_room_state(room, room_states_folder, True)

		room_details_file.write(json.dumps(room_details, indent=4, sort_keys=True))
		room_details_file.close()

		if count > 10 and hardcoded_variables.testing_mode == True:
			break

	# Generate a random password, then encrypt the ./report/username/ folder to a timestamped .zip file
	zip_file_name = zip_report_folder(user_report_folder, username)

	# Measure the size of the encrypted .zip file in MB
	zip_file_size = os.path.getsize(zip_file_name) / 1000000

	# Print the password and the encrypted .zip file name
	print("Report generated successfully on user: \"" + username + "\"\n\nYou can send this .zip file when reporting a user to law enforcement.\n")
	print(".zip file location: " + zip_file_name)
	print(".zip file size: " + str(zip_file_size) + " MB\n")

	return zip_file_name

def lookup_homeserver_admin(preset_baseurl):
	if hardcoded_variables.testing_mode == True:
		baseurl = hardcoded_variables.base_url
	elif preset_baseurl == '':
		baseurl = input("\nEnter the base URL to collect the admin contact details (Example: matrix.org): ")
	elif preset_baseurl != '':
		baseurl = preset_baseurl

	# If baseurl is matrix.org, return 'abuse@matrix.org' as a hardcoded response
	if baseurl == "matrix.org":
		print("\nAdmin contact email(s) for " + baseurl + " are: abuse@matrix.org")
		return {"admins": [{"email_address": "abuse@matrix.org"}]}, False

	# Check target homserver for MSC1929 support email
	url = f"https://{baseurl}/.well-known/matrix/support"
	try:
		response = requests.get(url)
	except requests.exceptions.RequestException as e:
		print(f"Error: Unable to connect to server {baseurl}. Trying WHOIS data...")
		response = None

	# If the request was successful, the status code will be 200
	if response.status_code == 200 and ( "email_address" in response.text or "matrix_id" in response.text ):
		# Parse the response as JSON
		data = json.loads(response.text)

		#print("\nAdmin contact details for " + baseurl + " are: " + str(data))

		return data, False
	else:
		print(f"Error: Unable to collect admin contact details from server {baseurl}")
		print("Attempting to collect admin email from WHOIS data...")

		# Get WHOIS data
		try:
			w = whois.whois(baseurl)
			if w.emails:
				# Check if the emails field is a list
				if isinstance(w.emails, list):
					# Create a list of dictionaries, each containing one email address
					emails_dict_list = [{"email_address": email} for email in w.emails]
					return {"admins": emails_dict_list}, True
				# If it's not a list, it must be a single string. So, we wrap it in a list
				else:
					return {"admins": [{"email_address": w.emails}]}, True
			else:
				print(f"\t\tError: Unable to collect admin email from WHOIS data for {baseurl}")
				return None, False
		except:
			print(f"\t\tError: Unable to collect WHOIS data for {baseurl}")
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
	email_address = hardcoded_variables.incident_report_return_email

	# Example email parameters
	email_subject = "Incident Report"
	email_content = "Hello! This is a test email. Please ignore it."
	email_attachments = ["./test_data/evil_clown.jpeg"]  # List of file paths. Adjust this to the actual files you want to attach.

	# Try to send the email
	if send_email(email_address, email_subject, email_content, email_attachments):
		print("\nEmail successfully sent.")
	else:
		print("\nFailed to send email.")

def generate_rdlist_report_summary(room_dict, user_id):
    #print(f"user_dict: {room_dict}")
    report_content = f"""\n~~~User Report~~~\n\nUsername: {user_id}\n"""

    for room_id, rdlist_tags in room_dict.items():
        report_content += f"\nWas a member of this room: {room_id}\nThis room has been flagged with the following rdlist tags:\n"
        for tag in rdlist_tags:
            tag_description = rdlist_tag_descriptions.get(tag, "No description available.")
            report_content += f"  - {tag} ({tag_description})\n"

    report_content

    return report_content

def prepare_email_content(user_dict, from_whois, baseurl):
	email_content = f"""Dear Administrator,

We regret to inform you that there have been incidents involving the following users in your homeserver:
	"""

	for full_username, room_dict in user_dict.items():
		email_content += f"\nUser: {full_username}\n"
		for room_id, rdlist_tags in room_dict.items():
			email_content += f"\n  Is in the room: {room_id}\n  This room has been flagged with the following rdlist tags:\n"
			for tag in rdlist_tags:
				tag_description = rdlist_tag_descriptions.get(tag, "No description available.")
				email_content += f"  - {tag} ({tag_description})\n"

	email_content += f"""

We request your immediate attention to this matter. It is recommended that you:
- Generate a report on these users' accounts and send it to law enforcement.
- Block and purge these rooms from your homeserver.
- Deactivate these users' accounts, or retain them for further observation.

All of these actions can be done automatically using this moderation tool:
https://github.com/PC-Admin/matrix-moderation-tool

**********************************************************************
\tTHIS EMAIL IS UNMONITORED, PLEASE DO NOT REPLY TO IT
**********************************************************************

To contact us please email {hardcoded_variables.incident_report_return_email}.

Thank you for helping us make Matrix safer.

Best regards,
Abuse Management Team
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

	email_content += confidentiality_warning
	return email_content

def prepare_message_content(user_dict, baseurl):
	message_content = f"""Dear Administrator,

We regret to inform you that there have been incidents involving the following users in your homeserver:
	"""

	for full_username, room_dict in user_dict.items():
		message_content += f"\nUser: {full_username}\n"
		for room_id, rdlist_tags in room_dict.items():
			message_content += f"\n  Is in the room: {room_id}\n  This room has been flagged with the following rdlist tags:\n"
			for tag in rdlist_tags:
				tag_description = rdlist_tag_descriptions.get(tag, "No description available.")
				message_content += f"  - {tag} ({tag_description})\n"

	message_content += f"""

We request your immediate attention to this matter. It is recommended that you:
- Generate a report on these users' accounts and send it to law enforcement.
- Block and purge these rooms from your homeserver.
- Deactivate these users' accounts, or retain them for further observation.

All of these actions can be done automatically using this moderation tool:
https://github.com/PC-Admin/matrix-moderation-tool

**********************************************************************
\tTHIS ACCOUNT IS UNMONITORED, PLEASE DO NOT REPLY TO IT
**********************************************************************

To contact us please message {hardcoded_variables.incident_report_return_mxid}.

Thank you for helping us make Matrix safer.

Best regards,
Abuse Management Team
https://{hardcoded_variables.base_url}
"""

	return message_content

async def send_incident_reports(incidents_dict):
	success = True
	homeserver_dict = {}

	# Aggregate incidents by homeserver.
	for full_username, room_dict in incidents_dict.items():
		baseurl = full_username.split(":")[1]

		if baseurl not in homeserver_dict:
			homeserver_dict[baseurl] = {}
		homeserver_dict[baseurl][full_username] = room_dict

	# Prepare and send one incident report per homeserver, including all users and rooms.
	for baseurl, user_dict in homeserver_dict.items():

		admin_contact_dict, from_whois = lookup_homeserver_admin(baseurl)

		if not admin_contact_dict or "admins" not in admin_contact_dict:
			print(f"Unable to find any admin emails for {baseurl}")
			success = False
			continue

		# Prepare and send one message or email per homeserver, including all users and rooms.
		for admin in admin_contact_dict["admins"]:
			#print(f"DEBUG: {type(admin)}")
			#print(f"DEBUG: {admin}")  # this will print the content of each admin dict
			if "matrix_id" in admin:	# If matrix_id exists
				message_content = prepare_message_content(user_dict, baseurl)

				try:
					print(f"\nSending Incident Report for users from {baseurl} to {admin['matrix_id']}")
					await bot_commands.send_message(admin["matrix_id"], message_content)
				except Exception as e:
					print(f"Failed to send message to {admin['matrix_id']}: {str(e)}")
					success = False
			# If email_address exists, or if message send failed, send Incident report via email
			elif "email_address" in admin or success == False:
				email_address = admin.get("email_address")
				if email_address:  # If email_address exists
					email_subject = f"Incident Report for users from {baseurl}"
					email_content = prepare_email_content(user_dict, from_whois, baseurl)

					email_attachments = []
					print(f"Sending Incident Report for users from {baseurl} to {admin['email_address']}")
					if not send_email(email_address, email_subject, email_content, email_attachments):
						print(f"Failed to send email to {email_address}")
						success = False

	return success

def test_send_incident_reports():
	incidents_dict = {
		f"@billybob:matrix.org": {
			"!dummyid1:matrix.org": ["csam", "loli", "beastiality"],
			"!dummyid2:matrix.org": ["csam", "anarchy"]
		},
		f"@johndoe:matrix.org": {
			"!dummyid3:matrix.org": ["csam", "loli", "toddlercon"],
			"!dummyid4:matrix.org": ["anarchy", "terrorism"]
		},
		f"@pedobear:perthchat.org": {
			"!dummyid5:matrix.org": ["csam", "loli", "jailbait"],
			"!dummyid6:matrix.org": ["csam", "hublinks"]
		},
		f"@randomcreep:perthchat.org": {
			"!dummyid7:matrix.org": ["csam", "jailbait"],
			"!dummyid8:matrix.org": ["csam", "preban"]
		},
		f"@fatweeb:grin.hu": {
			"!dummyid9:matrix.org": ["csam", "loli"],
			"!dummyid10:matrix.org": ["csam", "degen_porn"]
		}
	}

	try:
		if hardcoded_variables.testing_mode == True:
			print("\nNOTE: Testing mode is enabled, sending Incident Reports to you! :)\n")
		if asyncio.run(send_incident_reports(incidents_dict)):
			print("\nIncident reports successfully sent.")
		else:
			print("\nFailed to send the incident reports.")
	except Exception as e:
		print(f"\nFailed to send incident reports: {e}")
