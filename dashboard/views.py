from django.shortcuts import render, redirect
from django.http import QueryDict
import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()


def index(request):
    return render(request, 'index.html')


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
    if request.GET.__contains__('error'):
        return render(request, 'index.html', {'message': 'Error connecting Spotify account, please try again.'})
    else:
        authorization_code = request.GET.__getitem__('code')
        params = {
            'grant_type': 'authorization_code',
            'code': authorization_code,
            'redirect_uri': 'http://127.0.0.1:8000/login',
            'client_id': os.environ.get('CLIENT_ID'),
            'client_secret': os.environ.get('CLIENT_SECRET')
        }

        response = requests.post('https://accounts.spotify.com/api/token', data=params)
        if response.status_code == 200:
            response_json = json.loads(response.text)
            request.session['access_token'] = response_json['access_token']
            request.session['refresh_token'] = response_json['refresh_token']
            return redirect(index)
        else:
            return render(request, 'index.html', {'message': 'Error connecting Spotify account, please try again.'})


def logout(request):
    request.session.flush()
    return redirect(index)
