import asyncio
import hispan_shield_guardian
from telegram_client import client, start_listening
from analyzer import analyze_with_gpt
from database import save_message
from report_generator import generate_user_dossier

async def handle_message(event):
    user = await event.get_sender()
    text = event.raw_text
    evaluation = analyze_with_gpt(text)
    save_message(user.id, user.username, text, evaluation)
    print(f"[{evaluation.upper()}] {user.username}: {text[:50]}")

if __name__ == '__main__':
    asyncio.run(start_listening(handle_message))
