import datetime as dt

from .missile import Missile
from .earlywarningsystem import EarlyWarningSystem
from . import randomprocess as rp

def frange(start, stop, step):
  while start < stop:
    yield start
    start += step
SCALES = [dt.timedelta(seconds=10**n) for n in frange(0, 2, .2)]
WEIGHTS = [(s/dt.timedelta(seconds=1))**.5 / 10 for s in SCALES]
def make_ews_noise(seed, cauchy_coefficient=1):
  return rp.weighted_sum([
    (1, rp.white_noise(
           scales=SCALES,
           weights=WEIGHTS,
           seed=seed,
           origin=dt.datetime(2017, 9, 26, 0, 0, 0))),
    (1, rp.regularly_interpolate(
           rp.pseudorandom_static(seed=seed, f=(lambda r: cauchy_coefficient/r.normalvariate(0, 1))),
           origin=dt.datetime(2017, 9, 26, 0, 0, 0),
           scale=dt.timedelta(seconds=100)))])

class Game:
  def __init__(self, players):
    players = set(players)
    self.ewss = {(player, enemy): EarlyWarningSystem(player, enemy, make_ews_noise(seed=(player, enemy)))
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
