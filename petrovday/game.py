import datetime as dt

from .missile import Missile
from .earlywarningsystem import EarlyWarningSystem
from .randomprocess import white_noise

class Game:
  def __init__(self, players):
    players = set(players)
    self.ewss = {(player, enemy): EarlyWarningSystem(
                                    player, enemy,
                                    white_noise(scales=[dt.timedelta(seconds=1)],
                                                weights=[.1],
                                                seed=(player, enemy),
                                                origin=dt.datetime(2017, 9, 26, 0, 0, 0)))
                 for player in players
                 for enemy in players
                 if enemy != player}
    self.missiles = []

  @property
  def players(self):
    return set(k[0] for k in self.ewss)

  def enemies(self, player):
    return {p for p in self.players if p != player}

  def launch(self, aggressor, victim, departure_time, missile_flight_time=dt.timedelta(seconds=60)):
    if departure_time is None:
      departure_time = dt.datetime.now()
    self.missiles.append(Missile(origin=aggressor, destination=victim, departure_time=departure_time, eta=departure_time+missile_flight_time))

  def read_ews(self, location, target, time):
    return self.ewss[location, target].get_reading([m for m in self.missiles if m.departure_time < time < m.eta], time)
