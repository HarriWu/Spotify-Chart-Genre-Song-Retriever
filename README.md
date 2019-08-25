# Spotify Chart Genre Song Selector

Python scrapper to take in a URL from spotifycharts.com that has a ranking of songs and using BeautifulSoup to scrape the website for data on each track name and artist. Asks user for what artist genres they would like to omit or want. Then utilizes Spotify APIs to retrieve artists genres and use this information to store a new list of tracks based on the user's preferences into a csv file. Lastly, uploads the new list of tracks onto a Spotify playlist using Spotify APIs if the user decides to.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system. 

### Installation

Install all the third-party modules required in the directory where spotify_top_200.py are located.

Install spotipy
```
$ sudo pip3 install spotipy
```
Install requests
```
$ sudo pip3 install requests
```
Install BeautifulSoup
```
$ sudo pip3 install BeautifulSoup4
```

### Setup

Create a file called config.py in directory of spotify_top_200.py and in that file copy and paste
```
CLIENT_ID = ''
CLIENT_SECRET = ''
USER_AGENT = 'Your User Agent search online for my user agent'
```
Login to Spotify for Developers and go to your dashboard and select “create client id” and follow the instructions. Spotify are not too strict on providing permissions so put anything you like when they ask for commercial application. 
Copy/Paste client id and client secret in their respective fields, inside the quotation marks.
```
CLIENT_ID = 'aflsdkjflk'
CLIENT_SECRET = 'lskadjflk'
USER_AGENT = 'Your User Agent search online for my user agent'
```
If you want to download the songs onto your playlist go to the commercial application you have created and click on edit settings. 

Under redirect URIs add
```
http://localhost:8888/callback/
```

## Deployment

Navigate to the directory where spotify_top_200.py are located in Terminal and change the .py file’s permissions to make it executable

```
$ chmod +x spotify_top_200.py
```

To run

```
$ python3 spotify_top_200.py
```

## Dependencies

* Spotipy - lightweight Python library for the Spotify Web API
* BeautifulSoup - Scrapping library
* Requests - Python HTTP client interface library






