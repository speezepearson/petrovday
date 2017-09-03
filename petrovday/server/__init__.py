import os
import json
import bottle
import petrovday

STATIC_DIR = os.path.join(os.path.dirname(__file__), 'static')

class InvalidPlayer(Exception):
  def __init__(self, player):
    super().__init__()
    self.player = player

class Server:
  def __init__(self, app, game):
    self.clock = petrovday.DiscreteClock()
    self.app = app
    self.game = game
    self.app.route('/<player>')(lambda player: bottle.redirect(f'/{player}/'))
    self.app.route('/<player>/')(self.index)
    self.app.route('/favicon.ico')(lambda: bottle.HTTPError(status=404))
    self.app.route('/static/<filename>')(self.static)
    self.app.route('/<player>/enemies')(self.enemies)
    self.app.route('/<player>/launch/<enemy>')(self.launch)
    self.app.route('/<player>/drill/<enemy>')(self.drill)
    self.app.route('/<player>/update')(self.update)

  def handle_invalid_player(self, error):
    self.app.abort(400, f'Invalid player {error.player} (valid players are {self.game.players})')

  def ensure_valid_players(self, *players):
    for player in players:
      if player not in self.game.players:
        raise InvalidPlayer(player)

  def index(self, player):
    self.ensure_valid_players(player)
    return self.static('index.html')

  def static(self, filename):
    return bottle.static_file(filename=filename, root=STATIC_DIR)

  def enemies(self, player):
    self.ensure_valid_players(player)
    return json.dumps(list(sorted(self.game.enemies(player))))

  def launch(self, player, enemy):
    self.ensure_valid_players(player, enemy)
    self.game.launch(player, enemy, departure_time=self.clock.current_time)
    return ''

  def drill(self, player, enemy):
    self.ensure_valid_players(player, enemy)
    self.launch(enemy, player)
    return ''

  def update(self, player):
    self.ensure_valid_players(player)

    since = int(bottle.request.query['since'])
    self.clock.wait_until(since+1)
    now = self.clock.current_time

    reading_start_time = max(since+1, now-500)
    return json.dumps({
      'discrete_time': self.clock.current_time,
      'alive': self.game.is_alive(player, now),
      'enemy_info': {
        enemy: {'readings': {t: self.game.read_ews(player, enemy, t)
                             for t in range(reading_start_time, now+1)},
                'alive': self.game.is_alive(enemy, now),
                'time_to_impact': self.game.get_time_to_impact(player, enemy, now)}
        for enemy in self.game.enemies(player)}})
