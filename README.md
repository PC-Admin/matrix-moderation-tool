
# Matrix Moderation Tool


This is a script i wrote to make moderating a Synapse server easier.

Contact me at: @PC-Admin:perthchat.org if you get stuck or have an edit in mind.

***
## Licensing

This work is published under the MIT license, for more information on this license see here: https://opensource.org/license/mit/

***
## Setup script

You can hard code the server URL, federation port and access token for faster use, it will prompt you for these values if you don't.

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

***
## rdlist Functionality

'rdlist' is a comprehensive list of child abuse related rooms on Matrix, it's a safety initiative led by the [Legion of Janitors](https://matrix.to/#/#janitors:glowers.club).

This script can automatically load and block/purge abusive rooms from rdlist, making it **very easy** for inexperienced administrators to block this harmful content.

To get started, just dm me at [@michael:perthchat.org](https://matrix.to/#/@michael:perthchat.org) and I can invite you to the 'Legion of Janitors' room.

Once you have read access to the [rdlist repository](https://code.glowers.club/loj/rdlist), simply run this moderation script like so:
```
$ python3 modtool.py 

Please select one of the following options:
...
#### rdlist ####
30) Block all rooms with specific rdlist tags.
34) Block all rooms with recommended rdlist tags.
('q' or 'e') Exit.

34

rdlist repo already cloned...
Fetching origin
rdlist repo is up-to-date, no need to pull changes.

Using recommended rdlist tags.

Number of rooms being shutdown: 305

Are you sure you want to shutdown these rooms? y/n?

curl -kXGET 'https://matrix.perthchat.org/_synapse/admin/v1/rooms/!***REDACTED***:matrix.org/state?access_token=***REDACTED***' > ./!***REDACTED***:matrix.org_state_1688238203.json

  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100    50    0    50    0     0    891      0 --:--:-- --:--:-- --:--:--   892

Exported room state events to file, this data can be useful for profiling a room after you've blocked/purged it: ./state_events!***REDACTED***:matrix.org_state_1688238203.json
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   226    0    32  100   194    341   2069 --:--:-- --:--:-- --:--:--  2430
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   318    0   318    0     0   7095      0 --:--:-- --:--:-- --:--:--  7227
status: complete
!***REDACTED***:matrix.org has been successfully shutdown!
```

Note that this script before shutting these rooms down will save the state events to the "./state_events" folder, this data is important for law enforcement. Please collect these files and send them back to the [Legion of Janitors](https://matrix.to/#/#janitors:glowers.club) for collection and analysis.
