
#### User Account Commands ####

1) **Deactivate a user account.**

  - This function disables a specific user's account, making it unusable for the owner.

  https://matrix-org.github.io/synapse/v1.38/admin_api/user_admin_api.html#deactivate-account

2) **Deactivate multiple user accounts.**

  - Allows you to disable several user accounts at once. Requires a room list file with room_ids separated by newlines, see the example [./examples/room_list.txt](./examples/room_list.txt) file.

3) **Create a user account.**

  - Use this to generate a new user account.

  https://matrix-org.github.io/synapse/v1.38/admin_api/user_admin_api.html#create-or-modify-account

4) **Create multiple user accounts.**

  - This facilitates the creation of several user accounts simultaneously. Requires a user list file with user_ids separated by newlines, see the example [./examples/user_list.txt](./examples/user_list.txt) file.

5) **Reset a user's password.**

  - If a user forgets their password, this function helps set a new one.

  https://matrix-org.github.io/synapse/v1.38/admin_api/user_admin_api.html#reset-password

6) **Whois user account.**	

  - Provides detailed information about a specific user's account.

  https://matrix-org.github.io/synapse/v1.38/admin_api/user_admin_api.html#query-current-sessions-for-a-user

7) **Whois multiple user accounts.**

  - Retrieves detailed information for multiple user accounts at once. Requires a user list file with user_ids separated by newlines, see the example [./examples/user_list.txt](./examples/user_list.txt) file.

8) **Query user account.**	

  - Allows you to get specific details or attributes of a user account.

  https://matrix-org.github.io/synapse/v1.38/admin_api/user_admin_api.html#query-user-account

9) **Query multiple user accounts.**

  - Retrieve specific details for several user accounts simultaneously. Requires a user list file with user_ids separated by newlines, see the example [./examples/user_list.txt](./examples/user_list.txt) file.

10) **List room memberships of user.**	

  - Displays the list of rooms that a user is a part of.

  https://matrix-org.github.io/synapse/v1.38/admin_api/user_admin_api.html#list-room-memberships-of-a-user

11) **Promote a user to server admin.**	

  - Elevates a user's privileges, making them an administrator on the server.

  https://matrix-org.github.io/synapse/v1.38/admin_api/user_admin_api.html#change-whether-a-user-is-a-server-administrator-or-not

12) **List all user accounts.**

  - Displays or prints to file a comprehensive list of all user accounts on the server.

  https://matrix-org.github.io/synapse/v1.38/admin_api/user_admin_api.html#list-accounts

13) **Quarantine all media a user uploaded.**

  - This API quarantines all local media that a local user has uploaded. That is to say, if you would like to quarantine media uploaded by a user on a remote homeserver, you should instead use one of the other APIs. Useful for potential harmful or inappropriate content.

  https://matrix-org.github.io/synapse/v1.40/admin_api/media_admin_api.html#quarantining-all-media-of-a-user

14) **Collect account data.**

  - Retrieves all available data associated with a user's account.

15) **List account pushers.**

  - Shows devices and services that have push access to a user's account.

  https://matrix-org.github.io/synapse/v1.38/admin_api/user_admin_api.html#list-all-pushers

16) **Get rate limit of a user account.**

  - Displays the frequency at which a user can make requests or actions.

  https://matrix-org.github.io/synapse/v1.38/admin_api/user_admin_api.html#get-status-of-ratelimit

17) **Set rate limit of a user account.**

  - Adjusts the frequency rate at which a user can make requests or actions.

  https://matrix-org.github.io/synapse/v1.38/admin_api/user_admin_api.html#set-ratelimit

18) **Delete rate limit of a user account.**

  - Removes any rate limits set on a user's account, granting them unrestricted action frequency.

  https://matrix-org.github.io/synapse/v1.38/admin_api/user_admin_api.html#delete-ratelimit

19) **Check if user account exists.**

  - Verifies the existence of a specific user_id, for example "@johndoe:example.org" on the homeserver.

20) **Shadow ban a user.**	

  - Shadow-banning is a useful tool for moderating malicious or egregiously abusive users. A shadow-banned users receives successful responses to their client-server API requests, but the events are not propagated into rooms. This can be an effective tool as it (hopefully) takes longer for the user to realise they are being moderated before pivoting to another account.

  Shadow-banning a user should be used as a tool of last resort and may lead to confusing or broken behaviour for the client. A shadow-banned user will not receive any notification and it is generally more appropriate to ban or kick abusive users. A shadow-banned user will be unable to contact anyone on the server.

  https://matrix-org.github.io/synapse/v1.38/admin_api/user_admin_api.html#shadow-banning-users

21) **Find a user by their 3PID (Third-party ID).**
  
  - Allows you to locate a user based on their third-party identifiers, such as email or phone number.

> **Note:** All these commands utilize the Synapse API. Always exercise caution and ensure you have the necessary permissions when accessing and modifying user accounts.
