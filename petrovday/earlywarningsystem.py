import typing
import math
import random
from .missile import Missile

def _get_fractional_progress(m: Missile, time) -> float:
  return (time-m.departure_time) / (m.eta-m.departure_time)

def _clamp(low, x, high):
  return min(high, max(low, x))

class EarlyWarningSystem:

  false_alarm_p = 0.1

  def __init__(self, location, target, seed):
    self.location = location
    self.target = target
    self.seed = seed

  def __str__(self):
    return f'{self.__class__}({self.location!r}, {self.target!r})'

  @classmethod
  def fractional_increase_in_p_for_missile(cls, fractional_progress: float) -> float:
    x = fractional_progress
    return cls.false_alarm_p + (1-cls.false_alarm_p) * (x*(2-x))

  def get_reading(self, missiles: typing.Iterable[Missile], time) -> bool:
    alarm_p = self.false_alarm_p
    for m in missiles:
      if m.origin==self.target and m.destination==self.location:
        alarm_p += (1-alarm_p)*self.fractional_increase_in_p_for_missile(_get_fractional_progress(m, time))
        break
    return random.Random((self.seed, time)).random() < alarm_p
