from django.shortcuts import render, redirect
from django.http import QueryDict
from django.contrib import messages
from dotenv import load_dotenv
import random
import spotipy
import requests
import os
import json
import time

from spotipy import SpotifyException

load_dotenv()


def index(request):
    if request.session.__contains__('access_token'):
        return redirect(dashboard)
    else:
        return render(request, 'index.html')


def dashboard(request):
    try:
        sp = spotipy.Spotify(auth=request.session['access_token'])
        playlists = get_playlists(sp)
        return render(request, 'index.html', {'all_playlists': playlists})
    except SpotifyException as e:
        if e.http_status == 401:
            return redirect(authorize)
    except KeyError as e:
        return redirect(authorize)


def authorize(request):
    # if user has a cookie with a token, refresh it
    if request.session.__contains__('access_token') & request.session.__contains__('refresh_token'):
        params = {
            'grant_type': 'refresh_token',
            'refresh_token': request.session.__getitem__('refresh_token'),
            'client_id': os.environ.get('CLIENT_ID'),
            'client_secret': os.environ.get('CLIENT_SECRET')
        }
        response = requests.post('https://accounts.spotify.com/api/token', data=params)
        if response.status_code == 200:
            response_json = json.loads(response.text)
            request.session['access_token'] = response_json['access_token']
        return redirect(index)
    else:
        params = {
            'client_id': os.environ.get('CLIENT_ID'),
            'response_type': 'code',
            'redirect_uri': 'http://127.0.0.1:8000/login',
            'scope': 'playlist-read-private playlist-modify-private user-library-modify user-library-read'
        }

        q = QueryDict('', mutable=True)
        q.update(params)
        url = 'https://accounts.spotify.com/authorize' + '?' + q.urlencode()
        return redirect(url)


def login(request):
    # Return to homepage if user declines authorization
    if request.GET.__contains__('error'):
        return render(request, 'index.html', {'error_message': 'Error connecting Spotify account, please try again.'})
    else:
        params = {
            'grant_type': 'authorization_code',
            'code': request.GET.__getitem__('code'),
            'redirect_uri': 'http://127.0.0.1:8000/login',
            'client_id': os.environ.get('CLIENT_ID'),
            'client_secret': os.environ.get('CLIENT_SECRET')
        }

        response = requests.post('https://accounts.spotify.com/api/token', data=params)
        if response.status_code == 200:
            # parse response text into addressable JSON
            response_json = json.loads(response.text)

            # write tokens to cookie storage
            request.session['access_token'] = response_json['access_token']
            request.session['refresh_token'] = response_json['refresh_token']

            # get username and user_id from API and write to cookie storage
            header = {'Authorization': 'Authorization: Bearer ' + request.session['access_token']}
            user_response = requests.get('https://api.spotify.com/v1/me', headers=header)
            user_response_json = json.loads(user_response.text)
            request.session['username'] = user_response_json['display_name']
            request.session['user_id'] = user_response_json['id']
            return redirect(index)
        else:
            # error handling
            messages.error(request, 'Error connecting Spotify account, please try again.')
            return render(request, 'index.html')


def logout(request):
    # deletes the storage cookie
    request.session.flush()
    messages.success(request, 'Logged out successfully.')
    return render(request, 'index.html')


def add_saved_tracks(saved_tracks, all_tracks):
    for item in saved_tracks['items']:
        track = item['track']
        all_tracks.append(track)


def add_track_ids(tracks, track_ids):
    for item in tracks['items']:
        track = item['track']
        track_ids.append(track['id'])


def get_playlist_track_ids(sp, playlist_id):
    track_ids = []
    tracks = sp.playlist_tracks(playlist_id)
    add_track_ids(tracks, track_ids)
    while tracks['next']:
        tracks = sp.next(tracks)
        add_track_ids(tracks, track_ids)
    return track_ids


def get_saved_songs(sp):
    # Get list of saved songs
    all_tracks = []
    saved_tracks = sp.current_user_saved_tracks()
    add_saved_tracks(saved_tracks, all_tracks)
    while saved_tracks['next']:
        saved_tracks = sp.next(saved_tracks)
        add_saved_tracks(saved_tracks, all_tracks)
    return all_tracks


def get_playlists(sp):
    all_playlists = []
    playlist_batch = sp.current_user_playlists(limit=50)
    add_playlists(playlist_batch, all_playlists)
    while playlist_batch['next']:
        playlist_batch = sp.next(playlist_batch)
        add_playlists(playlist_batch, all_playlists)
    return all_playlists


def add_playlists(playlists, all_playlists):
    for item in playlists['items']:
        all_playlists.append(item)


def playlist_shuffle(request):
    start = time.process_time()
    try:
        sp = spotipy.Spotify(auth=request.session['access_token'])
    except SpotifyException as e:
        if e.http_status == 401:
            return redirect(authorize)

    playlist_id = request.POST.get('playlistSelection')
    username = request.session['username']

    # ID and tracks of selected playlist
    playlist_tracks = get_playlist_track_ids(sp, playlist_id)
    playlist_tracks_copy = playlist_tracks

    # Clear songs from playlist
    while playlist_tracks:
        sp.user_playlist_remove_all_occurrences_of_tracks(username, playlist_id, playlist_tracks[:100])
        playlist_tracks = playlist_tracks[100:]

    # Shuffle list of songs
    random.shuffle(playlist_tracks_copy)

    while playlist_tracks_copy:
        sp.user_playlist_add_tracks(username, playlist_id, playlist_tracks_copy[:100])
        playlist_tracks_copy = playlist_tracks_copy[100:]

    print(time.process_time() - start)
    messages.success(request, 'Playlist shuffled successfully.')
    return redirect('dashboard')


def daily_playlist(request):
    start = time.process_time()
    try:
        sp = spotipy.Spotify(auth=request.session['access_token'])
    except SpotifyException as e:
        if e.http_status == 401:
            return redirect(authorize)

    playlist_id = request.POST.get('playlistSelection')
    username = request.session['username']

    # ID and tracks of selected playlist
    playlist_tracks = get_playlist_track_ids(sp, playlist_id)

    # Clear songs from playlist
    while playlist_tracks:
        sp.user_playlist_remove_all_occurrences_of_tracks(username, playlist_id, playlist_tracks[:100])
        playlist_tracks = playlist_tracks[100:]

    # Shuffle list of saved songs
    track_ids = []
    all_tracks = get_saved_songs(sp)
    for track in all_tracks:
        track_ids.append(track['id'])
    random.shuffle(track_ids)

    while track_ids:
        sp.user_playlist_add_tracks(username, playlist_id, track_ids[:100])
        track_ids = track_ids[100:]
    print(time.process_time() - start)
    messages.success(request, 'Daily playlist created successfully.')
    return redirect('dashboard')
