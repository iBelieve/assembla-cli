import webbrowser
import click
import requests
from .util import prompt

client_id = 'dKeZ3o7E8r5yo5acwqjQXA'
client_secret = 'd8451207e916b468c4767e444f3a4d76'

access_token = None
refresh_token = None


def sign_in():
    global access_token, refresh_token

    webbrowser.open('https://api.assembla.com/authorization?client_id={}&response_type=pin_code'.format(client_id))
    click.echo('A browser will open and ask you to sign into Assembla. When done, copy the PIN code and paste it here.')
    pin_code = prompt('PIN code: ')
    data = fetch('https://{}:{}@api.assembla.com/token?grant_type=pin_code&pin_code={}'
                 .format(client_id, client_secret, pin_code), method='POST')
    access_token = data['access_token']
    refresh_token = data['refresh_token']


def authenticate():
    global access_token, refresh_token

    if not access_token:
        sign_in()

    data = fetch('https://{}:{}@api.assembla.com/token?client_id={}&grant_type=refresh_token&refresh_token={}'
                 .format(client_id, client_secret, client_id, refresh_token), method='POST')
    access_token = data['access_token']


def get_merge_request(space_name, merge_id):
    authenticate()
    return fetch('/spaces/{}/space_tools/git/merge_requests/{}.json'.format(space_name, merge_id))


def close_merge_request(space_name, merge_id):
    authenticate()
    return fetch('/spaces/{}/space_tools/git/merge_requests/{}/ignore.json'.format(space_name, merge_id), method='PUT')


def fetch(url, **kwargs):
    headers = kwargs.pop('headers', {})

    if not url.startswith('http'):
        url = 'https://api.assembla.com/v1' + url
        headers['Authorization'] = 'Bearer ' + access_token

    r = requests.request(kwargs.pop('method', 'GET'), url, headers=headers, **kwargs)

    try:
        data = r.json()
    except:
        data = r.text

    if isinstance(data, dict) and 'error' in data:
        error = data.get('error_description', data.get('error'))
        raise Exception(error)

    r.raise_for_status()

    return data
