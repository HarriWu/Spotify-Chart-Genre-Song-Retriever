#! /usr/bin/env python3
# pip3 install spotipy
# pip3 install requests
# pip3 install BeautifulSoup4

import spotipy
from spotipy import util
from spotipy.oauth2 import SpotifyClientCredentials
import time, random, csv
import requests, bs4
# Spotify API client id and client secret imports
from config import *


def add_songs_to_playlist(username, playlist_id, client_id, client_secret, spotify_songs_ids):
    """ Add all songs with ids in spotify_songs_ids into a Spotify playlist.

    Args:
        username: Spotify username.
        playlist_id: Spotify playlist id.
        client_id: Spotify client id.
        client_secret: Spotify client secret.
        spotify_songs_ids: An array containing all song ids.
    """
    # Get authentication
    token = util.prompt_for_user_token(username,
                                       scope='playlist-modify-private,playlist-modify-public',
                                       client_id=client_id,
                                       client_secret=client_secret,
                                       redirect_uri='http://localhost:8888/callback/')

    # If authentication is given add songs to playlist
    if token:
        song_count = len(spotify_songs_ids)
        bindex = 0
        endindex = bindex + 98
        sp = spotipy.Spotify(auth=token)

        while (True):
            if song_count - 98 <= 0:
                sp.user_playlist_add_tracks(user=username, playlist_id=playlist_id,
                                            tracks=spotify_songs_ids)
                break
            elif endindex >= song_count:
                sp.user_playlist_add_tracks(user=username, playlist_id=playlist_id,
                                            tracks=spotify_songs_ids[bindex:song_count])
                break
            else:
                sp.user_playlist_add_tracks(user=username, playlist_id=playlist_id,
                                            tracks=spotify_songs_ids[bindex:endindex])
                bindex = endindex + 1
                endindex = bindex + 98

            # Random time scrapping
            time.sleep(random.randint(10, 20))

        print('done')
    else:
        print('Unable to get token')


def main():
    """ Take in a URL from spotifycharts.com which is a ranking of songs and using BeautifulSoup to scrape the
        website for data on each track name and artist. Ask user for what artist genres they would like to omit or
        want. Then uses Spotify APIs to retrieve artists genres and use this information to store a
        new list of tracks based on the user's preferences inside a csv file. Lastly, uploads the new list
        of tracks onto a Spotify playlist using Spotify APIs if the user decides to.
    """
    # User Agent of user computer
    headers = {"User-Agent": USER_AGENT}

    url = input('Put URL of chart in spotifycharts.com e.g '
                'https://spotifycharts.com/regional/\n:')

    # Download page
    res = requests.get(url, headers=headers)
    res.raise_for_status()

    # Prepping to parse page
    soup = bs4.BeautifulSoup(res.text, features="html.parser")

    # Credentials needed to access Spotify Web API
    client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    # Spotify object to access API
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    arr = []
    arr_after = []
    arr_feed_into_csv = []
    song_ids = []
    genres_want = set()
    genres_not_want = set()

    # Get rid of unneeded data
    for i in soup.select('th[class="chart-table-track"]'):
        i.decompose()

    # From page get song name and song artist
    for i in soup.select('.chart-table-track'):
        song_name = i.select('strong')[0].getText()
        song_artist = i.select('span')[0].getText()[3:]
        arr.append([song_artist, song_name])

    # print(arr)

    # Retrieve data for genres that you want/don't want
    print('Disclaimer: If artist has no genre retrievable from Spotify database '
          'their songs will not be included in results')
    str_genres_not_want = input("Input genres of artist you DON'T WANT with '/' separating each "
                                "genre (All have to be typed in lowercase) e.g hip hop/rap\n"
                                "if have none just press ENTER:")
    str_genres_want = input("Input genres of artist you WANT with '/' separating each "
                            "genre (All have to be typed in lowercase) e.g pop/viral pop\n"
                            "if have none just press ENTER:")
    arr_genres_not_want = list(str_genres_not_want.split('/'))
    arr_genres_want = list(str_genres_want.split('/'))

    # Input all genres into set
    for i in arr_genres_not_want:
        genres_not_want.add(i)

    for i in arr_genres_want:
        genres_want.add(i)

    print('retrieving...')

    # Iterate through arr containing song names with song artists
    for g in arr:
        # Get artist genres
        results = sp.search(q='artist:' + g[0], type='artist')

        for i in results['artists']['items']:
            if i['genres'] is not None:
                artist_genres = i['genres']
                break

        # Logic to include a song or not based on artist genre
        found_not_want = False
        count = len(genres_want)

        for c in artist_genres:

            if c in genres_not_want:
                found_not_want = True

            # If set genres_want is Empty
            if genres_want == {''}:
                count = 0
            elif c in genres_want:
                count -= 1

        if found_not_want is False and count == 0:
            arr_after.append([g[0], g[1]])

    # Go through each element of arr_after
    for g in arr_after:
        # Get track id and put in song_ids array
        results = sp.search(q='track:' + g[1] + ' ' + 'artist:'
                              + g[0], type='track')

        for i in results['tracks']['items']:
            if i.get('id') is not None:
                song_ids.append(i['id'])
                break

        # Get all track external links
        for i in results['tracks']['items']:
            if i['external_urls']['spotify'] is not None:
                arr_feed_into_csv.append([g[1] + ' by ' + g[0], i['external_urls']['spotify']])
                break

    output_file = open('spotify.csv', 'w', newline='')
    output_writer = csv.writer(output_file)

    for i in arr_feed_into_csv:
        output_writer.writerow(i)

    output_file.close()

    # Give user the option of downloading songs onto playlist
    download_playlist = input("Put y for Yes ... Enter for no"
                              + "\nWould you like to put all songs into one of your playlist on Spotify: ")

    # Downloads songs in song_ids into Spotify playlist
    if download_playlist == 'y':
        username = input("Enter Spotify username: ")
        playlist_id = input("Enter Playlist ID: ")
        add_songs_to_playlist(username, playlist_id, CLIENT_ID, CLIENT_SECRET, song_ids)


main()


