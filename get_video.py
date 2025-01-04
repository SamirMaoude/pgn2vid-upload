from dotenv import load_dotenv
import os
import requests

load_dotenv('.env')

API_URL = os.getenv('API_URL')


def get_video_of_the_day():

    headersList = {
    "Accept": "*/*",
    }

    payload = ""

    response = requests.request("GET", API_URL, data=payload,  headers=headersList)

    if response.status_code == 200:
        data = response.json()
        video_url = data['video_url']

        output_file = 'video_of_the_day.mp4'

        try:
            # Envoyer une requête GET pour télécharger la vidéo
            response = requests.get(video_url, stream=True)
            response.raise_for_status()  # Vérifier les erreurs HTTP

            # Sauvegarder la vidéo en chunks (par morceaux)
            with open(output_file, 'wb') as video_file:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        video_file.write(chunk)
            
            print(f"✅ Vidéo téléchargée avec succès sous '{output_file}'")

            return data
        except requests.exceptions.RequestException as e:
            print(f"❌ Erreur lors du téléchargement : {e}")