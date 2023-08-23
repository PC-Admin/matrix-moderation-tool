
# Server Commands Guide

This guide provides detailed steps for server-side operations that use the database and SSH. The commands and scripts are essential for handling specific server operations related to Matrix's Synapse server.

## Table of Contents

- [1. Delete and Block Specific Media](#1-delete-and-block-specific-media)
- [2. Purge Remote Media Repository](#2-purge-remote-media-repository)
- [3. Prepare Database for Copying Events of Multiple Rooms](#3-prepare-database-for-copying-events-of-multiple-rooms)

---

100) **Delete and Block Specific Media.**	

> This command allows an admin to delete a specific media on their Matrix Synapse server and block it to prevent future accesses.

#### Process Flow:

1. Take `media_id` and remote server URL from the user.
2. Use SSH to query the Synapse PostgreSQL database for the associated `filesystem_id`.
3. Locate the target media files and thumbnails on the server's file system.
4. Zero out (empty) each file and make them immutable, meaning they cannot be modified or deleted.

#### Example:

For a media with ID `eDmjusOjnHyFPOYGxlrOsULJ`, the process would involve:

```bash
$ ssh matrix.perthchat.org "... SQL query to get filesystem_id..."
$ ssh matrix.perthchat.org "... command to locate files ..."
$ ssh matrix.perthchat.org "true > ...path to file..."
$ ssh matrix.perthchat.org "chattr +i ...path to file..."
```

101) **Purge Remote Media Repository**

This command purges the remote media repository for a certain range of days.
Process Flow:

    Ask the user for the range of days to purge.
    Calculate the epoch timestamp for each day in the range.
    Send a request to the Synapse server to purge media for that day.
    Repeat for each day in the range.

Example:
```bash
$ python3 moderation_tool.py

101

Enter the number of days to purge from: 30 

Enter the number of days to purge too: -2
{"deleted":0}
{"deleted":0}
{"deleted":3}
{"deleted":360}
{"deleted":469}
...
{"deleted":1020}
{"deleted":2440}
{"deleted":0}
{"deleted":0}
Done! :)
```

102) **Prepare Database for Copying Events of Multiple Rooms**

This command prepares the PostgreSQL database to export events from multiple Matrix rooms.
Process Flow:

    Prompt for a list of room IDs.
    Create a RAM disk on the server to store the export.
    For each room ID:
        Create a SQL query to extract room events.
        Write the query to a file on the RAM disk.
    Provide instructions for running the queries in the PostgreSQL container.

Notes:

    This function is compatible with Spantaleev's Matrix deploy script.
    Ensure proper permissions and consider the impact on the server when copying a large amount of data.

Example:
```bash
# As the root user on the target server:
$ mkdir /matrix/postgres/data/ramdisk
$ ... commands to set up RAM disk ...
$ ... commands to generate SQL queries for each room ...
$ docker exec -it matrix-postgres /bin/bash
bash-5.0$ ... commands to execute SQL queries ...
```

After copying the data, ensure to clean up the RAM disk:

```bash
$ rm -r /matrix/postgres/data/ramdisk/*
$ umount /matrix/postgres/data/ramdisk
```

103) **Show last 10 reported events.**

> Gets the last 10 reported events using the event reports API and returns it.

  https://matrix-org.github.io/synapse/latest/admin_api/event_reports.html#show-reported-events

104) **Paginate all reported events.**

> Combines all the events into a large JSON and returns it.

105) **Show details of a specific event report**

> This API returns information about a specific event report.

  https://matrix-org.github.io/synapse/latest/admin_api/event_reports.html#show-details-of-a-specific-event-report
