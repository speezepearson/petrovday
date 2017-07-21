import time
import os
import datetime as dt
import json
import flask
import petrovday

game = petrovday.Game(players=['Seattle', 'NYC', 'San Francisco', 'Boston'])

app = flask.Flask(__name__)

STATIC_DIR = os.path.join(os.path.dirname(__file__), 'static')

@app.route('/<player>/')
def index(player):
  if player not in game.players:
    return (f'Valid sides are: {game.players}', 404)
  return flask.send_from_directory(STATIC_DIR, 'index.html')

@app.route('/<player>/enemies')
def enemies(player):
  if player not in game.players:
    return (f'Valid sides are: {game.players}', 404)
  return json.dumps(list(sorted(game.enemies(player))))

@app.route('/<player>/launch/<enemy>')
def launch(player, enemy):
  if (player not in game.players) or (enemy not in game.players):
    return (f'Valid sides are: {game.players}', 404)
  game.launch(player, enemy, departure_time=dt.datetime.now())
  return ''

@app.route('/<player>/drill/<enemy>')
def drill(player, enemy):
  launch(enemy, player)
  return ''

@app.route('/<player>/read_ews/<enemy>')
def read_ews(player, enemy):
  if (player not in game.players) or (enemy not in game.players):
    return (f'Valid sides are: {game.players}', 404)
  time.sleep(1)
  import json
  return json.dumps(game.read_ews(player, enemy, dt.datetime.now()))
