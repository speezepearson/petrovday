import os
import json
import hashlib
import base64
import bottle
import petrovday

STATIC_DIR = os.path.join(os.path.dirname(__file__), 'static')

def requires_authentication(f):
  def authenticated_wrapper(self, player, *args, **kwargs):
    password = bottle.request.get_cookie('password')
    if password != self.get_password(player):
      return bottle.HTTPError(401)
    return f(self, player, *args, **kwargs)
  return authenticated_wrapper

class Server:
  def __init__(self, app, game, secret):
    self.clock = petrovday.DiscreteClock()
    self.app = app
    self.game = game
    self.secret = secret

    self.app.route('/<player>')(lambda player: bottle.redirect(f'/{player}/'))
    self.app.route('/<player>/')(self.index)
    self.app.route('/<player>/authenticate')(self.authenticate)
    self.app.route('/favicon.ico')(lambda: bottle.HTTPError(status=404))
    self.app.route('/static/<filename:path>')(self.static)
    self.app.route('/<player>/launch/<enemy>')(self.launch)
    self.app.route('/<player>/drill/<enemy>')(self.drill)
    self.app.route('/<player>/update')(self.update)

  def ensure_valid_players(self, *players):
    invalids = set(players) - set(self.game.players)
    if invalids:
      bottle.abort(400, f'Invalid players {invalids} (valid players are {self.game.players})')

  def get_password(self, player):
    return base64.b64encode(hashlib.sha256(self.secret+player.encode('utf-8')).digest())[:8].decode()

  def index(self, player):
    self.ensure_valid_players(player)
    return self.static('index.html')

  def authenticate(self, player):
    self.ensure_valid_players(player)
    password = bottle.request.query.get('password', '')
    if password != self.get_password(player):
      print(password, self.get_password(player))
      return bottle.HTTPError(status=401)
    bottle.response.set_cookie('password', bottle.request.query['password'])
    return json.dumps(self.get_update_dict(player, since=0))

  def static(self, filename):
    return bottle.static_file(filename=filename, root=STATIC_DIR)

  @requires_authentication
  def launch(self, player, enemy):
    self.ensure_valid_players(player, enemy)
    self.game.launch(player, enemy, departure_time=self.clock.current_time)
    return ''

  @requires_authentication
  def drill(self, player, enemy):
    self.ensure_valid_players(player, enemy)
    self.launch(enemy, player)
    return ''

  @requires_authentication
  def update(self, player):
    self.ensure_valid_players(player)

    since = int(bottle.request.query['since'])
    self.clock.wait_until(since+1)
    return json.dumps(self.get_update_dict(player, since))

  def get_update_dict(self, player, since) -> dict:
    now = self.clock.current_time

    reading_start_time = max(since+1, now-500)
    return {
      'discreteTime': self.clock.current_time,
      'alive': self.game.is_alive(player, now),
      'enemyInfos': {
        enemy: {'readings': {t: self.game.read_ews(player, enemy, t)
                             for t in range(
                               reading_start_time,
                               1+min(now, (self.game.missile_flight_time+self.game.get_previous_time_of_death(enemy, now, float('inf')))))},
                'lrrs': self.game.get_lrrs(player, enemy),
                'alive': self.game.is_alive(enemy, now),
                'timeOfDeath': self.game.get_previous_time_of_death(enemy, now),
                'timeToImpact': self.game.get_time_to_impact(player, enemy, now)}
        for enemy in self.game.enemies(player)}}
