import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import csv


response=requests.get(url="https://www.billboard.com/charts/hot-100/")
data=response.text

soup=BeautifulSoup(data,"html.parser")

songs=soup.select("ul li h3")
song_title=[song.getText().strip() for song in songs[0:20]]

artists=soup.find_all("span", class_="a-truncate-ellipsis-2line")
song_artists=[artist.getText().strip() for artist in artists[0:20]]


spotify=spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="9d5aea6402534b879f34509aebd39b47",client_secret="4d566e9bb32b4246a128ff70607a34b0",redirect_uri="http://example.com",
                                          scope="playlist-modify-private",cache_path="tokens.txt",username="beejay"))

song_IDs=[]
for i in range(20):
    try:
        result=spotify.search(q=f"track:{song_title[i]} artist:{song_artists[i]}",type="track",limit=1)
        song_IDs.append(result["tracks"]["items"][0]["id"])
    except IndexError:
        print("Song not found on Spotify. Track was skipped.")

user_id=spotify.current_user()["id"]
#playlist=spotify.user_playlist_create(user=user_id,name="Billboard Hot 20",public=False,description="Your weekly top 20 songs from the Billboard charts")
playlist_id="6sWnC4NkEIk6ErXanub7dg"
#spotify.playlist_add_items(playlist["id"],items=song_URIs,position=None)

spotify.playlist_replace_items(playlist_id,items=song_IDs)

field_names=["Position","Song","Artist"]
rows=[[i+1,song_title[i],song_artists[i]] for i in range(20)]

with open("Billboard Top 20.csv",'w') as file:
    writer=csv.writer(file)
    writer.writerow(field_names)
    writer.writerows(rows)