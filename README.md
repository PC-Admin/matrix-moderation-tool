
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
pip3 install pyAesCrypt
```


***
## Upgrade user to 'server admin'

https://github.com/matrix-org/synapse/tree/master/docs/admin_api

“So first connect to the correct db and then run the UPDATE users...”

$ sudo -i -u postgres

$ psql synapse

synapse=# UPDATE users SET admin=1 WHERE name='@PC-Admin:perthchat.org';

UPDATE 1

synapse=# 

‘-’ sign instead of ‘=’ means:

It means you didn't type a complete SQL query yet.

You need a semicolon to terminate the command.


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
- https://matrix-org.github.io/synapse/latest/admin_api/user_admin_api.html#account-data - DONE
- https://matrix-org.github.io/synapse/latest/admin_api/user_admin_api.html#list-all-pushers - DONE
- https://matrix-org.github.io/synapse/latest/admin_api/user_admin_api.html#override-ratelimiting-for-users - DONE
- https://matrix-org.github.io/synapse/latest/admin_api/user_admin_api.html#check-username-availability - DONE
- https://matrix-org.github.io/synapse/latest/admin_api/user_admin_api.html#find-a-user-based-on-their-id-in-an-auth-provider
- https://matrix-org.github.io/synapse/latest/admin_api/user_admin_api.html#find-a-user-based-on-their-third-party-id-threepid-or-3pid
- https://github.com/matrix-org/synapse/blob/master/docs/admin_api/delete_group.md
2) Make the menu prettier! - DONE
3) Modularise the functions into multiple files - DONE
4) Use URI module for all API calls instead of curl - DONE
5) Add more automated rdlist function with sane defaults - DONE
6) Add fully automated (should just return a web link and decryption password) reporting functions for users:
- Description of why the report was made (what happened)
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
- Summary of key information
7) Have recommended rdlist function return a list of offending accounts and the tags they accessed
8) Only email reportID in incident report?
9) Add a room report function to create a properly formatted report for rdlist
10) Skip already shutdown rooms for speeding up rdlist blocking
11) Add function for probing the support email of another server automatically
12) Automated incident report email to other server owners who has users in rdlist rooms for more scalable coordination
13) Automated public room joining and reminder if reporting email is not available?
14) Refine ipinfo module to also return region/state of IP


***
## rdlist Functionality

'rdlist' is a comprehensive list of child abuse related rooms on Matrix, it's a safety initiative led by the [Legion of Janitors](https://matrix.to/#/#janitors:glowers.club).

This script can automatically load and block/purge abusive rooms from rdlist, making it **very easy** for inexperienced administrators to block this harmful content.

If you are running a public server, please dm me at [@michael:perthchat.org](https://matrix.to/#/@michael:perthchat.org) and I can invite you to the 'Legion of Janitors' room.

Once you have read access to the [rdlist repository](https://code.glowers.club/loj/rdlist), simply run this moderation script like so:
```
$ python3 moderation_tool.py 

Please select one of the following options:
...
Please enter a number from the above menu, or enter 'q' or 'e' to exit.

51

@mod_team:perthchat.org account already exists. Resetting account password.

Ensuring @mod_team:perthchat.org account is a server admin.

rdlist repo already cloned...
Fetching origin
rdlist repo is up-to-date, no need to pull changes.

Using recommended rdlist tags. Rooms matching the following tags will be purged and/or blocked:
['hub_room_links', 'hub_room_trade', 'preban', 'degen_misc', 'beastiality', 'degen_porn', 'gore', 'snuff', 'degen_larp', 'hub_room_sussy', 'bot_spam', 'cfm', 'jailbait', 'bot_porn', 'toddlercon', 'loli', 'csam', 'tfm', 'degen_meet', 'stylized_3d_loli', '3d_loli']

WARNING! The following local users are current members of rooms tagged in rdlist: ['***REDACTED***:perthchat.org']

Do you want to generate a user report file for each of these users? y/n? n

Skipping user report generation...


Number of rdlist rooms being shutdown: 337

Are you sure you want to shutdown these rooms? y/n? y


Shutting down room: !***REDACTED***:matrix.org
!***REDACTED***:matrix.org has been successfully shutdown!


Shutting down room: !***REDACTED***:matrix.org
!***REDACTED***:matrix.org has been successfully shutdown!


Shutting down room: !***REDACTED***:anontier.nl
!***REDACTED***:anontier.nl has been successfully shutdown!


Shutting down room: !***REDACTED***:anontier.nl
!***REDACTED***:anontier.nl has been successfully shutdown!
...
```

Note that this script before shutting these rooms down will save the state events to the "./state_events" folder, please keep this data as it's important for law enforcement.


***
## One-touch Reporting

WARNING: This section is under heavy development and shouldn't be used by anyone!!!

This script can automatically generate reports about user accounts for law enforcement.

It collects as much data about the target user account as possible, then packages it into an encrypted ZIP file that can be shared:
```

Please enter a number from the above menu, or enter 'q' or 'e' to exit.

70

Please enter the username to automatically generate a report: michael

...

Report generated successfully on user: "michael"

You can send this .zip file and password when reporting a user to law enforcement.

Password: RwiFrw9zouhVO7Dy9kW7
Encrypted .zip file location: ./reports/michael_2023-07-23_02-21-56.zip.aes
Encrypted .zip file size: 0.503927 MB
```
