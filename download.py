import json
import time
from pathlib import Path

import click
import requests
from logzero import logger
from bs4 import BeautifulSoup

LADDER_URL = 'http://pokemonshowdown.com/ladder/{ladder}'
USERNAME_URL = ('http://replay.pokemonshowdown.com/search/?output=html&'
                'user={user}&format=&page={page}&output=html')
REPLAY_URL = 'http://replay.pokemonshowdown.com/{replay_id}'


@click.group()
def cmd():
    pass


@cmd.command()
@click.argument('save_dir', type=str)
@click.argument('ladder', type=str)
def top_users(save_dir, ladder):
    save_dir = Path(save_dir)
    save_dir.mkdir(exist_ok=True)
    save_file = save_dir / '{}_top_users.json'.format(ladder)

    url = LADDER_URL.format(ladder=ladder)
    text = requests.get(url).text
    soup = BeautifulSoup(text, 'html.parser')
    users = [a.get('href')
             for a in soup.find_all('a', {'class': 'subtle'})]
    users = [Path(user).name for user in users]

    save_file.write_text(json.dumps({'ladder': ladder, 'users': users}))


@cmd.command()
@click.argument('save_dir', type=str)
@click.argument('users_file', type=str)
def replay_ids(save_dir, users_file):
    save_dir = Path(save_dir)

    users_file = Path(users_file)
    data = json.loads(users_file.read_text())

    ladder = data['ladder']
    users = data['users']

    save_file = save_dir / '{}_replay_ids.json'.format(ladder)

    all_replay_ids = {}

    for user in users:
        logger.info('user = {}'.format(user))
        replay_ids = []
        alredy_ids = set()
        for page in range(1, 100):
            url = USERNAME_URL.format(
                user=user,
                page=page
            )
            html = requests.get(url).text
            time.sleep(1)
            soup = BeautifulSoup(html, 'html.parser')
            links = soup.find_all('a')
            ids = [link.get('href') for link in links]
            if len(ids) == 0:
                break

            ids = [x for x in ids if ladder in x]
            if len(ids) == 0:
                continue
            if ids[0] in alredy_ids or ids[-1] in alredy_ids:
                break

            replay_ids += ids
            alredy_ids |= set(ids)
        logger.info(len(replay_ids))
        all_replay_ids[user] = replay_ids

    save_file.write_text(json.dumps(
        {'ladder': ladder, 'replay_ids': all_replay_ids}))


@cmd.command()
@click.argument('save_dir', type=str)
@click.argument('replay_ids_file', type=str)
def battle_logs(save_dir, replay_ids_file):
    save_dir = Path(save_dir)

    replay_ids_file = Path(replay_ids_file)
    data = json.loads(replay_ids_file.read_text())

    ladder = data['ladder']
    replay_ids = data['replay_ids']

    save_file = save_dir / '{}_battle_logs.json'.format(ladder)
    battle_logs = {}

    for user, replay_id_list in replay_ids.items():
        logger.info('user = {}'.format(user))
        logs = []
        for replay_id in replay_id_list:
            html = requests.get(REPLAY_URL.format(replay_id=replay_id)).text
            soup = BeautifulSoup(html, 'html.parser')
            time.sleep(1)
            log = soup.find('script', {'class': 'log'})
            assert len(log) != 0
            logs.append(log)

        battle_logs[user] = logs

    save_file.write_text(json.dumps(
        {'ladder': ladder, 'battle_logs': battle_logs}))


if __name__ == '__main__':
    cmd()
