from bs4 import BeautifulSoup
import requests


Client_ID ="ce2ce61d18894e9086c747392e23f811"
Client_Secret = "a7980051cc264e67885dc346d2736725"
scope="playlist-modify-private"
rurl="http://example.com"

date= input("please enter to which you wish to travleback ( YYYY-MM-DD ): ")

import spotipy
from spotipy.oauth2 import SpotifyOAuth



spotify=spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=Client_ID,
        client_secret=Client_Secret,
        scope=scope,
        redirect_uri=rurl,
        cache_path="token.txt",
        show_dialog=True)
)

id=spotify.current_user()["id"]
print(id)



response = requests.get("https://www.billboard.com/charts/hot-100/" + date)
soup = BeautifulSoup(response.text, 'html.parser')


# List of songs
song_list_raw = soup.select(selector="div ul li ul li h3")
song_list = []
for s in range(99):
    song_list_raw[s]=song_list_raw[s].getText().replace('\t', '')
    song_list.append(song_list_raw[s].replace('\n', ''))
print(song_list)
song_list=song_list[:5]
#------------remove about linke--------------#
playlist_details=spotify.user_playlist_create(name=f"Top 100 songs of {date.split('-')[0]}", user=id ,public=False)
playlist_id=playlist_details["id"]

for song in song_list:
    rs=spotify.search(q=f"track:{song} year:{date.split('-')[0]}" , limit=2, offset=0, type='track', market=None)

    try:
        url=rs["tracks"]["items"][0]["external_urls"]["spotify"]
        uri=rs["tracks"]["items"][0]["uri"]
        spotify.playlist_add_items(playlist_id=playlist_id, items=[url])
        print(url)
    except IndexError:
        print(song, "could not be found ... skipped")
    #print(rs["tracks"]["items"][0])






