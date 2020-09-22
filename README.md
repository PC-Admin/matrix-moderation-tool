
# PC-Admin's Synapse Moderation Tool


This is a script i wrote to make moderating a Synapse server easier.

Contact me at: @PC-Admin:perthchat.org if you get stuck or have an edit in mind.

***
## Licensing

This work is licensed under GNU Affero General Public License v3, for more information on this license see here: https://www.gnu.org/licenses/agpl-3.0.txt

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

