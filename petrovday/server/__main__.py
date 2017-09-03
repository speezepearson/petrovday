import os
import json
import subprocess
import secrets
import argparse

import bottle

import petrovday

parser = argparse.ArgumentParser()
parser.add_argument('players', nargs='+')
parser.add_argument('--public', action='store_true')
args = parser.parse_args()

app = bottle.Bottle(__name__)
game = petrovday.Game(players=args.players)
secret = secrets.token_bytes(nbytes=8)
server = petrovday.server.Server(app=app, game=game, secret=secret)
server.clock.start()

print('\n###############################################################')
print('Passwords:')
n = max(len(p) for p in game.players)
for player in sorted(game.players):
  print(f'  {player: >{n}}: {server.get_password(player)}')
print('###############################################################\n')

bottle.run(app, host=('0.0.0.0' if args.public else 'localhost'), port=5000)
