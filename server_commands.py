
import os
import subprocess
import csv
import time
import requests
import datetime
import hardcoded_variables

def delete_block_media():
	# Take media_id from user
	media_id = input("\nEnter the media_id of the media you would like to delete and block on your server. (Example: For this media https://matrix.perthchat.org/_matrix/media/r0/download/matrix.org/eDmjusOjnHyFPOYGxlrOsULJ the media_id is 'eDmjusOjnHyFPOYGxlrOsULJ'): ")
	remote_server = input("\nEnter the remote servers URL without the 'https://' (Example: matrix.org): ")
	# find filesystem_id from database
	command_collect_filesystem_id = "ssh " + hardcoded_variables.homeserver_url + """ "/matrix/postgres/bin/cli-non-interactive --dbname=synapse -t -c 'SELECT DISTINCT filesystem_id FROM remote_media_cache WHERE media_id = '\\''""" + media_id + """'\\'" | xargs"""
	print(command_collect_filesystem_id)
	process_collect_filesystem_id = subprocess.run([command_collect_filesystem_id], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
	filesystem_id = process_collect_filesystem_id.stdout
	print(process_collect_filesystem_id.stdout)
	# list the target files on disk
	command_collect_thumbnails = "ssh " + hardcoded_variables.homeserver_url + ' "find /matrix/synapse/storage/media-store/remote_thumbnail/' + remote_server + '/' + filesystem_id[:2] + "/" + filesystem_id[2:4] + "/" + filesystem_id[4:].rstrip() + """ -type f -printf '%p\\n'\""""
	print(command_collect_thumbnails)
	process_collect_thumbnails = subprocess.run([command_collect_thumbnails], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
	remote_thumbnails_list = process_collect_thumbnails.stdout
	print(remote_thumbnails_list)
	command_content_location = "ssh " + hardcoded_variables.homeserver_url + ' "ls /matrix/synapse/storage/media-store/remote_content/' + remote_server + '/' + filesystem_id[:2] + "/" + filesystem_id[2:4] + "/" + filesystem_id[4:].rstrip() + '"'
	print(command_content_location)
	process_content_location = subprocess.run([command_content_location], shell=True, stdout=subprocess.PIPE, universal_newlines=True)
	remote_content_location = process_content_location.stdout
	print(remote_content_location)
	# Zero the target files on disk then chattr +i them
	for line in remote_thumbnails_list.split('\n'):
		if line:
			command_zero_thumbnails = 'ssh ' + hardcoded_variables.homeserver_url + ' "true > ' + line + '"'
			print(command_zero_thumbnails)
			process_zero_thumbnails = subprocess.run(command_zero_thumbnails, shell=True)
			print(process_zero_thumbnails.stdout)
			command_make_thumbnail_immutable = 'ssh ' + hardcoded_variables.homeserver_url + ' "chattr +i ' + line + '"'
			print(command_make_thumbnail_immutable)
			process_make_thumbnail_immutable = subprocess.run(command_make_thumbnail_immutable, shell=True)
			print(process_make_thumbnail_immutable.stdout)
	command_zero_media = 'ssh ' + hardcoded_variables.homeserver_url + ' "true > ' + remote_content_location.rstrip() + '"'
	print(command_zero_media)
	process_remove_media = subprocess.run(command_zero_media, shell=True)
	print(process_remove_media.stdout)
	command_make_content_immutable = 'ssh ' + hardcoded_variables.homeserver_url + ' "chattr +i ' + remote_content_location.rstrip() + '"'
	print(command_make_content_immutable)
	process_make_content_immutable = subprocess.run(command_make_content_immutable, shell=True)
	print(process_make_content_immutable.stdout)

# Example, first use the media_id to find the filesystem_id:
# $ ssh matrix.perthchat.org "/matrix/postgres/bin/cli-non-interactive --dbname=synapse -t -c 'SELECT DISTINCT filesystem_id FROM remote_media_cache WHERE media_id = '\''eDmjusOjnHyFPOYGxlrOsULJ'\'" | xargs
# ehckzWWeUkDhhPfNFkcfCFNv

# Then use that filesystem_id to locate the remote file and all it's thumbnails:
# $ ssh matrix.perthchat.org "find /matrix/synapse/storage/media-store/remote_thumbnail/matrix.org/eh/ck/zWWeUkDhhPfNFkcfCFNv -type f -printf '%p\n'"
#/matrix/synapse/storage/media-store/remote_thumbnail/matrix.org/eh/ck/zWWeUkDhhPfNFkcfCFNv/32-32-image-jpeg-crop
#/matrix/synapse/storage/media-store/remote_thumbnail/matrix.org/eh/ck/zWWeUkDhhPfNFkcfCFNv/640-480-image-jpeg-scale
# ...
# $ ssh matrix.perthchat.org "ls /matrix/synapse/storage/media-store/remote_content/matrix.org/eh/ck/zWWeUkDhhPfNFkcfCFNv"
# /matrix/synapse/storage/media-store/remote_content/matrix.org/eh/ck/zWWeUkDhhPfNFkcfCFNv

# Then zero each file and make it immutable:
# $ ssh matrix.perthchat.org "true > /matrix/synapse/storage/media-store/remote_thumbnail/matrix.org/eh/ck/zWWeUkDhhPfNFkcfCFNv/32-32-image-jpeg-crop"
# $ ssh matrix.perthchat.org "chattr +i /matrix/synapse/storage/media-store/remote_thumbnail/matrix.org/eh/ck/zWWeUkDhhPfNFkcfCFNv/32-32-image-jpeg-crop"
# $ ssh matrix.perthchat.org "true > /matrix/synapse/storage/media-store/remote_thumbnail/matrix.org/eh/ck/zWWeUkDhhPfNFkcfCFNv/640-480-image-jpeg-scale"
# $ ssh matrix.perthchat.org "chattr +i /matrix/synapse/storage/media-store/remote_thumbnail/matrix.org/eh/ck/zWWeUkDhhPfNFkcfCFNv/640-480-image-jpeg-scale"
# ...
# $ ssh matrix.perthchat.org "true > /matrix/synapse/storage/media-store/remote_content/matrix.org/eh/ck/zWWeUkDhhPfNFkcfCFNv"
# $ ssh matrix.perthchat.org "chattr +i /matrix/synapse/storage/media-store/remote_content/matrix.org/eh/ck/zWWeUkDhhPfNFkcfCFNv"

def purge_remote_media_repo():
	purge_from = int(input("\nEnter the number of days to purge from: "))
	purge_too = int(input("\nEnter the number of days to purge too: "))

	while purge_from >= purge_too:
		# Calculate the epoch timestamp for 'purge_from' days ago
		epoch_time = int((datetime.datetime.now() - datetime.timedelta(days=purge_from)).timestamp())
		# Convert to milliseconds (as per your original code)
		epoch_time_millis = epoch_time * 1000

		# Make the request
		headers = {"Authorization": "Bearer " + hardcoded_variables.access_token}
		url = f"https://{hardcoded_variables.homeserver_url}/_synapse/admin/v1/purge_media_cache"
		params = {"before_ts": epoch_time_millis}
		response = requests.post(url, headers=headers, params=params)

		print(response.text)

		purge_from -= 1
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

def get_reported_events(limit=100, _from=0, dir='b', user_id=None, room_id=None):
    url = f"https://{hardcoded_variables.homeserver_url}/_synapse/admin/v1/event_reports"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {hardcoded_variables.access_token}"
    }

    params = {
        'limit': limit,
        'from': _from,
        'dir': dir
    }

    if user_id:
        params['user_id'] = user_id

    if room_id:
        params['room_id'] = room_id

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching reported events: {response.status_code}, {response.text}")
        return None

def paginate_reported_events(limit=100, dir='b', user_id=None, room_id=None):
    _from = 0
    all_reports = []

    while True:
        reports = get_reported_events(limit=limit, _from=_from, dir=dir, user_id=user_id, room_id=room_id)
        if not reports or "event_reports" not in reports:
            break

        all_reports.extend(reports["event_reports"])

        if "next_token" in reports:
            _from = reports["next_token"]
        else:
            break

    return all_reports

def get_event_report_details(preset_report_id=''):
    if preset_report_id == '':
        report_id = input("\nEnter the report_id of the report you wish to query (Example: 56): ")
    elif preset_report_id != '':
        report_id = preset_report_id

    url = f"https://{hardcoded_variables.homeserver_url}/_synapse/admin/v1/event_reports/{report_id}"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {hardcoded_variables.access_token}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching event report details: {response.status_code}, {response.text}")
        return None
