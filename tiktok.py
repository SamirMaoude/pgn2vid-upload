from dotenv import load_dotenv
import os
import requests
from get_video import get_video_of_the_day

load_dotenv('.env')

TIKTOK_REFRESH_TOKEN = os.getenv('TIKTOK_REFRESH_TOKEN')
TIKTOK_CLIENT_KEY = os.getenv('TIKTOK_CLIENT_KEY')
TIKTOK_CLIENT_SECRET = os.getenv('TIKTOK_CLIENT_SECRET')
TIKTOK_BEARER_TOKEN = ""

url = 'https://open.tiktokapis.com/v2/oauth/token/'

# En-têtes
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cache-Control': 'no-cache'
}

data = {
    'client_key': TIKTOK_CLIENT_KEY,
    'client_secret': TIKTOK_CLIENT_SECRET,
    'grant_type': 'refresh_token',
    'refresh_token': TIKTOK_REFRESH_TOKEN
}

# Envoyer la requête POST
response = requests.post(url, headers=headers, data=data)

# Afficher la réponse
if response.status_code == 200:
    data = response.json()
    TIKTOK_BEARER_TOKEN = data['access_token']
    print("Réponse réussie :", TIKTOK_BEARER_TOKEN)
else:
    print("Échec de la requête :", response.status_code, response.text)


data = get_video_of_the_day()

import requests

url = 'https://open.tiktokapis.com/v2/post/publish/video/init/'
headers = {
    'Authorization': f'Bearer {TIKTOK_BEARER_TOKEN}',
    'Content-Type': 'application/json; charset=UTF-8',
}
tiktok_data = {
    "post_info": {
        "title": f"{data['white']} vs {data['black']} - {data['event']}({data['date']}) - {data['result']}",
        "privacy_level": "SELF_ONLY",
        "disable_duet": False,
        "disable_comment": False,
        "disable_stitch": False,
        "video_cover_timestamp_ms": 1000
    },
    "source_info": {
        "source": "PULL_FROM_URL",
        "video_url": data['video_url'],
    }
}

response = requests.post(url, headers=headers, json=tiktok_data)

# Vérifier la réponse
if response.ok:
    print("Succès:", response.json())
else:
    print("Erreur:", response.status_code, response.text)




