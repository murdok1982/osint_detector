from telethon import TelegramClient, events
from config import API_ID, API_HASH, GROUPS

client = TelegramClient('osint_session', API_ID, API_HASH)

async def start_listening(on_new_message):
    await client.start()
    for group in GROUPS:
        await client.get_entity(group)

    @client.on(events.NewMessage(chats=GROUPS))
    async def handler(event):
        await on_new_message(event)

    print("Escuchando grupos...")
    await client.run_until_disconnected()
