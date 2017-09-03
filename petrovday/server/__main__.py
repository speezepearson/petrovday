import os
import json
import subprocess
import argparse

import bottle

import petrovday

parser = argparse.ArgumentParser()
parser.add_argument('players', nargs='+')
args = parser.parse_args()

app = bottle.Bottle(__name__)
game = petrovday.Game(players=args.players)
server = petrovday.server.Server(app=app, game=game)
server.clock.start()

bottle.run(app, host='localhost', port=5000)
