
# Matrix Moderation Tool

A Matrix moderation tool to make managing a Synapse server easier.

Contact me at [@michael:perthchat.org](https://matrix.to/#/@michael:perthchat.org) if you get stuck or have an edit in mind.


***
## Licensing

This work is published under the MIT license, for more information on this license see here: https://opensource.org/license/mit/


***
## Setup script

You can hard code the server URL, federation port and access token into the [hardcoded_variables.py](./hardcoded_variables.py) file for faster use, it will prompt you for these values if you don't.

Your access token can be found in Element > Settings > Help & About, your user account must first be upgraded to a server admin.

This script also requires you to install the following PIP packages:
```
pip3 install python-whois
pip3 install requests
pip3 install matrix-nio
```


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
## Roadmap

To do:
1) Add the following functions:
- https://matrix-org.github.io/synapse/latest/admin_api/user_admin_api.html#find-a-user-based-on-their-id-in-an-auth-provider
- https://matrix-org.github.io/synapse/latest/admin_api/user_admin_api.html#find-a-user-based-on-their-third-party-id-threepid-or-3pid
- https://github.com/matrix-org/synapse/blob/master/docs/admin_api/delete_group.md
2) Add fully automated (should just return a web link and decryption password) reporting functions for users:
- Description of why the report was made (what happened), include key information
- User's ID - DONE
- Whois Data - DONE
- Account Data - DONE
- Query Data - DONE
- Pushers List - DONE
- IPs + ipinfo Data - DONE
- List of the rooms the user is participating in, divided into 1:1 conversations and larger rooms - DONE
- Any other usernames associated with that IP
- Timestamp for when illegal material was accessed
- Description of report format and contents (to guide the reader)
- Collect state event dumps of recently read rooms as well (as they may have looked at other suss rooms recently)
3) Have recommended rdlist function:
- return a list of offending accounts and the tags they accessed (for creating incident_dict's)
- add the shadowban function to prevent members alerting others after mass shutdowns - DONE
4) Only email reportID in incident report?
5) Add a room report function to create a properly formatted report for rdlist
6) Expand the incident reporting to also issue reports over Matrix
7) Automated public room joining and reminder if reporting email is not available?
8) Refine ipinfo module to also return extra details about the IP
9) Make existing functions compatible with JSON formatted inputs


***
## rdlist Functionality

'rdlist' is a comprehensive list of child abuse related rooms on Matrix, it's a safety initiative led by the [Legion of Janitors](https://matrix.to/#/#janitors:glowers.club).

This script can automatically load and block/purge abusive rooms from rdlist, making it **very easy** for inexperienced administrators to block this harmful content.

If you are running a public server, please dm me at [@michael:perthchat.org](https://matrix.to/#/@michael:perthchat.org) and I can invite you to the 'Legion of Janitors' room.

Once you have read access to the [rdlist repository](https://code.glowers.club/loj/rdlist), this script can be used for multiple rdlist related functions.


***
## Collect User Reports on local users in rdlist rooms

This script can automatically generate 'User Reports' for each one of your local users in rdlist rooms that have the 'recommended tags'.

These user reports can be given to law enforcement or shared in [#janitor-dumps](https://matrix.to/#/#janitor-dumps:glowers.club) to help us locate more abusive users/rooms.

```
130

rdlist repo already cloned...
Fetching origin
Pulling latest changes from rdlist repo...

WARNING! The following local users are current members of rooms tagged in rdlist: ['@fatweeb23838:perthchat.org', '@somecreep29330:perthchat.org']

Do you want to generate a user report file for each of these users? y/n? y

Generating user report for fatweeb23838...
Report generated successfully on user: "fatweeb23838"

You can send this .zip file when reporting a user to law enforcement.
.zip file location: /home/pcadmin/PerthchatVault/Perthchat_LIVE/matrix-moderation-tool/reports/fatweeb23838_2023-08-01_23-19-24.zip
.zip file size: 0.00966 MB


Generating user report for somecreep29330...
Report generated successfully on user: "somecreep29330"

You can send this .zip file when reporting a user to law enforcement.
.zip file location: /home/pcadmin/PerthchatVault/Perthchat_LIVE/matrix-moderation-tool/reports/somecreep29330_2023-08-01_23-19-27.zip
.zip file size: 0.29578 MB
```


***
## Send Incident Reports for remote users in rdlist rooms

This script can automatically generate 'Incident Reports' for every remote homeserver admin with users in rdlist rooms that have the 'recommended tags'.

It examines the homeserver involved to find a admin contact method via [MSC1929](https://github.com/matrix-org/matrix-spec-proposals/pull/1929). If an MXID is returned it will attempt to send the Incident Report over Matrix. If an email is provided it will send the Incident Report over email. If neither is found a whois lookup is performed and the Incident Report are sent to the domain registrar via email.

```
131

rdlist repo already cloned...
Fetching origin
Pulling latest changes from rdlist repo...

WARNING! The following remote users are current members of rooms tagged in rdlist: ['@pedobear:matrix.org', '@randomcreep:perthchat.org']

Do you want to send out incident reports for these users to every homeserver admin involved? y/n? y

Sending Incident Report for users from matrix.org to abuse@matrix.org

Sending Incident Report for users from perthchat.org to @michael:perthchat.org

```

![A preview of an Incident Report being sent over Matrix.](https://github.com/PC-Admin/matrix-moderation-tool/assets/29645145/db5a4a56-fd66-413a-ac44-1216c7b2f1fd)


## rdlist Block/Purge all rooms with recommended rdlist tags

Finally this script can be used to shutdown rooms with the recommended rdlist tags.

This function is much larger and will ask you if you also want to create user/incident reports before the shutdowns. (Recommended) It'll also ask you if you want to shadowban the users in these rooms to prevent them from alerting others. (Recommended) Finally it'll ask if you want to shutdown the local accounts located in these rooms.

```
$ python3 moderation_tool.py 

Please select one of the following options:
...
Please enter a number from the above menu, or enter 'q' or 'e' to exit.

132

@mod_team:perthchat.org account already exists. Resetting account password.

Ensuring @mod_team:perthchat.org account is a server admin.

rdlist repo already cloned...
Fetching origin
rdlist repo is up-to-date, no need to pull changes.

Using recommended rdlist tags. Rooms matching the following tags will be purged and/or blocked:
['hub_room_links', 'hub_room_trade', 'preban', 'degen_misc', 'beastiality', 'degen_porn', 'gore', 'snuff', 'degen_larp', 'hub_room_sussy', 'bot_spam', 'cfm', 'jailbait', 'bot_porn', 'toddlercon', 'loli', 'csam', 'tfm', 'degen_meet', 'stylized_3d_loli', '3d_loli']

WARNING! The following local users are current members of rooms tagged in rdlist: ['@***REDACTED***:perthchat.org']

Do you want to generate a user report file for each of these users? y/n? n

Skipping user report generation...

WARNING! The following remote users are current members of rooms tagged in rdlist: ['@***REDACTED***:matrix.org']

Do you want to send out incident reports for these users to every homeserver admin involved? y/n? n

Skipping incident report generation...


Number of rdlist rooms being shutdown: 346

Are you sure you want to block/shutdown these rooms? y/n? y


Skipping already blocked room: !***REDACTED***:matrix.org


Skipping already blocked room: !***REDACTED***:matrix.org


Skipping already blocked room: !***REDACTED***:matrix.org


Blocking unknown room: !***REDACTED***:matrix.org
Successfully blocked room !***REDACTED***:matrix.org


Blocking unknown room: !***REDACTED***:matrix.org
Successfully blocked room !***REDACTED***:matrix.org


Skipping already blocked room: !***REDACTED***:matrix.org


Shutting down known room: !***REDACTED***:sibnsk.net
Sleeping for 2 seconds...
Sleeping for 4 seconds...
Sleeping for 8 seconds...
!***REDACTED***:sibnsk.net has been successfully shutdown!
List of kicked users:
@***REDACTED***:perthchat.org


Skipping already blocked room: !***REDACTED***:anontier.nl


Room shutdowns completed!

User login details for your moderator account:

Username: mod_team
Password: ***REDACTED***

Print rdlist statistics:

Number of rooms blocked: 4
Number of rooms purged: 2
Number of local users located in rdlist rooms and kicked: 1

The following users were current members of rooms tagged in rdlist: ['@***REDACTED***:perthchat.org']

Do you want to also deactivate all these accounts that were kicked from rdlist rooms? y/n?
...
```


***
## One-touch Reporting

WARNING: This section is under heavy development and shouldn't be used by anyone!!!

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
