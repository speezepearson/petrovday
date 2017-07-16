import typing
import datetime as dt

Missile = typing.NamedTuple('Missile', [('origin', str),
                                        ('destination', str),
                                        ('departure_time', dt.datetime),
                                        ('eta', dt.datetime)])
