import webbrowser
import click
import requests
import os.path
import os
import json
from .util import prompt

client_id = 'dKeZ3o7E8r5yo5acwqjQXA'
client_secret = 'd8451207e916b468c4767e444f3a4d76'

config = {}

config_dirname = os.path.expanduser(os.path.join('~', '.config'))
config_filename = os.path.join(config_dirname, 'assembla-cli')

if os.path.exists(config_filename):
    with open(config_filename) as f:
        config = json.load(f)


def save_config():
    if not os.path.exists(config_dirname):
        os.mkdir(config_dirname)

    with open(config_filename, 'w') as f:
        json.dump(config, f)


def sign_in():
    webbrowser.open('https://api.assembla.com/authorization?client_id={}&response_type=pin_code'.format(client_id))
    click.echo('A browser will open and ask you to sign into Assembla. When done, copy the PIN code and paste it here.')
    pin_code = prompt('PIN code: ')
    data = fetch('https://{}:{}@api.assembla.com/token?grant_type=pin_code&pin_code={}'
                 .format(client_id, client_secret, pin_code), method='POST')
    config['access_token'] = data['access_token']
    config['refresh_token'] = data['refresh_token']


def authenticate():
    if 'access_token' not in config:
        sign_in()

    data = fetch('https://{}:{}@api.assembla.com/token?client_id={}&grant_type=refresh_token&refresh_token={}'
                 .format(client_id, client_secret, client_id, config['refresh_token']), method='POST')
    config['access_token'] = data['access_token']
    save_config()


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
        headers['Authorization'] = 'Bearer ' + config['access_token']

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
