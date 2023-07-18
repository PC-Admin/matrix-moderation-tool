
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
    A) https://github.com/matrix-org/synapse/blob/master/docs/admin_api/delete_group.md
    B) https://matrix-org.github.io/synapse/latest/admin_api/user_admin_api.html#account-data
    C) https://matrix-org.github.io/synapse/latest/admin_api/user_admin_api.html#list-all-pushers
    D) https://matrix-org.github.io/synapse/latest/admin_api/user_admin_api.html#override-ratelimiting-for-users
    E) https://matrix-org.github.io/synapse/latest/admin_api/user_admin_api.html#check-username-availability
    F) https://matrix-org.github.io/synapse/latest/admin_api/user_admin_api.html#find-a-user-based-on-their-id-in-an-auth-provider
    G) https://matrix-org.github.io/synapse/latest/admin_api/user_admin_api.html#find-a-user-based-on-their-third-party-id-threepid-or-3pid
2) Make the menu prettier! - DONE
3) Modularise the functions into multiple files - DONE
4) Use URI module for all API calls instead of curl - DONE
5) Add more automated rdlist function with sane defaults - DONE
6) Add fully automated (should just return a web link and decryption password) reporting functions for users:
- User's ID
- Whois Data
- Account Data
- Query Data
- Pushers List
- List of the rooms the user is participating in, divided into 1:1 conversations and larger rooms
- The content of the messages they've sent (if they were sent to rooms your server is participating in)
- Copies of any media they've sent
7) Add a room report function to create a properly formatted report for rdlist
8) Add a function to extract a users email or 3PID
9) Do room shutdowns in parallel


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
#### rdlist ####
30) Block all rooms with specific rdlist tags.
34) Block all rooms with recommended rdlist tags.
('q' or 'e') Exit.

34

Successfully set user as server admin.
rdlist repo already cloned...
Fetching origin
rdlist repo is up-to-date, no need to pull changes.

Using recommended rdlist tags.


Number of rooms being shutdown: 318

Are you sure you want to shutdown these rooms? y/n? y

https://matrix.perthchat.org/_synapse/admin/v1/rooms/!***REDACTED***:matrix.org/state

{"errcode":"M_NOT_FOUND","error":"Room not found"}
The room was not found.

https://matrix.perthchat.org/_synapse/admin/v1/rooms/!***REDACTED***:cuteworld.space/state

{"errcode":"M_NOT_FOUND","error":"Room not found"}
The room was not found.

https://matrix.perthchat.org/_synapse/admin/v1/rooms/!***REDACTED***:matrix.org/state

{"errcode":"M_NOT_FOUND","error":"Room not found"}
The room was not found.

https://matrix.perthchat.org/_synapse/admin/v1/rooms/!***REDACTED***:matrix.org/state

{"errcode":"M_NOT_FOUND","error":"Room not found"}
The room was not found.
...
```

Note that this script before shutting these rooms down will save the state events to the "./state_events" folder, please keep this data as it's important for law enforcement.
