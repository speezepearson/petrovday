import datetime as dt
from petrovday import Missile
from petrovday.randomprocess import RandomProcess
from petrovday.earlywarningsystem import EarlyWarningSystem

class TestReadings:
  ews = EarlyWarningSystem('USA', 'Russia', RandomProcess({1: 1}, seed=0))

  now = 100
  old_incoming_missile = Missile('Russia', 'USA', departure_time=now-9, eta=now+1)
  medium_incoming_missile = Missile('Russia', 'USA', departure_time=now-5, eta=now+5)
  young_incoming_missile = Missile('Russia', 'USA', departure_time=now-1, eta=now+9)
  old_benign_missile = Missile('Russia', 'France', departure_time=now-9, eta=now+1)
  medium_benign_missile = Missile('Russia', 'France', departure_time=now-5, eta=now+5)
  young_benign_missile = Missile('Russia', 'France', departure_time=now-1, eta=now+9)

  def test_signals_for_missiles_add(self):
    r0 = self.ews.get_reading([], self.now)
    r_yim = self.ews.get_reading([self.old_incoming_missile], self.now)
    r_obm = self.ews.get_reading([self.young_benign_missile], self.now)
    r_yim_obm = self.ews.get_reading([self.old_incoming_missile, self.young_benign_missile], self.now)

    d_yim = r_yim-r0
    d_obm = r_obm-r0
    d_yim_obm = r_yim_obm-r0
    assert abs(d_yim_obm - (d_yim+d_obm) < 1e-9)

  def test_nearer_incoming_missiles_increase_readings_more(self):
    assert (
      self.ews.get_reading([], self.now)
      < self.ews.get_reading([self.young_incoming_missile], self.now)
      < self.ews.get_reading([self.old_incoming_missile], self.now)
      < self.ews.get_reading([self.young_incoming_missile, self.old_incoming_missile], self.now))

  def test_progressing_benign_missiles_increase_readings_more_and_then_less(self):
    assert (
      self.ews.get_reading([], self.now)
      < self.ews.get_reading([self.old_benign_missile], self.now)
      < self.ews.get_reading([self.medium_benign_missile], self.now)
      > self.ews.get_reading([self.young_benign_missile], self.now))
