import time
import os
import json
import flask
import petrovday

game = petrovday.Game(players=['Seattle', 'NYC', 'San Francisco', 'Boston'])

START_TIME = time.time()
def get_integer_time():
  return int(time.time()-START_TIME)
def wait_until_next_integer_time():
  remainder = time.time() % 1
  time.sleep((1 if remainder==0 else 1-remainder) + 0.01)

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
  game.launch(player, enemy, departure_time=get_integer_time())
  return ''

@app.route('/<player>/drill/<enemy>')
def drill(player, enemy):
  launch(enemy, player)
  return ''

@app.route('/<player>/read_ewss')
def read_ews(player):
  if player not in game.players:
    return (f'Valid sides are: {game.players}', 404)

  since = int(flask.request.args['since'])
  if since == get_integer_time():
    wait_until_next_integer_time()

  now = get_integer_time()
  return json.dumps({
    enemy: {'readings': {t: game.read_ews(player, enemy, t)
                         for t in range(since+1, now)},
            'alive': game.is_alive(enemy, now),
            'time_to_impact': game.get_time_to_impact(player, enemy, now)}
    for enemy in game.enemies(player)})
