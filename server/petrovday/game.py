from .missile import Missile
from .earlywarningsystem import EarlyWarningSystem
from . import randomprocess as rp

class Game:
  def __init__(self, players, missile_flight_time=180):
    players = set(players)
    self.ewss = {(player, enemy): EarlyWarningSystem(player, enemy, seed=(player, enemy))
                 for player in players
                 for enemy in players
                 if enemy != player}
    self.missiles = []
    self.missile_flight_time = missile_flight_time

  @property
  def players(self):
    return set(k[0] for k in self.ewss)

  def enemies(self, player):
    return {p for p in self.players if p != player}

  def launch(self, aggressor, victim, departure_time):
    self.missiles.append(Missile(origin=aggressor, destination=victim, departure_time=departure_time, eta=departure_time+self.missile_flight_time))

  def read_ews(self, location, target, time):
    return self.ewss[location, target].get_reading([m for m in self.missiles if m.departure_time < time < m.eta], time)

  def is_alive(self, player, t):
    return not any(m.destination==player and m.eta < t for m in self.missiles)

  def get_time_to_impact(self, aggressor, victim, time):
    for missile in self.missiles:
      if missile.origin==aggressor and missile.destination==victim:
        return missile.eta-time
    return None

  def get_previous_time_of_death(self, victim, before, default=None):
    etas = [m.eta for m in self.missiles if m.destination == victim and m.eta <= before]
    if etas:
      return min(etas)
    return default
