import requests

def register_webhook(TWITCH_TOKENS: str, WEBHOOK_PATH: str = "http://127.0.0.1:5000/webhook"):
    print("Registering webhook...", TWITCH_TOKENS, WEBHOOK_PATH)