import typing
import math
from .missile import Missile

def _get_fractional_progress(m: Missile, time) -> float:
  return (time-m.departure_time) / (m.eta-m.departure_time)

def _clamp(low, x, high):
  return min(high, max(low, x))

class EarlyWarningSystem:
  def __init__(self, location, target, noise, limits=None):
    self.location = location
    self.target = target
    self.noise = noise
    self.limits = limits

  def __str__(self):
    return f'EarlyWarningSystem({self.location!r}, {self.target!r}, {self.noise!r})'

  @classmethod
  def _get_reading_for_incoming_missile(cls, missile_fractional_progress: float) -> float:
    return -5*math.log(1-missile_fractional_progress**.5)

  @classmethod
  def _get_reading_for_benign_missile(cls, missile_fractional_progress: float) -> float:
    x = missile_fractional_progress
    return 5*x*(1-x)

  def _get_noise_for_missile(self, missile: Missile, time) -> float:
    x = _get_fractional_progress(missile, time)
    return (
      0 if self.target != missile.origin
      else self._get_reading_for_incoming_missile(x) if missile.destination == self.location
      else self._get_reading_for_benign_missile(x))

  def get_reading(self, missiles: typing.Iterable[Missile], time) -> float:
    result = (
      self.noise(time) +
      sum(self._get_noise_for_missile(m, time) for m in missiles))
    if self.limits:
      low, high = self.limits
      return _clamp(low, result, high)
    return result
