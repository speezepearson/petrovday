import typing
import math
from . import Missile
from .randomprocess import RandomProcess

def _get_fractional_progress(m: Missile, time) -> float:
  return (time-m.departure_time) / (m.eta-m.departure_time)

class EarlyWarningSystem:
  def __init__(self, location, target, noise):
    self.location = location
    self.target = target
    self.noise = noise

  @classmethod
  def _get_reading_for_incoming_missile(cls, missile_fractional_progress: float) -> float:
    return -math.log(1-missile_fractional_progress)

  @classmethod
  def _get_reading_for_benign_missile(cls, missile_fractional_progress: float) -> float:
    x = missile_fractional_progress
    return x*(1-x)

  def _get_noise_for_missile(self, missile: Missile, time) -> float:
    x = _get_fractional_progress(missile, time)
    return (
      0 if self.target != missile.origin
      else self._get_reading_for_incoming_missile(x) if missile.destination == self.location
      else self._get_reading_for_benign_missile(x))

  def get_reading(self, missiles: typing.Iterable[Missile], time) -> float:
    return (
      self.noise.sample(time) +
      sum(self._get_noise_for_missile(m, time) for m in missiles))