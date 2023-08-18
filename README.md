
# Matrix Moderation Tool

A Matrix moderation tool to make managing a Synapse server easier.

Contact me at [@michael:perthchat.org](https://matrix.to/#/@michael:perthchat.org) if you get stuck or have an edit in mind.


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
- https://matrix-org.github.io/synapse/latest/admin_api/user_admin_api.html#find-a-user-based-on-their-third-party-id-threepid-or-3pid
- https://github.com/matrix-org/synapse/blob/master/docs/admin_api/delete_group.md
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
