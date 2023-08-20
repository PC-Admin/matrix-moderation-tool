
# Matrix Moderation Tool

A Matrix moderation tool to make managing a Synapse server easier.

Contact me at [@michael:perthchat.org](https://matrix.to/#/@michael:perthchat.org) if you get stuck or have an edit in mind.


***
## List of Functions

This tool abstracts the Synapse API so you can perform common moderation functions easier and in batch.

Here is a preview of the CLI interface:
```
##########################
# MATRIX MODERATION TOOL #
##########################

A tool for making common Synapse moderation tasks easier. Created by @PC-Admin.

----------------------------------------------

#### User Account Commands ####			    	#### Room Commands ####
1) Deactivate a user account.			    	50) List details of a room.
2) Deactivate multiple user accounts.			51) List the members of a room.
3) Create a user account.			        52) Export the state events of a room.
4) Create multiple user accounts.		    	53) Export the state events of multiple rooms.
5) Reset a users password.			        54) List rooms in public directory.
6) Whois user account.				        55) Remove a room from the public directory.
7) Whois multiple user accounts.		    	56) Remove multiple rooms from the public directory.
8) Query user account.				        57) Redact a room event.
9) Query multiple user accounts.		    	58) List/Download all media in a room.
10) List room memberships of user.		    	59) Download media from multiple rooms.
11) Promote a user to server admin.		    	60) Quarantine all media in a room.
12) List all user accounts.			        61) Shutdown a room.
13) Quarantine all media a users uploaded.		62) Shutdown multiple rooms.
14) Collect account data.			        63) Delete a room.
15) List account pushers.			        64) Delete multiple rooms.
16) Get rate limit of a user account.			65) Purge the event history of a room to a specific timestamp.
17) Set rate limit of a user account.			66) Purge the event history of multiple rooms to a specific timestamp.
18) Delete rate limit of a user account.		67) Get blocked status for room.
19) Check if user account exists.		    	68) Block a room.
20) Shadow ban a user.				        69) Unblock a room.
21) Find a user by their 3PID.

#### Server Commands ####					#### ipinfo.io ####
100) Delete and block a specific media.				140) Analyse a users country of origin.
101) Purge remote media repository up to a certain date.	141) Analyse multiple users country of origin.
102) Prepare database for copying events of multiple rooms.
103) Show last 10 reported events.				#### Report Generation ####
104) Get all reported events.					150) Generate user report.
105) Get details of a reported event.				151) Lookup homeserver admin contact details.
								152) Send a test email (to yourself).
#### rdlist - General ####					153) Send a test Matrix message (to yourself).
120) Block all rooms with specific rdlist tags.			154) Send test incident reports (to yourself).
121) Get rdlist tags for a room.

#### rdlist - Recommended Tags ####
For rdlist rooms with recommended tags, the following actions are available:
130) Collect User Reports on local accounts in rdlist rooms.
131) Send Incident Reports on remote accounts in rdlist rooms.
132) Block/Purge all rdlist rooms.
```


***
## Licensing

This work is published under the MIT license, for more information on this license see here: https://opensource.org/license/mit/


***
## Setup script

Firstly, you need hard code the 'server URL', 'federation port' and 'access token' into the [hardcoded_variables.py](./hardcoded_variables.py) file 
```
$ cp ./hardcoded_variables.py.sample ./hardcoded_variables.py
$ nano ./hardcoded_variables.py
```

Your access token can be found in Element > Settings > Help & About, your user account must first be upgraded to a server admin.

This script also requires you to install the following PIP packages:
```
$ pip3 install python-whois && \
pip3 install requests && \
pip3 install matrix-nio
```

***
## Running the script

`$ python3 moderation_tool.py`


***
## Upgrade user to 'server admin'

To use this moderation script you need an OAuth token of a "server admin" account. If you've just setup a Matrix server, you'll need to promote an account to server admin by altering your database.

https://github.com/matrix-org/synapse/tree/master/docs/admin_api

“So first connect to the correct db and then run the UPDATE users...”

$ sudo -i -u postgres

$ psql synapse

synapse=# UPDATE users SET admin=1 WHERE name='@PC-Admin:perthchat.org';

UPDATE 1

synapse=# 

Note: A ‘-’ sign instead of ‘=’ means you didn't type a complete SQL query yet!

(You need a semicolon (;) at the end to terminate the command.)


***
## Make sure /_synapse/ is mapped

A few of the commands will not work unless /_synapse/ is mapped to port 8008. Here is a example for nginx:

```

    location /_matrix {
        proxy_pass http://127.0.0.1:8008;
        proxy_set_header X-Forwarded-For $remote_addr;
    }

    location /_synapse {
        proxy_pass http://127.0.0.1:8008;
        proxy_set_header X-Forwarded-For $remote_addr;
    }

```

You can also run the script locally on your server if you do not wish to map /_synapse/.

With the popular [matrix-docker-ansible-deploy](https://github.com/spantaleev/matrix-docker-ansible-deploy) playbook you can expose this API interface by enabling 'Synapse Admin':

`matrix_synapse_admin_enabled: true`


***
## rdlist Functionality

'rdlist' is a comprehensive list of child abuse related rooms on Matrix, it's a safety initiative led by the [Legion of Janitors](https://matrix.to/#/#janitors:glowers.club).

This script can automatically load and block/purge abusive rooms from rdlist, making it **very easy** for inexperienced administrators to block this harmful content.

If you are running a public server, please dm me at [@michael:perthchat.org](https://matrix.to/#/@michael:perthchat.org) and I can invite you to the 'Legion of Janitors' room.

For more information on rdlist related function consult the [support document](./docs/rdlist_functions.md).


***
## One-touch Reporting

CAUTION: This section is under heavy development and probably shouldn't be used by anyone!

This script can automatically generate reports about user accounts for law enforcement.

It collects as much data about the target user account as possible, then packages it into an encrypted ZIP file that can be shared:
```

Please enter a number from the above menu, or enter 'q' or 'e' to exit.

150

Please enter the username to automatically generate a report: pedobear

...

Report generated successfully on user: "pedobear"

You can send this .zip file and password when reporting a user to law enforcement.

.zip file location: ./reports/pedobear_2023-07-23_02-21-56.zip
.zip file size: 0.503927 MB
```


***
## Roadmap

To do:
1) Add the following functions:
- https://matrix-org.github.io/synapse/latest/admin_api/user_admin_api.html#find-a-user-based-on-their-id-in-an-auth-provider
- https://matrix-org.github.io/synapse/latest/admin_api/user_admin_api.html#find-a-user-based-on-their-third-party-id-threepid-or-3pid - DONE
- https://github.com/matrix-org/synapse/blob/master/docs/admin_api/delete_group.md
- https://matrix-org.github.io/synapse/v1.38/admin_api/rooms.html#make-room-admin-api
- https://matrix-org.github.io/synapse/latest/admin_api/server_notices.html
- https://matrix-org.github.io/synapse/latest/admin_api/event_reports.html
- https://matrix-org.github.io/synapse/latest/usage/administration/admin_api/federation.html#destination-rooms
2) Add fully automated (should just return a web link and decryption password) reporting functions for users:
- Description of why the report was made (what happened), include key information
- Any other usernames associated with that IP
- Timestamp for when illegal material was accessed
- Description of report format and contents (to guide the reader)
- Collect state event dumps of recently read rooms as well (as they may have looked at other suss rooms recently)
3) Have recommended rdlist function:
- return a list of offending accounts and the tags they accessed (for creating incident_dict's) - DONE
- add the shadowban function to prevent members alerting others after mass shutdowns - DONE
4) Only email reportID in incident report?
5) Add a room report function to create a properly formatted report for rdlist
6) Expand the incident reporting to also issue reports over Matrix
7) Automated public room joining and reminder if reporting email is not available?
8) Refine ipinfo module to also return extra details about the IP
9) Make existing functions compatible with JSON formatted inputs
