import typing
import collections
import datetime as dt

Missile = typing.NamedTuple('Missile', [('origin', str),
                                        ('destination', str),
                                        ('departure_time', dt.datetime),
                                        ('eta', dt.datetime)])

from . import randomprocess
from .game import Game
from .earlywarningsystem import EarlyWarningSystem
