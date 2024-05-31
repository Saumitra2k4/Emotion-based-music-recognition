import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import time

client_id = '32d298ff4a25442bae344bbd3bacc1d6'  # Replace 'your_client_id_here' with your actual client ID
client_secret = '7c4f515e31794aeb80857a55b3e49164'  # Replace 'your_client_secret_here' with your actual client secret

auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)


def getTrackIDs(user, playlist_id):
    track_ids = []
    playlist = sp.user_playlist(user, playlist_id)
    for item in playlist['tracks']['items']:
        track = item['track']
        track_ids.append(track['id'])
    return track_ids


def getTrackFeatures(id):
    track_info = sp.track(id)

    name = track_info['name']
    album = track_info['album']['name']
    artist = track_info['album']['artists'][0]['name']
    # URL = track_info['external_urls']['spotify']

    track_data = [name, album, artist]
    return track_data


emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}
music_dist = {0: "5Sv8xB6N7i1Wau7UlGNF4o?si=rBl1nEfOS063Vzgfa4ZLWg&pi=a-NbTDwoMBRDSn", 1: "1muuGjBVcOXMfVfatLX2Z0?si=Nbq6Kg2PT3u8baRlDfBApQ&pi=a-Uf8lKvPNQ5Ka ",
              2: "26XeGg6dQZvMy7lSlNzoyb?si=dXDNREeyRnG9paTC6ArxcQ&pi=a-8zPpOfTTR-ys", 3: "7dVAxjVpv2X4ZdeYl0CCxw?si=0pR0QaM-SIqIrl1ANQ-YRg&pi",
              4: "4PFwZ4h1LMAOwdwXqvSYHd?si=U7kG--UbR5SMf_PE8Rv2pg&pi=a-ZGYP9sPkSSie", 5: "1MI8VpWOjBg7Jcv5CKensh?si=-pkOHwGmT0yXo2LwZhoBcQ&pi=a-43Oa0hnxQ_6l",
              6: "1akSQeOZ6UwGHOkpQ0nslf?si=wpdYkh65R9izRdkj1Jk4aQ"}


def generate_csv(emotion, music_dist_id):
    track_ids = getTrackIDs('spotify', music_dist_id)
    track_list = []
    for i in range(len(track_ids)):
        time.sleep(.3)
        track_data = getTrackFeatures(track_ids[i])
        track_list.append(track_data)
    df = pd.DataFrame(track_list, columns=['Name', 'Album', 'Artist', ])
    df.to_csv(f'songs/{emotion}.csv', index=False)
    print(f"{emotion} CSV Generated")


# Generate CSV files for each playlist
for emotion, music_dist_id in music_dist.items():
    generate_csv(emotion_dict[emotion], music_dist_id)
