import time
import os
import datetime as dt
import json
import flask
import petrovday

game = petrovday.Game(players=['USA', 'Russia', 'China'])

app = flask.Flask(__name__)

@app.route('/jquery-3.2.1.min.js')
def jquery():
  return flask.send_from_directory(os.path.join(os.path.dirname(__file__), 'resources'), 'jquery-3.2.1.min.js')

@app.route('/<player>/')
def index(player):
  if player not in game.players:
    return (f'Valid sides are: {game.players}', 404)
  return flask.send_from_directory(os.path.join(os.path.dirname(__file__), 'resources'), 'index.html')

@app.route('/<player>/enemies')
def enemies(player):
  if player not in game.players:
    return (f'Valid sides are: {game.players}', 404)
  return json.dumps(list(game.enemies(player)))

@app.route('/<player>/launch/<enemy>')
def launch(player, enemy):
  if (player not in game.players) or (enemy not in game.players):
    return (f'Valid sides are: {game.players}', 404)
  game.launch(player, enemy, departure_time=dt.datetime.now())
  return ''

@app.route('/<player>/read_ews/<enemy>')
def read_ews(player, enemy):
  if (player not in game.players) or (enemy not in game.players):
    return (f'Valid sides are: {game.players}', 404)
  time.sleep(3)
  return str(game.read_ews(player, enemy, dt.datetime.now()))
