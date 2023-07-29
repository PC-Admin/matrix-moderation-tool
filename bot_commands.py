
from nio import AsyncClient, RoomCreateResponse, LoginResponse
import asyncio
import hardcoded_variables

async def create_session(username: str, password: str, homeserver: str) -> AsyncClient:
	client = AsyncClient(homeserver, username)
	response = await client.login(password)

	if isinstance(response, LoginResponse):
		await client.sync()  # Perform a sync after login
		return client

	raise Exception(f"Failed to log in: {response}")

async def create_room(client: AsyncClient, name: str) -> str:
	response = await client.room_create(name=name)

	if isinstance(response, RoomCreateResponse):
		return response.room_id

	raise Exception(f"Failed to create room: {response}")

async def invite_user(client: AsyncClient, room_id: str, user_id: str):
	response = await client.room_invite(room_id, user_id)

	if not response:
		raise Exception(f"Failed to invite user: {response}")

async def send_message(receiver: str, message: str):
	homeserver = "https://" + hardcoded_variables.homeserver_url
	client = await create_session(hardcoded_variables.rdlist_bot_username, hardcoded_variables.rdlist_bot_password, homeserver)
	try:
		# Check if room with the receiver already exists
		for room in client.rooms.values():
			if receiver in room.users and len(room.users) == 2:
				room_id = room.room_id
				break
		else:
			# Create new room if it doesn't exist
			room_id = await create_room(client, "Incident Report")
			await invite_user(client, room_id, receiver)

		content = {
			"msgtype": "m.text",
			"body": message,
		}
		response = await client.room_send(room_id, message_type="m.room.message", content=content)
		if not response:
			raise Exception(f"Failed to send message: {response}")

	finally:
		await client.close()

def test_matrix_message():
	async def main():
		receiver = hardcoded_variables.report_return_mxid
		message = "Hello! This is a test message. Please ignore it."
		await send_message(receiver, message)
		print("\nMessage successfully sent.")

	asyncio.get_event_loop().run_until_complete(main())
