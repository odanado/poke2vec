import re
import json
from pathlib import Path

import click
from logzero import logger

USER_PLAYER = re.compile(r"\|player\|(?P<player>.+?)\|(?P<username>.+?)\|.*?")
POKE = re.compile(r"\|poke\|(?P<player>.+?)\|(?P<poke>.+?)\|.*?")


def to_id(name):
    return re.sub(r'[^a-z0-9]+', '', name.lower())


@click.command()
@click.argument('save_dir', type=str)
@click.argument('battle_logs_file', type=str)
def cmd(save_dir, battle_logs_file):
    print(save_dir, battle_logs_file)
    save_dir = Path(save_dir)
    battle_logs_file = Path(battle_logs_file)

    data = json.loads(battle_logs_file.read_text())

    ladder = data['ladder']
    battle_logs = data['battle_logs']

    save_file = save_dir / '{}_parsed_battle_logs.json'.format(ladder)

    players_list = []
    pokes_list = []

    for user, battle_log_list in sorted(battle_logs.items(),
                                        key=lambda x: x[0]):
        logger.info('user = {}'.format(user))
        for battle_log in battle_log_list:
            players = {}
            matches = USER_PLAYER.findall(battle_log)
            for match in matches:
                players[match[0]] = to_id(match[1])

            pokes = {}
            matches = POKE.findall(battle_log)
            for match in matches:
                player, poke = match
                poke = to_id(poke.split(',')[0])

                if player not in pokes:
                    pokes[player] = []

                pokes[player].append(poke)

            players_list.append(players)
            pokes_list.append(pokes)

    save_file.write_text(json.dumps({
        'ladder': ladder,
        'players': players_list,
        'pokes': pokes_list
    }))


if __name__ == '__main__':
    cmd()
