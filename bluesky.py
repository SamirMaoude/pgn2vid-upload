#!/usr/bin/env python

# Client.send_video helper introduced in 0.0.54
from atproto import Client
import os
from dotenv import load_dotenv

load_dotenv('.env')

from get_video import get_video_of_the_day




BLUESKY_HANDLE = os.getenv('BLUESKY_HANDLE')
BLUESKY_APP_PASSWORD = os.getenv('BLUESKY_APP_PASSWORD')


def at_login() -> Client:
    """Login with the atproto client
    """
    at_client = Client()
    profile = at_client.login(BLUESKY_HANDLE, BLUESKY_APP_PASSWORD)
    print("Logged in as: ", profile.display_name)
    return at_client


def send_post(at_client: Client, text: str, media: bytes, alt_text: str) -> bool:
    """Send post with the given text content and video bytes
    """
    print(f"Sending post with text:\n{text}")

    try:
        at_client.send_video(
            text=text,
            video=media,
            video_alt=alt_text,
        )
    except Exception as ex:
        print("Failed to send post. Got error: ", str(ex))
        return False
    return True


def main():
    DATA = get_video_of_the_day()
    # Login to BlueSky
    at_client: Client = at_login()

    description = f"{DATA['white']} vs {DATA['black']} - {DATA['event']}({DATA['date']}) - {DATA['result']}"

    attempts = 0
    success = False
    while attempts < 12 and not success:
        attempts += 1
        print(f"Attempt {attempts} posting to BlueSky...")
        success = send_post(
            at_client=at_client,
            text=description,
            media="./video_of_the_day.mp4",
            alt_text=f"{DATA['white']} vs {DATA['black']} - {DATA['event']}({DATA['date']}) - {DATA['result']}",
        )
        print("Posted to BlueSky!")
    if not success:
        print("Error posting to BlueSky")


if __name__ == "__main__":
    main()