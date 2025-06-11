import asyncio
import json
import time
import spotipy
from time import sleep
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.remote.command import Command
from webdriver_manager.chrome import ChromeDriverManager
from yandex_music import Client, Track, Account
from functools import partial

def is_active(driver):
    try:
        driver.execute(Command.GET_ALL_COOKIES)
        return True
    except Exception:
        return False

# gets Yandex Music user token after login
def get_token_ym():
    # make chrome log requests
    capabilities = DesiredCapabilities.CHROME
    capabilities["loggingPrefs"] = {"performance": "ALL"}
    capabilities['goog:loggingPrefs'] = {'performance': 'ALL'}
    driver = webdriver.Chrome(desired_capabilities=capabilities,
                              executable_path=ChromeDriverManager().install())
    driver.get(
        "https://oauth.yandex.ru/authorize?response_type=token&client_id=23cabbbdc6cd418abb4b39c32c41195d")

    token = None

    while token == None and is_active(driver):
        sleep(1)
        try:
            logs_raw = driver.get_log("performance")
        except:
            pass

        for lr in logs_raw:
            log = json.loads(lr["message"])["message"]
            url_fragment = log.get('params', {}).get('frame', {}).get('urlFragment')

            if url_fragment:
                token = url_fragment.split('&')[0].split('=')[1]

    try:
        driver.close()
    except:
        pass
    print(token)
    return token

# gets Spotify user token after login
def get_token_spotify(client_id, redirect_url, scopes):
    # create an obj to authorize in Spotify
    spotify_access = spotipy.SpotifyPKCE(client_id=client_id,
                                         redirect_uri=redirect_url,
                                         scope=scopes)
    
    capabilities = DesiredCapabilities.CHROME
    capabilities['goog:loggingPrefs'] = {"performance": "ALL", "browser": "ALL"}
    driver = webdriver.Chrome(desired_capabilities=capabilities,
                              executable_path=ChromeDriverManager().install())
    driver.get(spotify_access.get_authorize_url().replace('/authorize', '/ru/authorize'))
    
    auth_code = None
    while auth_code == None and is_active(driver):
        sleep(1)
        try:
            logs_raw = driver.get_log("performance")
        except:
            continue
        auth_code = None
        for log in logs_raw:
            log = json.loads(log["message"])["message"]
            if log["method"] == "Network.requestWillBeSent" and "documentURL" in log["params"]:
                url = log["params"]["documentURL"]
                if not url.startswith(redirect_url):
                    continue
                auth_code = url[url.find("code=")+len("code="):]
                break
    try:
        driver.close()
    except:
        pass
    return spotify_access.get_access_token(auth_code, check_cache=False)    

async def transfer(spotify_token, ym_token): 
    # create sotify user obj
    user_spotify = spotipy.Spotify(spotify_token)
    # create ym user obj
    user_ym = Client(ym_token).init()

    ym_username = user_ym.me.account.login
    print(f"YM account name: {ym_username}")
    
    spotify_username = user_spotify.current_user()['display_name']
    print(f"Spotify account name: {spotify_username}")
    
    # transfer favorite tracks
    if input("Transfer favorite tracks? (Y/n)") == 'Y':    
        favorite_tracks = user_spotify.current_user_saved_tracks(limit=50)['items']

        fav_option = int(input("Create a playlist or add tracks to favorite?(1/2)"))

        if fav_option == 1:
            playlist_name = 'Любимые треки из Spotify'
            new_playlist_ym = user_ym.users_playlists_create(playlist_name)
            print(f"Playlist '{playlist_name}' is created")
            playlist_kind = new_playlist_ym.kind
            position = 0
            
        for track in favorite_tracks:
        # get the track's artist's name
            track_artist = track['track']['artists'][0]['name']
            # get the track's name
            track_name = track['track']['name']           
                    
            # create a query to search the track
            query = track_artist + ' ' + track_name
            # get the search result (filter: track)
            search_result = user_ym.search(query)
            await asyncio.sleep(0.5)

            #if the track is found
            if search_result.best and type(search_result.best.result) == Track and search_result.best.result.artists[0].name == track_artist:
                # get the track id
                track_id = search_result.best.result.id
                if fav_option == 1:
                    # get the track album ID
                    album_id = search_result.best.result.albums[0].id
                    
                    # get the playlist revision
                    revision = new_playlist_ym.revision
                    # insert the track to the playlist
                    new_playlist_ym = user_ym.users_playlists_insert_track(kind = playlist_kind,
                                                                           track_id = track_id,
                                                                           album_id = album_id,
                                                                           at = position,
                                                                           revision = revision)                   
                    position += 1
                    print(f"\t{track_artist} - {track_name} is inserted to {playlist_name}")
                else:
                    # add the track to favs
                    user_ym.users_likes_tracks_add(track_id)
                    print(f"\t{track_artist} - {track_name} is added to favorite tracks")
                        
                await asyncio.sleep(1.5)
            else: 
                print(f"\t{track_artist} - {track_name} is not found and skipped")
                continue

    # get a list of the user's playlists
    playlists = user_spotify.current_user_playlists()['items']
    
    # through the list of playlists
    for playlist in playlists:
        # get the playlist name
        playlist_name = playlist['name']     

        if input(f"Transfer '{playlist_name}'? (Y/n) ") == 'n':
            continue
        
        # create a playlist with the same name in ym
        new_playlist_ym = user_ym.users_playlists_create(playlist_name)
        print(f"Playlist '{playlist_name}' is created")
        # get the playlist kind
        playlist_kind = new_playlist_ym.kind
        
       
        # get a list of the tracks in the playlist
        tracks = user_spotify.playlist_items(playlist['id'])['items']
        
        # track position in the playlist
        position = 0    
        
        # through the list of tracks
        for track in tracks:                    
            # get the track's artist's name
            track_artist = track['track']['artists'][0]['name']
            # get the track's name
            track_name = track['track']['name']
            
            # create a query to search the track
            query = track_artist + ' ' + track_name
            # get the search result (filter: track)
            search_result = user_ym.search(query)
            await asyncio.sleep(0.5)
            
            # if the track is found
            if search_result.best and type(search_result.best.result) == Track and search_result.best.result.artists[0].name == track_artist:
                # get the track id
                track_id = search_result.best.result.id
                # get the track album ID
                album_id = search_result.best.result.albums[0].id
                
                # get the playlist revision
                revision = new_playlist_ym.revision
                
                # insert the track to the playlist
                new_playlist_ym = user_ym.users_playlists_insert_track(kind = playlist_kind,
                                                                       track_id = track_id,
                                                                       album_id = album_id, at = position,
                                                                       revision = revision)
                print(f"\t{track_artist} - {track_name} is inserted to '{playlist_name}'")
                
                # update the track position in the playlist
                position += 1
                await asyncio.sleep(1.5)
            else: 
                print(f"\t{track_artist} - {track_name} is not found and skipped")
                continue

async def transfer_playlists(spotify_tokens, ym_tokens):
    # tasks array
    tasks = []
    for spotify_token, ym_token in zip(spotify_tokens, ym_tokens):
        # creating task
        task = asyncio.create_task(transfer(spotify_token, ym_token))
        # adding task to the array
        tasks.append(task)
    
    # gathering
    await asyncio.gather(*tasks)
