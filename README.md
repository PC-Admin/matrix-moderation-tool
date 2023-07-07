
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
('q' or 'e') Exit.

30
Cloning rdlist repo...
Cloning into 'rdlist'...
Username for 'https://code.glowers.club': PC-Admin
Password for 'https://PC-Admin@code.glowers.club': 
remote: Enumerating objects: 563, done.
remote: Counting objects: 100% (563/563), done.
remote: Compressing objects: 100% (556/556), done.
remote: Total 563 (delta 355), reused 0 (delta 0), pack-reused 0
Receiving objects: 100% (563/563), 5.47 MiB | 800.00 KiB/s, done.
Resolving deltas: 100% (355/355), done.


Printing details about the current tags in rdlist:

# Tags

### Greedy Tags

*Rooms with these tags may not exist to host such content, however do not remove it.*

Tag|Description
-|-
[`csam`][csam]          | Child Sexual Abuse Material
[`cfm`][cfm]            | An abundance of content which would directly appeal to those seeking csam.
[`jailbait`][jailbait]  | Photos which contain underage individuals in questionable or suggestive situations.
[`tfm`][tfm]            | An abundance of content which would directly appeal to those seeking jailbait.
`beastiality`           | Self explanatory.
`3d_loli`               | Pornography which depicts photorealistic underage characters.
`stylized_3d_loli`      | Pornography which depicts underage characters that are not depicted in a realistic style.
`gore`                  | Self explanatory.
`snuff`                 | Self explanatory.

### Topic Tags

*Tags here describe the room or the room's characteristics.*

Tag|Description
-|-
`degen_misc`            | Other types of coomers rooms.
`degen_larp`            | Coomer larp rooms.
`degen_meet`            | Coomer socializing rooms.
`degen_porn`            | Rooms dedicated to pornography, excluding types which have dedicated tags.
`bot_porn`              | Rooms which contain bots that spam pornographic content.
`bot_spam`              | Rooms which contain bots that spam content. Primarily for malvertising and cryptospam
`preban`                | Rooms which may not contain tagged content, however have clear intent. i.e: Rooms with names like "CP Room", "Child Porn", etc
`hub_room_trade`        | Rooms which exist solely to trade illegal or questionable content. i.e: csam, jailbait
`hub_room_sussy`        | A room which is sussy. This tag does not have a solid definition, see existing tagged rooms
`abandoned`             | Similar to `anarchy`, primarily for rooms which have automated spam bots.
`anarchy`               | Unmoderated rooms.
`hub_room_underage`     | Rooms which contain a disproportionate amount of underage users.
`hub_room_links`        | Rooms which exist to share links to other rooms.
`toddlercon`            | Lolicon but younger.
`loli`                  | Rooms which exist to host lolicon.

[csam]:             https://en.wikipedia.org/wiki/Child_pornography 'Child Sexual Abuse Material. COPAINE >=2'
[cfm]:              https://en.wikipedia.org/wiki/Child_erotica     'Child Fetish Material'
[jailbait]:         https://en.wikipedia.org/wiki/Jailbait_images   'Jailbait'
[tfm]:              about:blank                                     'Teen Fetish Material'
[wp:copaine-scale]: https://en.wikipedia.org/wiki/COPINE_scale      'COPINE scale - Wikipedia'

Please enter a space seperated list of tags you wish to block:

hub_room_links preban degen_misc beastiality degen_porn gore hub_room_trade snuff degen_larp hub_room_sussy bot_spam cfm 3d_loli jailbait bot_porn toddlercon loli csam tfm anarchy abandoned degen_meet stylized_3d_loli

Tag: csam
Room IDs: [***REDACTED***]

Tag: 3d_loli
Room IDs: [***REDACTED***]

Tag: jailbait
Room IDs: [***REDACTED***]

Tag: toddlercon
Room IDs: [***REDACTED***]

Tag: loli
Room IDs: [***REDACTED***]
...


Do you want to block/purge all these rooms? y/n? y

Please enter the local username that will create a 'muted violation room' for your users (Example: michael): mod_team

Please enter the room name of the muted violation room your users will be sent to: POLICY VIOLATION

Please enter the shutdown message that will be displayed to users: THIS ROOM HAS BEEN SHUTDOWN AS IT VIOLATES PERTHCHAT.ORG POLICIES!

Do you want to purge these rooms? (This deletes all the room history from your database.) y/n? y

Do you want to block these rooms? (This prevents your server users re-entering the room.) y/n? y

Number of rooms being shutdown: 320

Are you sure you want to shutdown these rooms? y/n? y

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
