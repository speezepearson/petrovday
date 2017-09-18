import typing

Missile = typing.NamedTuple('Missile', [('origin', str),
                                        ('destination', str),
                                        ('departure_time', int),
                                        ('eta', int)])
